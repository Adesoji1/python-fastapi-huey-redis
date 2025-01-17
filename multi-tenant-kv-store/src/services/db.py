from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_size=10,        
    max_overflow=20,    
    pool_timeout=30,     
    pool_recycle=1800,
    pool_pre_ping=True,
    echo=False    
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_schema_if_not_exists(schema_name: str):
 
    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))