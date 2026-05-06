import os
import shutil
import pytest

PROJECT_DIR = "/home/user"

def test_curl_binary_available():
    assert shutil.which("curl") is not None, "curl binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."
