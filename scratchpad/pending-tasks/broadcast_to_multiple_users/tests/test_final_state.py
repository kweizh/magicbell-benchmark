import os
import pytest

SCRIPT_PATH = "/home/user/magicbell-task/broadcast.sh"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_content():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    assert "https://api.magicbell.com/v2/broadcasts" in content, "Script does not send request to the correct MagicBell API endpoint."
    assert "X-MAGICBELL-API-KEY: YOUR_API_KEY" in content, "Script is missing the API Key header."
    assert "X-MAGICBELL-API-SECRET: YOUR_API_SECRET" in content, "Script is missing the API Secret header."
    assert "Content-Type: application/json" in content, "Script is missing the Content-Type header."
    assert "alice@example.com" in content, "Script is missing recipient alice@example.com."
    assert "bob@example.com" in content, "Script is missing recipient bob@example.com."
    assert "charlie@example.com" in content, "Script is missing recipient charlie@example.com."
    assert "System Update" in content, "Script is missing the correct broadcast title."
    assert "The system will go down for maintenance in 1 hour." in content, "Script is missing the correct broadcast content."
