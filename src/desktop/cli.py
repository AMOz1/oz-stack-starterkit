#!/usr/bin/env python3
"""
Command-line interface for launching the desktop application
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import our own modules
parent_dir = Path(__file__).parent.parent.parent
sys.path.append(str(parent_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("oz-stack.desktop.cli")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Oz Stack Desktop Application")
    
    parser.add_argument(
        "--version", action="store_true", help="Show version information and exit"
    )
    
    parser.add_argument(
        "--theme", type=str, choices=["light", "dark", "system"],
        default="system", help="Set the application theme"
    )
    
    parser.add_argument(
        "--color", type=str, choices=["blue", "green", "dark-blue"],
        default="blue", help="Set the application color scheme"
    )
    
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    if args.version:
        from src.desktop.app import APP_NAME, APP_VERSION
        print(f"{APP_NAME} v{APP_VERSION}")
        return 0
    
    # Set environment variables for CustomTkinter appearance
    os.environ["CTK_APPEARANCE"] = args.theme.capitalize()
    os.environ["CTK_THEME"] = args.color
    
    # Import and run the desktop app
    try:
        logger.info("Launching desktop application...")
        from src.desktop.app import run_desktop_app
        run_desktop_app()
        return 0
    except Exception as e:
        logger.error(f"Error running desktop application: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())