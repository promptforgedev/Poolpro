from fastapi import APIRouter, HTTPException, Depends
from typing import List

from routers.auth import get_current_customer

router = APIRouter(prefix="/portal", tags=["portal"])

# MongoDB will be accessed from server.py
db = None

def init_db(database):
    """Initialize database connection"""
    global db
    db = database


@router.get("/pools")
async def get_customer_pools(current_customer: dict = Depends(get_current_customer)):
    """Get all pools for authenticated customer"""
    pools = current_customer.get("pools", [])
    
    # Return pools with formatted data
    return {
        "customer_id": current_customer.get("id"),
        "customer_name": current_customer.get("name"),
        "pools": pools
    }


@router.get("/invoices")
async def get_customer_invoices(current_customer: dict = Depends(get_current_customer)):
    """Get all invoices for authenticated customer"""
    
    customer_id = current_customer.get("id")
    invoices = await db.invoices.find({"customer_id": customer_id}).to_list(100)
    
    # Calculate totals
    total_invoiced = sum(inv.get("total", 0) for inv in invoices)
    total_paid = sum(inv.get("paid_amount", 0) for inv in invoices)
    total_outstanding = sum(inv.get("balance_due", 0) for inv in invoices)
    
    return {
        "customer_id": customer_id,
        "customer_name": current_customer.get("name"),
        "invoices": invoices,
        "summary": {
            "total_invoiced": round(total_invoiced, 2),
            "total_paid": round(total_paid, 2),
            "total_outstanding": round(total_outstanding, 2),
            "invoice_count": len(invoices)
        }
    }


@router.get("/invoices/{invoice_id}")
async def get_invoice_detail(
    invoice_id: str,
    current_customer: dict = Depends(get_current_customer)
):
    """Get specific invoice detail"""
    db = await init_db()
    
    customer_id = current_customer.get("id")
    invoice = await db.invoices.find_one({
        "id": invoice_id,
        "customer_id": customer_id
    })
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return invoice


@router.get("/jobs")
async def get_customer_jobs(current_customer: dict = Depends(get_current_customer)):
    """Get all jobs for authenticated customer"""
    db = await init_db()
    
    customer_id = current_customer.get("id")
    jobs = await db.jobs.find({"customer_id": customer_id}).to_list(100)
    
    # Separate by status
    scheduled = [j for j in jobs if j.get("status") == "scheduled"]
    in_progress = [j for j in jobs if j.get("status") == "in-progress"]
    completed = [j for j in jobs if j.get("status") == "completed"]
    
    return {
        "customer_id": customer_id,
        "customer_name": current_customer.get("name"),
        "jobs": jobs,
        "summary": {
            "total_jobs": len(jobs),
            "scheduled": len(scheduled),
            "in_progress": len(in_progress),
            "completed": len(completed)
        }
    }


@router.get("/quotes")
async def get_customer_quotes(current_customer: dict = Depends(get_current_customer)):
    """Get all quotes for authenticated customer"""
    db = await init_db()
    
    customer_id = current_customer.get("id")
    quotes = await db.quotes.find({"customer_id": customer_id}).to_list(100)
    
    # Separate by status
    pending = [q for q in quotes if q.get("status") == "pending"]
    approved = [q for q in quotes if q.get("status") == "approved"]
    declined = [q for q in quotes if q.get("status") == "declined"]
    
    return {
        "customer_id": customer_id,
        "customer_name": current_customer.get("name"),
        "quotes": quotes,
        "summary": {
            "total_quotes": len(quotes),
            "pending": len(pending),
            "approved": len(approved),
            "declined": len(declined)
        }
    }


@router.get("/service-history")
async def get_service_history(current_customer: dict = Depends(get_current_customer)):
    """Get service history from pool chemical readings"""
    pools = current_customer.get("pools", [])
    
    # Collect all chemical readings from all pools
    all_readings = []
    for pool in pools:
        pool_readings = pool.get("chem_readings", [])
        for reading in pool_readings:
            all_readings.append({
                "pool_id": pool.get("id"),
                "pool_name": pool.get("name"),
                "date": reading.get("date"),
                "fc": reading.get("fc"),
                "ph": reading.get("ph"),
                "ta": reading.get("ta"),
                "ch": reading.get("ch"),
                "cya": reading.get("cya")
            })
    
    # Sort by date descending
    all_readings.sort(key=lambda x: x.get("date", ""), reverse=True)
    
    return {
        "customer_id": current_customer.get("id"),
        "customer_name": current_customer.get("name"),
        "service_history": all_readings
    }


@router.get("/alerts")
async def get_customer_alerts(current_customer: dict = Depends(get_current_customer)):
    """Get alerts related to customer's pools"""
    db = await init_db()
    
    customer_id = current_customer.get("id")
    alerts = await db.alerts.find({"customer_id": customer_id}).to_list(100)
    
    # Separate by resolved status
    unresolved = [a for a in alerts if not a.get("resolved", False)]
    resolved = [a for a in alerts if a.get("resolved", False)]
    
    return {
        "customer_id": customer_id,
        "customer_name": current_customer.get("name"),
        "alerts": alerts,
        "summary": {
            "total_alerts": len(alerts),
            "unresolved": len(unresolved),
            "resolved": len(resolved)
        }
    }
