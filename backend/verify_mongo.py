import asyncio
from database import job_collection, job_helper
from bson.objectid import ObjectId

async def verify_crud():
    print("Starting CRUD verification...")

    # 1. Create
    new_job = {
        "title": "Test Job",
        "description": "This is a test job",
        "company": "Test Company",
        "location": "Test Location"
    }
    print(f"Creating job: {new_job}")
    insert_result = await job_collection.insert_one(new_job)
    job_id = insert_result.inserted_id
    print(f"Job created with ID: {job_id}")

    # 2. Read
    print(f"Reading job with ID: {job_id}")
    job = await job_collection.find_one({"_id": job_id})
    if job:
        print(f"Job found: {job_helper(job)}")
    else:
        print("Job not found!")
        return

    # 3. Update
    print(f"Updating job with ID: {job_id}")
    update_result = await job_collection.update_one(
        {"_id": job_id}, {"$set": {"title": "Updated Test Job"}}
    )
    print(f"Modified count: {update_result.modified_count}")
    
    updated_job = await job_collection.find_one({"_id": job_id})
    print(f"Updated job: {job_helper(updated_job)}")

    # 4. Delete
    print(f"Deleting job with ID: {job_id}")
    delete_result = await job_collection.delete_one({"_id": job_id})
    print(f"Deleted count: {delete_result.deleted_count}")

    # Verify deletion
    deleted_job = await job_collection.find_one({"_id": job_id})
    if not deleted_job:
        print("Job successfully deleted.")
    else:
        print("Job still exists!")

    print("CRUD verification completed.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(verify_crud())
