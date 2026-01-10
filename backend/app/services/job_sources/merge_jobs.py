import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.database import database
from app.models.hybrid_job import HybridJob
from app.services.job_sources.api_jobs import fetch_jsearch_jobs
from app.services.job_sources.scrape_remoteok import scrape_remoteok
from app.services.job_sources.scrape_wwr import scrape_wwr
from app.services.job_sources.scrape_hn_jobs import scrape_hn_jobs
from app.services.job_sources.deduplicate import deduplicate_jobs

CACHE_COLLECTION = "hybrid_jobs_cache"
CACHE_DURATION_HOURS = 6

async def get_hybrid_jobs(query: str, location: str = "", remote: bool = False) -> Dict[str, Any]:
    """
    Fetch jobs from multiple sources, merge, deduplicate, and cache.
    """
    # Create a cache key
    cache_key = f"{query.lower()}_{location.lower()}_{remote}"
    
    # 1. Check Cache
    cache_entry = await database.get_collection(CACHE_COLLECTION).find_one({"query_key": cache_key})
    
    if cache_entry:
        fetched_at = cache_entry.get("fetched_at")
        if fetched_at and (datetime.utcnow() - fetched_at) < timedelta(hours=CACHE_DURATION_HOURS):
            print(f"Serving from cache: {cache_key}")
            # Convert dicts back to HybridJob objects
            jobs = [HybridJob(**job) for job in cache_entry.get("jobs", [])]
            return {
                "jobs": jobs,
                "sources_used": cache_entry.get("sources_used", []),
                "from_cache": True
            }
            
    # 2. Fetch from Sources
    print(f"Fetching fresh data for: {cache_key}")
    
    tasks = [
        fetch_jsearch_jobs(query, location, remote),
        scrape_remoteok(query),
        scrape_wwr(query),
        scrape_hn_jobs(query)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    all_jobs = []
    sources_used = []
    
    # Process Results
    # 0: API
    if isinstance(results[0], list):
        all_jobs.extend(results[0])
        if results[0]: sources_used.append("api")
        
    # 1: RemoteOK
    if isinstance(results[1], list):
        all_jobs.extend(results[1])
        if results[1]: sources_used.append("remoteok")
        
    # 2: WWR
    if isinstance(results[2], list):
        all_jobs.extend(results[2])
        if results[2]: sources_used.append("wwr")
        
    # 3: HN
    if isinstance(results[3], list):
        all_jobs.extend(results[3])
        if results[3]: sources_used.append("hn")
        
    # 3. Deduplicate
    unique_jobs = deduplicate_jobs(all_jobs)
    
    # 4. Sort (Date DESC, then API priority implicitly via dedupe sort, but let's sort by date if available)
    # Jobs without date go to bottom? Or top? Let's put them at bottom.
    unique_jobs.sort(key=lambda x: x.published_at or datetime.min, reverse=True)
    
    # 5. Cache
    cache_data = {
        "query_key": cache_key,
        "jobs": [job.dict() for job in unique_jobs],
        "sources_used": sources_used,
        "fetched_at": datetime.utcnow()
    }
    
    # Upsert cache
    await database.get_collection(CACHE_COLLECTION).update_one(
        {"query_key": cache_key},
        {"$set": cache_data},
        upsert=True
    )
    
    return {
        "jobs": unique_jobs,
        "sources_used": sources_used,
        "from_cache": False
    }
