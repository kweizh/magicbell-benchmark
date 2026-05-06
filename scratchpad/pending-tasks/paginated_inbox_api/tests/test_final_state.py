import os
import subprocess
import time
import socket
import json
import pytest

PROJECT_DIR = "/home/user/magicbell-task"

def wait_for_port(port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def run_task_script():
    # Start the mock server
    mock_server = subprocess.Popen(
        ["node", "mock_server.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(8080):
        import signal
        os.killpg(os.getpgid(mock_server.pid), signal.SIGTERM)
        pytest.fail("Mock server failed to start on port 8080.")

    # Run the user's script
    env = os.environ.copy()
    env["MAGICBELL_API_URL"] = "http://localhost:8080/v2"
    env["MAGICBELL_API_KEY"] = "test_key"
    env["MAGICBELL_API_SECRET"] = "test_secret"
    
    script_result = subprocess.run(
        ["node", "fetch_notifications.js"],
        cwd=PROJECT_DIR,
        env=env,
        capture_output=True,
        text=True
    )
    
    # Shut down the mock server
    import signal
    os.killpg(os.getpgid(mock_server.pid), signal.SIGTERM)
    mock_server.wait(timeout=10)

    return script_result

def test_script_execution_success(run_task_script):
    assert run_task_script.returncode == 0, \
        f"fetch_notifications.js failed with error: {run_task_script.stderr}"

def test_output_file_exists():
    output_path = os.path.join(PROJECT_DIR, "output.json")
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_output_contains_all_notifications():
    output_path = os.path.join(PROJECT_DIR, "output.json")
    with open(output_path) as f:
        try:
            titles = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {output_path} is not valid JSON.")
    
    assert isinstance(titles, list), "Output should be a JSON array."
    assert len(titles) == 5, f"Expected 5 notifications, but got {len(titles)}."
    
    expected_titles = ["Notif 1", "Notif 2", "Notif 3", "Notif 4", "Notif 5"]
    for expected in expected_titles:
        assert expected in titles, f"Expected notification '{expected}' missing from output."
