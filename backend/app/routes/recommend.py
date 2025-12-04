from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.database import database
from app.models.user import User
from app.core.security import get_current_user
from app.services.matching_engine import calculate_match_score, rank_jobs
from app.models.resume import Resume
from app.models.job import ResponseModel

router = APIRouter()

@router.get("/recommend", response_description="Get recommended jobs based on resume")
async def get_recommendations(
    sort: str = Query("match", regex="^(match|latest|salary)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    try:
        # 1. Fetch User's Resume
        resume_data = await database.get_collection("resumes").find_one({"user_id": current_user["id"]})
        if not resume_data:
            raise HTTPException(status_code=404, detail="Resume not found. Please upload a resume first.")
        
        if "_id" in resume_data:
            resume_data["id"] = str(resume_data["_id"])
            
        resume = Resume(**resume_data)
        
        # 2. Fetch Jobs to Match Against
        cached_jobs_cursor = database.get_collection("cached_jobs").find()
        cached_jobs = await cached_jobs_cursor.to_list(length=100)
        
        if not cached_jobs:
            return ResponseModel([], "No jobs found to recommend. Please search for jobs first to populate recommendations.")
            
        # 3. Run Matching Algorithm
        scored_jobs = []
        for job in cached_jobs:
            scored_job = calculate_match_score(job, resume)
            if scored_job["match_score"] > 0:
                scored_jobs.append(scored_job)
            
        # 4. Rank Results
        ranked_jobs = rank_jobs(scored_jobs, sort)
        
        # 5. Pagination
        total_count = len(ranked_jobs)
        start = (page - 1) * limit
        end = start + limit
        paginated_jobs = ranked_jobs[start:end]
        
        return {
            "total": total_count,
            "jobs": paginated_jobs,
            "page": page,
            "limit": limit,
            "total_pages": (total_count + limit - 1) // limit
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
