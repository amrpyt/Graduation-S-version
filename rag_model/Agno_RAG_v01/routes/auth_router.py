from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client
from config import Settings

settings = Settings()
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Initialize Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm="HS256")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    # Check if user exists
    user = supabase.table("users").select("*").eq("email", user_data.email).execute()
    if user.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user in Supabase
    hashed_password = get_password_hash(user_data.password)
    new_user = {
        "email": user_data.email,
        "password": hashed_password,
        "full_name": user_data.full_name
    }
    
    result = supabase.table("users").insert(new_user).execute()
    user_id = result.data[0]["id"]
    
    # Create access token
    access_token = create_access_token({"sub": str(user_id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = supabase.table("users").select("*").eq("email", form_data.username).execute()
    if not user.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    user = user.data[0]
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token({"sub": str(user["id"])})
    return {"access_token": access_token, "token_type": "bearer"} 