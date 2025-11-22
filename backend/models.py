from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal
from datetime import datetime, timezone
import uuid


# Chemical Reading Model
class ChemReading(BaseModel):
    date: str
    fc: float  # Free Chlorine
    ph: float
    ta: int  # Total Alkalinity
    ch: int  # Calcium Hardness
    cya: int  # Cyanuric Acid


# Pool/Body of Water Model
class Pool(BaseModel):
    id: str = Field(default_factory=lambda: f"pool-{str(uuid.uuid4())[:8]}")
    name: str
    type: str  # In-Ground, Above-Ground, Spa/Hot Tub
    color: str  # Hex color for UI
    gallons: int
    equipment: List[str]
    last_service: str
    chem_readings: List[ChemReading] = []


class PoolCreate(BaseModel):
    name: str
    type: str
    color: str = "#3B82F6"
    gallons: int
    equipment: List[str] = []
    last_service: str


# Customer Model
class Customer(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: f"cust-{str(uuid.uuid4())[:8]}")
    name: str
    email: str
    phone: str
    address: str
    status: Literal["active", "paused", "inactive"] = "active"
    account_balance: float = 0.0
    service_day: str  # Monday, Tuesday, etc.
    route_position: int = 1
    autopay: bool = False
    pools: List[Pool] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    status: Literal["active", "paused", "inactive"] = "active"
    account_balance: float = 0.0
    service_day: str
    route_position: int = 1
    autopay: bool = False
    pools: List[PoolCreate] = []


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: Optional[Literal["active", "paused", "inactive"]] = None
    account_balance: Optional[float] = None
    service_day: Optional[str] = None
    route_position: Optional[int] = None
    autopay: Optional[bool] = None


# Chemical Reading Create Model
class ChemReadingCreate(BaseModel):
    date: str
    fc: float
    ph: float
    ta: int
    ch: int
    cya: int


# Quote Models
class QuoteItem(BaseModel):
    description: str
    quantity: int = 1
    unit_price: float
    total: float


class Quote(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: f"quote-{str(uuid.uuid4())[:8]}")
    customer_id: str
    customer_name: str
    status: Literal["pending", "approved", "declined", "expired"] = "pending"
    items: List[QuoteItem] = []
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    notes: Optional[str] = None
    valid_until: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuoteCreate(BaseModel):
    customer_id: str
    customer_name: str
    items: List[QuoteItem]
    subtotal: float
    tax: float = 0.0
    total: float
    notes: Optional[str] = None
    valid_until: str


class QuoteUpdate(BaseModel):
    status: Optional[Literal["pending", "approved", "declined", "expired"]] = None
    items: Optional[List[QuoteItem]] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    notes: Optional[str] = None
    valid_until: Optional[str] = None


# Job Models
class Job(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: f"job-{str(uuid.uuid4())[:8]}")
    customer_id: str
    customer_name: str
    customer_address: str
    quote_id: Optional[str] = None
    status: Literal["scheduled", "in-progress", "completed", "cancelled"] = "scheduled"
    service_type: str  # Routine Service, Repair, One-time Service
    scheduled_date: str
    scheduled_time: str
    technician: str
    pools: List[str] = []  # Pool IDs to service
    notes: Optional[str] = None
    completion_notes: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobCreate(BaseModel):
    customer_id: str
    customer_name: str
    customer_address: str
    quote_id: Optional[str] = None
    service_type: str
    scheduled_date: str
    scheduled_time: str
    technician: str
    pools: List[str] = []
    notes: Optional[str] = None


class JobUpdate(BaseModel):
    status: Optional[Literal["scheduled", "in-progress", "completed", "cancelled"]] = None
    scheduled_date: Optional[str] = None
    scheduled_time: Optional[str] = None
    technician: Optional[str] = None
    notes: Optional[str] = None
    completion_notes: Optional[str] = None


