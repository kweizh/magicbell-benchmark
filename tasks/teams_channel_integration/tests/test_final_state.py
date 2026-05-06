import os
import subprocess
import threading
import json
import pytest
from http.server import BaseHTTPRequestHandler, HTTPServer

PROJECT_DIR = "/home/user/magicbell-task"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "save_teams_token.sh")

class MockServerRequestHandler(BaseHTTPRequestHandler):
    requests = []

    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        MockServerRequestHandler.requests.append({
            'path': self.path,
            'headers': dict(self.headers),
            'body': post_data.decode('utf-8')
        })
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{}')

    def log_message(self, format, *args):
        pass

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_fails_without_args():
    result = subprocess.run([SCRIPT_PATH], capture_output=True)
    assert result.returncode != 0, "Script should exit with non-zero status when arguments are missing."

def test_script_sends_correct_request():
    MockServerRequestHandler.requests = []
    server = HTTPServer(('localhost', 8080), MockServerRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        env = os.environ.copy()
        env['MAGICBELL_API_URL'] = 'http://localhost:8080'
        
        jwt = "mock_jwt_123"
        webhook_url = "https://teams.webhook.example.com"
        
        result = subprocess.run(
            [SCRIPT_PATH, jwt, webhook_url],
            env=env,
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script failed with output: {result.stderr}"
        
        assert len(MockServerRequestHandler.requests) == 1, "Expected exactly one request to the mock server."
        req = MockServerRequestHandler.requests[0]
        
        assert req['path'] == '/channels/teams/tokens' or req['path'] == '/v2/channels/teams/tokens', \
            f"Expected request path to end with /channels/teams/tokens, got {req['path']}"
            
        assert req['headers'].get('Authorization') == f"Bearer {jwt}" or req['headers'].get('authorization') == f"Bearer {jwt}", \
            f"Expected Authorization header 'Bearer {jwt}', got {req['headers'].get('Authorization')}"
            
        try:
            body = json.loads(req['body'])
            assert body.get('webhook', {}).get('url') == webhook_url, \
                f"Expected payload to contain webhook.url = {webhook_url}, got {body}"
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse request body as JSON: {req['body']}")
            
    finally:
        server.shutdown()
        server.server_close()
