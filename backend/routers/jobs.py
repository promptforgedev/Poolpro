from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime, timezone

from models import Job, JobCreate, JobUpdate

router = APIRouter(prefix="/jobs", tags=["jobs"])

# MongoDB will be accessed from server.py
db = None

def init_db(database):
    global db
    db = database


@router.get("/", response_model=List[Job])
async def get_all_jobs(status: Optional[str] = None):
    """Get all jobs, optionally filtered by status"""
    query = {}
    if status:
        query["status"] = status
    jobs = await db.jobs.find(query, {"_id": 0}).to_list(1000)
    return jobs


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str):
    """Get a specific job by ID"""
    job = await db.jobs.find_one({"id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/", response_model=Job)
async def create_job(job: JobCreate):
    """Create a new job"""
    job_dict = job.model_dump()
    new_job = Job(**job_dict)
    await db.jobs.insert_one(new_job.model_dump())
    return new_job


@router.put("/{job_id}", response_model=Job)
async def update_job(job_id: str, job_update: JobUpdate):
    """Update a job"""
    existing_job = await db.jobs.find_one({"id": job_id}, {"_id": 0})
    if not existing_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = job_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    # If status is being updated to completed, set completion time
    if update_data.get("status") == "completed":
        update_data["completed_at"] = datetime.now(timezone.utc)
    
    await db.jobs.update_one({"id": job_id}, {"$set": update_data})
    
    updated_job = await db.jobs.find_one({"id": job_id}, {"_id": 0})
    return Job(**updated_job)


@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """Delete a job"""
    result = db.jobs.delete_one({"id": job_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}


@router.post("/{job_id}/start")
async def start_job(job_id: str):
    """Mark a job as in-progress"""
    job = db.jobs.find_one({"id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.jobs.update_one(
        {"id": job_id}, 
        {"$set": {"status": "in-progress", "updated_at": datetime.now(timezone.utc)}}
    )
    
    updated_job = db.jobs.find_one({"id": job_id}, {"_id": 0})
    return {"message": "Job started", "job": updated_job}


@router.post("/{job_id}/complete")
async def complete_job(job_id: str, completion_notes: Optional[str] = None):
    """Mark a job as completed"""
    job = db.jobs.find_one({"id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_data = {
        "status": "completed",
        "completed_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    if completion_notes:
        update_data["completion_notes"] = completion_notes
    
    db.jobs.update_one({"id": job_id}, {"$set": update_data})
    
    updated_job = db.jobs.find_one({"id": job_id}, {"_id": 0})
    return {"message": "Job completed", "job": updated_job}


@router.get("/by-date/{date}")
async def get_jobs_by_date(date: str):
    """Get all jobs scheduled for a specific date"""
    jobs = list(db.jobs.find({"scheduled_date": date}, {"_id": 0}))
    return jobs


@router.get("/by-technician/{technician}")
async def get_jobs_by_technician(technician: str):
    """Get all jobs assigned to a specific technician"""
    jobs = list(db.jobs.find({"technician": technician}, {"_id": 0}))
    return jobs
