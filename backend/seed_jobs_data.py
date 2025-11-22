import os
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = MongoClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Get existing customers for reference
customers = list(db.customers.find({}, {"_id": 0}))

if not customers:
    print("No customers found. Please seed customers first.")
    exit(1)

# Create quotes
quotes_data = [
    {
        "id": "quote-001",
        "customer_id": customers[0]["id"],
        "customer_name": customers[0]["name"],
        "status": "pending",
        "items": [
            {"description": "Pool Equipment Upgrade - Variable Speed Pump", "quantity": 1, "unit_price": 1200.00, "total": 1200.00},
            {"description": "Installation Labor", "quantity": 4, "unit_price": 75.00, "total": 300.00}
        ],
        "subtotal": 1500.00,
        "tax": 120.00,
        "total": 1620.00,
        "notes": "Includes removal of old pump and disposal",
        "valid_until": (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d"),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "id": "quote-002",
        "customer_id": customers[1]["id"],
        "customer_name": customers[1]["name"],
        "status": "approved",
        "items": [
            {"description": "Pool Resurfacing - Pebble Tec", "quantity": 1, "unit_price": 5500.00, "total": 5500.00},
            {"description": "Acid Wash & Prep", "quantity": 1, "unit_price": 300.00, "total": 300.00}
        ],
        "subtotal": 5800.00,
        "tax": 464.00,
        "total": 6264.00,
        "notes": "3-5 day project, weather dependent",
        "valid_until": (datetime.now(timezone.utc) + timedelta(days=15)).strftime("%Y-%m-%d"),
        "created_at": (datetime.now(timezone.utc) - timedelta(days=5)),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "id": "quote-003",
        "customer_id": customers[2]["id"],
        "customer_name": customers[2]["name"],
        "status": "declined",
        "items": [
            {"description": "Pool Heater Replacement - Gas", "quantity": 1, "unit_price": 3200.00, "total": 3200.00},
            {"description": "Installation & Gas Line", "quantity": 1, "unit_price": 800.00, "total": 800.00}
        ],
        "subtotal": 4000.00,
        "tax": 320.00,
        "total": 4320.00,
        "notes": "Customer opted for electric heater instead",
        "valid_until": (datetime.now(timezone.utc) - timedelta(days=5)).strftime("%Y-%m-%d"),
        "created_at": (datetime.now(timezone.utc) - timedelta(days=20)),
        "updated_at": (datetime.now(timezone.utc) - timedelta(days=3))
    },
    {
        "id": "quote-004",
        "customer_id": customers[3]["id"],
        "customer_name": customers[3]["name"],
        "status": "pending",
        "items": [
            {"description": "Saltwater System Installation", "quantity": 1, "unit_price": 1800.00, "total": 1800.00},
            {"description": "Salt & Initial Chemicals", "quantity": 1, "unit_price": 150.00, "total": 150.00}
        ],
        "subtotal": 1950.00,
        "tax": 156.00,
        "total": 2106.00,
        "notes": "Includes 1-year warranty on equipment",
        "valid_until": (datetime.now(timezone.utc) + timedelta(days=45)).strftime("%Y-%m-%d"),
        "created_at": (datetime.now(timezone.utc) - timedelta(days=2)),
        "updated_at": (datetime.now(timezone.utc) - timedelta(days=2))
    }
]

# Create jobs
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
next_week = (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%d")
yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")

jobs_data = [
    {
        "id": "job-001",
        "customer_id": customers[0]["id"],
        "customer_name": customers[0]["name"],
        "customer_address": customers[0]["address"],
        "quote_id": None,
        "status": "scheduled",
        "service_type": "Routine Service",
        "scheduled_date": today,
        "scheduled_time": "09:00 AM",
        "technician": "Mike Johnson",
        "pools": [customers[0]["pools"][0]["id"]] if customers[0]["pools"] else [],
        "notes": "Check pump pressure and clean skimmer",
        "completion_notes": None,
        "completed_at": None,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "id": "job-002",
        "customer_id": customers[1]["id"],
        "customer_name": customers[1]["name"],
        "customer_address": customers[1]["address"],
        "quote_id": "quote-002",
        "status": "in-progress",
        "service_type": "Pool Resurfacing",
        "scheduled_date": today,
        "scheduled_time": "08:00 AM",
        "technician": "Sarah Martinez",
        "pools": [customers[1]["pools"][0]["id"]] if customers[1]["pools"] else [],
        "notes": "Day 2 of resurfacing project",
        "completion_notes": None,
        "completed_at": None,
        "created_at": (datetime.now(timezone.utc) - timedelta(days=1)),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "id": "job-003",
        "customer_id": customers[2]["id"],
        "customer_name": customers[2]["name"],
        "customer_address": customers[2]["address"],
        "quote_id": None,
        "status": "completed",
        "service_type": "Routine Service",
        "scheduled_date": yesterday,
        "scheduled_time": "02:00 PM",
        "technician": "Mike Johnson",
        "pools": [customers[2]["pools"][0]["id"]] if customers[2]["pools"] else [],
        "notes": "Weekly maintenance",
        "completion_notes": "All levels good. Added 2 lbs chlorine. Filter cleaned.",
        "completed_at": datetime.now(timezone.utc) - timedelta(hours=20),
        "created_at": (datetime.now(timezone.utc) - timedelta(days=2)),
        "updated_at": (datetime.now(timezone.utc) - timedelta(hours=20))
    },
    {
        "id": "job-004",
        "customer_id": customers[3]["id"],
        "customer_name": customers[3]["name"],
        "customer_address": customers[3]["address"],
        "quote_id": None,
        "status": "scheduled",
        "service_type": "Repair",
        "scheduled_date": tomorrow,
        "scheduled_time": "10:30 AM",
        "technician": "David Chen",
        "pools": [customers[3]["pools"][0]["id"]] if customers[3]["pools"] else [],
        "notes": "Customer reports pool cleaner not working",
        "completion_notes": None,
        "completed_at": None,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "id": "job-005",
        "customer_id": customers[4]["id"],
        "customer_name": customers[4]["name"],
        "customer_address": customers[4]["address"],
        "quote_id": None,
        "status": "scheduled",
        "service_type": "Routine Service",
        "scheduled_date": next_week,
        "scheduled_time": "11:00 AM",
        "technician": "Sarah Martinez",
        "pools": [customers[4]["pools"][0]["id"]] if customers[4]["pools"] else [],
        "notes": "Regular weekly service",
        "completion_notes": None,
        "completed_at": None,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "id": "job-006",
        "customer_id": customers[0]["id"],
        "customer_name": customers[0]["name"],
        "customer_address": customers[0]["address"],
        "quote_id": None,
        "status": "completed",
        "service_type": "Routine Service",
        "scheduled_date": (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d"),
        "scheduled_time": "09:00 AM",
        "technician": "Mike Johnson",
        "pools": [customers[0]["pools"][0]["id"]] if customers[0]["pools"] else [],
        "notes": "Weekly maintenance",
        "completion_notes": "Pool balanced. All equipment functioning properly.",
        "completed_at": datetime.now(timezone.utc) - timedelta(days=7),
        "created_at": (datetime.now(timezone.utc) - timedelta(days=8)),
        "updated_at": (datetime.now(timezone.utc) - timedelta(days=7))
    }
]

# Create invoices
invoices_data = [
    {
        "id": "inv-001",
        "customer_id": customers[0]["id"],
        "customer_name": customers[0]["name"],
        "job_id": "job-006",
        "quote_id": None,
        "invoice_number": "INV-2025-001",
        "status": "paid",
        "line_items": [
            {"description": "Weekly Pool Maintenance", "quantity": 1, "unit_price": 125.00, "total": 125.00},
            {"description": "Pool Chemicals", "quantity": 1, "unit_price": 35.00, "total": 35.00}
        ],
        "subtotal": 160.00,
        "tax": 12.80,
        "total": 172.80,
        "paid_amount": 172.80,
        "balance_due": 0.00,
        "issue_date": (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d"),
        "due_date": (datetime.now(timezone.utc) + timedelta(days=23)).strftime("%Y-%m-%d"),
        "paid_date": (datetime.now(timezone.utc) - timedelta(days=5)).strftime("%Y-%m-%d"),
        "notes": "Thank you for your business!",
        "created_at": (datetime.now(timezone.utc) - timedelta(days=7)),
        "updated_at": (datetime.now(timezone.utc) - timedelta(days=5))
    },
    {
        "id": "inv-002",
        "customer_id": customers[1]["id"],
        "customer_name": customers[1]["name"],
        "job_id": None,
        "quote_id": "quote-002",
        "invoice_number": "INV-2025-002",
        "status": "sent",
        "line_items": [
            {"description": "Pool Resurfacing - Pebble Tec", "quantity": 1, "unit_price": 5500.00, "total": 5500.00},
            {"description": "Acid Wash & Prep", "quantity": 1, "unit_price": 300.00, "total": 300.00}
        ],
        "subtotal": 5800.00,
        "tax": 464.00,
        "total": 6264.00,
        "paid_amount": 0.00,
        "balance_due": 6264.00,
        "issue_date": today,
        "due_date": (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d"),
        "paid_date": None,
        "notes": "50% deposit required to begin work",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "id": "inv-003",
        "customer_id": customers[2]["id"],
        "customer_name": customers[2]["name"],
        "job_id": "job-003",
        "quote_id": None,
        "invoice_number": "INV-2025-003",
        "status": "sent",
        "line_items": [
            {"description": "Weekly Pool Maintenance", "quantity": 1, "unit_price": 125.00, "total": 125.00},
            {"description": "Additional Chlorine", "quantity": 1, "unit_price": 20.00, "total": 20.00}
        ],
        "subtotal": 145.00,
        "tax": 11.60,
        "total": 156.60,
        "paid_amount": 0.00,
        "balance_due": 156.60,
        "issue_date": yesterday,
        "due_date": (datetime.now(timezone.utc) + timedelta(days=29)).strftime("%Y-%m-%d"),
        "paid_date": None,
        "notes": None,
        "created_at": (datetime.now(timezone.utc) - timedelta(days=1)),
        "updated_at": (datetime.now(timezone.utc) - timedelta(days=1))
    },
    {
        "id": "inv-004",
        "customer_id": customers[3]["id"],
        "customer_name": customers[3]["name"],
        "job_id": None,
        "quote_id": None,
        "invoice_number": "INV-2025-004",
        "status": "overdue",
        "line_items": [
            {"description": "Monthly Pool Service - January", "quantity": 4, "unit_price": 125.00, "total": 500.00}
        ],
        "subtotal": 500.00,
        "tax": 40.00,
        "total": 540.00,
        "paid_amount": 0.00,
        "balance_due": 540.00,
        "issue_date": (datetime.now(timezone.utc) - timedelta(days=45)).strftime("%Y-%m-%d"),
        "due_date": (datetime.now(timezone.utc) - timedelta(days=15)).strftime("%Y-%m-%d"),
        "paid_date": None,
        "notes": "Payment overdue",
        "created_at": (datetime.now(timezone.utc) - timedelta(days=45)),
        "updated_at": datetime.now(timezone.utc)
    },
    {
        "id": "inv-005",
        "customer_id": customers[4]["id"],
        "customer_name": customers[4]["name"],
        "job_id": None,
        "quote_id": None,
        "invoice_number": "INV-2025-005",
        "status": "draft",
        "line_items": [
            {"description": "Pool Opening Service", "quantity": 1, "unit_price": 250.00, "total": 250.00},
            {"description": "Chemical Balance & Testing", "quantity": 1, "unit_price": 75.00, "total": 75.00}
        ],
        "subtotal": 325.00,
        "tax": 26.00,
        "total": 351.00,
        "paid_amount": 0.00,
        "balance_due": 351.00,
        "issue_date": today,
        "due_date": (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d"),
        "paid_date": None,
        "notes": "Draft - review before sending",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
]

# Clear existing data
db.quotes.delete_many({})
db.jobs.delete_many({})
db.invoices.delete_many({})

# Insert data
db.quotes.insert_many(quotes_data)
db.jobs.insert_many(jobs_data)
db.invoices.insert_many(invoices_data)

print(f"✅ Seeded {len(quotes_data)} quotes")
print(f"✅ Seeded {len(jobs_data)} jobs")
print(f"✅ Seeded {len(invoices_data)} invoices")

client.close()
