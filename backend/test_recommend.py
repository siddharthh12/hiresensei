import requests
import sys

BASE_URL = "http://localhost:8000"

def test_recommend_endpoint():
    print("Testing /jobs/recommend endpoint...")
    
    # 1. Login
    login_data = {
        "username": "testuser@example.com",
        "password": "password123"
    }
    try:
        res = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if res.status_code != 200:
             # Register if needed
            reg_data = {"full_name": "Test User", "email": "testuser@example.com", "password": "password123"}
            requests.post(f"{BASE_URL}/auth/register", json=reg_data)
            res = requests.post(f"{BASE_URL}/auth/login", data=login_data)
            
        if res.status_code != 200:
            print(f"Login failed: {res.status_code} {res.text}")
            return
        
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful.")

        # 2. Hit Recommend Endpoint
        print(f"Requesting {BASE_URL}/jobs/recommend?sort=match")
        res = requests.get(f"{BASE_URL}/jobs/recommend?sort=match", headers=headers)
        
        print(f"Status Code: {res.status_code}")
        if res.status_code == 200:
            print("Success! Response:")
            print(res.json())
        else:
            print(f"Failed: {res.text}")

    except requests.exceptions.ConnectionError:
        print("Connection Error: Could not connect to backend. Is it running?")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_recommend_endpoint()
