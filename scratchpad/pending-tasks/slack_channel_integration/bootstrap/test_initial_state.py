import os
import shutil
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_curl_binary_available():
    assert shutil.which("curl") is not None, "curl binary not found in PATH."

def test_bash_binary_available():
    assert shutil.which("bash") is not None, "bash binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."