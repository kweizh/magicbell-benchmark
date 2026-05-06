import os
import subprocess
import time
import socket
import pytest

PROJECT_DIR = "/home/user/myproject"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--host"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(5173):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 5173.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_theme_css_exists_and_contains_variables():
    theme_path = os.path.join(PROJECT_DIR, "src", "theme.css")
    assert os.path.isfile(theme_path), f"theme.css not found at {theme_path}"
    
    with open(theme_path, "r") as f:
        content = f.read()
        
    assert "--magicbell-bg-default" in content, "Missing --magicbell-bg-default in theme.css"
    assert "#111827" in content, "Missing #111827 for background color in theme.css"
    assert "--magicbell-text-default" in content, "Missing --magicbell-text-default in theme.css"
    assert "#f5f5f5" in content, "Missing #f5f5f5 for text color in theme.css"

def test_package_json_contains_magicbell():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found at {package_json_path}"
    
    with open(package_json_path, "r") as f:
        content = f.read()
        
    assert "@magicbell/react" in content, "@magicbell/react not found in package.json"

def test_app_loads(start_app):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:5173"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"curl command failed: {result.stderr}"
    assert result.stdout.strip() == "200", f"Expected HTTP 200, got {result.stdout}"
