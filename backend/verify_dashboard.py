import requests
import sys

BASE_URL = "http://localhost:8000"

def login(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.text}")
        sys.exit(1)

def verify_dashboard(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n--- Testing Dashboard Summary ---")
    response = requests.get(f"{BASE_URL}/dashboard/summary", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("Success!")
        print(f"Stats: {data['stats']}")
        print(f"Profile: {data['profile']}")
        print(f"Recent Activity: {len(data['recent_activity']['saved_jobs'])} saved, {len(data['recent_activity']['applied_jobs'])} applied")
    else:
        print(f"Failed: {response.status_code} - {response.text}")

    print("\n--- Testing Skill Analytics ---")
    response = requests.get(f"{BASE_URL}/dashboard/skills", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("Success!")
        print(f"Top User Skills: {data['top_user_skills']}")
        print(f"Missing Skills: {data['missing_skills']}")
        print(f"Recommended Skills (Top 3): {data['recommended_skills'][:3]}")
    else:
        print(f"Failed: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Use a test user that likely exists or create one. 
    # Assuming 'test@example.com' from previous sessions or I can try to register/login.
    # I'll try to login with a known user or just use the one from previous context if available.
    # Since I don't know the password for sure, I might need to register a new one or use a hardcoded one if I created it.
    # I'll try 'test@example.com' / 'password123' which is common in these tasks, or register a new one.
    
    email = "dashboard_test@example.com"
    password = "password123"
    
    # Try register first just in case
    try:
        requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password, "full_name": "Dashboard Test"})
    except:
        pass

    token = login(email, password)
    with open("verify_output.txt", "w") as f:
        sys.stdout = f
        verify_dashboard(token)
