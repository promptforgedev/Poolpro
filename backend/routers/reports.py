from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/reports", tags=["reports"])

# MongoDB will be accessed from server.py
db = None

def init_db(database):
    """Initialize database connection"""
    global db
    db = database

@router.get("/revenue")
async def get_revenue_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = "month"  # day, week, month, year
):
    """Get revenue breakdown by time period"""
    db = await init_db()
    
    # Build date filter
    date_filter = {}
    if start_date:
        date_filter["$gte"] = start_date
    if end_date:
        date_filter["$lte"] = end_date
    
    query = {}
    if date_filter:
        query["invoice_date"] = date_filter
    
    # Get all invoices
    invoices = await db.invoices.find(query).to_list(1000)
    
    # Calculate revenue by status
    total_revenue = 0
    paid_revenue = 0
    outstanding_revenue = 0
    
    for inv in invoices:
        total = inv.get("total", 0)
        status = inv.get("status", "")
        
        total_revenue += total
        if status == "paid":
            paid_revenue += total
        else:
            outstanding_revenue += total
    
    # Get monthly breakdown
    monthly_breakdown = {}
    for inv in invoices:
        invoice_date = inv.get("invoice_date", "")
        if invoice_date:
            month_key = invoice_date[:7]  # YYYY-MM
            if month_key not in monthly_breakdown:
                monthly_breakdown[month_key] = {
                    "period": month_key,
                    "total": 0,
                    "paid": 0,
                    "outstanding": 0,
                    "count": 0
                }
            total = inv.get("total", 0)
            monthly_breakdown[month_key]["total"] += total
            monthly_breakdown[month_key]["count"] += 1
            if inv.get("status") == "paid":
                monthly_breakdown[month_key]["paid"] += total
            else:
                monthly_breakdown[month_key]["outstanding"] += total
    
    return {
        "summary": {
            "total_revenue": round(total_revenue, 2),
            "paid_revenue": round(paid_revenue, 2),
            "outstanding_revenue": round(outstanding_revenue, 2),
            "total_invoices": len(invoices)
        },
        "breakdown": list(monthly_breakdown.values())
    }

