import logging
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas import KeyValueRequest, KeyValueResponse
from src.routers.auth import get_current_user
from src.services.redis_client import (
    set_key,
    get_key,
    delete_key,
    get_ttl
)

router = APIRouter(prefix="/kv", tags=["Key-Value Operations"])

logger = logging.getLogger(__name__)

@router.post("/", response_model=KeyValueResponse, status_code=status.HTTP_201_CREATED)
def create_keyval(data: KeyValueRequest, tenant_id: int = Depends(get_current_user)):
    try:
        existing = get_key(tenant_id, data.key)
        if existing is not None:
            logger.warning(
                f"Create Key Failed: Key '{data.key}' already exists for tenant {tenant_id}."
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Key already exists. Use update instead."
            )
        set_key(
            tenant_id=tenant_id,
            key=data.key,
            value=data.value,
            ttl=data.ttl,
            tags=data.tags,
            version=data.version
        )
        logger.info(f"Key '{data.key}' created successfully for tenant {tenant_id}.")
        ttl = get_ttl(tenant_id, data.key)
        return KeyValueResponse(
            key=data.key,
            value=data.value,
            ttl=ttl,
            tags=data.tags,
            version=data.version
        )
    except Exception as e:
        logger.error(f"Error creating key '{data.key}' for tenant {tenant_id}: {e}")
        raise

@router.get("/{key}", response_model=KeyValueResponse)
def read_keyval(key: str, tenant_id: int = Depends(get_current_user)):
    try:
        data = get_key(tenant_id, key)
        if data is None:
            logger.warning(f"Key '{key}' not found for tenant {tenant_id}.")
            raise HTTPException(status_code=404, detail="Key not found in Redis.")
        ttl = get_ttl(tenant_id, key)
        logger.info(f"Key '{key}' retrieved successfully for tenant {tenant_id}.")
        return KeyValueResponse(
            key=key,
            value=data.get("value"),
            ttl=ttl,
            tags=data.get("tags"),
            version=data.get("version")
        )
    except Exception as e:
        logger.error(f"Error reading key '{key}' for tenant {tenant_id}: {e}")
        raise

@router.put("/", response_model=KeyValueResponse, status_code=status.HTTP_200_OK)
def update_keyval(data: KeyValueRequest, tenant_id: int = Depends(get_current_user)):
    try:
        existing = get_key(tenant_id, data.key)
        if existing is None:
            logger.info(f"Key '{data.key}' not found for tenant {tenant_id}; creating new key (UPSERT).")
        set_key(
            tenant_id=tenant_id,
            key=data.key,
            value=data.value,
            ttl=data.ttl,
            tags=data.tags,
            version=data.version
        )
        updated_ttl = get_ttl(tenant_id, data.key)
        logger.info(f"Key '{data.key}' updated (or created) successfully for tenant {tenant_id}.")
        return KeyValueResponse(
            key=data.key,
            value=data.value,
            ttl=updated_ttl,
            tags=data.tags,
            version=data.version
        )
    except Exception as e:
        logger.error(f"Error updating key '{data.key}' for tenant {tenant_id}: {e}")
        raise

@router.delete("/{key}", status_code=status.HTTP_200_OK)
def delete_keyval(key: str, tenant_id: int = Depends(get_current_user)):
    try:
        # Return a message but do NOT raise 404 if the key is missing.
        delete_key(tenant_id, key)
        logger.info(f"Key '{key}' deleted or did not exist for tenant {tenant_id}.")
        return {"message": f"Key '{key}' deleted (or was already absent)."}
    except Exception as e:
        logger.error(f"Error deleting key '{key}' for tenant {tenant_id}: {e}")
        raise
