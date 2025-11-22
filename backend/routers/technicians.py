from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime, timezone

from models import Technician, TechnicianCreate, TechnicianUpdate

router = APIRouter(prefix="/technicians", tags=["technicians"])

# MongoDB will be accessed from server.py
db = None

def init_db(database):
    """Initialize database connection"""
    global db
    db = database


@router.get("/", response_model=List[Technician])
async def get_all_technicians():
    """Get all technicians"""
    technicians = await db.technicians.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for technician in technicians:
        if isinstance(technician.get('created_at'), str):
            technician['created_at'] = datetime.fromisoformat(technician['created_at'])
        if isinstance(technician.get('updated_at'), str):
            technician['updated_at'] = datetime.fromisoformat(technician['updated_at'])
    
    return technicians


@router.get("/{technician_id}", response_model=Technician)
async def get_technician(technician_id: str):
    """Get a specific technician by ID"""
    technician = await db.technicians.find_one({"id": technician_id}, {"_id": 0})
    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Technician with id {technician_id} not found"
        )
    
    # Convert ISO string timestamps
    if isinstance(technician.get('created_at'), str):
        technician['created_at'] = datetime.fromisoformat(technician['created_at'])
    if isinstance(technician.get('updated_at'), str):
        technician['updated_at'] = datetime.fromisoformat(technician['updated_at'])
    
    return Technician(**technician)


@router.post("/", response_model=Technician, status_code=status.HTTP_201_CREATED)
async def create_technician(technician_data: TechnicianCreate):
    """Create a new technician"""
    technician = Technician(**technician_data.model_dump())
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = technician.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    
    # Insert into database
    await db.technicians.insert_one(doc)
    
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
