import os
import pytest

PROJECT_DIR = "/home/user/project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "fetch_notifications.sh")

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_script_contains_correct_curl_command():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
        
    assert "curl" in content, "Script does not contain a curl command"
    assert "https://api.magicbell.com/v2/notifications" in content, "Script does not target the correct MagicBell API endpoint"
    assert "Authorization:" in content and "Bearer dummy_user_jwt_token" in content, "Script does not contain the correct Authorization header with the provided JWT"