# Invoice Models
class InvoiceLineItem(BaseModel):
    description: str
    quantity: int = 1
    unit_price: float
    total: float


class Invoice(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: f"inv-{str(uuid.uuid4())[:8]}")
    customer_id: str
    customer_name: str
    job_id: Optional[str] = None
    quote_id: Optional[str] = None
    invoice_number: str
    status: Literal["draft", "sent", "paid", "overdue", "cancelled"] = "draft"
    line_items: List[InvoiceLineItem] = []
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    paid_amount: float = 0.0
    balance_due: float = 0.0
    issue_date: str
    due_date: str
    paid_date: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InvoiceCreate(BaseModel):
    customer_id: str
    customer_name: str
    job_id: Optional[str] = None
    quote_id: Optional[str] = None
    invoice_number: str
    line_items: List[InvoiceLineItem]
    subtotal: float
    tax: float = 0.0
    total: float
    issue_date: str
    due_date: str
    notes: Optional[str] = None


class InvoiceUpdate(BaseModel):
    status: Optional[Literal["draft", "sent", "paid", "overdue", "cancelled"]] = None
    line_items: Optional[List[InvoiceLineItem]] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    paid_amount: Optional[float] = None
    balance_due: Optional[float] = None
    paid_date: Optional[str] = None
    notes: Optional[str] = None



# Technician Models
class Technician(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: f"tech-{str(uuid.uuid4())[:8]}")
    name: str
    email: str
    phone: str
    color: str = "#3B82F6"  # Hex color for UI visualization
    status: Literal["active", "inactive"] = "active"
    assigned_days: List[str] = []  # Days they work (e.g., ["Monday", "Tuesday"])
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TechnicianCreate(BaseModel):
    name: str
    email: str
    phone: str
    color: str = "#3B82F6"
    status: Literal["active", "inactive"] = "active"
    assigned_days: List[str] = []


class TechnicianUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    color: Optional[str] = None
    status: Optional[Literal["active", "inactive"]] = None
    assigned_days: Optional[List[str]] = None


# Route Models
class Route(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: f"route-{str(uuid.uuid4())[:8]}")
    name: str  # e.g., "Monday Route A"
    technician_id: str
    technician_name: str
    day: str  # Monday, Tuesday, Wednesday, etc.
    jobs: List[str] = []  # List of job IDs in order
    total_stops: int = 0
    estimated_duration: int = 0  # In minutes
    status: Literal["active", "inactive"] = "active"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RouteCreate(BaseModel):
    name: str
    technician_id: str
    technician_name: str
    day: str
    jobs: List[str] = []
    estimated_duration: int = 0


class RouteUpdate(BaseModel):
    name: Optional[str] = None
    technician_id: Optional[str] = None
    technician_name: Optional[str] = None
    day: Optional[str] = None
    jobs: Optional[List[str]] = None
    estimated_duration: Optional[int] = None
    status: Optional[Literal["active", "inactive"]] = None


class RouteJobReorder(BaseModel):
    jobs: List[str]  # New order of job IDs



# Alert Models
class Alert(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: f"alert-{str(uuid.uuid4())[:8]}")
    type: Literal["chemical", "flow", "leak", "time", "cost"]
    severity: Literal["high", "medium", "low"]
    title: str
    message: str
    customer_id: str
    customer_name: str
    pool_id: Optional[str] = None  # For chemical/flow/leak alerts
    pool_name: Optional[str] = None
    job_id: Optional[str] = None  # For time/cost alerts
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AlertCreate(BaseModel):
    type: Literal["chemical", "flow", "leak", "time", "cost"]
    severity: Literal["high", "medium", "low"]
    title: str
    message: str
    customer_id: str
    customer_name: str
    pool_id: Optional[str] = None
    pool_name: Optional[str] = None
    job_id: Optional[str] = None


class AlertUpdate(BaseModel):
    resolved: Optional[bool] = None
    resolved_at: Optional[datetime] = None
