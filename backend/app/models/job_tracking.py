from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class JobTrackingBase(BaseModel):
    job_id: str
    job_data: Dict[str, Any]

class JobTrackingCreate(JobTrackingBase):
    pass

class JobTracking(JobTrackingBase):
    id: str
    user_id: str
    status: str # saved, applied, not_interested
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class JobTrackingResponse(BaseModel):
    saved: list = []
    applied: list = []
    not_interested: list = []
