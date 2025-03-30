from fastapi import FastAPI, Request, HTTPException, Depends, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from pathlib import Path
import uvicorn
import os
import logging
import secrets
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("oz-stack")

# Load environment variables
load_dotenv()

# Import API router and auth
from .api import router as api_router
from .auth import require_auth, get_current_user, set_auth_cookie, clear_auth_cookie, AUTH_DISABLED

# Import database
from .database.db import engine, init_db

# Create FastAPI application
app_name = os.getenv("APP_NAME", "Oz Stack Starter Kit")
app_version = os.getenv("APP_VERSION", "1.0.0")

# Generate a secret key if not provided
if not os.getenv("SECRET_KEY"):
    logger.warning("SECRET_KEY not found in environment variables. Generating a random one for this session.")
    logger.warning("For production, set a permanent SECRET_KEY in your .env file.")
    os.environ["SECRET_KEY"] = secrets.token_hex(32)

app = FastAPI(
    title=app_name,
    description="A lightweight web application starter kit with FastAPI, HTMX, and Tailwind CSS",
    version=app_version,
    docs_url="/api/docs" if os.getenv("DEBUG", "True").lower() == "true" else None,
    redoc_url="/api/redoc" if os.getenv("DEBUG", "True").lower() == "true" else None,
)

# Setup middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup static files and templates
base_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=base_dir / "static"), name="static")
templates = Jinja2Templates(directory=base_dir / "templates")

# Include API router with authentication
if not AUTH_DISABLED:
    api_router.dependencies.append(Depends(require_auth))
app.include_router(api_router)

# Define error handlers
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Internal server error: {exc}")
    return templates.TemplateResponse("errors/500.html", {"request": request}, status_code=500)

# Authentication routes
@app.get("/login")
async def login_page(request: Request):
    """Render the login page"""
    # If authentication is disabled, redirect to home
    if AUTH_DISABLED:
        return RedirectResponse(url="/")
        
    # If already authenticated, redirect to home
    if get_current_user(request):
        return RedirectResponse(url="/")
        
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, password: str = Form(...)):
    """Handle login form submission"""
    # If authentication is disabled, redirect to home
    if AUTH_DISABLED:
        return RedirectResponse(url="/")
        
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
    if set_auth_cookie(response, password):
        logger.info("User logged in successfully")
        return response
    else:
        logger.warning("Failed login attempt")
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Invalid password"}, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )

@app.get("/logout")
async def logout():
    """Log out the user by clearing the auth cookie"""
    response = RedirectResponse(url="/login")
    clear_auth_cookie(response)
    return response

# Define protected routes
@app.get("/")
async def index(request: Request, authenticated: bool = Depends(get_current_user)):
    """Render the home page"""
    # If authentication is enabled and user is not authenticated, redirect to login
    if not AUTH_DISABLED and not authenticated:
        return RedirectResponse(url="/login")
        
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hello")
async def hello(request: Request, name: str = "World", authenticated: bool = Depends(get_current_user)):
    """Render a personalized greeting component"""
    # If authentication is enabled and user is not authenticated, redirect to login
    if not AUTH_DISABLED and not authenticated:
        return RedirectResponse(url="/login")
        
    return templates.TemplateResponse("components/greeting.html", {"request": request, "name": name})

@app.get("/demo")
async def demo(request: Request, authenticated: bool = Depends(get_current_user)):
    """Render the demo page"""
    # If authentication is enabled and user is not authenticated, redirect to login
    if not AUTH_DISABLED and not authenticated:
        return RedirectResponse(url="/login")
        
    return templates.TemplateResponse("demo.html", {"request": request})

@app.get("/favicon.ico")
async def favicon():
    """Serve the favicon"""
    return RedirectResponse(url="/static/favicon.ico")

@app.get("/health")
async def health():
    """Health check endpoint (publicly accessible)"""
    return {"status": "ok", "version": app_version}

# Initialize database
@app.on_event("startup")
async def startup_db_client():
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")

# Run the application
if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    # Log authentication status
    if AUTH_DISABLED:
        logger.info("Authentication is DISABLED")
    else:
        logger.info("Authentication is ENABLED")
    
    logger.info(f"Starting {app_name} v{app_version}")
    logger.info(f"Debug mode: {debug}")
    
    # Check if desktop mode is enabled
    desktop_mode = os.getenv("DESKTOP_MODE", "False").lower() == "true"
    if desktop_mode:
        logger.info("Running in desktop mode")
        try:
            # Initialize the database
            init_db()
            
            # Launch the desktop app
            from .desktop.app import run_desktop_app
            run_desktop_app()
        except ImportError:
            logger.error("Desktop module not found. Make sure CustomTkinter is installed.")
        except Exception as e:
            logger.error(f"Error running desktop app: {str(e)}")
    else:
        # Run the web server
        uvicorn.run(
            "src.main:app", 
            host=host,
            port=port,
            reload=debug,
            log_level="info" if debug else "warning"
        )
