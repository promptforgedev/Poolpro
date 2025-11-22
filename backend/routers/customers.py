from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os

from models import Customer, CustomerCreate, CustomerUpdate, Pool, PoolCreate, ChemReading, ChemReadingCreate

router = APIRouter(prefix="/api/customers", tags=["customers"])

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


@router.get("/", response_model=List[Customer])
async def get_customers():
    """Get all customers with their pools"""
    customers = await db.customers.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for customer in customers:
        if isinstance(customer.get('created_at'), str):
            customer['created_at'] = datetime.fromisoformat(customer['created_at'])
        if isinstance(customer.get('updated_at'), str):
            customer['updated_at'] = datetime.fromisoformat(customer['updated_at'])
    
    return customers


@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str):
    """Get a specific customer by ID"""
    customer = await db.customers.find_one({"id": customer_id}, {"_id": 0})
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(customer.get('created_at'), str):
        customer['created_at'] = datetime.fromisoformat(customer['created_at'])
    if isinstance(customer.get('updated_at'), str):
        customer['updated_at'] = datetime.fromisoformat(customer['updated_at'])
    
    return customer


@router.post("/", response_model=Customer)
async def create_customer(customer_input: CustomerCreate):
    """Create a new customer"""
    customer_dict = customer_input.model_dump()
    
    # Convert PoolCreate objects to Pool objects with IDs
    pools = []
    for pool_data in customer_dict.get('pools', []):
        pool = Pool(**pool_data)
        pools.append(pool.model_dump())
    
    customer_dict['pools'] = pools
    customer = Customer(**customer_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = customer.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    
    await db.customers.insert_one(doc)
    return customer


@router.put("/{customer_id}", response_model=Customer)
async def update_customer(customer_id: str, customer_update: CustomerUpdate):
    """Update a customer"""
    existing_customer = await db.customers.find_one({"id": customer_id}, {"_id": 0})
    
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Update only provided fields
    update_data = customer_update.model_dump(exclude_unset=True)
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    await db.customers.update_one(
        {"id": customer_id},
        {"$set": update_data}
    )
    
    # Fetch updated customer
    updated_customer = await db.customers.find_one({"id": customer_id}, {"_id": 0})
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(updated_customer.get('created_at'), str):
        updated_customer['created_at'] = datetime.fromisoformat(updated_customer['created_at'])
    if isinstance(updated_customer.get('updated_at'), str):
        updated_customer['updated_at'] = datetime.fromisoformat(updated_customer['updated_at'])
    
    return updated_customer


@router.delete("/{customer_id}")
async def delete_customer(customer_id: str):
    """Delete a customer"""
    result = await db.customers.delete_one({"id": customer_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"message": "Customer deleted successfully"}


@router.post("/{customer_id}/pools", response_model=Customer)
async def add_pool_to_customer(customer_id: str, pool_input: PoolCreate):
    """Add a pool to a customer"""
    existing_customer = await db.customers.find_one({"id": customer_id}, {"_id": 0})
    
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Create pool with ID
    pool = Pool(**pool_input.model_dump())
    
    # Add pool to customer's pools array
    await db.customers.update_one(
        {"id": customer_id},
        {
            "$push": {"pools": pool.model_dump()},
            "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
        }
    )
    
    # Fetch updated customer
    updated_customer = await db.customers.find_one({"id": customer_id}, {"_id": 0})
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(updated_customer.get('created_at'), str):
        updated_customer['created_at'] = datetime.fromisoformat(updated_customer['created_at'])
    if isinstance(updated_customer.get('updated_at'), str):
        updated_customer['updated_at'] = datetime.fromisoformat(updated_customer['updated_at'])
    
    return updated_customer


@router.post("/{customer_id}/pools/{pool_id}/readings", response_model=Customer)
async def add_chem_reading(customer_id: str, pool_id: str, reading: ChemReadingCreate):
    """Add a chemical reading to a specific pool"""
    existing_customer = await db.customers.find_one({"id": customer_id}, {"_id": 0})
    
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Find the pool in the customer's pools array
    pool_found = False
    for pool in existing_customer.get('pools', []):
        if pool['id'] == pool_id:
            pool_found = True
            break
    
    if not pool_found:
        raise HTTPException(status_code=404, detail="Pool not found")
    
    # Add reading to the pool's chem_readings array
    chem_reading = ChemReading(**reading.model_dump())
    
    await db.customers.update_one(
        {"id": customer_id, "pools.id": pool_id},
        {
            "$push": {"pools.$.chem_readings": chem_reading.model_dump()},
            "$set": {
                "pools.$.last_service": reading.date,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    # Fetch updated customer
    updated_customer = await db.customers.find_one({"id": customer_id}, {"_id": 0})
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(updated_customer.get('created_at'), str):
        updated_customer['created_at'] = datetime.fromisoformat(updated_customer['created_at'])
    if isinstance(updated_customer.get('updated_at'), str):
        updated_customer['updated_at'] = datetime.fromisoformat(updated_customer['updated_at'])
    
    return updated_customer


@router.get("/{customer_id}/pools/{pool_id}/readings", response_model=List[ChemReading])
async def get_chem_readings(customer_id: str, pool_id: str):
    """Get all chemical readings for a specific pool"""
    customer = await db.customers.find_one({"id": customer_id}, {"_id": 0})
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Find the pool
    for pool in customer.get('pools', []):
        if pool['id'] == pool_id:
            return pool.get('chem_readings', [])
    
    raise HTTPException(status_code=404, detail="Pool not found")
