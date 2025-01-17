from sqlalchemy.orm import Session
from src.models import Tenant

def create_tenant(db: Session, email: str, password_hash: str) -> int:
    tenant = Tenant(email=email, password_hash=password_hash)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant.id

def get_tenant_by_email(db: Session, email: str):
    return db.query(Tenant).filter(Tenant.email == email).first()
