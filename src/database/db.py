from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from typing import Generator
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger("oz-stack.db")

# Database URL configuration - using SQLite by default
SQLITE_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create SQLAlchemy engine
engine = create_engine(
    SQLITE_DATABASE_URL, 
    connect_args={"check_same_thread": False} if SQLITE_DATABASE_URL.startswith("sqlite") else {},
    echo=os.getenv("DEBUG", "True").lower() == "true"
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

def get_db() -> Generator:
    """
    Dependency function to get a database session that will be used in a route
    and then closed after the route is done.
    
    Usage:
    ```
    @app.get("/users")
    def read_users(db: Session = Depends(get_db)):
        users = db.query(User).all()
        return users
    ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """
    Initialize the database by creating all tables.
    Should be called once at application startup.
    """
    from . import models  # Import here to avoid circular imports
    
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise