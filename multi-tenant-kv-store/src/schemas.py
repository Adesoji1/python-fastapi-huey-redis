from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    tenant_id: Optional[int] = None


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class SignUpResponse(BaseModel):
    message: str


# Key-Value Schemas
class KeyValueRequest(BaseModel):
    key: str
    value: str
    ttl: Optional[int] = Field(default=None, description="Time-to-live in seconds")
    tags: Optional[str] = Field(default=None, description="Descriptive tags")
    version: Optional[int] = Field(default=None, description="Version number")


class KeyValueResponse(BaseModel):
    key: str
    value: str
    ttl: Optional[int] = None
    tags: Optional[str] = None
    version: Optional[int] = None

    class Config:
        orm_mode = True
