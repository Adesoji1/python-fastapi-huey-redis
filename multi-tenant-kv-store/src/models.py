from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, email={self.email})>"


class KeyValue(Base):
    __tablename__ = "key_values"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    key = Column(String(255), nullable=False, index=True)
    value = Column(String, nullable=False)
    ttl = Column(Integer, nullable=True)
    tags = Column(String, nullable=True)
    version = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    
    tenant = relationship("Tenant", back_populates="key_values")
    
    def __repr__(self):
        return f"<KeyValue(id={self.id}, key={self.key})>"

Tenant.key_values = relationship("KeyValue", back_populates="tenant")
