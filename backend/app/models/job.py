from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class JobSchema(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    company: str = Field(...)
    location: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Software Engineer",
                "description": "Develop amazing applications",
                "company": "Tech Corp",
                "location": "Remote"
            }
        }

class CachedJob(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    job_type: Optional[str]
    apply_link: Optional[str]
    description: Optional[str]
    source: str
    posted_date: Optional[str]
    query_key: str
    fetched_at: datetime

    class Config:
        from_attributes = True

class UpdateJobModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Senior Software Engineer",
                "description": "Lead the team",
                "company": "Tech Corp",
                "location": "Remote"
            }
        }

def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message,
    }
