from fastapi import APIRouter, Depends, HTTPException
from app.services.skill_analysis import SkillAnalysisService
from app.routes.auth import get_current_user

router = APIRouter()
skill_service = SkillAnalysisService()

@router.get("/analysis")
async def get_skill_analysis(current_user: dict = Depends(get_current_user)):
    """
    Get skill gap analysis for the current user.
    """
    user_id = current_user["id"]
    try:
        analysis = await skill_service.analyze_skills(user_id)
        return {
            "data": analysis,
            "code": 200,
            "message": "Skill analysis retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
