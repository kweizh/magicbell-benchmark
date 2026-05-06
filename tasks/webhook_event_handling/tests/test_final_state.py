import os
import subprocess
import time
import socket
import json
import pytest
import urllib.request

PROJECT_DIR = "/home/user/project"
LOG_FILE = os.path.join(PROJECT_DIR, "magicbell_events.log")

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_server():
    # Install dependencies just in case
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)
    
    # Start the server
    process = subprocess.Popen(
        ["node", "server.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the server to be ready
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Server failed to start and listen on port 3000.")

    yield

    # Shut down the server
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_webhook_event_handling(start_server):
    # Payload
    payload = {
        "event": "notification_read",
        "notification": {"id": "notif_abc123"},
        "user": {"email": "user@example.com"}
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:3000/webhooks/magicbell",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        response = urllib.request.urlopen(req, timeout=5)
        status_code = response.getcode()
    except urllib.error.HTTPError as e:
        status_code = e.code
    except Exception as e:
        pytest.fail(f"Failed to send request to the server: {e}")

    assert status_code == 200, f"Expected 200 OK, got {status_code}"

    # Verify log file
    assert os.path.isfile(LOG_FILE), f"Log file not found at {LOG_FILE}"
    
    with open(LOG_FILE, "r") as f:
        content = f.read()
        
    expected_line = "notif_abc123 read by user@example.com"
    assert expected_line in content, f"Expected log line '{expected_line}' not found in {LOG_FILE}. Content: {content}"
