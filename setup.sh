#!/bin/bash
# Setup script for Oz Stack Starter Kit

# Create virtual environment
echo "Creating Python virtual environment..."
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install tailwindcss@latest daisyui@latest

# Build CSS
echo "Building CSS..."
npm run build:css

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To start development:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the development server:"
echo "   npm run dev"
echo ""
echo "3. In a separate terminal, watch for CSS changes (optional):"
echo "   npm run watch:css"
echo ""
echo "Access your application at: http://localhost:8000"