from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from app.database import job_collection, job_helper, database
from app.models.job import (
    JobSchema,
    UpdateJobModel,
    ResponseModel,
    ErrorResponseModel,
    CachedJob
)
from app.services.job_fetcher import fetch_jobs_from_api
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import hashlib

router = APIRouter()

@router.get("/test-api", response_description="Test RapidAPI Connection")
async def test_api():
    try:
        jobs = await fetch_jobs_from_api(query="Python", location="Remote", remote=True)
        return {
            "status": "success",
            "jobs": jobs[:3] if jobs else []
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def generate_query_key(query: str, location: str, remote: bool) -> str:
    raw = f"{query.lower()}-{location.lower() if location else ''}-{str(remote).lower()}"
    return hashlib.md5(raw.encode()).hexdigest()

@router.get("/search", response_description="Search jobs from API or Cache")
async def search_jobs(
    query: str = Query(..., min_length=1),
    location: str = Query(None),
    remote: bool = Query(False),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    query_key = generate_query_key(query, location, remote)
    skip = (page - 1) * limit
    
    # 1. Check Cache
    cached_jobs_cursor = database.get_collection("cached_jobs").find({"query_key": query_key})
    total_count = await database.get_collection("cached_jobs").count_documents({"query_key": query_key})
    cached_jobs = await cached_jobs_cursor.skip(skip).limit(limit).to_list(length=limit)
    
    if cached_jobs:
        # Check if cache is fresh (e.g., < 24 hours)
        # Assuming all jobs in a batch have similar fetched_at, check the first one
        first_job = cached_jobs[0]
        if "fetched_at" in first_job:
            fetched_at = first_job["fetched_at"]
            if datetime.utcnow() - fetched_at < timedelta(hours=24):
                # Return cached
                # Convert ObjectId to str for response
                for job in cached_jobs:
                    job["_id"] = str(job["_id"])
                
                return {
                    "data": cached_jobs,
                    "code": 200,
                    "message": "Jobs retrieved from cache",
                    "meta": {
                        "page": page,
                        "limit": limit,
                        "total": total_count,
                        "total_pages": (total_count + limit - 1) // limit
                    }
                }
            else:
                # Cache expired, delete old entries
                await database.get_collection("cached_jobs").delete_many({"query_key": query_key})
    
    # 2. Fetch from API
    fetched_data = await fetch_jobs_from_api(query, location, remote)
    
    if not fetched_data:
        return {
            "data": [],
            "code": 200,
            "message": "No jobs found",
            "meta": {
                "page": page,
                "limit": limit,
                "total": 0,
                "total_pages": 0
            }
        }
        
    # 3. Save to Cache
    jobs_to_cache = []
    for job in fetched_data:
        job["query_key"] = query_key
        job["fetched_at"] = datetime.utcnow()
        jobs_to_cache.append(job)
        
    if jobs_to_cache:
        await database.get_collection("cached_jobs").insert_many(jobs_to_cache)
    
    for job in fetched_data:
        if "_id" in job:
            job["_id"] = str(job["_id"])

    # Pagination for API results (in-memory since API returns all or limited batch)
    # Assuming fetch_jobs_from_api returns a list, we slice it here if it's large, 
    # but typically external APIs paginate. Here we just return what we got, 
    # but to be consistent with the interface, we'll pretend it's one page or slice it.
    # Since we just cached them, we can query the cache again or just return the slice.
    # For simplicity, let's return the slice of what we just fetched.
    
    total_fetched = len(fetched_data)
    start = (page - 1) * limit
    end = start + limit
    paginated_data = fetched_data[start:end]
        
    return {
        "data": paginated_data,
        "code": 200,
        "message": "Jobs fetched from API",
        "meta": {
            "page": page,
            "limit": limit,
            "total": total_fetched,
            "total_pages": (total_fetched + limit - 1) // limit
        }
    }

# --- Existing CRUD Operations ---

@router.post("", response_description="Job data added into the database")
async def add_job_data(job: JobSchema = Body(...)):
    job = jsonable_encoder(job)
    new_job = await job_collection.insert_one(job)
    created_job = await job_collection.find_one({"_id": new_job.inserted_id})
    return ResponseModel(job_helper(created_job), "Job added successfully.")

@router.get("s", response_description="Jobs retrieved")
async def get_jobs():
    jobs = []
    async for job in job_collection.find():
        jobs.append(job_helper(job))
    return ResponseModel(jobs, "Jobs data retrieved successfully")

@router.get("/{id}", response_description="Job data retrieved")
async def get_job_data(id: str):
    job = await job_collection.find_one({"_id": ObjectId(id)})
    if job:
        return ResponseModel(job_helper(job), "Job data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Job doesn't exist.")

@router.put("/{id}")
async def update_job_data(id: str, req: UpdateJobModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_job = await job_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": req}
    )
    if updated_job.modified_count == 1:
        return ResponseModel(
            "Job with ID: {} name update is successful".format(id),
            "Job name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the job data.",
    )

@router.delete("/{id}", response_description="Job data deleted from the database")
async def delete_job_data(id: str):
    deleted_job = await job_collection.delete_one({"_id": ObjectId(id)})
    if deleted_job.deleted_count == 1:
        return ResponseModel(
            "Job with ID: {} removed".format(id), "Job deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Job with id {0} doesn't exist".format(id)
    )
