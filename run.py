#!/usr/bin/env python3
"""
Corpus Collection Engine - Main Runner
Run this file to start the application
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import bcrypt
        import jwt
        from PIL import Image
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "data",
        "data/uploads", 
        "data/metadata"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def main():
    print("🏛️ Corpus Collection Engine")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Run the enhanced app
    print("🚀 Starting the application...")
    print("📱 Open your browser to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    main()