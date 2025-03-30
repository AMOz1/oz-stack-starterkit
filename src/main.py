from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API router
from .api import router as api_router

app = FastAPI(
    title="Oz Stack Starter Kit",
    description="A lightweight web application starter kit with FastAPI, HTMX, and Tailwind CSS",
    version="1.0.0"
)

# Setup static files and templates
base_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=base_dir / "static"), name="static")
templates = Jinja2Templates(directory=base_dir / "templates")

# Include API router
app.include_router(api_router)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hello")
async def hello(request: Request, name: str = "World"):
    return templates.TemplateResponse("components/greeting.html", {"request": request, "name": name})

@app.get("/demo")
async def demo(request: Request):
    return templates.TemplateResponse("demo.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", 
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )
