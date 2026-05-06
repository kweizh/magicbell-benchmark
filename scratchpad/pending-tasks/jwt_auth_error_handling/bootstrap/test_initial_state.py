import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/magicbell-app"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(path), f"File {path} does not exist."

def test_server_js_exists():
    path = os.path.join(PROJECT_DIR, "server.js")
    assert os.path.isfile(path), f"File {path} does not exist."

def test_app_jsx_exists():
    path = os.path.join(PROJECT_DIR, "src", "App.jsx")
    assert os.path.isfile(path), f"File {path} does not exist."

def test_initial_jwt_algorithm_is_rs256():
    path = os.path.join(PROJECT_DIR, "server.js")
    with open(path) as f:
        content = f.read()
    assert "algorithm: 'RS256'" in content, "Expected initial algorithm to be 'RS256' in server.js."
