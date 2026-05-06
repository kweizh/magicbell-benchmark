import os
import json
import pytest

PAYLOAD_FILE = "/home/user/magicbell-project/payload.json"

def test_payload_file_exists():
    """Priority 3: basic file existence check."""
    assert os.path.isfile(PAYLOAD_FILE), \
        f"payload.json not found at {PAYLOAD_FILE}"

def test_payload_structure():
    """Priority 3: Parse JSON and verify fields."""
    with open(PAYLOAD_FILE) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {PAYLOAD_FILE} is not valid JSON.")
    
    assert "broadcast" in data, "Expected top-level 'broadcast' object."
    broadcast = data["broadcast"]
    
    assert broadcast.get("title") == "Alert", \
        f"Expected broadcast.title to be 'Alert', got: {broadcast.get('title')}"
        
    assert broadcast.get("content") == "System down", \
        f"Expected broadcast.content to be 'System down', got: {broadcast.get('content')}"
        
    assert broadcast.get("action_url") == "https://example.com/alert", \
        f"Expected broadcast.action_url to be 'https://example.com/alert', got: {broadcast.get('action_url')}"
        
    recipients = broadcast.get("recipients", [])
    assert isinstance(recipients, list) and len(recipients) > 0, \
        "Expected broadcast.recipients to be a non-empty array."
    assert any(r.get("email") == "admin@example.com" for r in recipients), \
        f"Expected recipients to contain email 'admin@example.com', got: {recipients}"
        
    overrides = broadcast.get("overrides", {})
    channels = overrides.get("channels", {})
    slack = channels.get("slack", {})
    
    assert slack.get("action_url") == "https://example.com/slack-alert", \
        f"Expected broadcast.overrides.channels.slack.action_url to be 'https://example.com/slack-alert', got: {slack.get('action_url')}"
