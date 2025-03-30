from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Pydantic schemas for Task model
class TaskBase(BaseModel):
    """Base schema for Task data"""
    name: str = Field(..., min_length=1, max_length=100, description="Task name or title")
    description: Optional[str] = Field(None, description="Detailed task description")
    status: Optional[str] = Field("Pending", description="Current task status")


class TaskCreate(TaskBase):
    """Schema for creating a new Task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing Task"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """Schema for Task response"""
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Allow converting ORM objects to response schemas


# Add more schemas as needed for your application