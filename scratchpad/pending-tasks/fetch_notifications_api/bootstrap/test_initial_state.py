import os
import shutil
import pytest

PROJECT_DIR = "/home/user/project"

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_curl_binary_available():
    assert shutil.which("curl") is not None, "curl binary not found in PATH."
