from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import List, Dict, Any
import random

router = APIRouter(prefix="/api")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

# Sample data for demo purposes
sample_data = [
    {"id": 1, "name": "Task 1", "status": "Pending"},
    {"id": 2, "name": "Task 2", "status": "Completed"},
    {"id": 3, "name": "Task 3", "status": "In Progress"},
]

@router.get("/tasks")
async def get_tasks() -> List[Dict[str, Any]]:
    """Return a list of sample tasks as JSON"""
    return sample_data

@router.get("/tasks/html")
async def get_tasks_html(request: Request):
    """Return tasks rendered as HTML for HTMX"""
    return templates.TemplateResponse(
        "components/tasks.html", 
        {"request": request, "tasks": sample_data}
    )

@router.get("/random")
async def get_random_number():
    """Generate a random number"""
    return {"number": random.randint(1, 100)}

@router.get("/random/html")
async def get_random_html(request: Request):
    """Return a random number rendered as HTML for HTMX"""
    number = random.randint(1, 100)
    return templates.TemplateResponse(
        "components/random.html", 
        {"request": request, "number": number}
    )