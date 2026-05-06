import os
import pytest

OUTPUT_FILE = "/home/user/output.txt"

def test_output_file_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

def test_output_file_content():
    """Priority 3 fallback: check file content for HTTP status code."""
    with open(OUTPUT_FILE) as f:
        content = f.read().strip()
    assert "401" in content, f"Expected output file to contain '401', got: {content}"
