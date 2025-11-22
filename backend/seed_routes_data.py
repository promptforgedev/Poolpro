"""
Seed script for technicians and routes data
Run this script to populate the database with initial technicians and route data
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'poolpro')

# Sample technicians data
TECHNICIANS = [
    {
        "id": "tech-001",
        "name": "Mike Johnson",
        "email": "mike.johnson@poolpro.com",
        "phone": "(555) 123-4567",
        "color": "#3B82F6",
        "status": "active",
        "assigned_days": ["Monday", "Wednesday", "Friday"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": "tech-002",
        "name": "Sarah Martinez",
        "email": "sarah.martinez@poolpro.com",
        "phone": "(555) 234-5678",
        "color": "#10B981",
        "status": "active",
        "assigned_days": ["Tuesday", "Thursday"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": "tech-003",
        "name": "David Chen",
        "email": "david.chen@poolpro.com",
        "phone": "(555) 345-6789",
        "color": "#F59E0B",
        "status": "active",
        "assigned_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    },
    {
        "id": "tech-004",
        "name": "Emily Rodriguez",
        "email": "emily.rodriguez@poolpro.com",
        "phone": "(555) 456-7890",
        "color": "#8B5CF6",
        "status": "active",
        "assigned_days": ["Wednesday", "Friday"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
]


async def seed_routes_data():
    """Seed the database with technicians and routes data"""
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        # Clear existing data
        await db.technicians.delete_many({})
        await db.routes.delete_many({})
        print("✓ Cleared existing technicians and routes data")
        
        # Insert technicians
        await db.technicians.insert_many(TECHNICIANS)
        print(f"✓ Inserted {len(TECHNICIANS)} technicians")
        
        # Fetch existing jobs to assign to routes
        jobs = await db.jobs.find({}, {"_id": 0}).to_list(1000)
        print(f"✓ Found {len(jobs)} existing jobs")
        
        # Create routes by day and assign jobs
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        routes = []
        
        for day in days:
            # Filter jobs for this day
            day_jobs = [job for job in jobs if job.get("scheduled_date", "").startswith("2025-")]
            
            # Assign jobs to technicians working this day
            techs_for_day = [t for t in TECHNICIANS if day in t["assigned_days"]]
            
            for idx, tech in enumerate(techs_for_day):
                # Get subset of jobs for this technician
                tech_jobs = day_jobs[idx::len(techs_for_day)][:3]  # Max 3 jobs per route
                job_ids = [job["id"] for job in tech_jobs]
                
                route = {
                    "id": f"route-{day.lower()[:3]}-{tech['id'].split('-')[1]}",
                    "name": f"{day} Route - {tech['name']}",
                    "technician_id": tech["id"],
                    "technician_name": tech["name"],
                    "day": day,
                    "jobs": job_ids,
                    "total_stops": len(job_ids),
                    "estimated_duration": len(job_ids) * 45,  # 45 min per stop
                    "status": "active",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }
                routes.append(route)
        
        # Insert routes
        if routes:
            await db.routes.insert_many(routes)
            print(f"✓ Inserted {len(routes)} routes")
        
        print("\n✅ Routes seeding completed successfully!")
        print(f"   - {len(TECHNICIANS)} technicians created")
        print(f"   - {len(routes)} routes created")
        
    except Exception as e:
        print(f"❌ Error seeding routes data: {e}")
        raise
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_routes_data())
