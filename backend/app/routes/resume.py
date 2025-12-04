from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from app.services.resume_parser import extract_text_from_pdf, extract_text_from_docx, parse_resume_text
from app.models.resume import ResumeParsedData, ResumeCreate, Resume, ResumeSaveRequest
from app.models.user import User
from app.core.security import get_current_user
from app.database import database
import shutil
import os
import uuid
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}

def validate_file_extension(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    validate_file_extension(file.filename)
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
        
    return {"filename": unique_filename, "file_path": file_path}

@router.post("/parse", response_model=ResumeParsedData)
async def parse_resume(
    file_path: str,
    current_user: User = Depends(get_current_user)
):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            text = extract_text_from_docx(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        parsed_data = parse_resume_text(text)
        return parsed_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")

from app.models.resume import ResumeParsedData, ResumeCreate, Resume, ResumeSaveRequest

# ... (imports remain the same, just updating the line above if needed, but I will just update the function)

@router.post("/save", response_model=Resume)
async def save_resume(
    resume_data: ResumeSaveRequest,
    current_user: User = Depends(get_current_user)
):
    resume_dict = resume_data.dict()
    resume_dict["user_id"] = current_user["id"]
    # file_path is already in resume_dict
    resume_dict["created_at"] = datetime.utcnow()
    
    # Check if resume exists for this user
    existing_resume = await database.get_collection("resumes").find_one({"user_id": current_user["id"]})
    
    if existing_resume:
        # Update existing resume
        await database.get_collection("resumes").update_one(
            {"_id": existing_resume["_id"]},
            {"$set": resume_dict}
        )
        resume_id = existing_resume["_id"]
    else:
        # Insert new resume
        new_resume = await database.get_collection("resumes").insert_one(resume_dict)
        resume_id = new_resume.inserted_id
    
    created_resume = await database.get_collection("resumes").find_one({"_id": resume_id})
    
    return {
        "id": str(created_resume["_id"]),
        **created_resume
    }
