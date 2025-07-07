#!/usr/bin/env python3
"""
Multi-Process Startup Script - StableAgents Desktop App Generator

This script starts the multi-process architecture with:
- Main Process: Manages API server and renderer process
- Renderer Process: Handles UI and user interactions
- API Server: Handles AI generation and desktop app creation
- Frontend Server: Serves the web interface
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path

def print_banner():
    """Print startup banner."""
    print("=" * 70)
    print("🚀 StableAgents Desktop App Generator - Multi-Process Architecture")
    print("=" * 70)
    print("This will start the multi-process architecture:")
    print("• Main Process: Manages all sub-processes and IPC")
    print("• Renderer Process: Handles UI and user interactions")
    print("• API Server: Handles AI generation and app creation")
    print("• Frontend Server: Serves the web interface")
    print("=" * 70)
    print()

def check_dependencies():
    """Check if required dependencies are installed."""
    dependencies = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('google.genai', 'Google Genai'),
        ('requests', 'Requests'),
    ]
    
    optional_dependencies = [
        ('webview', 'PyWebView (optional - for native window)'),
    ]
    
    print("🔍 Checking dependencies...")
    
    # Check required dependencies
    missing_required = []
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"✅ {name} available")
        except ImportError:
            print(f"❌ {name} not found")
            missing_required.append(name)
    
    # Check optional dependencies
    for module, name in optional_dependencies:
        try:
            __import__(module)
            print(f"✅ {name} available")
        except ImportError:
            print(f"⚠️  {name} not found (will use browser fallback)")
    
    if missing_required:
        print(f"\n❌ Missing required dependencies: {', '.join(missing_required)}")
        print("Please install: pip install fastapi uvicorn google-genai requests")
        return False
    
    return True

def check_files():
    """Check if required files exist."""
    required_files = [
        'main_process.py',
        'renderer_process.py',
        'stableagents/api_server.py',
        'frontend/server.py',
        'frontend/index.html',
        'frontend/js/app.js',
    ]
    
    print("\n📁 Checking required files...")
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    return True

def start_multi_process():
    """Start the multi-process architecture."""
    print("🚀 Starting multi-process architecture...")
    
    # Get the path to the main process script
    main_script = Path(__file__).parent / "main_process.py"
    
    if not main_script.exists():
        print(f"❌ Main process script not found: {main_script}")
        return False
    
    try:
        # Start the main process
        print("🔧 Launching main process...")
        process = subprocess.Popen([
            sys.executable, str(main_script)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("✅ Main process launched successfully")
        print("📱 Renderer process should open automatically")
        print("🔗 API server will be available at: http://localhost:8000")
        print("🌐 Frontend will be available at: http://localhost:3000")
        print("\n⏹️  Press Ctrl+C to stop all processes")
        
        # Monitor the process
        try:
            while True:
                # Check if process is still running
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    print(f"\n❌ Main process has stopped")
                    if stdout:
                        print(f"STDOUT: {stdout}")
                    if stderr:
                        print(f"STDERR: {stderr}")
                    break
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down by user request...")
            process.terminate()
            try:
                process.wait(timeout=10)
                print("✅ All processes stopped gracefully")
            except subprocess.TimeoutExpired:
                print("⚠️  Force killing processes...")
                process.kill()
                process.wait()
                print("✅ All processes stopped")
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting multi-process architecture: {e}")
        return False

def show_architecture_info():
    """Show information about the multi-process architecture."""
    print("\n🏗️ Multi-Process Architecture Overview")
    print("=" * 50)
    print()
    print("📋 Process Structure:")
    print("┌─────────────────────────────────────────────────┐")
    print("│                Main Process                     │")
    print("│  ┌─────────────┐  ┌─────────────┐              │")
    print("│  │ API Server  │  │ Frontend    │              │")
    print("│  │ Process     │  │ Server      │              │")
    print("│  │             │  │ Process     │              │")
    print("│  └─────────────┘  └─────────────┘              │")
    print("│         │                │                      │")
    print("│         └────────┬───────┘                      │")
    print("│                  │                              │")
    print("│         ┌────────▼────────┐                     │")
    print("│         │   Renderer      │                     │")
    print("│         │   Process       │                     │")
    print("│         │   (UI/Web)      │                     │")
    print("│         └─────────────────┘                     │")
    print("└─────────────────────────────────────────────────┘")
    print()
    print("🔗 Communication:")
    print("• Main ↔ Renderer: IPC (Inter-Process Communication)")
    print("• Renderer ↔ Frontend: HTTP (Web interface)")
    print("• Frontend ↔ API: HTTP (REST API)")
    print()
    print("🎯 Benefits:")
    print("• Isolation: UI crashes don't affect backend")
    print("• Scalability: Easy to add new processes")
    print("• Security: Sandboxed renderer process")
    print("• Reliability: Automatic process monitoring")
    print("• Flexibility: Can restart individual processes")
    print()

def show_usage():
    """Show usage information."""
    print("\n📖 Usage Information")
    print("=" * 30)
    print()
    print("🚀 Quick Start:")
    print("  python start_multi_process.py")
    print()
    print("🔧 Development Mode:")
    print("  # Start main process only")
    print("  python main_process.py")
    print()
    print("  # Start renderer process only (for testing)")
    print("  python renderer_process.py")
    print()
    print("🌐 Access Points:")
    print("  • Web Interface: http://localhost:3000")
    print("  • API Documentation: http://localhost:8000/docs")
    print("  • API Health Check: http://localhost:8000/health")
    print()
    print("🛠️ Troubleshooting:")
    print("  • Check logs for each process")
    print("  • Verify all dependencies are installed")
    print("  • Ensure ports 8000 and 3000 are available")
    print("  • Check firewall settings")
    print()

def main():
    """Main function."""
    print_banner()
    
    # Show architecture info
    show_architecture_info()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        sys.exit(1)
    
    # Check files
    if not check_files():
        print("\n❌ Please ensure all required files are present.")
        sys.exit(1)
    
    # Show usage info
    show_usage()
    
    # Ask user if they want to continue
    try:
        response = input("🚀 Start the multi-process architecture? (y/n): ").strip().lower()
        if response not in ['y', 'yes']:
            print("👋 Goodbye!")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    # Start the multi-process architecture
    success = start_multi_process()
    
    if success:
        print("\n🎉 Multi-process architecture completed successfully!")
    else:
        print("\n❌ Multi-process architecture failed to start properly.")
        sys.exit(1)

if __name__ == "__main__":
    main() 