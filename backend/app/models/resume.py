from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ResumeBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    experience: List[str] = []
    education: List[str] = []
    certifications: List[str] = []
    location: Optional[str] = None

class ResumeCreate(ResumeBase):
    user_id: str
    file_path: str

class Resume(ResumeBase):
    id: str
    user_id: str
    file_path: str
    created_at: datetime

    class Config:
        orm_mode = True

class ResumeParsedData(ResumeBase):
    pass

class ResumeSaveRequest(ResumeBase):
    file_path: str
