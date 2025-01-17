from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.models import Tenant
from src.services.db import get_db
from src.security import hash_password, verify_password, create_access_token
from src.services.db_tenants import create_tenant
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.security import decode_access_token
from src.services.redis_client import get_cached_access_token, cache_access_token
import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/signup")
def signup(email: str, password: str, db: Session = Depends(get_db)):
    existing_tenant = db.query(Tenant).filter(Tenant.email == email).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant already exists.")
    
    hashed_password = hash_password(password)
    tenant_id = create_tenant(db, email, hashed_password)
    return {"message": f"Tenant created with ID: {tenant_id}"}



@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.email == form_data.username).first()
    if not tenant or not verify_password(form_data.password, tenant.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

    cached_token = get_cached_access_token(tenant.id)  
    if cached_token:
        logger.info(f"Using cached token for tenant {tenant.id}.")
        return {"access_token": cached_token, "token_type": "bearer"}
    
    access_token = create_access_token(data={"tenant_id": tenant.id})
    cache_access_token(tenant.id, access_token)  
    return {"access_token": access_token, "token_type": "bearer"}



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        tenant_id = payload.get("tenant_id")
        if not tenant_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: tenant_id is missing.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return tenant_id
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
