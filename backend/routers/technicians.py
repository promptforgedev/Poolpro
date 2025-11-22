from fastapi import APIRouter, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
import os
from datetime import datetime, timezone

from models import Technician, TechnicianCreate, TechnicianUpdate

router = APIRouter(prefix="/api/technicians", tags=["technicians"])

# MongoDB connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.poolpro
technicians_collection = db.technicians


@router.get("/", response_model=List[Technician])
async def get_all_technicians():
    """Get all technicians"""
    technicians = []
    async for technician in technicians_collection.find():
        technicians.append(Technician(**technician))
    return technicians


@router.get("/{technician_id}", response_model=Technician)
async def get_technician(technician_id: str):
    """Get a specific technician by ID"""
    technician = await technicians_collection.find_one({"id": technician_id})
    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Technician with id {technician_id} not found"
        )
    return Technician(**technician)


@router.post("/", response_model=Technician, status_code=status.HTTP_201_CREATED)
async def create_technician(technician_data: TechnicianCreate):
    """Create a new technician"""
    technician = Technician(**technician_data.model_dump())
    
    # Insert into database
    await technicians_collection.insert_one(technician.model_dump())
    
    return technician


@router.put("/{technician_id}", response_model=Technician)
async def update_technician(technician_id: str, technician_data: TechnicianUpdate):
    """Update a technician"""
    # Check if technician exists
    existing = await technicians_collection.find_one({"id": technician_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Technician with id {technician_id} not found"
        )
    
    # Prepare update data
    update_data = {k: v for k, v in technician_data.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    # Update in database
    await technicians_collection.update_one(
        {"id": technician_id},
        {"$set": update_data}
    )
    
    # Fetch and return updated technician
    updated = await technicians_collection.find_one({"id": technician_id})
    return Technician(**updated)


@router.delete("/{technician_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_technician(technician_id: str):
    """Delete a technician"""
    result = await technicians_collection.delete_one({"id": technician_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Technician with id {technician_id} not found"
        )
    
    return None
