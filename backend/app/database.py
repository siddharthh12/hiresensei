import motor.motor_asyncio
from bson.objectid import ObjectId
from app.core.config import settings

MONGO_DETAILS = settings.MONGO_DETAILS

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.ai_job_db

job_collection = database.get_collection("jobs_collection")
user_collection = database.get_collection("users_collection")

# Helpers

def job_helper(job) -> dict:
    return {
        "id": str(job["_id"]),
        "title": job["title"],
        "description": job["description"],
        "company": job["company"],
        "location": job["location"],
    }

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "full_name": user.get("full_name"),
        "email": user["email"],
        "created_at": user.get("created_at"),
    }
