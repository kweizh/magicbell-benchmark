import os
import subprocess
import time
import socket
import pytest

PROJECT_DIR = "/home/user/project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "update_preferences.js")
LOG_FILE = os.path.join(PROJECT_DIR, "mock_server.log")

def wait_for_port(port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(0.5)
    return False

@pytest.fixture(scope="module")
def setup_mock_server():
    mock_server_code = f"""
const http = require('http');
const jwt = require('jsonwebtoken');
const fs = require('fs');

function log(msg) {{
    fs.appendFileSync('{LOG_FILE}', msg + '\\n');
}}

const server = http.createServer((req, res) => {{
    let body = '';
    req.on('data', chunk => {{
        body += chunk.toString();
    }});
    req.on('end', () => {{
        try {{
            if (req.method !== 'PUT' || req.url !== '/v2/channels/user_preferences') {{
                log('ERROR_INVALID_ENDPOINT: ' + req.method + ' ' + req.url);
                res.writeHead(404);
                return res.end('Not Found');
            }}

            const authHeader = req.headers['authorization'];
            if (!authHeader || !authHeader.startsWith('Bearer ')) {{
                log('ERROR_MISSING_BEARER');
                res.writeHead(401);
                return res.end('Unauthorized');
            }}

            const token = authHeader.split(' ')[1];
            const decoded = jwt.verify(token, 'test_secret');
            
            if (decoded.user_email !== 'user@example.com') {{
                log('ERROR_WRONG_EMAIL: ' + decoded.user_email);
                res.writeHead(400);
                return res.end();
            }}
            if (decoded.api_key !== 'test_key') {{
                log('ERROR_WRONG_API_KEY: ' + decoded.api_key);
                res.writeHead(400);
                return res.end();
            }}

            const parsedBody = JSON.parse(body);
            const category = parsedBody.categories.find(c => c.key === 'updates');
            if (!category) {{
                log('ERROR_MISSING_CATEGORY');
                res.writeHead(400);
                return res.end();
            }}

            const emailChannel = category.channels.find(c => c.name === 'email');
            if (!emailChannel || emailChannel.enabled !== false) {{
                log('ERROR_CHANNEL_NOT_DISABLED');
                res.writeHead(400);
                return res.end();
            }}

            log('VERIFICATION_SUCCESS');
            res.writeHead(200);
            res.end(JSON.stringify({{ success: true }}));
        }} catch (e) {{
            log('ERROR_EXCEPTION: ' + e.message);
            res.writeHead(500);
            res.end();
        }}
    }});
}});

server.listen(4000, () => {{
    log('Mock server listening on 4000');
}});
"""
    mock_server_path = os.path.join(PROJECT_DIR, "mock_server.js")
    with open(mock_server_path, "w") as f:
        f.write(mock_server_code)

    # Ensure log file is empty
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # Start mock server
    process = subprocess.Popen(
        ["node", "mock_server.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        preexec_fn=os.setsid
    )

    if not wait_for_port(4000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Mock server failed to start on port 4000.")

    yield process

    # Shut down the mock server
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=5)

def test_update_preferences_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_script_execution_and_verification(setup_mock_server):
    # Run the user's script
    env = os.environ.copy()
    env["MAGICBELL_API_KEY"] = "test_key"
    env["MAGICBELL_API_SECRET"] = "test_secret"
    env["MAGICBELL_API_URL"] = "http://localhost:4000/v2"

    result = subprocess.run(
        ["node", "update_preferences.js"],
        cwd=PROJECT_DIR,
        env=env,
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Script execution failed: {result.stderr}\\n{result.stdout}"

    # Read mock server output from log file
    time.sleep(1)
    
    assert os.path.exists(LOG_FILE), "Mock server log file was not created."
    with open(LOG_FILE, "r") as f:
        mock_output = f.read()

    assert "VERIFICATION_SUCCESS" in mock_output, f"Mock server did not verify success. Output:\\n{mock_output}"
