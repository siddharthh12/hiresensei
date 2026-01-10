from app.models.hybrid_job import HybridJob
from datetime import datetime, timezone
from typing import Dict, Any, List

def normalize_job_data(
    job_id: str,
    title: str,
    company: str,
    location: str,
    description: str,
    apply_link: str,
    source: str,
    job_type: str = "Full-time",
    published_at: datetime = None,
    skills: List[str] = [],
    raw_data: Dict[str, Any] = {}
) -> HybridJob:
    """
    Helper to create a HybridJob instance with default values and validation.
    """
    # Normalize published_at to UTC naive
    if published_at and published_at.tzinfo:
        published_at = published_at.astimezone(timezone.utc).replace(tzinfo=None)

    return HybridJob(
        job_id=str(job_id),
        title=title or "Unknown Title",
        company=company or "Unknown Company",
        location=location or "Remote",
        description=description or "",
        job_type=job_type,
        apply_link=apply_link or "#",
        source=source,
        published_at=published_at,
        skills=skills,
        raw_data=raw_data,
        fetched_at=datetime.utcnow()
    )
