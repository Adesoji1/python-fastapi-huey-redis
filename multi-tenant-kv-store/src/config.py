import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

class Settings:
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))

    HUEY_REDIS_HOST = os.getenv("HUEY_REDIS_HOST", REDIS_HOST)
    HUEY_REDIS_PORT = int(os.getenv("HUEY_REDIS_PORT", REDIS_PORT))
    HUEY_REDIS_DB = int(os.getenv("HUEY_REDIS_DB", "1"))

   
    encoded_password = urllib.parse.quote_plus(POSTGRES_PASSWORD)

    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{encoded_password}@"
        f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
        f"{POSTGRES_DB}?sslmode=require"
    )

settings = Settings()

