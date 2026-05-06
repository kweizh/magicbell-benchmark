import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/magicbell-project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "send_broadcast.js")

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_script_payload_and_headers():
    # We will use nock to intercept the request and print the captured data.
    verifier_script = """
const nock = require('nock');
const fs = require('fs');

nock('https://api.magicbell.com')
  .post('/v2/broadcasts')
  .reply(200, function(uri, requestBody) {
    fs.writeFileSync('/tmp/captured_request.json', JSON.stringify({
      headers: this.req.headers,
      body: requestBody
    }));
    return { broadcast: { id: "mocked_id" } };
  });

try {
  // Set NODE_PATH so global nock can be found if needed, though it's better to run in a directory where nock is available
  require('%s');
} catch (e) {
  console.error("Error running script:", e);
}
""" % SCRIPT_PATH

    verifier_path = "/tmp/run_verifier.js"
    with open(verifier_path, "w") as f:
        f.write(verifier_script)

    # Run the verifier script
    env = os.environ.copy()
    env["NODE_PATH"] = "/usr/lib/node_modules"
    
    result = subprocess.run(
        ["node", verifier_path],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env
    )
    
    # Wait a bit or just check if the file was written (since axios is async, the script might exit before the request completes if it doesn't await)
    # Actually, if they don't await, Node might exit. But nock intercepts synchronously in the same tick usually, or we can just wait.
    # A better verifier waits for nock:
    
    verifier_script_async = """
const nock = require('nock');
const fs = require('fs');

let requestCaptured = false;
nock('https://api.magicbell.com')
  .post('/v2/broadcasts')
  .reply(200, function(uri, requestBody) {
    fs.writeFileSync('/tmp/captured_request.json', JSON.stringify({
      headers: this.req.headers,
      body: requestBody
    }));
    requestCaptured = true;
    return { broadcast: { id: "mocked_id" } };
  });

require('%s');

// Keep process alive briefly to allow async axios request to complete
setTimeout(() => {
    if (!requestCaptured) {
        console.error("Request was not captured by nock.");
        process.exit(1);
    }
}, 2000);
""" % SCRIPT_PATH
    
    with open(verifier_path, "w") as f:
        f.write(verifier_script_async)

    subprocess.run(
        ["node", verifier_path],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env
    )

    captured_file = "/tmp/captured_request.json"
    assert os.path.isfile(captured_file), "The script did not make a POST request to https://api.magicbell.com/v2/broadcasts."

    with open(captured_file, "r") as f:
        data = json.load(f)

    headers = data.get("headers", {})
    body = data.get("body", {})

    # Check headers
    assert headers.get("x-magicbell-api-key") == "dummy_key", "Missing or incorrect X-MAGICBELL-API-KEY header."
    assert headers.get("x-magicbell-api-secret") == "dummy_secret", "Missing or incorrect X-MAGICBELL-API-SECRET header."

    # Check body
    broadcast = body.get("broadcast", {})
    assert broadcast.get("title") == "Welcome to our platform", "Incorrect broadcast title."
    
    recipients = broadcast.get("recipients", [])
    assert any(r.get("email") == "newuser@example.com" for r in recipients), "Missing recipient newuser@example.com."
    
    overrides = broadcast.get("overrides", {})
    # The overrides structure could be {"providers": {"email": ...}} or {"channels": {"email": ...}}
    # We will check if "email" key exists somewhere in overrides and contains the html.
    overrides_str = json.dumps(overrides)
    assert "Welcome Email" in overrides_str, "Email override title not found in payload."
    assert "<h1>Welcome!</h1>" in overrides_str, "Email override HTML not found in payload."
