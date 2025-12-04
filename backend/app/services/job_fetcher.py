import httpx
import os
from typing import List, Optional
from app.core.config import settings

BASE_URL = "https://jsearch.p.rapidapi.com/search"

async def fetch_jobs_from_api(query: str, location: Optional[str] = None, remote: bool = False) -> List[dict]:
    if not settings.RAPIDAPI_KEY:
        print("WARNING: RapidAPI key not configured")
        return []

    # Using x-api-key as per user instruction, but keeping host as x-rapidapi-host if that's standard, 
    # or maybe the user meant x-api-key for the key header. 
    # The requirement said: headers = { "x-rapidapi-key": settings.RAPIDAPI_KEY, "x-rapidapi-host": settings.RAPIDAPI_HOST }
    # But the user also said "this is name - x-api-key".
    # I will try to use the standard RapidAPI headers first as per the requirements text, 
    # but I will add a fallback or just stick to the requirements text which is more formal.
    # Actually, let's stick to the requirements text:
    headers = {
        "x-rapidapi-key": settings.RAPIDAPI_KEY,
        "x-rapidapi-host": settings.RAPIDAPI_HOST
    }
    
    search_query = query
    if location:
        search_query += f" in {location}"
    
    params = {
        "query": search_query,
        "page": "1",
        "num_pages": "1"
    }
    
    if remote:
        params["remote_jobs_only"] = "true"

    async with httpx.AsyncClient() as client:
        try:
            print(f"Fetching jobs from: {BASE_URL}")
            print(f"Params: {params}")
            response = await client.get(BASE_URL, headers=headers, params=params, timeout=10.0)
            # print(f"Response Status: {response.status_code}")
            # print(f"Response Text: {response.text}") 
            response.raise_for_status()
            data = response.json()
            # print(f"Response Data Keys: {data.keys()}")
            if "data" in data:
                pass # print(f"Number of jobs found: {len(data['data'])}")
            else:
                print("No 'data' key in response")
            
            jobs = []
            if "data" in data:
                for item in data["data"]:
                    jobs.append({
                        "job_id": item.get("job_id"),
                        "title": item.get("job_title"),
                        "company": item.get("employer_name"),
                        "location": f"{item.get('job_city', '')}, {item.get('job_country', '')}".strip(", "),
                        "job_type": item.get("job_employment_type"),
                        "apply_link": item.get("job_apply_link"),
                        "description": item.get("job_description"),
                        "source": "RapidAPI",
                        "posted_date": item.get("job_posted_at_datetime_utc")
                    })
            return jobs
        except httpx.HTTPStatusError as e:
            print(f"API Error: {e}")
            return []
        except Exception as e:
            print(f"Error fetching jobs: {e}")
            return []
