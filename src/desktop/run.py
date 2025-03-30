#!/usr/bin/env python3
"""
Convenient script for running the desktop application
"""

import os
import sys
from pathlib import Path
import subprocess

# Add parent directory to path so we can import our own modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.append(str(parent_dir))

if __name__ == "__main__":
    # Set desktop mode environment variable
    os.environ["DESKTOP_MODE"] = "True"
    
    # Run the main module
    try:
        from src.main import app_name, app_version
        print(f"Starting {app_name} v{app_version} in desktop mode...")
        
        # Import and run the desktop app
        from src.desktop.app import run_desktop_app
        run_desktop_app()
    except ImportError as e:
        print(f"Error: {str(e)}")
        print("Make sure customtkinter is installed: pip install customtkinter")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting desktop application: {str(e)}")
        sys.exit(1)