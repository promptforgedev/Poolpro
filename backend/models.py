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
