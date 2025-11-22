from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime, timezone
from models import Alert, AlertCreate, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["alerts"])

# Database will be injected by server.py
db = None

def init_db(database):
    global db
    db = database


@router.get("/", response_model=List[Alert])
async def get_alerts(
    resolved: Optional[bool] = None,
    severity: Optional[str] = None,
    type: Optional[str] = None,
    customer_id: Optional[str] = None
):
    """Get all alerts with optional filters"""
    query = {}
    
    if resolved is not None:
        query["resolved"] = resolved
    
    if severity:
        query["severity"] = severity
    
    if type:
        query["type"] = type
    
    if customer_id:
        query["customer_id"] = customer_id
    
    alerts = await db.alerts.find(query, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for alert in alerts:
        if isinstance(alert.get('created_at'), str):
            alert['created_at'] = datetime.fromisoformat(alert['created_at'])
        if isinstance(alert.get('updated_at'), str):
            alert['updated_at'] = datetime.fromisoformat(alert['updated_at'])
        if alert.get('resolved_at') and isinstance(alert['resolved_at'], str):
            alert['resolved_at'] = datetime.fromisoformat(alert['resolved_at'])
    
    return alerts


@router.get("/{alert_id}", response_model=Alert)
async def get_alert(alert_id: str):
    """Get a specific alert by ID"""
    alert = await db.alerts.find_one({"id": alert_id}, {"_id": 0})
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(alert.get('created_at'), str):
        alert['created_at'] = datetime.fromisoformat(alert['created_at'])
    if isinstance(alert.get('updated_at'), str):
        alert['updated_at'] = datetime.fromisoformat(alert['updated_at'])
    if alert.get('resolved_at') and isinstance(alert['resolved_at'], str):
        alert['resolved_at'] = datetime.fromisoformat(alert['resolved_at'])
    
    return alert


@router.post("/", response_model=Alert)
async def create_alert(alert: AlertCreate):
    """Create a new alert"""
    alert_obj = Alert(**alert.model_dump())
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = alert_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    if doc.get('resolved_at'):
        doc['resolved_at'] = doc['resolved_at'].isoformat()
    
    await db.alerts.insert_one(doc)
    return alert_obj


@router.put("/{alert_id}", response_model=Alert)
async def update_alert(alert_id: str, alert_update: AlertUpdate):
    """Update an alert"""
    # Get existing alert
    existing_alert = await db.alerts.find_one({"id": alert_id}, {"_id": 0})
    
    if not existing_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Update fields
    update_data = alert_update.model_dump(exclude_unset=True)
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    # If resolving the alert, set resolved_at timestamp
    if update_data.get('resolved') and not existing_alert.get('resolved'):
        update_data['resolved_at'] = datetime.now(timezone.utc).isoformat()
    
    # Serialize any datetime objects
    for key, value in update_data.items():
        if isinstance(value, datetime):
            update_data[key] = value.isoformat()
    
    await db.alerts.update_one({"id": alert_id}, {"$set": update_data})
    
    # Get and return updated alert
    updated_alert = await db.alerts.find_one({"id": alert_id}, {"_id": 0})
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(updated_alert.get('created_at'), str):
        updated_alert['created_at'] = datetime.fromisoformat(updated_alert['created_at'])
    if isinstance(updated_alert.get('updated_at'), str):
        updated_alert['updated_at'] = datetime.fromisoformat(updated_alert['updated_at'])
    if updated_alert.get('resolved_at') and isinstance(updated_alert['resolved_at'], str):
        updated_alert['resolved_at'] = datetime.fromisoformat(updated_alert['resolved_at'])
    
    return updated_alert


@router.delete("/{alert_id}")
async def delete_alert(alert_id: str):
    """Delete an alert"""
    result = await db.alerts.delete_one({"id": alert_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {"message": "Alert deleted successfully"}


@router.post("/{alert_id}/resolve", response_model=Alert)
async def resolve_alert(alert_id: str):
    """Mark an alert as resolved"""
    # Get existing alert
    existing_alert = await db.alerts.find_one({"id": alert_id}, {"_id": 0})
    
    if not existing_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    # Update alert to resolved
    now = datetime.now(timezone.utc)
    update_data = {
        "resolved": True,
        "resolved_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    
    await db.alerts.update_one({"id": alert_id}, {"$set": update_data})
    
    # Get and return updated alert
    updated_alert = await db.alerts.find_one({"id": alert_id}, {"_id": 0})
    
    # Convert ISO string timestamps back to datetime objects
    if isinstance(updated_alert.get('created_at'), str):
        updated_alert['created_at'] = datetime.fromisoformat(updated_alert['created_at'])
    if isinstance(updated_alert.get('updated_at'), str):
        updated_alert['updated_at'] = datetime.fromisoformat(updated_alert['updated_at'])
    if updated_alert.get('resolved_at') and isinstance(updated_alert['resolved_at'], str):
        updated_alert['resolved_at'] = datetime.fromisoformat(updated_alert['resolved_at'])
    
    return updated_alert


@router.get("/stats/summary")
async def get_alert_stats():
    """Get alert statistics"""
    total_alerts = await db.alerts.count_documents({})
    unresolved_alerts = await db.alerts.count_documents({"resolved": False})
    resolved_alerts = await db.alerts.count_documents({"resolved": True})
    
    # Get counts by severity
    high_severity = await db.alerts.count_documents({"severity": "high", "resolved": False})
    medium_severity = await db.alerts.count_documents({"severity": "medium", "resolved": False})
    low_severity = await db.alerts.count_documents({"severity": "low", "resolved": False})
    
    # Get counts by type
    chemical_alerts = await db.alerts.count_documents({"type": "chemical", "resolved": False})
    flow_alerts = await db.alerts.count_documents({"type": "flow", "resolved": False})
    leak_alerts = await db.alerts.count_documents({"type": "leak", "resolved": False})
    time_alerts = await db.alerts.count_documents({"type": "time", "resolved": False})
    cost_alerts = await db.alerts.count_documents({"type": "cost", "resolved": False})
    
    return {
        "total": total_alerts,
        "unresolved": unresolved_alerts,
        "resolved": resolved_alerts,
        "by_severity": {
            "high": high_severity,
            "medium": medium_severity,
            "low": low_severity
        },
        "by_type": {
            "chemical": chemical_alerts,
            "flow": flow_alerts,
            "leak": leak_alerts,
            "time": time_alerts,
            "cost": cost_alerts
        }
    }
