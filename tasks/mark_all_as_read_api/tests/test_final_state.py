import os
import subprocess
import pytest

PROJECT_DIR = "/home/user"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "mark_read.sh")

def test_script_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_script_execution():
    """Priority 1: Execute the script and verify the response from MagicBell API."""
    env = os.environ.copy()
    env["MAGICBELL_API_KEY"] = "dummy_key"
    env["MAGICBELL_USER_EMAIL"] = "test@example.com"
    
    result = subprocess.run(
        ["bash", "mark_read.sh"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        env=env
    )
    
    assert "incorrect_api_key" in result.stdout or "incorrect_api_key" in result.stderr, \
        f"Expected 'incorrect_api_key' in the output, indicating a correctly routed request to MagicBell. Got stdout: {result.stdout}, stderr: {result.stderr}"
