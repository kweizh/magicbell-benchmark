import os
import subprocess
import time
import socket
import pytest
import json
import base64
import urllib.request

BACKEND_DIR = "/home/user/magicbell-backend"
FRONTEND_DIR = "/home/user/magicbell-migration"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_backend():
    process = subprocess.Popen(
        ["node", "server.js"],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(3001):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Backend server failed to start and listen on port 3001.")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_backend_auth_endpoint(start_backend):
    req = urllib.request.Request("http://localhost:3001/auth")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode())
            assert "token" in data, "Response JSON must contain 'token' key."
            token = data["token"]
            
            # Decode JWT payload
            parts = token.split('.')
            assert len(parts) == 3, "Token does not look like a valid JWT."
            
            # Add padding if necessary
            payload_b64 = parts[1]
            payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
            payload_json = base64.urlsafe_b64decode(payload_b64).decode('utf-8')
            payload = json.loads(payload_json)
            
            assert payload.get("user_email") == "test@example.com", \
                f"Expected user_email 'test@example.com' in token payload, got: {payload.get('user_email')}"
    except Exception as e:
        pytest.fail(f"Failed to fetch or parse auth endpoint: {e}")

def test_frontend_dependencies_updated():
    pkg_json_path = os.path.join(FRONTEND_DIR, "package.json")
    with open(pkg_json_path) as f:
        data = json.load(f)
    deps = data.get("dependencies", {})
    
    assert "@magicbell/react-headless" not in deps, "Deprecated @magicbell/react-headless should be removed from dependencies."
    assert "@magicbell/react" in deps, "New @magicbell/react should be added to dependencies."

def test_frontend_app_jsx_imports():
    app_jsx_path = os.path.join(FRONTEND_DIR, "src", "App.jsx")
    with open(app_jsx_path) as f:
        content = f.read()
        
    assert "@magicbell/react/context-provider" in content, "Expected import from @magicbell/react/context-provider in App.jsx"
    assert "@magicbell/react/inbox" in content, "Expected import from @magicbell/react/inbox in App.jsx"

def test_frontend_build_succeeds():
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=FRONTEND_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Frontend build failed: {result.stderr}\n{result.stdout}"
