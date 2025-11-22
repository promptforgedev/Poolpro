from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime, timezone

from models import Route, RouteCreate, RouteUpdate, RouteJobReorder

router = APIRouter(prefix="/routes", tags=["routes"])

# MongoDB will be accessed from server.py
db = None

def init_db(database):
    """Initialize database connection"""
    global db
    db = database


@router.get("/", response_model=List[Route])
async def get_all_routes(day: Optional[str] = Query(None, description="Filter by day")):
    """Get all routes, optionally filtered by day"""
    query = {}
    if day:
        query["day"] = day
    
    routes = await db.routes.find(query, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for route in routes:
        if isinstance(route.get('created_at'), str):
            route['created_at'] = datetime.fromisoformat(route['created_at'])
        if isinstance(route.get('updated_at'), str):
            route['updated_at'] = datetime.fromisoformat(route['updated_at'])
    
    return routes


@router.get("/by-day/{day}", response_model=List[Route])
async def get_routes_by_day(day: str):
    """Get all routes for a specific day"""
    routes = await db.routes.find({"day": day}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for route in routes:
        if isinstance(route.get('created_at'), str):
            route['created_at'] = datetime.fromisoformat(route['created_at'])
        if isinstance(route.get('updated_at'), str):
            route['updated_at'] = datetime.fromisoformat(route['updated_at'])
    
    return routes


@router.get("/by-technician/{technician_id}", response_model=List[Route])
async def get_routes_by_technician(technician_id: str):
    """Get all routes assigned to a specific technician"""
    routes = await db.routes.find({"technician_id": technician_id}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for route in routes:
        if isinstance(route.get('created_at'), str):
            route['created_at'] = datetime.fromisoformat(route['created_at'])
        if isinstance(route.get('updated_at'), str):
            route['updated_at'] = datetime.fromisoformat(route['updated_at'])
    
    return routes


@router.get("/{route_id}", response_model=Route)
async def get_route(route_id: str):
    """Get a specific route by ID"""
    route = await db.routes.find_one({"id": route_id}, {"_id": 0})
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with id {route_id} not found"
        )
    
    # Convert ISO string timestamps
    if isinstance(route.get('created_at'), str):
        route['created_at'] = datetime.fromisoformat(route['created_at'])
    if isinstance(route.get('updated_at'), str):
        route['updated_at'] = datetime.fromisoformat(route['updated_at'])
    
    return Route(**route)


@router.post("/", response_model=Route, status_code=status.HTTP_201_CREATED)
async def create_route(route_data: RouteCreate):
    """Create a new route"""
    route = Route(**route_data.model_dump())
    route.total_stops = len(route.jobs)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = route.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    
    # Insert into database
    await db.routes.insert_one(doc)
    
    return route


@router.put("/{route_id}", response_model=Route)
async def update_route(route_id: str, route_data: RouteUpdate):
    """Update a route"""
    # Check if route exists
    existing = await db.routes.find_one({"id": route_id}, {"_id": 0})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with id {route_id} not found"
        )
    
    # Prepare update data
    update_data = {k: v for k, v in route_data.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    # Update total_stops if jobs were updated
    if "jobs" in update_data:
        update_data["total_stops"] = len(update_data["jobs"])
    
    # Update in database
    await db.routes.update_one(
        {"id": route_id},
        {"$set": update_data}
    )
    
    # Fetch and return updated route
    updated = await db.routes.find_one({"id": route_id}, {"_id": 0})
    
    # Convert ISO string timestamps
    if isinstance(updated.get('created_at'), str):
        updated['created_at'] = datetime.fromisoformat(updated['created_at'])
    if isinstance(updated.get('updated_at'), str):
        updated['updated_at'] = datetime.fromisoformat(updated['updated_at'])
    
    return Route(**updated)


@router.delete("/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(route_id: str):
    """Delete a route"""
    result = await db.routes.delete_one({"id": route_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with id {route_id} not found"
        )
    
    return None


@router.post("/{route_id}/add-job", response_model=Route)
async def add_job_to_route(route_id: str, job_id: str):
    """Add a job to a route"""
    # Check if route exists
    existing = await db.routes.find_one({"id": route_id}, {"_id": 0})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with id {route_id} not found"
        )
    
    # Convert ISO string timestamps
    if isinstance(existing.get('created_at'), str):
        existing['created_at'] = datetime.fromisoformat(existing['created_at'])
    if isinstance(existing.get('updated_at'), str):
        existing['updated_at'] = datetime.fromisoformat(existing['updated_at'])
    
    route = Route(**existing)
    
    # Add job if not already in route
    if job_id not in route.jobs:
        route.jobs.append(job_id)
        route.total_stops = len(route.jobs)
        route.updated_at = datetime.now(timezone.utc)
        
        # Update in database
        await db.routes.update_one(
            {"id": route_id},
            {"$set": {
                "jobs": route.jobs, 
                "total_stops": route.total_stops, 
                "updated_at": route.updated_at.isoformat()
            }}
        )
    
    return route


@router.delete("/{route_id}/remove-job/{job_id}", response_model=Route)
async def remove_job_from_route(route_id: str, job_id: str):
    """Remove a job from a route"""
    # Check if route exists
    existing = await db.routes.find_one({"id": route_id}, {"_id": 0})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with id {route_id} not found"
        )
    
    # Convert ISO string timestamps
    if isinstance(existing.get('created_at'), str):
        existing['created_at'] = datetime.fromisoformat(existing['created_at'])
    if isinstance(existing.get('updated_at'), str):
        existing['updated_at'] = datetime.fromisoformat(existing['updated_at'])
    
    route = Route(**existing)
    
    # Remove job if it exists in route
    if job_id in route.jobs:
        route.jobs.remove(job_id)
        route.total_stops = len(route.jobs)
        route.updated_at = datetime.now(timezone.utc)
        
        # Update in database
        await db.routes.update_one(
            {"id": route_id},
            {"$set": {
                "jobs": route.jobs, 
                "total_stops": route.total_stops, 
                "updated_at": route.updated_at.isoformat()
            }}
        )
    
    return route


@router.put("/{route_id}/reorder", response_model=Route)
async def reorder_route_jobs(route_id: str, reorder_data: RouteJobReorder):
    """Reorder jobs in a route (for drag-drop support)"""
    # Check if route exists
    existing = await db.routes.find_one({"id": route_id}, {"_id": 0})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route with id {route_id} not found"
        )
    
    # Update job order
    update_data = {
        "jobs": reorder_data.jobs,
        "total_stops": len(reorder_data.jobs),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.routes.update_one(
        {"id": route_id},
        {"$set": update_data}
    )
    
    # Fetch and return updated route
    updated = await db.routes.find_one({"id": route_id}, {"_id": 0})
    
    # Convert ISO string timestamps
    if isinstance(updated.get('created_at'), str):
        updated['created_at'] = datetime.fromisoformat(updated['created_at'])
    if isinstance(updated.get('updated_at'), str):
        updated['updated_at'] = datetime.fromisoformat(updated['updated_at'])
    
    return Route(**updated)
