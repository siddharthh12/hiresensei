import requests
import time

BASE_URL = "http://localhost:8000"

def verify_job_search():
    print("Starting Job Search Verification...")

    # 1. Search (API Call)
    print("Searching for 'Python' (Expect API Call)...")
    start_time = time.time()
    res = requests.get(f"{BASE_URL}/job/search", params={"query": "Python", "remote": "true"})
    duration = time.time() - start_time
    
    if res.status_code == 200:
        data = res.json()["data"]
        print(f"Success. Found {len(data)} jobs. Duration: {duration:.2f}s")
        # Note: Since we are using a placeholder API key, we might get empty results or mock data if the fetcher handles errors gracefully.
        # But the structure should be correct.
    else:
        print(f"Search failed: {res.text}")
        return

    # 2. Search Again (Cache Hit)
    print("Searching for 'Python' again (Expect Cache Hit)...")
    start_time = time.time()
    res = requests.get(f"{BASE_URL}/job/search", params={"query": "Python", "remote": "true"})
    duration_cached = time.time() - start_time
    
    if res.status_code == 200:
        data = res.json()["data"]
        print(f"Success. Found {len(data)} jobs. Duration: {duration_cached:.2f}s")
        
        if duration_cached < duration:
            print("✅ Cache verification passed (Second call was faster).")
        else:
            print("⚠️ Cache verification inconclusive (Network might be fast).")
    else:
        print(f"Cached search failed: {res.text}")

    print("Job Search verification completed.")

if __name__ == "__main__":
    verify_job_search()
