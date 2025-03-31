# Oz Stack Starter Kit

A personal, opinionated starter kit for macOS development with Python and HTMX. Built for clean, efficient development without unnecessary complexity.

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

- **Python 3.11** (Required) - [Download & Install Python](https://www.python.org/downloads/)
  ```bash
  # Verify Python installation
  python3 --version  # Must show exactly 3.11.x
  ```
  
  > ⚠️ **Important**: This project specifically requires Python 3.11 due to dependency compatibility. Other versions (including newer ones like 3.13) are not supported.
  
  **Installing Python 3.11:**
  - On macOS (recommended):
    ```bash
    brew install python@3.11
    # Add to your PATH (add to ~/.zshrc or ~/.bash_profile)
    export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"
    ```
  - On Windows: Download Python 3.11.x from [Python.org](https://www.python.org/downloads/)
  - On Linux: Use your package manager to install Python 3.11

- **Rust Toolchain** (Required) - Some Python dependencies require Rust to compile
  ```bash
  # Install Rust (all platforms)
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  
  # Verify Rust installation
  rustc --version  # Should show any recent version
  cargo --version  # Should show any recent version
  ```
  
  > ⚠️ **Note**: If you skip this step, you'll see cryptography-related errors during pip install.
  
  **Platform-specific notes:**
  - On macOS:
    ```bash
    # Can also install via Homebrew
    brew install rust
    ```
  - On Windows: Download the installer from [rustup.rs](https://rustup.rs)
  - On Linux: Most package managers have rust and cargo packages available

- **Node.js 14+** and **npm 6+** - [Download & Install Node.js](https://nodejs.org/)
  ```bash
  # Verify Node.js and npm installation
  node --version     # Should show 14.x or higher
  npm --version      # Should show 6.x or higher
  ```

- **Git** - [Download & Install Git](https://git-scm.com/downloads)
  ```bash
  # Verify Git installation
  git --version      # Should show 2.x or higher
  ```

#### macOS-specific Prerequisites

If using macOS:

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python, Node.js, and Git
brew install python node git

# Important: On macOS, Python is installed as 'python3'
# Verify the installation:
python3 --version
# If you want to use just 'python' command, you can add an alias to your shell:
echo "alias python=python3" >> ~/.zshrc  # for zsh (default in newer macOS)
# OR
echo "alias python=python3" >> ~/.bash_profile  # for bash
```

Let me explain why each part is important:

1. **Homebrew Installation**: This is the package manager for macOS, making it easier to install and manage software
2. **Installing Dependencies**: Using Homebrew to install Python, Node.js, and Git in one command
3. **Python3 Clarification**: This explicitly tells macOS users that they need to use `python3` command
4. **Optional Alias**: This helps users who want to use just `python` instead of `python3`

Would you like me to:
1. Show you exactly where this section should go in the file (line numbers)?
2. Explain any of these parts in more detail?
3. Help you with applying any other sections from our previous suggestions?

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
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

##### 3. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

##### 3b. Initialize the database

```bash
# Create and update the database with all models
python -m alembic upgrade head
```

The database file (app.db) will be created in the project root directory.

##### 4. Install Tailwind CSS

```bash
# Download Tailwind CSS standalone CLI for macOS ARM (M-series)
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64
chmod +x tailwindcss-macos-arm64
mv tailwindcss-macos-arm64 tailwindcss

# Initialize Tailwind configuration
./tailwindcss init
```

##### 5. Initialize and Build CSS

```bash
# Create Tailwind CSS input file
cat > src/static/css/app.css << EOL
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  /* Your custom components here */
}
EOL

# Build CSS (one-time build)
./tailwindcss -i ./src/static/css/app.css -o ./src/static/css/output.css --minify

# Or start the CSS watcher for development
./tailwindcss -i ./src/static/css/app.css -o ./src/static/css/output.css --watch
```

> ⚠️ **Note**: This setup uses the standalone Tailwind CLI, which is perfect for macOS M-series computers and doesn't require Node.js. If you need DaisyUI or other plugins, you'll need to add them to your `tailwind.config.js` file.

### Dependency Verification

This starter kit requires specific versions of key dependencies, all installed locally per project:

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

The project includes a pre-configured `.env` file with sensible defaults for local development. This file is git-ignored for security, but contains all necessary settings for immediate development on your MacMini M4.

Key environment variables include:
- `HOST`: Set to `127.0.0.1` for reliable local development
- `PORT`: Default is `8000`
- `DEBUG`: Set to `True` for development
- `SECRET_KEY`: Pre-generated secure key
- `AUTH_PASSWORD`: Your preferred password for the admin interface
- `DATABASE_URL`: SQLite database path
- `CTK_APPEARANCE`: Desktop UI theme preference

> ⚠️ **Note**: The `.env` file is automatically created during the setup process. If you need to recreate it manually, you can find a backup copy in your personal notes or contact the repository owner.

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

# Start the Tailwind CSS watcher with DaisyUI
npx @tailwindcss/cli -i ./src/static/css/app.css -o ./src/static/css/output.css --watch
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

### Verify All Prerequisites

Run these commands to ensure all required software is properly installed:

```bash
# Python version check
# On macOS:
python3 --version  # Should show 3.8 or higher
# On Windows/Linux:
python --version   # Should show 3.8 or higher

# Node.js and npm check
node --version     # Should show 14.x or higher
npm --version      # Should show 6.x or higher

# Git check
git --version      # Should show 2.x or higher
```

If any of these commands fail or show incorrect versions, please revisit the installation steps for that component.

### Database Configuration

The starter kit uses SQLite with SQLAlchemy ORM, configured for reliability:

##### 3b. Initialize the database

```bash
# Create and update the database with all models
python -m alembic upgrade head
```

The database file (app.db) will be created in the project root directory.

> ⚠️ **Important Database Settings**:
> - Connection timeout: 30 seconds
> - Connection pool size: 5 connections
> - Pool recycling: Every 30 minutes
> - Pre-ping enabled: Yes (verifies connections before use)
> 
> These settings can be adjusted in your `.env` file if needed.