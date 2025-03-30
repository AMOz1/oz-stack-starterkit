# Authentication Guide

This document explains how the simple password authentication system works in the Oz Stack Starter Kit.

## Overview

The starter kit includes a simple, single-user password authentication system that:

1. Protects all routes with a single password (no username required)
2. Uses secure cookies for session management
3. Can be easily enabled or disabled via configuration

This approach is perfect for personal projects or internal tools where you want minimal protection without the complexity of a full user management system.

## How It Works

The authentication system uses:
- Password verification against an environment variable
- Secure, signed cookies for maintaining session state
- Redirect-based flow for unauthenticated users

### Authentication Flow

1. User attempts to access a protected route
2. If not authenticated, they are redirected to `/login`
3. User enters the password
4. On successful login, a secure cookie is set
5. User is redirected to the originally requested page

## Configuration

Authentication settings are controlled via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `AUTH_DISABLED` | Disable authentication entirely | `False` |
| `AUTH_PASSWORD` | The password required to log in | `admin` |
| `SECRET_KEY` | Secret key for signing cookies | Random value |
| `AUTH_TOKEN_EXPIRY` | Session duration in seconds | `86400` (24 hours) |
| `AUTH_COOKIE_NAME` | Name of the auth cookie | `oz_stack_auth` |

## Setting Up Authentication

1. Create a `.env` file in the project root (or use the one created by setup.sh)
2. Configure authentication settings:
   ```
   # Authentication settings
   SECRET_KEY="your-secure-secret-key"
   AUTH_PASSWORD="your-secure-password"
   AUTH_DISABLED=False
   ```

3. Generate a secure random key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

## Disabling Authentication

If you're developing locally or don't need authentication, you can disable it:

```
AUTH_DISABLED=True
```

## Security Considerations

While this authentication system is simple, it follows security best practices:

- Passwords are never stored in plain text in the code
- Cookies are signed and have expiration times
- The auth cookie is HTTP-only to prevent JavaScript access
- In production, cookies are secure (HTTPS only)

## Customizing Authentication

If you need more advanced authentication:

1. For multiple users: Extend the `auth.py` module to check against a database
2. For OAuth/social login: Consider integrating with a library like [Authlib](https://authlib.org/)
3. For API tokens: Implement JWT authentication with [python-jose](https://github.com/mpdavis/python-jose)

## Routes

The authentication system provides these routes:

- `/login` - Login page with password form
- `/logout` - Endpoint to log out by clearing the cookie

## Public Routes

By default, the following routes are public (accessible without authentication):

- `/login` - Login page
- `/logout` - Logout endpoint
- `/health` - Health check endpoint
- `/favicon.ico` - Favicon endpoint