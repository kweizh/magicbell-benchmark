import os
import json
import pytest

PROJECT_DIR = "/home/user"
SCRIPT_FILE = os.path.join(PROJECT_DIR, "send_broadcast.sh")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.json")

def test_script_exists_and_executable():
    """Priority 3: Check if the script was created and is executable."""
    assert os.path.isfile(SCRIPT_FILE), f"Script {SCRIPT_FILE} does not exist."
    assert os.access(SCRIPT_FILE, os.X_OK), f"Script {SCRIPT_FILE} is not executable."

def test_output_file_exists():
    """Priority 3: Check if the output file was created."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."

def test_output_json_validity_and_content():
    """Priority 3: Check the content of the API response."""
    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_FILE} does not contain valid JSON.")
    
    assert "broadcast" in data, f"Expected 'broadcast' object in response, got: {data}"
    broadcast = data["broadcast"]
    
    assert "action_url" in broadcast, f"Expected 'action_url' in broadcast object, got: {broadcast}"
    assert broadcast["action_url"] == "https://example.com/start", \
        f"Expected action_url to be 'https://example.com/start', got: {broadcast['action_url']}"
