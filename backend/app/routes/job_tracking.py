from fastapi import APIRouter, Depends, HTTPException, Body
from app.database import database
from app.models.user import User
from app.core.security import get_current_user
from app.models.job_tracking import JobTrackingCreate, JobTrackingResponse
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

@router.get("/list", response_model=JobTrackingResponse)
async def list_tracked_jobs(current_user: User = Depends(get_current_user)):
    collection = database.get_collection("job_tracking")
    cursor = collection.find({"user_id": current_user["id"]}).sort("updated_at", -1)
    
    jobs = await cursor.to_list(length=1000)
    
    response = {
        "saved": [],
        "applied": [],
        "not_interested": []
    }
    
    for job in jobs:
        # Map _id to id for the frontend if needed, but here we just return the job_data + tracking info
        job_info = job["job_data"]
        job_info["tracking_id"] = str(job["_id"])
        job_info["status"] = job["status"]
        job_info["updated_at"] = job["updated_at"]
        
        if job["status"] in response:
            response[job["status"]].append(job_info)
            
    return response

@router.get("/status/{job_id}")
async def get_job_status(job_id: str, current_user: User = Depends(get_current_user)):
    collection = database.get_collection("job_tracking")
    job = await collection.find_one({"user_id": current_user["id"], "job_id": job_id})
    if job:
        return {"status": job["status"]}
    return {"status": None}
