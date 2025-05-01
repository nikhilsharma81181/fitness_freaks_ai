#!/usr/bin/env python
"""
Setup script for Fitness Coach AI project.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 13):
        print("Error: Python 3.13 or higher is required")
        sys.exit(1)


def check_uv_installed():
    """Check if uv package manager is installed."""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, text=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def setup_virtual_env():
    """Set up a virtual environment using uv."""
    print("Setting up virtual environment...")
    subprocess.run(["uv", "venv"], check=True)
    
    if os.name == 'nt':  # Windows
        activate_script = ".venv\\Scripts\\activate"
    else:  # Unix/MacOS
        activate_script = ".venv/bin/activate"
    
    print(f"\nTo activate the virtual environment, run:\n    {activate_script}")


def install_dependencies():
    """Install the project dependencies using uv."""
    print("Installing dependencies...")
    subprocess.run(["uv", "pip", "install", "-e", "."], check=True)


def setup_env_file():
    """Set up the .env file from the template if it doesn't exist."""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("Created .env file from .env.example template.")
            print("Please edit .env to add your API keys.")
        else:
            print("Warning: .env.example not found, could not create .env file.")
    else:
        print(".env file already exists.")


def create_data_dirs():
    """Create data directories if they don't exist."""
    data_dirs = ["data/exercises", "data/nutrition"]
    for dir_path in data_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("Created data directories.")


def main():
    """Main setup function."""
    print("Setting up Fitness Coach AI project...")
    
    # Check Python version
    check_python_version()
    
    # Check if uv is installed
    if not check_uv_installed():
        print("Error: uv package manager is not installed.")
        print("Please install uv by following the instructions at: https://github.com/astral-sh/uv")
        sys.exit(1)
    
    # Set up virtual environment
    setup_virtual_env()
    
    # Install dependencies
    install_dependencies()
    
    # Set up .env file
    setup_env_file()
    
    # Create data directories
    create_data_dirs()
    
    print("\nSetup complete!")
    print("\nTo start the application, run:")
    print("    python -m src.main")


if __name__ == "__main__":
    main()