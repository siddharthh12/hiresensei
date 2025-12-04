from typing import List, Dict, Any
from app.models.job import CachedJob
from app.models.resume import Resume
from app.utils.text_similarity import calculate_similarity, extract_years_of_experience, normalize_skills
import re

def calculate_match_score(job: Dict[str, Any], resume: Resume) -> Dict[str, Any]:
    """
    Calculate a match score (0-100) and provide explanation details.
    """
    
    # 1. Skills Match (50%)
    resume_skills = normalize_skills(resume.skills)
    
    # Extract skills from job description (simple keyword matching against resume skills for now)
    # In a real system, we'd use NER to extract skills from job description first.
    # Here, we check which of the user's skills appear in the job description/title
    job_text = (job.get("title", "") + " " + job.get("description", "")).lower()
    
    matching_skills = []
    for skill in resume_skills:
        # Check if skill exists in job text as a whole word
        if re.search(r'\b' + re.escape(skill) + r'\b', job_text):
            matching_skills.append(skill)
            
    # Estimate total required skills (heuristic: length of matching skills + some factor, 
    # or just based on coverage of user's skills if we assume user applies to relevant jobs)
    # Better approach: Let's assume the job has some implicit skills. 
    # For this MVP, let's define score based on how many of USER's skills are relevant.
    # But the requirement says: matched_skills / total_job_skills.
    # Since we don't have structured job skills, we'll infer "missing skills" by looking for common tech keywords 
    # in the job description that are NOT in the resume.
    
    common_tech_stack = ["python", "javascript", "react", "node", "aws", "docker", "sql", "java", "c++", "typescript", "go", "rust", "kubernetes", "html", "css", "django", "fastapi", "flask", "next.js", "vue"]
    
    job_implied_skills = []
    for tech in common_tech_stack:
        pattern = r'\b' + re.escape(tech) + r'\b'
        if tech == "java":
             pattern = r'\bjava\b(?!\s*-?script)'
             
        if re.search(pattern, job_text):
            job_implied_skills.append(tech)
            
    # Add matching skills to implied skills if not already there
    for ms in matching_skills:
        if ms not in job_implied_skills:
            job_implied_skills.append(ms)
            
    if not job_implied_skills:
        # Fallback if no skills detected
        skill_score = 0.5 # Neutral
        missing_skills = []
    else:
        # Intersection of resume skills and job implied skills
        # Note: matching_skills calculation above was slightly different (user skills in job text).
        # Let's refine:
        intersection = [s for s in job_implied_skills if s in resume_skills]
        missing = [s for s in job_implied_skills if s not in resume_skills]
        
        skill_score = len(intersection) / len(job_implied_skills)
        matching_skills = intersection # Update to be consistent
        missing_skills = missing

    # 2. Role Similarity (30%)
    # We don't have a specific "targeted role" in the Resume model yet, 
    # so we'll use the most recent experience title or just assume the user's resume title (if it existed).
    # For now, let's infer targeted role from the resume's "name" or just use the job title vs resume skills/experience text similarity?
    # Requirement says: "User’s targeted role (from resume)". 
    # Let's assume the first item in experience is the current role.
    user_current_role = ""
    if resume.experience:
        # Heuristic: First line of first experience entry might be the role
        user_current_role = resume.experience[0].split('\n')[0]
    
    role_similarity = calculate_similarity(user_current_role, job.get("title", "")) / 100.0
    
    # 3. Experience Match (20%)
    user_exp_years = extract_years_of_experience(resume.experience)
    
    # Extract required exp from job description
    job_req_exp = extract_years_of_experience([job.get("description", "")])
    if job_req_exp == 0:
        job_req_exp = 1.0 # Default to 1 year if not specified
        
    if user_exp_years >= job_req_exp:
        exp_score = 1.0
        exp_diff = f"You have {user_exp_years} years (Job needs {job_req_exp}+)"
    else:
        exp_score = user_exp_years / job_req_exp
        exp_diff = f"Gap: You have {user_exp_years} years (Job needs {job_req_exp}+)"

    # 4. Location Match (Strict Filter)
    # User Requirement: Show ONLY jobs that match User Location OR are Remote.
    user_location = (resume.location or "").lower().strip()
    job_location = (job.get("location") or "").lower().strip()
    
    is_location_match = False
    is_remote = "remote" in job_location
    
    if not user_location:
        # If user hasn't set a location, we can't filter by it. 
        # Assume all locations are okay, or maybe prioritize Remote?
        # For now, let's treat it as a match to avoid hiding everything.
        is_location_match = True
    else:
        # Check for direct match or substring match (e.g. "mumbai" in "mumbai, india")
        if user_location in job_location or job_location in user_location:
            is_location_match = True
        elif is_remote:
            is_location_match = True
            
    if not is_location_match:
        # strict filter: return 0 score if location doesn't match
        return {
            "job_id": job.get("job_id") or str(job.get("_id")),
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "match_score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "experience_difference": "Location mismatch",
            "reason": "Location does not match profile",
            "apply_link": job.get("apply_link"),
            "source": job.get("source"),
            "posted_date": job.get("posted_date"),
            "description": job.get("description")[:200] + "..."
        }

    # Location Bonus (if it's a specific location match, give a small boost over remote?)
    # Let's keep the previous bonus logic but simplified since we already filtered.
    location_score = 0.0
    if user_location and user_location in job_location:
         location_score = 0.15 # Bonus for being in the specific city vs just Remote
            
    # Final Score Calculation
    # Base score from skills, role, experience (sum = 1.0)
    base_score = (skill_score * 0.5) + (role_similarity * 0.3) + (exp_score * 0.2)
    
    # Add location bonus
    final_score = base_score + location_score
    final_score_normalized = min(int(final_score * 100), 100)
    
    # Generate Reason
    reasons = []
    if is_remote and "remote" in job_location:
         reasons.append("Remote job")
    elif location_score > 0:
        reasons.append("Location match")
        
    if skill_score > 0.7:
        reasons.append("Strong skill match")
    elif skill_score > 0.4:
        reasons.append("Good skill overlap")
        
    if role_similarity > 0.8:
        reasons.append("Role aligns perfectly")
    elif role_similarity > 0.5:
        reasons.append("Similar role")
        
    if exp_score == 1.0:
        reasons.append("Experience requirement met")
        
    reason_str = ", ".join(reasons) if reasons else "Partial match based on profile"

    return {
        "job_id": job.get("job_id") or str(job.get("_id")),
        "title": job.get("title"),
        "company": job.get("company"),
        "location": job.get("location"),
        "match_score": final_score_normalized,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills[:5], # Limit to top 5
        "experience_difference": exp_diff,
        "reason": reason_str,
        "apply_link": job.get("apply_link"),
        "source": job.get("source"),
        "posted_date": job.get("posted_date"),
        "description": job.get("description")[:200] + "..." # Truncate for preview
    }

def rank_jobs(jobs_with_scores: List[Dict[str, Any]], sort_key: str = "match") -> List[Dict[str, Any]]:
    """
    Sort jobs based on the requested key.
    """
    if sort_key == "match":
        return sorted(jobs_with_scores, key=lambda x: x["match_score"], reverse=True)
    elif sort_key == "latest":
        # Handle potential missing dates or format issues
        return sorted(jobs_with_scores, key=lambda x: x.get("posted_date") or "", reverse=True)
    elif sort_key == "salary":
        # Placeholder: we don't have salary parsed yet, so keep as is or implement heuristic later
        return jobs_with_scores 
    
    return jobs_with_scores
