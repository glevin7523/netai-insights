"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os

# Use SQLite for simplicity (can be changed to PostgreSQL later)
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/network_analytics.db"

# Create engine with connection pooling
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    """
    Get database session
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        # Test database connection PROPERLY
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        yield db
    finally:
        db.close()

# Create all tables (will be called from main.py)
def create_tables():
    """Create all database tables"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")