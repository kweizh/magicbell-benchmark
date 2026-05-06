import os
import subprocess
import time
import json
import socket
import pytest

PROJECT_DIR = "/home/user/project"
MOCK_OUTPUT_FILE = "/tmp/mock_output.json"

def wait_for_port(port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(0.5)
    return False

@pytest.fixture(scope="module")
def run_script_with_mock_server():
    # Write the mock server script
    mock_server_code = """
import http.server
import json

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            parsed_body = json.loads(body)
        except:
            parsed_body = body
        
        log_data = {
            "method": self.command,
            "path": self.path,
            "headers": dict(self.headers),
            "body": parsed_body
        }
        with open('/tmp/mock_output.json', 'w') as f:
            json.dump(log_data, f)
            
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status": "ok"}')

if __name__ == '__main__':
    server = http.server.HTTPServer(('localhost', 8080), RequestHandler)
    server.handle_request()
"""
    server_script_path = "/tmp/mock_server.py"
    with open(server_script_path, "w") as f:
        f.write(mock_server_code)

    # Start the mock server
    server_process = subprocess.Popen(
        ["python3", server_script_path],
        preexec_fn=os.setsid
    )

    if not wait_for_port(8080):
        import signal
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        pytest.fail("Mock server failed to start on port 8080.")

    # Run the user's script
    env = os.environ.copy()
    env.update({
        "MAGICBELL_API_URL": "http://localhost:8080",
        "MAGICBELL_API_KEY": "test_api_key",
        "MAGICBELL_API_SECRET": "test_api_secret",
        "TWILIO_ACCOUNT_SID": "AC123456789",
        "TWILIO_API_KEY": "SK123456789",
        "TWILIO_API_SECRET": "secret123",
        "TWILIO_FROM_NUMBER": "+1234567890"
    })

    script_path = os.path.join(PROJECT_DIR, "setup_twilio.sh")
    assert os.path.isfile(script_path), "setup_twilio.sh not found in project directory."
    
    # Ensure it is executable
    os.chmod(script_path, 0o755)

    result = subprocess.run(
        [script_path],
        cwd=PROJECT_DIR,
        env=env,
        capture_output=True,
        text=True
    )

    # Wait a moment to ensure server writes the file
    time.sleep(1)

    # Shut down the server
    import signal
    os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
    server_process.wait(timeout=5)

    return result

def test_script_execution_success(run_script_with_mock_server):
    result = run_script_with_mock_server
    assert result.returncode == 0, f"setup_twilio.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"

def test_mock_output_exists(run_script_with_mock_server):
    assert os.path.isfile(MOCK_OUTPUT_FILE), "Mock server did not write output file. The script might not have made the request."

def test_request_details(run_script_with_mock_server):
    with open(MOCK_OUTPUT_FILE, "r") as f:
        data = json.load(f)

    assert data["method"] == "PUT", f"Expected PUT request, got {data['method']}"
    assert data["path"] == "/v2/integrations/twilio", f"Expected path /v2/integrations/twilio, got {data['path']}"

    # Headers are typically lowercased by BaseHTTPRequestHandler
    headers = {k.lower(): v for k, v in data["headers"].items()}
    assert headers.get("x-magicbell-api-key") == "test_api_key", "Missing or incorrect X-MAGICBELL-API-KEY header."
    assert headers.get("x-magicbell-api-secret") == "test_api_secret", "Missing or incorrect X-MAGICBELL-API-SECRET header."
    assert "application/json" in headers.get("content-type", "").lower(), "Missing or incorrect Content-Type header."

    body = data.get("body", {})
    assert isinstance(body, dict), "Request body is not a valid JSON object."
    assert body.get("account_sid") == "AC123456789", "Incorrect account_sid in request body."
    assert body.get("api_key") == "SK123456789", "Incorrect api_key in request body."
    assert body.get("api_secret") == "secret123", "Incorrect api_secret in request body."
    assert body.get("from") == "+1234567890", "Incorrect from number in request body."
