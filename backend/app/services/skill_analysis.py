from typing import List, Dict, Any
from collections import Counter
from app.database import database
from app.models.resume import Resume
from app.models.job import CachedJob
from app.utils.skill_extraction import normalize_skill_list, extract_skills_from_text

class SkillAnalysisService:
    async def analyze_skills(self, user_id: str) -> Dict[str, Any]:
        # 1. Get User Skills
        user_skills = await self._get_user_skills(user_id)
        
        # 2. Get Market Skills (from all cached jobs)
        market_skills_data = await self._get_market_skills()
        market_skills_counter = market_skills_data["counter"]
        total_jobs = market_skills_data["total_jobs"]
        
        # 3. Identify Missing Skills
        missing_skills = []
        user_skill_set = set(user_skills)
        
        # Filter market skills that appear in at least 2 jobs (Rule 2)
        relevant_market_skills = {k: v for k, v in market_skills_counter.items() if v >= 2}
        
        max_frequency = max(relevant_market_skills.values()) if relevant_market_skills else 1
        
        for skill, frequency in relevant_market_skills.items():
            if skill not in user_skill_set:
                priority = int((frequency / max_frequency) * 100)
                missing_skills.append({
                    "skill": skill,
                    "priority": priority,
                    "frequency": frequency
                })
        
        # Sort missing skills by priority (descending)
        missing_skills.sort(key=lambda x: x["priority"], reverse=True)
        
        # 4. Prepare Top Market Skills
        top_market_skills = [
            {"skill": skill, "frequency": freq}
            for skill, freq in sorted(relevant_market_skills.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        # 5. Calculate Skill Strengths (User skills coverage vs market demand)
        skill_strengths = []
        for skill in user_skills:
            freq = relevant_market_skills.get(skill, 0)
            # Simple strength metric: if it's in demand, it's a strong skill. 
            # If user has it, coverage is 100% relative to themselves, 
            # but maybe we want to show how 'valuable' it is?
            # The prompt example says: { "skill": "Python", "coverage": 100 }
            # Let's map coverage to relative market importance for now.
            coverage = int((freq / max_frequency) * 100) if max_frequency > 0 else 0
            skill_strengths.append({
                "skill": skill,
                "coverage": coverage
            })
        
        skill_strengths.sort(key=lambda x: x["coverage"], reverse=True)

        return {
            "user_skills": user_skills,
            "market_skills": list(relevant_market_skills.keys()),
            "missing_skills": missing_skills,
            "top_market_skills": top_market_skills,
            "skill_strengths": skill_strengths,
            "total_jobs_analyzed": total_jobs
        }

    async def _get_user_skills(self, user_id: str) -> List[str]:
        resume_data = await database["resumes"].find_one({"user_id": user_id})
        if resume_data and "skills" in resume_data:
            return normalize_skill_list(resume_data["skills"])
        return []

    async def _get_market_skills(self) -> Dict[str, Any]:
        # Fetch all cached jobs
        cursor = database["cached_jobs"].find({})
        jobs = await cursor.to_list(length=1000)
        
        all_skills = []
        for job in jobs:
            # Extract skills from title and description
            text = f"{job.get('title', '')} {job.get('description', '')}"
            skills = extract_skills_from_text(text)
            all_skills.extend(skills)
            
        return {
            "counter": Counter(all_skills),
            "total_jobs": len(jobs)
        }
