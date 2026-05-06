import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_package_json_exists():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found in {PROJECT_DIR}."

def test_app_js_exists():
    app_js_path = os.path.join(PROJECT_DIR, "App.js")
    assert os.path.isfile(app_js_path), f"App.js not found in {PROJECT_DIR}."
