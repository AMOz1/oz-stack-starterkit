# Oz Stack Starter Kit

A bulletproof, production-ready application starter kit built with:

- **Backend**: FastAPI (Python)
- **Frontend**: HTMX + Desktop UI with CustomTkinter
- **Database**: SQLite with SQLAlchemy ORM
- **Styling**: Tailwind CSS 4.x + DaisyUI 5.x
- **Optional JS**: Hyperscript, Alpine.js
- **Authentication**: Simple password protection

[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.0.0-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![DaisyUI](https://img.shields.io/badge/DaisyUI-5.0.9-5A0EF8?style=flat&logo=daisyui&logoColor=white)](https://daisyui.com/)

## Comprehensive Setup Guide

### Prerequisites

Before beginning, ensure you have the following installed on your system:

- **Python 3.8+** - [Download & Install Python](https://www.python.org/downloads/)
  ```bash
  # Verify installation
  python --version  # Should be 3.8 or higher
  ```

- **Node.js 14+** and **npm 6+** - [Download & Install Node.js](https://nodejs.org/)
  ```bash
  # Verify installation
  node --version  # Should be 14.x or higher
  npm --version   # Should be 6.x or higher
  ```

- **Git** - [Download & Install Git](https://git-scm.com/downloads)
  ```bash
  # Verify installation
  git --version
  ```

#### macOS-specific Prerequisites

If using macOS:

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python, Node.js, and Git
brew install python node git
```

#### Windows-specific Prerequisites

- For Windows users, consider installing [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install) for a better development experience
- Ensure Python is added to your PATH during installation
- Install [Git for Windows](https://gitforwindows.org/) which includes Git Bash

### Setup Options

#### Option 1: Automated Setup (Recommended)

For Unix-based systems (macOS, Linux) or Windows with Git Bash:

```bash
# Clone the repository
git clone https://github.com/yourusername/oz-stack-starterkit.git
cd oz-stack-starterkit

# Run the setup script
chmod +x setup.sh
./setup.sh
```

#### Option 2: Manual Setup

If the automated script doesn't work for your environment, follow these steps:

##### 1. Clone the repository

```bash
git clone https://github.com/yourusername/oz-stack-starterkit.git
cd oz-stack-starterkit
```

##### 2. Create and activate a Python virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows (Command Prompt):
venv\Scripts\activate.bat
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On Windows (Git Bash):
source venv/Scripts/activate
```

##### 3. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

##### 4. Install Node.js dependencies

```bash
npm install
```

##### 5. Build the CSS

```bash
npm run build:css
```

### Dependency Verification

This starter kit requires specific versions of key dependencies:

- **Tailwind CSS**: 4.x
- **DaisyUI**: 5.x

After installation, verify you have the correct versions:

```bash
npm run verify-versions
```

If you need to fix version issues:

```bash
npm run fix-versions
```

### Configuration

#### Environment Variables

Create a `.env` file in the project root (it's gitignored by default):

```bash
# Create .env file
touch .env
```

Add the following configuration (customize as needed):

```
# Server settings
HOST=127.0.0.1
PORT=8000
DEBUG=True

# Application settings
APP_NAME="Oz Stack Starter Kit"
APP_VERSION="1.0.0"

# Authentication settings
# Generate a good secret key with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY="your-secure-secret-key-here-at-least-32-chars"
AUTH_PASSWORD="admin"  # Change this to a secure password
AUTH_TOKEN_EXPIRY=86400  # 24 hours in seconds
AUTH_COOKIE_NAME="oz_stack_auth"
AUTH_DISABLED=False  # Set to True to disable authentication

# Database settings
DATABASE_URL="sqlite:///./app.db"  # SQLite database path

# Desktop application settings
DESKTOP_MODE=False  # Set to True to run the desktop app
CTK_APPEARANCE="System"  # Options: System, Light, Dark
CTK_THEME="blue"  # Options: blue, green, dark-blue
```

For your convenience, you can copy the `.env.example` file:

```bash
cp .env.example .env
# Then edit the file to customize your settings
```

## Development Workflow

### Start the development server

```bash
# Make sure your virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the development server with hot reloading
npm run dev
```

This will start a development server at http://localhost:8000 with auto-reload enabled.

### Watch for CSS changes

In a separate terminal:

```bash
# Make sure to activate the virtual environment in this terminal too
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the CSS watcher
npm run watch:css
```

### Stopping the servers

Press `Ctrl+C` in each terminal to stop the respective processes.

Remember to deactivate your virtual environment when you're done:

```bash
deactivate
```

## Project Structure Explained

```
oz-stack-starterkit/
├── .env                    # Environment variables (create this file manually)
├── .gitignore              # Git ignore file
├── package.json            # Node.js package configuration
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── setup.sh                # Automated setup script
├── tailwind.config.js      # Tailwind CSS configuration
│
└── src/                    # Source code directory
    ├── __init__.py         # Python package indicator
    ├── api.py              # API endpoints
    ├── main.py             # Application entry point
    │
    ├── static/             # Static files
    │   ├── css/
    │   │   ├── app.css     # Tailwind CSS source file
    │   │   └── output.css  # Generated CSS (git-ignored)
    │   └── js/             # JavaScript files (if needed)
    │
    └── templates/          # Jinja2 templates
        ├── components/     # Reusable UI components
        │   ├── greeting.html
        │   ├── random.html
        │   └── tasks.html
        ├── base.html       # Base template with layout
        ├── demo.html       # Demo page
        └── index.html      # Home page
```

## Included Technologies

### Backend

- **FastAPI**: Modern, high-performance web framework for building APIs with Python
- **Uvicorn**: ASGI server for serving FastAPI applications
- **Jinja2**: Template engine for generating HTML
- **python-dotenv**: For loading environment variables from .env files

### Frontend

- **HTMX**: Allows HTTP requests directly from HTML, enabling dynamic content without writing JavaScript
- **Hyperscript**: Small scripting language for adding interactivity
- **Alpine.js**: Minimalist JavaScript framework for adding behavior to your markup

### Styling

- **Tailwind CSS**: Utility-first CSS framework
- **DaisyUI**: Component library for Tailwind CSS

### Security

- **Authentication**: Simple password protection with secure cookie sessions
- **python-jose**: JSON Web Token implementation
- **passlib**: Password hashing library with bcrypt support
- **itsdangerous**: Secure cookie signing

For more details on authentication, see [AUTH.md](AUTH.md)

### Database

- **SQLAlchemy**: Powerful Python ORM for database access
- **SQLite**: Built-in database with zero configuration
- **Alembic**: Database migration tool for version control
- **Pydantic**: Data validation for request/response models

For more details on database usage, see [DATABASE.md](DATABASE.md)

### Desktop UI

- **CustomTkinter**: Modern desktop UI framework built on Tkinter
- **Same business logic**: Shared codebase between web and desktop interfaces
- **Dark/Light modes**: Support for different themes and appearances

For more details on desktop application, see [DESKTOP.md](DESKTOP.md)

## Common Tasks

### Adding a new page

1. Create a new HTML template in `src/templates/`
2. Add a route in `src/main.py`:

```python
@app.get("/your-new-page")
async def your_new_page(request: Request):
    return templates.TemplateResponse("your-new-page.html", {"request": request})
```

### Adding a new API endpoint

Add your endpoint to `src/api.py`:

```python
@router.get("/your-endpoint")
async def your_endpoint():
    return {"message": "Your data here"}
```

### Adding new Python dependencies

1. Add the dependency to `requirements.txt`
2. Install it with:

```bash
pip install -r requirements.txt
```

### Adding new NPM packages

```bash
npm install package-name
```

Then update your `package.json` accordingly.

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError" when running the application

Ensure your virtual environment is activated and all dependencies are installed:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### CSS not updating

Make sure you're running the CSS watcher:

```bash
npm run watch:css
```

Verify that your HTML templates are correctly referencing the CSS file (`/static/css/output.css`).

#### Port 8000 already in use

Change the port in your `.env` file or directly in the command:

```bash
PORT=8001 python -m src.main
```

#### Connection refused when trying to access the app

If you can't connect to the application in your browser:

```bash
# Try changing the HOST in your .env file from 0.0.0.0 to 127.0.0.1
HOST=127.0.0.1
# Then restart the server
```

Some systems have network interface binding issues with 0.0.0.0. Using 127.0.0.1 (localhost) is more reliable for local development.

#### Virtual environment issues

If you encounter problems with your virtual environment, you can create a new one:

```bash
# Remove the old environment
rm -rf venv

# Create a new one
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Node.js/npm errors

Ensure you have a compatible version of Node.js and npm:

```bash
node --version  # Should be 14.x or higher
npm --version   # Should be 6.x or higher
```

### Getting Help

If you encounter any issues not covered here, please:

1. Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
2. Check the [HTMX documentation](https://htmx.org/docs/)
3. Check the [Tailwind CSS documentation](https://tailwindcss.com/docs)
4. Open an issue on the GitHub repository

## Production Deployment

For production deployment, consider:

1. Setting `DEBUG=False` in your `.env` file
2. Using a production ASGI server like Uvicorn with Gunicorn
3. Setting up a reverse proxy like Nginx
4. Using a process manager like Supervisor or systemd

Example production deployment command:

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
```

## License

This project is licensed under the ISC License.