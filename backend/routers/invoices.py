from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime, timezone

from models import Invoice, InvoiceCreate, InvoiceUpdate

router = APIRouter(prefix="/invoices", tags=["invoices"])

# MongoDB will be accessed from server.py
db = None

def init_db(database):
    global db
    db = database


@router.get("/", response_model=List[Invoice])
async def get_all_invoices(status: Optional[str] = None):
    """Get all invoices, optionally filtered by status"""
    query = {}
    if status:
        query["status"] = status
    invoices = await db.invoices.find(query, {"_id": 0}).to_list(1000)
    return invoices


@router.get("/{invoice_id}", response_model=Invoice)
async def get_invoice(invoice_id: str):
    """Get a specific invoice by ID"""
    invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.post("/", response_model=Invoice)
async def create_invoice(invoice: InvoiceCreate):
    """Create a new invoice"""
    invoice_dict = invoice.model_dump()
    
    # Calculate balance due
    invoice_dict["balance_due"] = invoice_dict["total"]
    invoice_dict["paid_amount"] = 0.0
    
    new_invoice = Invoice(**invoice_dict)
    await db.invoices.insert_one(new_invoice.model_dump())
    return new_invoice


@router.put("/{invoice_id}", response_model=Invoice)
async def update_invoice(invoice_id: str, invoice_update: InvoiceUpdate):
    """Update an invoice"""
    existing_invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not existing_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    update_data = invoice_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    # Recalculate balance due if paid_amount changes
    if "paid_amount" in update_data:
        total = update_data.get("total", existing_invoice["total"])
        update_data["balance_due"] = total - update_data["paid_amount"]
        
        # Update status based on payment
        if update_data["balance_due"] <= 0:
            update_data["status"] = "paid"
            update_data["paid_date"] = datetime.now(timezone.utc).isoformat()
    
    await db.invoices.update_one({"id": invoice_id}, {"$set": update_data})
    
    updated_invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    return Invoice(**updated_invoice)


@router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: str):
    """Delete an invoice"""
    result = await db.invoices.delete_one({"id": invoice_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "Invoice deleted successfully"}


@router.post("/{invoice_id}/send")
async def send_invoice(invoice_id: str):
    """Mark an invoice as sent"""
    invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    await db.invoices.update_one(
        {"id": invoice_id}, 
        {"$set": {"status": "sent", "updated_at": datetime.now(timezone.utc)}}
    )
    
    updated_invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    return {"message": "Invoice sent", "invoice": updated_invoice}


@router.post("/{invoice_id}/pay")
async def pay_invoice(invoice_id: str, amount: float):
    """Record a payment for an invoice"""
    invoice = db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    current_paid = invoice.get("paid_amount", 0.0)
    new_paid_amount = current_paid + amount
    total = invoice["total"]
    balance_due = total - new_paid_amount
    
    update_data = {
        "paid_amount": new_paid_amount,
        "balance_due": balance_due,
        "updated_at": datetime.now(timezone.utc)
    }
    
    if balance_due <= 0:
        update_data["status"] = "paid"
        update_data["paid_date"] = datetime.now(timezone.utc).isoformat()
    
    db.invoices.update_one({"id": invoice_id}, {"$set": update_data})
    
    updated_invoice = db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    return {"message": f"Payment of ${amount} recorded", "invoice": updated_invoice}


@router.get("/by-customer/{customer_id}")
async def get_invoices_by_customer(customer_id: str):
    """Get all invoices for a specific customer"""
    invoices = list(db.invoices.find({"customer_id": customer_id}, {"_id": 0}))
    return invoices
