# Oz Stack Quick Start Guide

This guide will help you get up and running with the Oz Stack Starter Kit in under 5 minutes.

## Prerequisites

Ensure you have:
- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

## Quick Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/oz-stack-starterkit.git
cd oz-stack-starterkit
```

### Step 2: Run the setup script

```bash
# For macOS/Linux:
chmod +x setup.sh
./setup.sh

# For Windows (Git Bash):
bash setup.sh
```

The setup script will:
1. Check prerequisites
2. Create a Python virtual environment
3. Install Python dependencies
4. Install Node.js dependencies
5. Build the CSS
6. Create a default .env file

### Step 3: Start the development server

```bash
# Activate the virtual environment if not already activated
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Start the server
npm run dev
```

### Step 4: View your application

Open your browser and go to:
```
http://localhost:8000
```

## What's Included

- **Home page**: A simple page with HTMX and Hyperscript examples
- **Demo page**: Shows API integration with HTMX
- **API endpoints**: Sample REST API with JSON and HTML responses

## Next Steps

1. Modify `src/templates/index.html` to change the home page
2. Add new routes in `src/main.py`
3. Create new API endpoints in `src/api.py`
4. Add new components in `src/templates/components/`

## Need More Information?

Refer to the full [README.md](README.md) for detailed documentation, including:

- Complete project structure explanation
- Detailed setup instructions
- Development workflow
- Troubleshooting
- Deployment guides

## Quick Command Reference

```bash
# Start development server
npm run dev

# Watch for CSS changes
npm run watch:css

# Build CSS
npm run build:css

# Clean project (remove venv, node_modules, output.css)
npm run clean

# Reinstall everything
npm run reinstall
```