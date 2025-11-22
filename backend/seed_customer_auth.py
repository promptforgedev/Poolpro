"""
Seed customer auth data for testing customer portal
This script creates auth records for existing customers
Default password for all test accounts: "password123"
"""
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
import asyncio

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_customer_auth():
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    db = client.poolpro
    
    # Clear existing auth data
    await db.customer_auth.delete_many({})
    print("Cleared existing customer auth data")
    
    # Get existing customers
    customers = await db.customers.find({}, {"_id": 0}).to_list(100)
    print(f"Found {len(customers)} customers")
    
    # Create auth for each customer
    # Default password: "password123"
    password_hash = pwd_context.hash("password123")
    
    auth_records = []
    for customer in customers:
        auth_record = {
            "id": f"auth-{customer['id']}",
            "customer_id": customer["id"],
            "email": customer["email"],
            "password_hash": password_hash,
            "created_at": "2024-01-15T10:00:00",
            "updated_at": "2024-01-15T10:00:00"
        }
        auth_records.append(auth_record)
    
    if auth_records:
        result = await db.customer_auth.insert_many(auth_records)
        print(f"✅ Inserted {len(result.inserted_ids)} customer auth records")
        print(f"Default password for all accounts: 'password123'")
        print("\nTest accounts:")
        for customer in customers:
            print(f"  Email: {customer['email']} | Password: password123")
    else:
        print("No customers found to create auth records")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_customer_auth())
