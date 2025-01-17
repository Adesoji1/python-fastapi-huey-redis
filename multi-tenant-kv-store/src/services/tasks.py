import time
import logging
from huey import RedisHuey, crontab
from src.config import settings
from src.services.db import create_schema_if_not_exists


logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('huey.log'),  
        logging.StreamHandler()          
    ]
)

logger = logging.getLogger(__name__)

huey = RedisHuey(
    'multi-tenant-kv-store',
    host=settings.HUEY_REDIS_HOST,
    port=settings.HUEY_REDIS_PORT,
    db=settings.HUEY_REDIS_DB,
)

def get_pending_task_count():
 
    try:
        return huey.pending_count()
    except Exception as e:
        logger.error(f"Error retrieving pending task count: {e}")
        return 0

@huey.periodic_task(crontab(minute='*/5'))
def audit_logging():
    logger.info("[Audit Logging] - Periodic task started.")
    time.sleep(1)
    logger.info("[Audit Logging] - Periodic task completed.")

@huey.task()
def process_expired_keys():
    logger.info("[TTL] Checking for expired keys (custom logic)...")
    time.sleep(1)
    logger.info("[TTL] Done checking.")

@huey.task()
def async_create_schema(schema_name: str):
    logger.info(f"[Schema Creation] - Starting creation of schema: {schema_name}")
    try:
        create_schema_if_not_exists(schema_name)
        logger.info(f"[Schema Creation] - Successfully created schema: {schema_name}")
    except Exception as e:
        logger.error(f"[Schema Creation] - Failed to create schema {schema_name}: {e}")
