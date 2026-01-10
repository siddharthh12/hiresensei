from typing import List
from app.models.hybrid_job import HybridJob
from fuzzywuzzy import fuzz

def deduplicate_jobs(jobs: List[HybridJob]) -> List[HybridJob]:
    """
    Remove duplicates based on apply_link and (title + company).
    Prioritize API source over scrapers if duplicate found.
    """
    unique_jobs = []
    seen_links = set()
    seen_title_company = set()
    
    # Sort jobs to prioritize API source (so it gets processed first)
    # Priority: api > wwr > remoteok > hn
    source_priority = {"api": 0, "wwr": 1, "remoteok": 2, "hn": 3}
    jobs.sort(key=lambda x: source_priority.get(x.source, 99))
    
    for job in jobs:
        # 1. Check Link
        if job.apply_link in seen_links:
            continue
            
        # 2. Check Title + Company (Fuzzy or Exact)
        # Simple normalization
        t = job.title.lower().strip()
        c = job.company.lower().strip()
        key = (t, c)
        
        if key in seen_title_company:
            continue
            
        # Add to unique list
        unique_jobs.append(job)
        seen_links.add(job.apply_link)
        seen_title_company.add(key)
        
    return unique_jobs
