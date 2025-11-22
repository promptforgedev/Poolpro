"""
Seed script to populate the database with initial customer and pool data
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
db_name = os.environ['DB_NAME']

# Mock customer data
mock_customers = [
    {
        "id": "cust-1",
        "name": "John Anderson",
        "email": "john.anderson@email.com",
        "phone": "(555) 123-4567",
        "address": "1234 Oak Street, Austin, TX 78701",
        "status": "active",
        "account_balance": 0.0,
        "service_day": "Monday",
        "route_position": 1,
        "autopay": True,
        "pools": [
            {
                "id": "pool-1",
                "name": "Main Pool",
                "type": "In-Ground",
                "color": "#3B82F6",
                "gallons": 25000,
                "equipment": ["Pump", "Filter", "Heater", "Salt Cell"],
                "last_service": "2025-01-15",
                "chem_readings": [
                    {"date": "2025-01-15", "fc": 3.2, "ph": 7.4, "ta": 120, "ch": 250, "cya": 50},
                    {"date": "2025-01-08", "fc": 2.8, "ph": 7.6, "ta": 115, "ch": 240, "cya": 50},
                    {"date": "2025-01-01", "fc": 3.5, "ph": 7.2, "ta": 125, "ch": 260, "cya": 50}
                ]
            }
        ]
    },
    {
        "id": "cust-2",
        "name": "Sarah Mitchell",
        "email": "sarah.mitchell@email.com",
        "phone": "(555) 234-5678",
        "address": "5678 Pine Avenue, Austin, TX 78702",
        "status": "active",
        "account_balance": -125.50,
        "service_day": "Monday",
        "route_position": 2,
        "autopay": False,
        "pools": [
            {
                "id": "pool-2",
                "name": "Main Pool",
                "type": "In-Ground",
                "color": "#3B82F6",
                "gallons": 18000,
                "equipment": ["Pump", "Filter", "Salt Cell"],
                "last_service": "2025-01-15",
                "chem_readings": [
                    {"date": "2025-01-15", "fc": 2.5, "ph": 7.8, "ta": 140, "ch": 280, "cya": 60},
                    {"date": "2025-01-08", "fc": 2.2, "ph": 7.9, "ta": 145, "ch": 290, "cya": 60}
                ]
            },
            {
                "id": "pool-3",
                "name": "Spa",
                "type": "Spa/Hot Tub",
                "color": "#F59E0B",
                "gallons": 400,
                "equipment": ["Heater", "Jets"],
                "last_service": "2025-01-15",
                "chem_readings": [
                    {"date": "2025-01-15", "fc": 4.0, "ph": 7.5, "ta": 100, "ch": 180, "cya": 30}
                ]
            }
        ]
    },
    {
        "id": "cust-3",
        "name": "Michael Torres",
        "email": "michael.torres@email.com",
        "phone": "(555) 345-6789",
        "address": "9012 Elm Drive, Austin, TX 78703",
        "status": "active",
        "account_balance": 75.00,
        "service_day": "Tuesday",
        "route_position": 1,
        "autopay": True,
        "pools": [
            {
                "id": "pool-4",
                "name": "Pool",
                "type": "Above-Ground",
                "color": "#10B981",
                "gallons": 15000,
                "equipment": ["Pump", "Filter"],
                "last_service": "2025-01-14",
                "chem_readings": [
                    {"date": "2025-01-14", "fc": 3.0, "ph": 7.3, "ta": 110, "ch": 230, "cya": 45}
                ]
            }
        ]
    },
    {
        "id": "cust-4",
        "name": "Emily Roberts",
        "email": "emily.roberts@email.com",
        "phone": "(555) 456-7890",
        "address": "3456 Maple Court, Austin, TX 78704",
        "status": "active",
        "account_balance": 0.0,
        "service_day": "Wednesday",
        "route_position": 1,
        "autopay": True,
        "pools": [
            {
                "id": "pool-5",
                "name": "Main Pool",
                "type": "In-Ground",
                "color": "#3B82F6",
                "gallons": 30000,
                "equipment": ["Pump", "Filter", "Heater", "Salt Cell", "Automation"],
                "last_service": "2025-01-13",
                "chem_readings": [
                    {"date": "2025-01-13", "fc": 3.8, "ph": 7.2, "ta": 105, "ch": 220, "cya": 40}
                ]
            }
        ]
    },
    {
        "id": "cust-5",
        "name": "David Chen",
        "email": "david.chen@email.com",
        "phone": "(555) 567-8901",
        "address": "7890 Cedar Lane, Austin, TX 78705",
        "status": "paused",
        "account_balance": 0.0,
        "service_day": "Thursday",
        "route_position": 1,
        "autopay": False,
        "pools": [
            {
                "id": "pool-6",
                "name": "Pool",
                "type": "In-Ground",
                "color": "#3B82F6",
                "gallons": 22000,
                "equipment": ["Pump", "Filter"],
                "last_service": "2024-12-28",
                "chem_readings": [
                    {"date": "2024-12-28", "fc": 2.9, "ph": 7.5, "ta": 115, "ch": 245, "cya": 55}
                ]
            }
        ]
    }
]


async def seed_database():
    """Seed the database with initial customer data"""
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("🌱 Starting database seed...")
    
    # Clear existing customers
    await db.customers.delete_many({})
    print("✅ Cleared existing customers")
    
    # Insert mock customers
    from datetime import datetime, timezone
    for customer in mock_customers:
        customer['created_at'] = datetime.now(timezone.utc).isoformat()
        customer['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    result = await db.customers.insert_many(mock_customers)
    print(f"✅ Inserted {len(result.inserted_ids)} customers")
    
    # Verify insertion
    count = await db.customers.count_documents({})
    print(f"✅ Total customers in database: {count}")
    
    client.close()
    print("🎉 Database seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_database())
