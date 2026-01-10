import asyncio
import time
from app.services.job_sources.api_jobs import fetch_jsearch_jobs
from app.services.job_sources.scrape_remoteok import scrape_remoteok
from app.services.job_sources.scrape_wwr import scrape_wwr
from app.services.job_sources.scrape_hn_jobs import scrape_hn_jobs
from app.services.job_sources.merge_jobs import get_hybrid_jobs

async def test_source(name, func, query):
    print(f"--- Testing {name} ---")
    start = time.time()
    try:
        jobs = await func(query)
        elapsed = time.time() - start
        print(f"[{name}] Success: Found {len(jobs)} jobs in {elapsed:.2f}s")
        if jobs:
            print(f"  Sample: {jobs[0].title} @ {jobs[0].company}")
        return jobs
    except Exception as e:
        elapsed = time.time() - start
        print(f"[{name}] Failed after {elapsed:.2f}s: {e}")
        return []

async def debug_all():
    query = "python"
    print(f"Debug Query: '{query}'")
    
    # Test individually
    await test_source("JSearch", lambda q: fetch_jsearch_jobs(q, "", True), query)
    await test_source("WeWorkRemotely", scrape_wwr, query)
    await test_source("RemoteOK", scrape_remoteok, query)
    await test_source("HackerNews", scrape_hn_jobs, query)
    
    # Test Aggregation
    print("\n--- Testing Aggregation (get_hybrid_jobs) ---")
    start = time.time()
    result = await get_hybrid_jobs(query, remote=True)
    elapsed = time.time() - start
    
    jobs = result["jobs"]
    sources = result["sources_used"]
    print(f"[Aggregation] Total Jobs: {len(jobs)} in {elapsed:.2f}s")
    print(f"[Aggregation] Sources Used: {sources}")
    
    # Count by source
    counts = {}
    for job in jobs:
        counts[job.source] = counts.get(job.source, 0) + 1
    print(f"[Aggregation] Counts: {counts}")

if __name__ == "__main__":
    asyncio.run(debug_all())
