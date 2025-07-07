#!/usr/bin/env python3
"""
Startup script for StableAgents Desktop App Generator.
Runs both the API server and frontend server.
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

def print_banner():
    """Print startup banner."""
    print("=" * 60)
    print("🚀 StableAgents Desktop App Generator")
    print("=" * 60)
    print("This will start both the API server and frontend server.")
    print("API Server: http://localhost:8000")
    print("Frontend:   http://localhost:3000")
    print("=" * 60)
    print()

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI and Uvicorn are available")
    except ImportError:
        print("❌ FastAPI or Uvicorn not found")
        print("Please install: pip install fastapi uvicorn")
        return False
    
    try:
        import google.genai
        print("✅ Google Genai is available")
    except ImportError:
        print("❌ Google Genai not found")
        print("Please install: pip install google-genai")
        return False
    
    return True

def start_api_server():
    """Start the API server in a subprocess."""
    print("🔧 Starting API server...")
    
    # Get the path to the API server script
    api_script = Path(__file__).parent / "stableagents" / "api_server.py"
    
    if not api_script.exists():
        print(f"❌ API server script not found: {api_script}")
        return None
    
    try:
        # Start the API server
        api_process = subprocess.Popen([
            sys.executable, str(api_script)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if the process is still running
        if api_process.poll() is None:
            print("✅ API server started successfully")
            return api_process
        else:
            stdout, stderr = api_process.communicate()
            print(f"❌ API server failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return None

def start_frontend_server():
    """Start the frontend server in a subprocess."""
    print("🎨 Starting frontend server...")
    
    # Get the path to the frontend server script
    frontend_script = Path(__file__).parent / "frontend" / "server.py"
    
    if not frontend_script.exists():
        print(f"❌ Frontend server script not found: {frontend_script}")
        return None
    
    try:
        # Start the frontend server
        frontend_process = subprocess.Popen([
            sys.executable, str(frontend_script)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Check if the process is still running
        if frontend_process.poll() is None:
            print("✅ Frontend server started successfully")
            return frontend_process
        else:
            stdout, stderr = frontend_process.communicate()
            print(f"❌ Frontend server failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting frontend server: {e}")
        return None

def cleanup(api_process, frontend_process):
    """Clean up processes on exit."""
    print("\n🛑 Shutting down servers...")
    
    if api_process:
        api_process.terminate()
        try:
            api_process.wait(timeout=5)
            print("✅ API server stopped")
        except subprocess.TimeoutExpired:
            api_process.kill()
            print("⚠️  API server force killed")
    
    if frontend_process:
        frontend_process.terminate()
        try:
            frontend_process.wait(timeout=5)
            print("✅ Frontend server stopped")
        except subprocess.TimeoutExpired:
            frontend_process.kill()
            print("⚠️  Frontend server force killed")

def main():
    """Main function."""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        sys.exit(1)
    
    api_process = None
    frontend_process = None
    
    try:
        # Start API server
        api_process = start_api_server()
        if not api_process:
            print("\n❌ Failed to start API server. Exiting.")
            sys.exit(1)
        
        # Start frontend server
        frontend_process = start_frontend_server()
        if not frontend_process:
            print("\n❌ Failed to start frontend server. Exiting.")
            cleanup(api_process, None)
            sys.exit(1)
        
        print("\n🎉 Both servers started successfully!")
        print("📱 Open your browser and go to: http://localhost:3000")
        print("🔗 API documentation: http://localhost:8000/docs")
        print("⏹️  Press Ctrl+C to stop both servers")
        print()
        
        # Keep the main process running
        while True:
            time.sleep(1)
            
            # Check if either process has died
            if api_process.poll() is not None:
                print("❌ API server has stopped unexpectedly")
                break
            
            if frontend_process.poll() is not None:
                print("❌ Frontend server has stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Shutting down by user request...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        cleanup(api_process, frontend_process)
        print("👋 Goodbye!")

if __name__ == "__main__":
    main() 