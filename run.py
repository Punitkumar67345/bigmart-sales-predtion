import subprocess
import time
import sys
import os

def start_servers():
    print("========================================")
    print("🚀 INITIALIZING NEXUS ENGINE 🚀")
    print("========================================")
    
    # 1. Start FastAPI Backend
    print("🟢 Starting Backend Server (FastAPI on Port 8000)...")
    backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"])
    
    # Wait 2 seconds for backend to wake up
    time.sleep(2) 
    
    # 2. Start Streamlit Frontend
    print("🌌 Starting Frontend UI (Streamlit on Port 8501)...")
    frontend = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])
    
    try:
        # Keep both running
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        # If you press Ctrl+C, kill both safely
        print("\n🛑 Shutting down all Nexus systems...")
        backend.terminate()
        frontend.terminate()
        print("✅ System offline.")

if __name__ == "__main__":
    start_servers()