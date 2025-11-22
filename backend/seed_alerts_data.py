from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timezone, timedelta

load_dotenv()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


async def seed_alerts():
    """Seed the database with sample alert data"""
    
    # Clear existing alerts
    await db.alerts.delete_many({})
    
    # Get some customers and jobs for realistic data
    customers = await db.customers.find({}, {"_id": 0}).to_list(5)
    jobs = await db.jobs.find({}, {"_id": 0}).to_list(6)
    
    if not customers:
        print("⚠️  No customers found. Please run seed_data.py first.")
        return
    
    alerts = []
    
    # Chemical Alerts
    if len(customers) > 0 and customers[0].get('pools'):
        customer = customers[0]
        pool = customer['pools'][0]
        alerts.append({
            "id": "alert-001",
            "type": "chemical",
            "severity": "high",
            "title": "Low Chlorine Level",
            "message": f"Free Chlorine (FC) is critically low at 0.5 ppm. Recommended: 1-3 ppm. Immediate attention required.",
            "customer_id": customer['id'],
            "customer_name": customer['name'],
            "pool_id": pool['id'],
            "pool_name": pool['name'],
            "job_id": None,
            "resolved": False,
            "resolved_at": None,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
        })
    
    if len(customers) > 1 and customers[1].get('pools'):
        customer = customers[1]
        pool = customer['pools'][0]
        alerts.append({
            "id": "alert-002",
            "type": "chemical",
            "severity": "medium",
            "title": "High pH Level",
            "message": f"pH level is elevated at 8.2. Recommended: 7.2-7.6. Adjustment needed.",
            "customer_id": customer['id'],
            "customer_name": customer['name'],
            "pool_id": pool['id'],
            "pool_name": pool['name'],
            "job_id": None,
            "resolved": False,
            "resolved_at": None,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
        })
    
    if len(customers) > 2 and customers[2].get('pools'):
        customer = customers[2]
        pool = customer['pools'][0]
        alerts.append({
            "id": "alert-003",
            "type": "chemical",
            "severity": "low",
            "title": "Low Total Alkalinity",
            "message": f"Total Alkalinity is slightly low at 70 ppm. Recommended: 80-120 ppm.",
            "customer_id": customer['id'],
            "customer_name": customer['name'],
            "pool_id": pool['id'],
            "pool_name": pool['name'],
            "job_id": None,
            "resolved": False,
            "resolved_at": None,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=8)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=8)).isoformat()
        })
    
    # Flow Alert
    if len(customers) > 3 and customers[3].get('pools'):
        customer = customers[3]
        pool = customer['pools'][0]
        alerts.append({
            "id": "alert-004",
            "type": "flow",
            "severity": "high",
            "title": "Reduced Flow Detected",
            "message": f"Pump flow rate has decreased by 40%. Possible filter clog or pump issue.",
            "customer_id": customer['id'],
            "customer_name": customer['name'],
            "pool_id": pool['id'],
            "pool_name": pool['name'],
            "job_id": None,
            "resolved": False,
            "resolved_at": None,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()
        })
    
    # Leak Alert
    if len(customers) > 4 and customers[4].get('pools'):
        customer = customers[4]
        pool = customer['pools'][0]
        alerts.append({
            "id": "alert-005",
            "type": "leak",
            "severity": "high",
            "title": "Potential Water Leak",
            "message": f"Water level has dropped 2 inches in 24 hours. Possible leak detected.",
            "customer_id": customer['id'],
            "customer_name": customer['name'],
            "pool_id": pool['id'],
            "pool_name": pool['name'],
            "job_id": None,
            "resolved": False,
            "resolved_at": None,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=18)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=18)).isoformat()
        })
    
    # Time Alert
    if len(jobs) > 0 and len(customers) > 0:
        job = jobs[0]
        customer = customers[0]
        alerts.append({
            "id": "alert-006",
            "type": "time",
            "severity": "medium",
            "title": "Service Time Exceeded",
            "message": f"Job has exceeded estimated time by 45 minutes. Review needed.",
            "customer_id": customer['id'],
            "customer_name": customer['name'],
            "pool_id": None,
            "pool_name": None,
            "job_id": job['id'],
            "resolved": False,
            "resolved_at": None,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat()
        })
    
    # Cost Alert
    if len(jobs) > 1 and len(customers) > 1:
        job = jobs[1]
        customer = customers[1]
        alerts.append({
            "id": "alert-007",
            "type": "cost",
            "severity": "medium",
            "title": "Budget Threshold Exceeded",
            "message": f"Job cost has exceeded budgeted amount by $150. Approval may be required.",
            "customer_id": customer['id'],
            "customer_name": customer['name'],
            "pool_id": None,
            "pool_name": None,
            "job_id": job['id'],
            "resolved": False,
            "resolved_at": None,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(hours=6)).isoformat()
        })
    
    # Add some resolved alerts for historical data
    if len(customers) > 0 and customers[0].get('pools'):
        customer = customers[0]
        pool = customer['pools'][0]
        alerts.append({
            "id": "alert-008",
            "type": "chemical",
            "severity": "high",
            "title": "High Cyanuric Acid",
            "message": f"CYA level was elevated at 95 ppm. Recommended: 30-50 ppm. Water dilution performed.",
            "customer_id": customer['id'],
            "customer_name": customer['name'],
            "pool_id": pool['id'],
            "pool_name": pool['name'],
            "job_id": None,
            "resolved": True,
            "resolved_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "created_at": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        })
    
    if len(customers) > 1 and customers[1].get('pools'):
        customer = customers[1]
        pool = customer['pools'][0]
        alerts.append({
            "id": "alert-009",
            "type": "flow",
            "severity": "medium",
            "title": "Filter Cleaning Required",
            "message": f"Filter pressure increased. Cleaning completed and flow restored.",
            "customer_id": customer['id'],
            "customer_name": customer['name'],
            "pool_id": pool['id'],
            "pool_name": pool['name'],
            "job_id": None,
            "resolved": True,
            "resolved_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(),
            "created_at": (datetime.now(timezone.utc) - timedelta(days=4)).isoformat(),
            "updated_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
        })
    
    # Insert all alerts
    if alerts:
        await db.alerts.insert_many(alerts)
        print(f"✅ Successfully seeded {len(alerts)} alerts!")
    else:
        print("⚠️  No alerts created. Please ensure customer and job data exists.")


async def main():
    await seed_alerts()
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
