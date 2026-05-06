import os
import requests
import time
import subprocess
import jwt

def test_final_state():
    app_dir = "/home/user/magicbell-app"
    
    # Wait for the backend to be up
    max_retries = 30
    backend_up = False
    for _ in range(max_retries):
        try:
            res = requests.get("http://localhost:3001/api/token?email=test@example.com")
            if res.status_code in [200, 401, 500]:
                backend_up = True
                break
        except Exception:
            pass
        time.sleep(1)
        
    assert backend_up, "Backend server did not start on port 3001"
    
    # Test valid token generation
    res = requests.get("http://localhost:3001/api/token?email=test@example.com")
    assert res.status_code == 200, f"Expected 200 OK, got {res.status_code}"
    
    data = res.json()
    assert "token" in data, "Response missing 'token' field"
    token = data["token"]
    
    # Verify the token payload and signature
    secret = os.environ.get("MAGICBELL_API_SECRET", "test_api_secret")
    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.InvalidAlgorithmError:
        assert False, "Token was not signed with HS256 algorithm"
    except Exception as e:
        assert False, f"Failed to decode token: {e}"
        
    assert "user_email" in decoded, "Token payload missing 'user_email'"
    assert decoded["user_email"] == "test@example.com", "Token payload 'user_email' is incorrect"
    
    assert "api_key" in decoded, "Token payload missing 'api_key'"
    assert decoded["api_key"] == os.environ.get("MAGICBELL_API_KEY", "test_api_key"), "Token payload 'api_key' is incorrect"
    
    # Test error handling in frontend code
    app_jsx_path = os.path.join(app_dir, "src", "App.jsx")
    with open(app_jsx_path, "r") as f:
        app_jsx = f.read()
        
    assert 'id="error-message"' in app_jsx, "Frontend missing error message div with id='error-message'"
    assert "Authentication failed" in app_jsx, "Frontend missing 'Authentication failed' text"
