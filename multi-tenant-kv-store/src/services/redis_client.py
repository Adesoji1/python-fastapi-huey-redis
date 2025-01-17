import redis
import json
from src.config import settings
import logging
from redis.exceptions import RedisError
import time


logger = logging.getLogger(__name__)


try:
    r = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
        socket_connect_timeout=5,  
        health_check_interval=30,  
    )
    r.ping()
    logger.info("Successfully connected to Redis.")
except redis.ConnectionError as e:
    logger.error(f"Redis connection error: {e}")
    r = None


def set_key(tenant_id: int, key: str, value: str, ttl: int = None, tags: str = None, version: int = None):
    if r is None:
        logger.error("Redis client is not initialized. Cannot set key.")
        return

    namespaced_key = f"{tenant_id}:{key}"
    data = {
        "value": value,
        "tags": tags,
        "version": version
    }
    try:
        r.set(namespaced_key, json.dumps(data))
        if ttl:
            r.expire(namespaced_key, ttl)
        logger.info(f"Key '{key}' set successfully for tenant {tenant_id}.")
    except Exception as e:
        logger.error(f"Error setting key '{key}' for tenant {tenant_id}: {e}")


def get_key(tenant_id: int, key: str):
    if r is None:
        logger.error("Redis client is not initialized. Cannot get key.")
        return None

    namespaced_key = f"{tenant_id}:{key}"
    try:
        raw_data = r.get(namespaced_key)
        if raw_data is None:
            logger.warning(f"Key '{key}' not found for tenant {tenant_id}.")
            return None
        logger.info(f"Key '{key}' retrieved successfully for tenant {tenant_id}.")
        return json.loads(raw_data)
    except Exception as e:
        logger.error(f"Error retrieving key '{key}' for tenant {tenant_id}: {e}")
        return None


def delete_key(tenant_id: int, key: str):
    if r is None:
        logger.error("Redis client is not initialized. Cannot delete key.")
        return

    namespaced_key = f"{tenant_id}:{key}"
    try:
        result = r.delete(namespaced_key)
        if result == 1:
            logger.info(f"Key '{key}' deleted successfully for tenant {tenant_id}.")
        else:
            logger.warning(f"Key '{key}' not found for deletion for tenant {tenant_id}.")
    except Exception as e:
        logger.error(f"Error deleting key '{key}' for tenant {tenant_id}: {e}")


def get_ttl(tenant_id: int, key: str):
    if r is None:
        logger.error("Redis client is not initialized. Cannot get TTL.")
        return None

    namespaced_key = f"{tenant_id}:{key}"
    try:
        ttl = r.ttl(namespaced_key)
        if ttl == -2:
            logger.warning(f"Key '{key}' for tenant {tenant_id} has expired.")
            return None
        elif ttl == -1:
            logger.info(f"Key '{key}' for tenant {tenant_id} does not have a TTL.")
        else:
            logger.info(f"Key '{key}' for tenant {tenant_id} has TTL: {ttl} seconds.")
        return ttl
    except Exception as e:
        logger.error(f"Error retrieving TTL for key '{key}' for tenant {tenant_id}: {e}")
        return None

def cache_access_token(tenant_id: int, token: str, ttl: int = 9000):
    r.set(f"auth_token:{tenant_id}", token, ex=ttl)

def get_cached_access_token(tenant_id: int) -> str:
    return r.get(f"auth_token:{tenant_id}")


def set_key_with_retry(tenant_id: int, key: str, value: str, retries: int = 3, ttl: int = None):
    for attempt in range(retries):
        try:
            set_key(tenant_id, key, value, ttl)
            return
        except RedisError as e:
            logger.warning(f"Retrying set_key for {key} (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(1)
    logger.error(f"Failed to set key {key} after {retries} retries.")
