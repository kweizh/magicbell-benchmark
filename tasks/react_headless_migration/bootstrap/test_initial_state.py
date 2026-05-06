import os
import shutil
import pytest
import json

BACKEND_DIR = "/home/user/magicbell-backend"
FRONTEND_DIR = "/home/user/magicbell-migration"

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_backend_dir_exists():
    assert os.path.isdir(BACKEND_DIR), f"Backend directory {BACKEND_DIR} does not exist."

def test_frontend_dir_exists():
    assert os.path.isdir(FRONTEND_DIR), f"Frontend directory {FRONTEND_DIR} does not exist."

def test_frontend_initial_package_json():
    pkg_json_path = os.path.join(FRONTEND_DIR, "package.json")
    assert os.path.isfile(pkg_json_path), f"package.json missing at {pkg_json_path}"
    with open(pkg_json_path) as f:
        data = json.load(f)
    deps = data.get("dependencies", {})
    assert "@magicbell/react-headless" in deps, "Expected @magicbell/react-headless in initial package.json"

def test_frontend_initial_app_jsx():
    app_jsx_path = os.path.join(FRONTEND_DIR, "src", "App.jsx")
    assert os.path.isfile(app_jsx_path), f"App.jsx missing at {app_jsx_path}"
    with open(app_jsx_path) as f:
        content = f.read()
    assert "@magicbell/react-headless" in content, "Expected @magicbell/react-headless import in initial App.jsx"
