#!/usr/bin/env python3
"""
Simple script to run the Pet Breed Classifier locally without Docker
"""

import subprocess
import sys
import os

def install_requirements():
    """Install requirements if not already installed"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def run_streamlit():
    """Run the Streamlit app"""
    print("Starting Streamlit app...")
    try:
        # Set environment variables
        env = os.environ.copy()
        env['STREAMLIT_SERVER_PORT'] = '8501'
        env['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ], env=env)
    except KeyboardInterrupt:
        print("\n🛑 App stopped by user")
    except Exception as e:
        print(f"❌ Failed to run app: {e}")

def main():
    print("🐕 Pet Breed Classifier - Local Runner")
    print("=" * 40)
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ app.py not found! Make sure you're in the correct directory.")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Run the app
    run_streamlit()

if __name__ == "__main__":
    main() 