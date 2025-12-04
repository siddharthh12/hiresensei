from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from app.database import database as db
from app.routes.auth import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.job_tracking import JobTracking
from app.models.job import CachedJob
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from app.database import database as db
from app.routes.auth import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.job_tracking import JobTracking
from app.models.job import CachedJob
from collections import Counter

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(current_user: User = Depends(get_current_user)):
    try:
        user_id = current_user["id"]

        # 1. Basic Stats
        # Recommended: Count of cached jobs (proxy for now, ideally filtered by user relevance if we had that stored)
        # For now, we'll just count total cached jobs as a placeholder or maybe jobs matching user skills if possible.
        # The prompt says "total_jobs_recommended -> count of jobs matched in last search".
        # Since we don't strictly persist "last search results" per user in a separate collection, 
        # we can count all CachedJobs or just return a placeholder if no search done.
        # Let's count all CachedJobs for now as a simple proxy for "available matches".
        total_recommended = await db["cached_jobs"].count_documents({})

        # Tracking Stats
        saved_count = await db["job_tracking"].count_documents({"user_id": user_id, "status": "saved"})
        applied_count = await db["job_tracking"].count_documents({"user_id": user_id, "status": "applied"})
        not_interested_count = await db["job_tracking"].count_documents({"user_id": user_id, "status": "not_interested"})

        # 2. Profile Stats
        resume = await db["resumes"].find_one({"user_id": user_id})
        skills_count = 0
        experience_years = 0
        profile_completion = 0

        if resume:
            skills_count = len(resume.get("skills", []))
            # Experience years calculation
            from app.utils.text_similarity import extract_years_of_experience
            experience_years = extract_years_of_experience(resume.get("experience", [])) 
            
            # Profile Completion Calculation
            # Resume uploaded -> +30%
            profile_completion += 30
            # Skills extracted -> +20% (if > 0)
            if skills_count > 0:
                profile_completion += 20
            # Experience parsed -> +20% (if > 0)
            if experience_years > 0:
                profile_completion += 20
            
        # Tracking started -> +10% (if any tracking exists)
        total_tracking = saved_count + applied_count + not_interested_count
        if total_tracking > 0:
            profile_completion += 10
        
        # Recommended jobs viewed -> +20% (We don't track "viewed" strictly, but if they have tracking data or we assume they visited dashboard)
        # Let's assume if they have any tracking data, they viewed jobs. Or we can just give it if they have performed a search (cached jobs exist).
        if total_recommended > 0:
            profile_completion += 20

        profile_completion = min(profile_completion, 100)

        # 3. Recent Activity
        # Get last 3 saved
        cursor_saved = db["job_tracking"].find({"user_id": user_id, "status": "saved"}).sort("updated_at", -1).limit(3)
        recent_saved = await cursor_saved.to_list(length=3)
        
        # Get last 3 applied
        cursor_applied = db["job_tracking"].find({"user_id": user_id, "status": "applied"}).sort("updated_at", -1).limit(3)
        recent_applied = await cursor_applied.to_list(length=3)

        # Format recent activity
        def format_activity(tracking_docs):
            activity = []
            for doc in tracking_docs:
                job_data = doc.get("job_data", {})
                activity.append({
                    "id": str(doc["_id"]),
                    "job_id": doc.get("job_id"),
                    "title": job_data.get("title", "Unknown Title"),
                    "company": job_data.get("company", "Unknown Company"),
                    "status": doc.get("status"),
                    "updated_at": doc.get("updated_at")
                })
            return activity

        return {
            "stats": {
                "recommended": total_recommended,
                "saved": saved_count,
                "applied": applied_count,
                "not_interested": not_interested_count
            },
            "profile": {
                "skills_count": skills_count,
                "experience_years": experience_years,
                "profile_completion": profile_completion
            },
            "recent_activity": {
                "saved_jobs": format_activity(recent_saved),
                "applied_jobs": format_activity(recent_applied)
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/skills")
async def get_skill_analytics(current_user: User = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        resume = await db["resumes"].find_one({"user_id": user_id})
        
        user_skills = []
        if resume:
            user_skills = resume.get("skills", [])

        # Recommended Skills (Market Demand)
        # Aggregate skills from CachedJobs. 
        # Since CachedJob doesn't have a structured 'skills' field, we have to extract them or use description.
        # For this MVP, we will do a simple word frequency on job descriptions or titles if description is too heavy,
        # BUT the prompt suggests "skills that occur frequently in job descriptions".
        # Doing NLP on all descriptions on the fly is too slow.
        # We will try to fetch a sample of jobs and do a quick keyword match against a predefined list of common tech skills
        # OR just return a static list of "hot" skills if dynamic is too hard.
        # BETTER APPROACH: Let's assume we have some extracted skills in jobs or we just look for common keywords.
        # For now, I will use a simple predefined list of common tech skills and count their occurrence in a sample of job descriptions.
        
        common_skills = ["Python", "Java", "JavaScript", "React", "Node.js", "SQL", "NoSQL", "AWS", "Docker", "Kubernetes", "TypeScript", "Go", "Rust", "C++", "C#", "HTML", "CSS", "Git", "CI/CD", "Machine Learning", "AI", "FastAPI", "Django", "Flask", "Spring", "Vue", "Angular", "MongoDB", "PostgreSQL", "Redis"]
        
        # Fetch a sample of recent jobs to analyze
        recent_jobs = await db["cached_jobs"].find({}).limit(50).to_list(length=50)
        
        skill_counts = Counter()
        for job in recent_jobs:
            text = (job.get("description", "") + " " + job.get("title", "")).lower()
            for skill in common_skills:
                import re
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if skill.lower() == "java":
                    pattern = r'\bjava\b(?!\s*-?script)'
                
                if re.search(pattern, text):
                    skill_counts[skill] += 1
                    
        recommended_skills_data = [{"skill": skill, "frequency": count} for skill, count in skill_counts.most_common(10)]
        
        # Missing Skills
        # Skills in recommended (top 10) that are NOT in user_skills
        # Normalize for comparison
        user_skills_lower = set(s.lower() for s in user_skills)
        missing_skills = []
        
        for item in recommended_skills_data:
            if item["skill"].lower() not in user_skills_lower:
                missing_skills.append(item["skill"])

        return {
            "top_user_skills": user_skills[:10], # Top 10 user skills
            "missing_skills": missing_skills,
            "recommended_skills": recommended_skills_data
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
