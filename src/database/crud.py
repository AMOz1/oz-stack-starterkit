from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from . import models, schemas

# CRUD operations for Task model

def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Get a single task by ID"""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    filters: Optional[Dict[str, Any]] = None
) -> List[models.Task]:
    """
    Get a list of tasks with optional pagination and filtering
    
    Args:
        db: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        filters: Dictionary of filter conditions (e.g. {"status": "Pending"})
    
    Returns:
        List of Task objects
    """
    query = db.query(models.Task)
    
    # Apply filters if provided
    if filters:
        for field, value in filters.items():
            if hasattr(models.Task, field):
                query = query.filter(getattr(models.Task, field) == value)
    
    return query.offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """Create a new task"""
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate) -> Optional[models.Task]:
    """Update an existing task"""
    db_task = get_task(db, task_id)
    if db_task:
        # Only update fields that are provided (not None)
        update_data = task.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task by ID"""
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False


# Add more CRUD functions as needed for your application