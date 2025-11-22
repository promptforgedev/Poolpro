from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime, timezone

from models import Quote, QuoteCreate, QuoteUpdate

router = APIRouter(prefix="/quotes", tags=["quotes"])

# MongoDB will be accessed from server.py
db = None

def init_db(database):
    global db
    db = database


@router.get("/", response_model=List[Quote])
async def get_all_quotes():
    """Get all quotes"""
    quotes = await db.quotes.find({}, {"_id": 0}).to_list(1000)
    return quotes


@router.get("/{quote_id}", response_model=Quote)
async def get_quote(quote_id: str):
    """Get a specific quote by ID"""
    quote = await db.quotes.find_one({"id": quote_id}, {"_id": 0})
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.post("/", response_model=Quote)
async def create_quote(quote: QuoteCreate):
    """Create a new quote"""
    quote_dict = quote.model_dump()
    new_quote = Quote(**quote_dict)
    await db.quotes.insert_one(new_quote.model_dump())
    return new_quote


@router.put("/{quote_id}", response_model=Quote)
async def update_quote(quote_id: str, quote_update: QuoteUpdate):
    """Update a quote"""
    existing_quote = db.quotes.find_one({"id": quote_id}, {"_id": 0})
    if not existing_quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    update_data = quote_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    db.quotes.update_one({"id": quote_id}, {"$set": update_data})
    
    updated_quote = db.quotes.find_one({"id": quote_id}, {"_id": 0})
    return Quote(**updated_quote)


@router.delete("/{quote_id}")
async def delete_quote(quote_id: str):
    """Delete a quote"""
    result = db.quotes.delete_one({"id": quote_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Quote not found")
    return {"message": "Quote deleted successfully"}


@router.post("/{quote_id}/approve")
async def approve_quote(quote_id: str):
    """Approve a quote and optionally create a job"""
    quote = db.quotes.find_one({"id": quote_id}, {"_id": 0})
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    db.quotes.update_one(
        {"id": quote_id}, 
        {"$set": {"status": "approved", "updated_at": datetime.now(timezone.utc)}}
    )
    
    updated_quote = db.quotes.find_one({"id": quote_id}, {"_id": 0})
    return {"message": "Quote approved", "quote": updated_quote}


@router.post("/{quote_id}/decline")
async def decline_quote(quote_id: str):
    """Decline a quote"""
    quote = db.quotes.find_one({"id": quote_id}, {"_id": 0})
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    db.quotes.update_one(
        {"id": quote_id}, 
        {"$set": {"status": "declined", "updated_at": datetime.now(timezone.utc)}}
    )
    
    updated_quote = db.quotes.find_one({"id": quote_id}, {"_id": 0})
    return {"message": "Quote declined", "quote": updated_quote}
