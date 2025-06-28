#!/usr/bin/env python3
"""
Entry point for Hugging Face Spaces
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    # Set environment variables for Streamlit
    os.environ.setdefault("STREAMLIT_SERVER_PORT", "8501")
    os.environ.setdefault("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    
    # Run the Streamlit app
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ]) 