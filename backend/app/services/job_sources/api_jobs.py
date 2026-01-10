import httpx
from typing import List, Optional
from app.core.config import settings
from app.services.job_sources.normalize import normalize_job_data
from app.models.hybrid_job import HybridJob
from datetime import datetime

BASE_URL = "https://jsearch.p.rapidapi.com/search"

async def fetch_jsearch_jobs(query: str, location: Optional[str] = None, remote: bool = False) -> List[HybridJob]:
    if not settings.RAPIDAPI_KEY:
        print("WARNING: RapidAPI key not configured")
        return []

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
            print(f"Fetching JSearch jobs: {search_query}")
            response = await client.get(BASE_URL, headers=headers, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            jobs = []
            if "data" in data:
                for item in data["data"]:
                    # Parse date if possible, else None
                    published_at = None
                    # JSearch returns ISO format usually
                    
                    job = normalize_job_data(
                        job_id=item.get("job_id"),
                        title=item.get("job_title"),
                        company=item.get("employer_name"),
                        location=f"{item.get('job_city', '')}, {item.get('job_country', '')}".strip(", "),
                        description=item.get("job_description"),
                        apply_link=item.get("job_apply_link"),
                        source="api",
                        job_type=item.get("job_employment_type"),
                        published_at=published_at, # TODO: Parse date
                        raw_data=item
                    )
                    jobs.append(job)
            return jobs
        except Exception as e:
            print(f"Error fetching JSearch jobs: {e}")
            return []
