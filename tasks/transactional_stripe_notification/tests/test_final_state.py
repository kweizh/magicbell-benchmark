import os
import subprocess
import time
import socket
import pytest
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/magicbell-stripe"

# Global to store received requests in the mock server
received_requests = []

class MockMagicBellHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        received_requests.append({
            "path": self.path,
            "headers": dict(self.headers),
            "body": post_data.decode('utf-8')
        })
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"broadcast": {"id": "test_id"}}')
        
    def log_message(self, format, *args):
        pass # Suppress logging

def wait_for_port(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def mock_magicbell_server():
    server = HTTPServer(('localhost', 8000), MockMagicBellHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    server.server_close()

@pytest.fixture(scope="module")
def start_app():
    env = os.environ.copy()
    env["MAGICBELL_API_URL"] = "http://localhost:8000"
    env["MAGICBELL_API_KEY"] = "test_api_key"
    env["MAGICBELL_API_SECRET"] = "test_api_secret"
    
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=env
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_webhook_processing(mock_magicbell_server, start_app):
    # Clear any previous requests
    received_requests.clear()
    
    # Send request to Express app
    webhook_payload = {
        "type": "invoice.payment_succeeded",
        "data": {
            "object": {
                "subscription": "sub_test123",
                "customer_email": "user@example.com"
            }
        }
    }
    
    req = urllib.request.Request(
        "http://localhost:3000/webhook/stripe",
        data=json.dumps(webhook_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        response = urllib.request.urlopen(req)
        assert response.getcode() == 200, f"Expected status code 200, got {response.getcode()}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Webhook request failed with status {e.code}: {e.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to webhook endpoint: {e.reason}")
        
    # Give the app a moment to make the outgoing request if it's async
    time.sleep(1)
    
    # Verify mock server received the broadcast
    assert len(received_requests) > 0, "Mock MagicBell server did not receive any requests."
    
    broadcast_req = received_requests[0]
    
    # Verify path
    assert broadcast_req["path"] == "/v2/broadcasts", f"Expected request to /v2/broadcasts, got {broadcast_req['path']}"
    
    # Verify headers
    headers = broadcast_req["headers"]
    assert headers.get("X-MAGICBELL-API-KEY") == "test_api_key", "Missing or incorrect X-MAGICBELL-API-KEY header."
    assert headers.get("X-MAGICBELL-API-SECRET") == "test_api_secret", "Missing or incorrect X-MAGICBELL-API-SECRET header."
    
    # Verify body
    body = json.loads(broadcast_req["body"])
    assert "broadcast" in body, "Missing 'broadcast' key in payload."
    broadcast = body["broadcast"]
    assert broadcast.get("title") == "Payment Successful", "Incorrect broadcast title."
    assert broadcast.get("content") == "Your payment for subscription sub_test123 was successful.", "Incorrect broadcast content."
    recipients = broadcast.get("recipients", [])
    assert len(recipients) > 0, "Missing recipients."
    assert recipients[0].get("email") == "user@example.com", "Incorrect recipient email."