@router.get("/jobs-performance")
async def get_jobs_performance():
    """Get job completion statistics"""
    db = await init_db()
    
    # Get all jobs
    jobs = await db.jobs.find({}).to_list(1000)
    
    # Calculate stats
    total_jobs = len(jobs)
    completed_jobs = len([j for j in jobs if j.get("status") == "completed"])
    in_progress_jobs = len([j for j in jobs if j.get("status") == "in-progress"])
    scheduled_jobs = len([j for j in jobs if j.get("status") == "scheduled"])
    
    # Calculate completion rate
    completion_rate = (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0
    
    # Jobs by service type
    service_types = {}
    for job in jobs:
        service_type = job.get("service_type", "Other")
        if service_type not in service_types:
            service_types[service_type] = {
                "type": service_type,
                "total": 0,
                "completed": 0,
                "in_progress": 0,
                "scheduled": 0
            }
        service_types[service_type]["total"] += 1
        status = job.get("status", "")
        if status == "completed":
            service_types[service_type]["completed"] += 1
        elif status == "in-progress":
            service_types[service_type]["in_progress"] += 1
        elif status == "scheduled":
            service_types[service_type]["scheduled"] += 1
    
    return {
        "summary": {
            "total_jobs": total_jobs,
            "completed_jobs": completed_jobs,
            "in_progress_jobs": in_progress_jobs,
            "scheduled_jobs": scheduled_jobs,
            "completion_rate": round(completion_rate, 2)
        },
        "by_service_type": list(service_types.values())
    }

@router.get("/customer-stats")
async def get_customer_statistics():
    """Get customer statistics"""
    db = await init_db()
    
    # Get all customers
    customers = await db.customers.find({}).to_list(1000)
    
    total_customers = len(customers)
    active_customers = len([c for c in customers if c.get("status") == "active"])
    paused_customers = len([c for c in customers if c.get("status") == "paused"])
    inactive_customers = len([c for c in customers if c.get("status") == "inactive"])
    
    # Calculate total pools
    total_pools = sum(len(c.get("pools", [])) for c in customers)
    avg_pools_per_customer = (total_pools / total_customers) if total_customers > 0 else 0
    
    # Customers with autopay
    autopay_customers = len([c for c in customers if c.get("autopay", False)])
    
    return {
        "total_customers": total_customers,
        "active_customers": active_customers,
        "paused_customers": paused_customers,
        "inactive_customers": inactive_customers,
        "total_pools": total_pools,
        "avg_pools_per_customer": round(avg_pools_per_customer, 2),
        "autopay_customers": autopay_customers,
        "autopay_percentage": round((autopay_customers / total_customers * 100) if total_customers > 0 else 0, 2)
    }

@router.get("/technician-performance")
async def get_technician_performance():
    """Get technician performance metrics"""
    db = await init_db()
    
    # Get all technicians and jobs
    technicians = await db.technicians.find({}).to_list(100)
    jobs = await db.jobs.find({}).to_list(1000)
    
    # Calculate performance per technician
    tech_performance = {}
    
    for tech in technicians:
        tech_id = tech.get("id")
        tech_name = tech.get("name")
        
        # Get jobs for this technician
        tech_jobs = [j for j in jobs if j.get("technician_id") == tech_id]
        
        total_jobs = len(tech_jobs)
        completed_jobs = len([j for j in tech_jobs if j.get("status") == "completed"])
        in_progress_jobs = len([j for j in tech_jobs if j.get("status") == "in-progress"])
        scheduled_jobs = len([j for j in tech_jobs if j.get("status") == "scheduled"])
        
        completion_rate = (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0
        
        tech_performance[tech_id] = {
            "technician_id": tech_id,
            "technician_name": tech_name,
            "total_jobs": total_jobs,
            "completed_jobs": completed_jobs,
            "in_progress_jobs": in_progress_jobs,
            "scheduled_jobs": scheduled_jobs,
            "completion_rate": round(completion_rate, 2)
        }
    
    return {
        "technicians": list(tech_performance.values())
    }

@router.get("/financial-summary")
async def get_financial_summary():
    """Get overall financial summary"""
    db = await init_db()
    
    # Get all invoices
    invoices = await db.invoices.find({}).to_list(1000)
    
    total_invoiced = 0
    total_paid = 0
    total_outstanding = 0
    overdue_amount = 0
    
    paid_count = 0
    sent_count = 0
    draft_count = 0
    overdue_count = 0
    
    for inv in invoices:
        total = inv.get("total", 0)
        paid_amount = inv.get("paid_amount", 0)
        balance_due = inv.get("balance_due", 0)
        status = inv.get("status", "")
        
        total_invoiced += total
        total_paid += paid_amount
        total_outstanding += balance_due
        
        if status == "paid":
            paid_count += 1
        elif status == "sent":
            sent_count += 1
        elif status == "draft":
            draft_count += 1
        elif status == "overdue":
            overdue_count += 1
            overdue_amount += balance_due
    
    # Get quotes stats
    quotes = await db.quotes.find({}).to_list(1000)
    pending_quotes = len([q for q in quotes if q.get("status") == "pending"])
    approved_quotes = len([q for q in quotes if q.get("status") == "approved"])
    declined_quotes = len([q for q in quotes if q.get("status") == "declined"])
    
    # Calculate conversion rate
    total_quotes = len(quotes)
    quote_conversion_rate = (approved_quotes / total_quotes * 100) if total_quotes > 0 else 0
    
    return {
        "invoices": {
            "total_invoiced": round(total_invoiced, 2),
            "total_paid": round(total_paid, 2),
            "total_outstanding": round(total_outstanding, 2),
            "overdue_amount": round(overdue_amount, 2),
            "paid_count": paid_count,
            "sent_count": sent_count,
            "draft_count": draft_count,
            "overdue_count": overdue_count
        },
        "quotes": {
            "total_quotes": total_quotes,
            "pending_quotes": pending_quotes,
            "approved_quotes": approved_quotes,
            "declined_quotes": declined_quotes,
            "conversion_rate": round(quote_conversion_rate, 2)
        }
    }

@router.get("/dashboard-stats")
async def get_dashboard_statistics():
    """Get key statistics for dashboard"""
    db = await init_db()
    
    # Get counts
    customers = await db.customers.count_documents({})
    active_customers = await db.customers.count_documents({"status": "active"})
    jobs = await db.jobs.count_documents({})
    completed_jobs = await db.jobs.count_documents({"status": "completed"})
    alerts = await db.alerts.count_documents({"resolved": False})
    
    # Get revenue
    invoices = await db.invoices.find({}).to_list(1000)
    total_revenue = sum(inv.get("total", 0) for inv in invoices)
    paid_revenue = sum(inv.get("paid_amount", 0) for inv in invoices)
    outstanding_revenue = sum(inv.get("balance_due", 0) for inv in invoices)
    
    return {
        "customers": {
            "total": customers,
            "active": active_customers
        },
        "jobs": {
            "total": jobs,
            "completed": completed_jobs
        },
        "alerts": {
            "unresolved": alerts
        },
        "revenue": {
            "total": round(total_revenue, 2),
            "paid": round(paid_revenue, 2),
            "outstanding": round(outstanding_revenue, 2)
        }
    }
