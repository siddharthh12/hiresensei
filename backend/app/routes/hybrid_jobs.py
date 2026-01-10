from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.database import database
from app.models.user import User
from app.core.security import get_current_user
from app.models.resume import Resume
from app.models.hybrid_job import HybridJob, HybridJobResponse
from app.services.job_sources.merge_jobs import get_hybrid_jobs
from app.services.job_sources.search_links import generate_search_links
from app.services.matching_engine import calculate_match_score, rank_jobs
from app.utils.text_similarity import extract_years_of_experience
import re

router = APIRouter()

@router.get("/recommended", response_model=HybridJobResponse)
async def get_recommended_hybrid_jobs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """
    Get recommended jobs from hybrid sources (API + Scrapers) based on user profile.
    Strictly filters by Experience Level and Skills.
    """
    # 1. Fetch User Resume
    resume_data = await database.get_collection("resumes").find_one({"user_id": current_user["id"]})
    if not resume_data:
        raise HTTPException(status_code=404, detail="Resume not found. Please upload a resume first.")
    
    if "_id" in resume_data:
        resume_data["id"] = str(resume_data["_id"])
    resume = Resume(**resume_data)
    
    # 2. Determine Search Query from Resume
    query = "Software Engineer" 
    if resume.skills:
        query = resume.skills[0] 
    
    location = resume.location or ""
    
    # Calculate User Experience
    user_experience_years = 0.0
    if resume.experience:
        # Extract years from experience descriptions
        # experience is List[str]
        exp_texts = resume.experience
        user_experience_years = extract_years_of_experience(exp_texts)
    
    # 3. Fetch Hybrid Jobs
    # Fetch broadly by "Software Engineer" if specific skill query might limit "Remote" results too much?
    # No, stick to skill for relevance, but maybe fetch more to filter down.
    # Actually, let's fetch based on the top skill, as that's most relevant.
    result = await get_hybrid_jobs(query, location, remote=True)
    
    initial_jobs = result["jobs"]
    sources_used = result["sources_used"]
    
    # Fallback: If low count, try broader query BUT we will strictly filter results later
    if len(initial_jobs) < 5 and query.lower() != "software engineer":
        print(f"Low job count ({len(initial_jobs)}). Fetching fallback...")
        fallback_result = await get_hybrid_jobs("Software Engineer", location, remote=True)
        
        existing_ids = {j.job_id for j in initial_jobs}
        for job in fallback_result["jobs"]:
            if job.job_id not in existing_ids:
                initial_jobs.append(job)
        
        for source in fallback_result["sources_used"]:
             if source not in sources_used and source not in sources_used: # Avoid dupes
                sources_used.append(source)
    
    # 4. Strict Filtering Logic
    filtered_jobs = []
    
    # Prepare exclusions regex
    # Fresher exclusions
    senior_pattern = re.compile(r'\b(Senior|Sr\.|Lead|Principal|Manager|Architect|Head|Director|VP)\b', re.IGNORECASE)
    # Experienced exclusions (> 3 years)
    junior_pattern = re.compile(r'\b(Intern|Internship|Junior|Jr\.|Entry Level|Trainee)\b', re.IGNORECASE)
    
    user_skills_lower = {s.lower() for s in (resume.skills or [])}
    
    for job in initial_jobs:
        title = job.title
        desc = job.description
        text_to_check = (title + " " + desc).lower()
        
        # A. Experience Filter
        if user_experience_years < 1.5:
            # User is Fresher/Junior
            if senior_pattern.search(title):
                continue # Skip senior roles
        elif user_experience_years > 3.0:
            # User is Experienced
            if junior_pattern.search(title):
                continue # Skip junior roles
                
        # B. Skill Relevance Filter
        # Job MUST contain at least one user skill to be relevant
        # (Prevent "Remote" generic marketing jobs for a Developer)
        if user_skills_lower:
            has_skill = False
            for skill in user_skills_lower:
                # Simple word boundary check
                if re.search(r'\b' + re.escape(skill) + r'\b', text_to_check):
                    has_skill = True
                    break
            
            if not has_skill:
                continue # Skip irrelevant job
        
        filtered_jobs.append(job)

    # 5. Run Matching Engine (Ranking) on Filtered Jobs
    scored_jobs = []
    for job in filtered_jobs:
        job_dict = job.dict()
        scored_job = calculate_match_score(job_dict, resume)
        
        if scored_job["match_score"] > 0:
            scored_job["source"] = job.source
            scored_job["job_type"] = job.job_type
            scored_job["published_at"] = job.published_at
            scored_jobs.append(scored_job)
            
    # 6. Rank
    ranked_jobs = rank_jobs(scored_jobs, "match")
    
    # 7. Pagination
    start = (page - 1) * limit
    end = start + limit
    final_jobs = ranked_jobs[start:end]
    
    # 8. External Links
    external_links = generate_search_links(query, location)
    
    return {
        "jobs": final_jobs,
        "external_search_links": external_links,
        "sources_used": sources_used,
        "total": len(ranked_jobs)
    }

@router.get("/search")
async def search_hybrid_jobs(
    role: str = Query(..., min_length=1),
    location: str = Query("", min_length=0),
    remote: bool = Query(False),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50)
):
    """
    Search jobs across hybrid sources.
    """
    result = await get_hybrid_jobs(role, location, remote)
    jobs = result["jobs"]
    sources_used = result["sources_used"]
    
    # Sort by date (newest first)
    # jobs are already sorted by date in merge_jobs.py
    
    start = (page - 1) * limit
    end = start + limit
    final_jobs = jobs[start:end]
    
    external_links = generate_search_links(role, location)
    
    return {
        "jobs": final_jobs,
        "external_search_links": external_links,
        "sources_used": sources_used,
        "total": len(jobs)
    }
