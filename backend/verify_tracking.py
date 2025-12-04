import requests
import sys
import uuid

BASE_URL = "http://localhost:8000"

def verify_tracking():
    print("Verifying Job Tracking System...")

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

        # 2. Save a Job
        job_id = str(uuid.uuid4())
        job_data = {
            "job_id": job_id,
            "title": "Test Job",
            "company": "Test Company",
            "location": "Remote",
            "description": "A test job description."
        }
        
        print(f"Saving job {job_id}...")
        res = requests.post(f"{BASE_URL}/tracking/save", json={"job_id": job_id, "job_data": job_data}, headers=headers)
        if res.status_code == 200:
            print("Job saved successfully.")
        else:
            print(f"Failed to save job: {res.status_code} {res.text}")
            return

        # 3. List Jobs
        print("Listing tracked jobs...")
        res = requests.get(f"{BASE_URL}/tracking/list", headers=headers)
        if res.status_code == 200:
            data = res.json()
            saved_jobs = data.get("saved", [])
            print(f"Saved jobs count: {len(saved_jobs)}")
            found = False
            for job in saved_jobs:
                if job.get("job_id") == job_id:
                    found = True
                    break
            if found:
                print("SUCCESS: Saved job found in list.")
            else:
                print("FAILURE: Saved job NOT found in list.")
        else:
            print(f"Failed to list jobs: {res.status_code} {res.text}")

        # 4. Mark as Applied
        print(f"Marking job {job_id} as applied...")
        res = requests.post(f"{BASE_URL}/tracking/applied", json={"job_id": job_id, "job_data": job_data}, headers=headers)
        if res.status_code == 200:
            print("Job marked as applied.")
        else:
            print(f"Failed to mark applied: {res.status_code} {res.text}")

        # 5. List Jobs Again (Check if moved)
        print("Listing tracked jobs again...")
        res = requests.get(f"{BASE_URL}/tracking/list", headers=headers)
        if res.status_code == 200:
            data = res.json()
            applied_jobs = data.get("applied", [])
            saved_jobs = data.get("saved", [])
            
            found_applied = any(job.get("job_id") == job_id for job in applied_jobs)
            found_saved = any(job.get("job_id") == job_id for job in saved_jobs)
            
            if found_applied and not found_saved:
                print("SUCCESS: Job moved to Applied list.")
            else:
                print(f"FAILURE: Job status update failed. Applied: {found_applied}, Saved: {found_saved}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_tracking()
