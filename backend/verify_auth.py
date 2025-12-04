import requests
import sys

BASE_URL = "http://localhost:8000"

def verify_auth():
    print("Starting Auth verification...")

    # 1. Register
    register_data = {
        "full_name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    }
    print(f"Registering user: {register_data['email']}")
    try:
        res = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if res.status_code == 200:
            print("Registration successful")
            print(res.json())
        elif res.status_code == 400 and "Email already registered" in res.text:
            print("User already registered, proceeding to login")
        else:
            print(f"Registration failed: {res.status_code} {res.text}")
            return
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return

    # 2. Login
    login_data = {
        "username": "testuser@example.com",
        "password": "password123"
    }
    print(f"Logging in user: {login_data['username']}")
    res = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if res.status_code != 200:
        print(f"Login failed: {res.status_code} {res.text}")
        return
    
    token_data = res.json()
    access_token = token_data["access_token"]
    print("Login successful, token received")

    # 3. Access Protected Route (/me)
    print("Accessing protected route /auth/me")
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if res.status_code == 200:
        print("Protected route accessed successfully")
        print(res.json())
    else:
        print(f"Access failed: {res.status_code} {res.text}")
        return

    print("Auth verification completed.")

if __name__ == "__main__":
    verify_auth()
