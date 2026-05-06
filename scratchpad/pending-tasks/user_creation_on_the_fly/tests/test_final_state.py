import os
import json
import pytest

PROJECT_DIR = "/home/user/project"
RUN_SCRIPT = os.path.join(PROJECT_DIR, "run.sh")
OUTPUT_LOG = os.path.join(PROJECT_DIR, "output.log")

def test_run_script_exists_and_content():
    """Priority 3 fallback: basic file existence and content check."""
    assert os.path.isfile(RUN_SCRIPT), f"Script not found at {RUN_SCRIPT}"
    
    with open(RUN_SCRIPT, "r") as f:
        content = f.read()
        
    assert "https://api.magicbell.com/v2/broadcasts" in content, \
        "Expected API endpoint 'https://api.magicbell.com/v2/broadcasts' in run.sh"
    
    assert "X-MAGICBELL-API-KEY" in content and "dummy_key" in content, \
        "Expected 'X-MAGICBELL-API-KEY: dummy_key' header in run.sh"
        
    assert "X-MAGICBELL-API-SECRET" in content and "dummy_secret" in content, \
        "Expected 'X-MAGICBELL-API-SECRET: dummy_secret' header in run.sh"
        
    # Check JSON structure fragments
    assert "Welcome" in content, "Expected 'Welcome' in the JSON payload"
    assert "Hello new user" in content, "Expected 'Hello new user' in the JSON payload"
    assert "new_user_on_the_fly@example.com" in content, "Expected email 'new_user_on_the_fly@example.com' in the JSON payload"
    assert "broadcast" in content, "Expected 'broadcast' key in the JSON payload"
    assert "recipients" in content, "Expected 'recipients' key in the JSON payload"

def test_output_log_exists_and_content():
    """Priority 3 fallback: check output log for expected API response."""
    assert os.path.isfile(OUTPUT_LOG), f"Log file not found at {OUTPUT_LOG}"
    
    with open(OUTPUT_LOG, "r") as f:
        content = f.read()
        
    assert "invalid_jwt_format" in content or "errors" in content or "unauthorized" in content.lower(), \
        f"Expected MagicBell API error response (e.g., 'invalid_jwt_format') in {OUTPUT_LOG}, got: {content}"
