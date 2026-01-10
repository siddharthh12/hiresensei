import asyncio
from app.services.job_sources.merge_jobs import get_hybrid_jobs
from app.services.matching_engine import calculate_match_score
from app.models.resume import Resume
from datetime import datetime

async def debug_recommendations():
    print("Debugging Recommendations Flow...")
    
    # 1. Simulate Query
    query = "react"
    print(f"Query: {query}")
    
    # 2. Fetch Jobs
    result = await get_hybrid_jobs(query, remote=True)
    jobs = result["jobs"]
    
    print(f"Total Jobs: {len(jobs)}")
    
    # Print first 5 jobs and their dates/sources
    for i, job in enumerate(jobs[:5]):
        print(f"Job {i}: {job.source} - {job.published_at}")
        
    # Check Source Counts
    wwr_jobs = [j for j in jobs if j.source == "wwr"]
    remoteok_jobs = [j for j in jobs if j.source == "remoteok"]
    print(f"WWR Jobs: {len(wwr_jobs)}")
    print(f"RemoteOK Jobs: {len(remoteok_jobs)}")
    
    # 4. Simulate Matching
    # Mock Resume
    resume = Resume(
        id="mock",
        user_id="mock",
        file_path="mock.pdf",
        created_at=datetime.utcnow(),
        email="test@example.com",
        skills=["Python", "Django", "React"],
        experience=["Software Engineer at Tech Co"],
        education=[],
        location="Remote"
    )
    
    scored_jobs = []
    for job in jobs:
        score = calculate_match_score(job.dict(), resume)
        if score["match_score"] > 0:
            scored_jobs.append(score)
            
    # Sort by match score like the endpoint does
    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
            
    print(f"Total Scored Jobs: {len(scored_jobs)}")
    for i, job in enumerate(scored_jobs[:10]):
        print(f"Rank {i}: {job['source']} - Score: {job['match_score']} - {job['title']}")
            
    wwr_scored = [j for j in scored_jobs if j["source"] == "wwr"]
    remoteok_scored = [j for j in scored_jobs if j["source"] == "remoteok"]
    
    print(f"WWR Jobs (Post-Match): {len(wwr_scored)}")
    print(f"RemoteOK Jobs (Post-Match): {len(remoteok_scored)}")
    
    if wwr_jobs and not wwr_scored:
        print("WWR Job 0 Match Details:")
        score = calculate_match_score(wwr_jobs[0].dict(), resume)
        print(score)

if __name__ == "__main__":
    asyncio.run(debug_recommendations())
