from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from models import CustomerAuth, CustomerRegister, CustomerLogin, Token, TokenData

router = APIRouter(prefix="/auth", tags=["auth"])

# MongoDB will be accessed from server.py
db = None

def init_db(database):
    """Initialize database connection"""
    global db
    db = database

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_customer(token: str = Depends(oauth2_scheme)):
    """Get current authenticated customer from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        customer_id: str = payload.get("sub")
        if customer_id is None:
            raise credentials_exception
        token_data = TokenData(customer_id=customer_id)
    except JWTError:
        raise credentials_exception
    
    customer = await db.customers.find_one({"id": token_data.customer_id})
    if customer is None:
        raise credentials_exception
    return customer


@router.post("/register", response_model=Token)
async def register_customer(register_data: CustomerRegister):
    """Register a new customer for portal access"""
    
    # Check if customer exists
    customer = await db.customers.find_one({"id": register_data.customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if email already registered
    existing_auth = await db.customer_auth.find_one({"email": register_data.email})
    if existing_auth:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create auth record
    auth_data = CustomerAuth(
        customer_id=register_data.customer_id,
        email=register_data.email,
        password_hash=get_password_hash(register_data.password)
    )
    
    await db.customer_auth.insert_one(auth_data.model_dump())
    
    # Create token
    access_token = create_access_token(
        data={"sub": register_data.customer_id}
    )
    
    return Token(
        access_token=access_token,
        customer_id=register_data.customer_id,
        customer_name=customer.get("name", "")
    )


@router.post("/login", response_model=Token)
async def login_customer(login_data: CustomerLogin):
    """Login customer to portal"""
    
    # Find auth record
    auth = await db.customer_auth.find_one({"email": login_data.email})
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, auth.get("password_hash")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Get customer info
    customer = await db.customers.find_one({"id": auth.get("customer_id")})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Create token
    access_token = create_access_token(
        data={"sub": auth.get("customer_id")}
    )
    
    return Token(
        access_token=access_token,
        customer_id=auth.get("customer_id"),
        customer_name=customer.get("name", "")
    )


@router.get("/me")
async def get_current_customer_info(current_customer: dict = Depends(get_current_customer)):
    """Get current authenticated customer's information"""
    return {
        "id": current_customer.get("id"),
        "name": current_customer.get("name"),
        "email": current_customer.get("email"),
        "phone": current_customer.get("phone"),
        "address": current_customer.get("address"),
        "status": current_customer.get("status"),
        "account_balance": current_customer.get("account_balance"),
        "service_day": current_customer.get("service_day"),
        "autopay": current_customer.get("autopay")
    }
