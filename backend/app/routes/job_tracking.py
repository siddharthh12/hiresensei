from fastapi import APIRouter, Depends, HTTPException, Body
from app.database import database
from app.models.user import User
from app.core.security import get_current_user
from app.models.job_tracking import JobTrackingCreate
from datetime import datetime
from typing import List

router = APIRouter()

async def upsert_job_status(user_id: str, job_id: str, status: str, job_data: dict):
    collection = database.get_collection("job_tracking")
    
    existing_entry = await collection.find_one({"user_id": user_id, "job_id": job_id})
    
    if existing_entry:
        await collection.update_one(
            {"_id": existing_entry["_id"]},
            {"$set": {"status": status, "updated_at": datetime.utcnow(), "job_data": job_data}}
        )
    else:
        new_entry = {
            "user_id": user_id,
            "job_id": job_id,
            "status": status,
            "job_data": job_data,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        await collection.insert_one(new_entry)

@router.post("/save")
async def save_job(
    data: JobTrackingCreate,
    current_user: User = Depends(get_current_user)
):
    await upsert_job_status(current_user["id"], data.job_id, "saved", data.job_data)
    return {"message": "Job saved successfully"}

@router.post("/applied")
async def mark_applied(
    data: JobTrackingCreate,
    current_user: User = Depends(get_current_user)
):
    await upsert_job_status(current_user["id"], data.job_id, "applied", data.job_data)
    return {"message": "Job marked as applied"}

@router.post("/not-interested")
async def mark_not_interested(
    data: JobTrackingCreate,
    current_user: User = Depends(get_current_user)
):
    await upsert_job_status(current_user["id"], data.job_id, "not_interested", data.job_data)
    return {"message": "Job marked as not interested"}

@router.get("/list")
async def list_tracked_jobs(
    status: str = "saved",
    page: int = 1,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    collection = database.get_collection("job_tracking")
    skip = (page - 1) * limit
    
    query = {"user_id": current_user["id"]}
    if status:
        query["status"] = status
        
    total_count = await collection.count_documents(query)
    cursor = collection.find(query).sort("updated_at", -1).skip(skip).limit(limit)
    
    jobs = await cursor.to_list(length=limit)
    
    data = [] 
    for job in jobs:
        job_info = job["job_data"]
        job_info["tracking_id"] = str(job["_id"])
        job_info["status"] = job["status"]
        job_info["updated_at"] = job["updated_at"]
        data.append(job_info)
            
    return {
        "data": data,
        "total": total_count,
        "page": page,
        "limit": limit,
        "total_pages": (total_count + limit - 1) // limit
    }

@router.get("/status/{job_id}")
async def get_job_status(job_id: str, current_user: User = Depends(get_current_user)):
    collection = database.get_collection("job_tracking")
    job = await collection.find_one({"user_id": current_user["id"], "job_id": job_id})
    if job:
        return {"status": job["status"]}
    return {"status": None}
