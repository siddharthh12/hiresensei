from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class HybridJob(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    description: str
    job_type: Optional[str] = "Full-time"
    apply_link: str
    source: str = Field(..., description="Source of the job: api | remoteok | wwr | hn")
    published_at: Optional[datetime] = None
    skills: List[str] = []
    raw_data: Dict[str, Any] = {}
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Matching Engine Fields
    match_score: Optional[int] = None
    matching_skills: List[str] = []
    missing_skills: List[str] = []
    experience_difference: Optional[str] = None
    reason: Optional[str] = None

class HybridJobResponse(BaseModel):
    jobs: List[HybridJob]
    external_search_links: Dict[str, str]
    sources_used: List[str]
    total: int
