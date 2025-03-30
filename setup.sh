#!/bin/bash
# Setup script for Oz Stack Starter Kit

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Print colored messages
print_success() {
  echo -e "\033[0;32m$1\033[0m"
}

print_info() {
  echo -e "\033[0;34m$1\033[0m"
}

print_warning() {
  echo -e "\033[0;33m$1\033[0m"
}

print_error() {
  echo -e "\033[0;31m$1\033[0m"
}

# Check prerequisites
check_prerequisites() {
  print_info "Checking prerequisites..."
  
  # Check for Python 3.8+
  if ! command_exists python; then
    if command_exists python3; then
      print_info "Python 3 found as 'python3'. Creating alias..."
      alias python=python3
    else
      print_error "Python 3.8+ is required but not found. Please install Python and try again."
      print_info "Visit: https://www.python.org/downloads/"
      exit 1
    fi
  fi
  
  # Check Python version more robustly
  PYTHON_VERSION_OUTPUT=$(python --version 2>&1)
  if [[ "$PYTHON_VERSION_OUTPUT" =~ ([0-9]+)\.([0-9]+)\.([0-9]+) ]]; then
    PYTHON_MAJOR="${BASH_REMATCH[1]}"
    PYTHON_MINOR="${BASH_REMATCH[2]}"
    PYTHON_PATCH="${BASH_REMATCH[3]}"
    PYTHON_VERSION="$PYTHON_MAJOR.$PYTHON_MINOR.$PYTHON_PATCH"
    
    if [[ "$PYTHON_MAJOR" -lt 3 ]] || [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -lt 8 ]]; then
      print_error "Python 3.8+ is required. Found: Python $PYTHON_VERSION"
      print_info "Please upgrade Python and try again."
      exit 1
    else
      print_success "Found Python $PYTHON_VERSION"
    fi
  else
    print_error "Could not determine Python version from output: $PYTHON_VERSION_OUTPUT"
    print_info "Please ensure you have Python 3.8+ installed and try again."
    exit 1
  fi
  
  # Check for pip
  if ! command_exists pip; then
    if command_exists pip3; then
      print_info "pip3 found. Creating alias..."
      alias pip=pip3
    else
      print_error "pip is required but not found. Please install pip and try again."
      exit 1
    fi
  else
    print_success "Found pip"
  fi
  
  # Check for Node.js
  if ! command_exists node; then
    print_error "Node.js is required but not found. Please install Node.js and try again."
    print_info "Visit: https://nodejs.org/"
    exit 1
  else
    NODE_VERSION=$(node --version | cut -c 2-)
    print_success "Found Node.js $NODE_VERSION"
  fi
  
  # Check for npm
  if ! command_exists npm; then
    print_error "npm is required but not found. Please install npm and try again."
    exit 1
  else
    NPM_VERSION=$(npm --version)
    print_success "Found npm $NPM_VERSION"
  fi
  
  print_success "All prerequisites met!"
}

# Create and setup virtual environment
setup_virtual_env() {
  print_info "Creating Python virtual environment..."
  
  # Check if venv already exists
  if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Do you want to recreate it? (y/n)"
    read -r recreate
    if [[ "$recreate" == "y" ]]; then
      print_info "Removing existing virtual environment..."
      rm -rf venv
    else
      print_info "Using existing virtual environment."
      return
    fi
  fi
  
  # Create virtual environment
  python -m venv venv
  
  if [ ! -d "venv" ]; then
    print_error "Failed to create virtual environment. Please check your Python installation."
    exit 1
  fi
  
  print_success "Virtual environment created successfully!"
}

# Install Python dependencies
install_python_deps() {
  print_info "Installing Python dependencies..."
  
  # Activate virtual environment based on OS
  if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # For Git Bash on Windows
    source venv/Scripts/activate
  else
    # For Unix-like systems (Linux, macOS)
    source venv/bin/activate
  fi
  
  # Upgrade pip
  pip install --upgrade pip
  
  # Install dependencies
  pip install -r requirements.txt
  
  if [ $? -ne 0 ]; then
    print_error "Failed to install Python dependencies. See error messages above."
    exit 1
  fi
  
  print_success "Python dependencies installed successfully!"
}

# Install Node.js dependencies
install_node_deps() {
  print_info "Installing Node.js dependencies..."
  
  npm install
  
  if [ $? -ne 0 ]; then
    print_error "Failed to install Node.js dependencies. See error messages above."
    exit 1
  fi
  
  print_info "Verifying dependency versions..."
  node verify-versions.js || {
    print_warning "Version mismatch detected. Attempting to fix..."
    npm run fix-versions
    
    # Verify again after fix attempt
    node verify-versions.js || {
      print_error "Could not fix version issues. Please run 'npm run fix-versions' manually."
      exit 1
    }
  }
  
  print_success "Node.js dependencies installed successfully!"
}

# Build CSS
build_css() {
  print_info "Building CSS..."
  
  npm run build:css
  
  if [ $? -ne 0 ]; then
    print_error "Failed to build CSS. See error messages above."
    exit 1
  fi
  
  print_success "CSS built successfully!"
}

# Create .env file if it doesn't exist
create_env_file() {
  print_info "Checking for .env file..."
  
  if [ ! -f ".env" ]; then
    print_info "Creating .env file with default settings..."
    
    # Generate a secure random key
    RANDOM_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
    
    cat > .env << EOF
# Server settings
HOST=127.0.0.1
PORT=8000
DEBUG=True

# Application settings
APP_NAME="Oz Stack Starter Kit"
APP_VERSION="1.0.0"

# Authentication settings
SECRET_KEY="${RANDOM_KEY}"
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

# Add any other environment variables your app needs
EOF
    
    print_success ".env file created successfully!"
    print_warning "IMPORTANT: Change the default password in .env to a secure one!"
  else
    print_info ".env file already exists. Skipping."
  fi
}

# Main setup function
main() {
  echo "====================================================="
  echo "        Oz Stack Starter Kit - Setup Script          "
  echo "====================================================="
  
  check_prerequisites
  setup_virtual_env
  install_python_deps
  install_node_deps
  build_css
  create_env_file
  
  echo ""
  print_success "Setup complete! 🎉"
  echo ""
  print_info "To start development:"
  echo "1. Activate the virtual environment:"
  
  if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "   source venv/Scripts/activate  # Git Bash"
    echo "   venv\\Scripts\\activate.bat    # Command Prompt"
    echo "   venv\\Scripts\\Activate.ps1    # PowerShell"
  else
    echo "   source venv/bin/activate"
  fi
  
  echo ""
  echo "2. Run the development server:"
  echo "   npm run dev"
  echo ""
  echo "3. In a separate terminal, watch for CSS changes (optional):"
  echo "   npm run watch:css"
  echo ""
  echo "Access your application at: http://localhost:8000"
  echo ""
  echo "For more information, see the README.md file."
  echo "====================================================="
}

# Run the main function
main