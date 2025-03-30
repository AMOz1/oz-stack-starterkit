from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import secrets
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "admin")  # Default password, CHANGE THIS
AUTH_TOKEN_EXPIRY = int(os.getenv("AUTH_TOKEN_EXPIRY", "86400"))  # 24 hours in seconds
AUTH_COOKIE_NAME = os.getenv("AUTH_COOKIE_NAME", "oz_stack_auth")
AUTH_DISABLED = os.getenv("AUTH_DISABLED", "False").lower() == "true"

# Security utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()
serializer = URLSafeTimedSerializer(SECRET_KEY)

def verify_password(plain_password: str, stored_hash: Optional[str] = None) -> bool:
    """
    Verify a password against a stored hash or the environment variable password.
    For simplicity, we allow a plain text password in environment variables.
    """
    if stored_hash and pwd_context.verify(plain_password, stored_hash):
        return True
    
    # For single user mode, just check against the environment variable
    return plain_password == AUTH_PASSWORD


def get_auth_token(password: str) -> Optional[str]:
    """Generate an authentication token if password is correct."""
    if verify_password(password):
        return serializer.dumps({"authenticated": True})
    return None


def validate_auth_token(token: str) -> bool:
    """Validate an authentication token."""
    try:
        data = serializer.loads(token, max_age=AUTH_TOKEN_EXPIRY)
        return data.get("authenticated", False)
    except (SignatureExpired, BadSignature):
        return False


def get_current_user(request: Request) -> bool:
    """
    Validate user authentication from cookie.
    Returns True if user is authenticated, False otherwise.
    """
    # Skip authentication if disabled
    if AUTH_DISABLED:
        return True
        
    token = request.cookies.get(AUTH_COOKIE_NAME)
    if not token:
        return False
        
    return validate_auth_token(token)


def require_auth(request: Request):
    """Dependency to require authentication for routes."""
    # Skip authentication if disabled
    if AUTH_DISABLED:
        return True
        
    if not get_current_user(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


def set_auth_cookie(response: Response, password: str) -> bool:
    """Set the authentication cookie if the password is correct."""
    token = get_auth_token(password)
    if token:
        response.set_cookie(
            key=AUTH_COOKIE_NAME,
            value=token,
            httponly=True,
            max_age=AUTH_TOKEN_EXPIRY,
            secure=os.getenv("DEBUG", "True").lower() != "true",  # Secure in production
            samesite="lax"
        )
        return True
    return False


def clear_auth_cookie(response: Response):
    """Clear the authentication cookie."""
    response.delete_cookie(key=AUTH_COOKIE_NAME)