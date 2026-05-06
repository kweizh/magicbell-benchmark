import os
import pytest

SCRIPT_PATH = "/home/user/myproject/send_slack_broadcast.sh"

def test_script_exists_and_executable():
    """Priority 3 fallback: basic file existence and permissions check."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable."

def test_script_uses_env_vars():
    """Priority 3 fallback: check file contents for environment variables."""
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    
    assert "MAGICBELL_API_KEY" in content, "Expected script to use MAGICBELL_API_KEY environment variable."
    assert "MAGICBELL_API_SECRET" in content, "Expected script to use MAGICBELL_API_SECRET environment variable."

def test_script_payload_structure():
    """Priority 3 fallback: check file contents for correct payload structure."""
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    
    assert "https://api.magicbell.com/v2/broadcasts" in content, "Expected script to call the MagicBell broadcasts endpoint."
    assert "System Alert" in content, "Expected payload to include title 'System Alert'."
    assert "General alert message" in content, "Expected payload to include content 'General alert message'."
    assert "user@example.com" in content, "Expected payload to include recipient 'user@example.com'."
    assert "overrides" in content, "Expected payload to include 'overrides' object."
    assert "slack" in content, "Expected payload to include 'slack' override."
    assert "Slack-specific alert message" in content, "Expected payload to include 'Slack-specific alert message'."