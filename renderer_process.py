#!/usr/bin/env python3
"""
Renderer Process - StableAgents Desktop App Generator

This is the renderer process that handles:
- User interface (web-based or native)
- Communication with main process via IPC
- User interactions and app generation requests
"""

import os
import sys
import time
import json
import logging
import threading
import webbrowser
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import multiprocessing as mp

# Try to import webview for native window
try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("⚠️  webview not available, will use browser instead")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('RendererProcess')

class RendererProcess:
    """Renderer process for the desktop app generator."""
    
    def __init__(self):
        self.main_process_queue: Optional[mp.Queue] = None
        self.response_queue: Optional[mp.Queue] = None
        self.running = False
        self.window = None
        self.frontend_url = "http://localhost:3000"
        
        # IPC message handlers
        self.message_handlers = {
            'status_update': self._handle_status_update,
            'app_created': self._handle_app_created,
            'error_occurred': self._handle_error,
            'project_list': self._handle_project_list,
        }
    
    def start(self):
        """Start the renderer process."""
        logger.info("🖥️ Starting Renderer Process...")
        self.running = True
        
        try:
            # Set up IPC communication
            self._setup_ipc()
            
            # Wait for frontend server to be ready
            self._wait_for_frontend()
            
            # Start the UI
            self._start_ui()
            
            # Start IPC message handler
            self._start_ipc_handler()
            
            logger.info("✅ Renderer process started successfully")
            
            # Keep renderer process running
            self._main_loop()
            
        except Exception as e:
            logger.error(f"❌ Error starting renderer process: {e}")
            self.shutdown()
    
    def _setup_ipc(self):
        """Set up IPC communication with main process."""
        try:
            # Get IPC queue from environment (set by main process)
            queue_str = os.environ.get('STABLEAGENTS_IPC_QUEUE')
            if queue_str:
                # In a real implementation, you'd need to properly serialize/deserialize the queue
                # For now, we'll use a simple approach
                logger.info("📡 IPC queue reference received from main process")
            
            # Create our own response queue
            self.response_queue = mp.Queue()
            logger.info("✅ IPC communication set up")
            
        except Exception as e:
            logger.error(f"❌ Failed to set up IPC: {e}")
            raise
    
    def _wait_for_frontend(self):
        """Wait for the frontend server to be ready."""
        logger.info("⏳ Waiting for frontend server...")
        
        import requests
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(self.frontend_url, timeout=2)
                if response.status_code == 200:
                    logger.info("✅ Frontend server is ready")
                    return
            except requests.exceptions.RequestException:
                pass
            
            attempt += 1
            time.sleep(1)
        
        raise TimeoutError("Frontend server did not become ready in time")
    
    def _start_ui(self):
        """Start the user interface."""
        if WEBVIEW_AVAILABLE:
            self._start_native_window()
        else:
            self._start_browser_window()
    
    def _start_native_window(self):
        """Start a native window using webview."""
        logger.info("🪟 Starting native window with webview...")
        
        try:
            # Create the webview window
            self.window = webview.create_window(
                title="StableAgents Desktop App Generator",
                url=self.frontend_url,
                width=1200,
                height=800,
                resizable=True,
                text_select=True,
                confirm_close=True
            )
            
            # Start webview in a separate thread
            def run_webview():
                webview.start(debug=True)
            
            webview_thread = threading.Thread(target=run_webview, daemon=True)
            webview_thread.start()
            
            logger.info("✅ Native window started")
            
        except Exception as e:
            logger.error(f"❌ Failed to start native window: {e}")
            logger.info("🔄 Falling back to browser window...")
            self._start_browser_window()
    
    def _start_browser_window(self):
        """Start the UI in a browser window."""
        logger.info("🌐 Opening browser window...")
        
        try:
            # Open the frontend URL in the default browser
            webbrowser.open(self.frontend_url)
            logger.info("✅ Browser window opened")
            
        except Exception as e:
            logger.error(f"❌ Failed to open browser: {e}")
            raise
    
    def _start_ipc_handler(self):
        """Start the IPC message handler thread."""
        logger.info("📡 Starting IPC message handler...")
        
        def ipc_handler():
            while self.running:
                try:
                    # Check for messages from main process
                    if self.response_queue and not self.response_queue.empty():
                        message = self.response_queue.get_nowait()
                        self._handle_ipc_message(message)
                    time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error in IPC handler: {e}")
        
        ipc_thread = threading.Thread(target=ipc_handler, daemon=True)
        ipc_thread.start()
        logger.info("✅ IPC message handler started")
    
    def _handle_ipc_message(self, message: Dict[str, Any]):
        """Handle IPC messages from main process."""
        try:
            msg_type = message.get('type')
            handler = self.message_handlers.get(msg_type)
            
            if handler:
                handler(message)
            else:
                logger.warning(f"Unknown message type: {msg_type}")
                
        except Exception as e:
            logger.error(f"Error handling IPC message: {e}")
    
    def _handle_status_update(self, message: Dict[str, Any]):
        """Handle status update from main process."""
        try:
            status = message.get('status', {})
            logger.info(f"📊 Status update: {status}")
            
            # Could update UI here if needed
            # For now, just log the status
            
        except Exception as e:
            logger.error(f"Error handling status update: {e}")
    
    def _handle_app_created(self, message: Dict[str, Any]):
        """Handle app creation success."""
        try:
            app_data = message.get('data', {})
            logger.info(f"🎉 App created successfully: {app_data}")
            
            # Could show notification or update UI here
            
        except Exception as e:
            logger.error(f"Error handling app created: {e}")
    
    def _handle_error(self, message: Dict[str, Any]):
        """Handle error from main process."""
        try:
            error = message.get('error', 'Unknown error')
            logger.error(f"❌ Error from main process: {error}")
            
            # Could show error notification here
            
        except Exception as e:
            logger.error(f"Error handling error message: {e}")
    
    def _handle_project_list(self, message: Dict[str, Any]):
        """Handle project list from main process."""
        try:
            projects = message.get('projects', [])
            logger.info(f"📁 Project list received: {len(projects)} projects")
            
            # Could update UI with project list here
            
        except Exception as e:
            logger.error(f"Error handling project list: {e}")
    
    def send_to_main(self, message_type: str, data: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Send message to main process and wait for response."""
        try:
            if not self.main_process_queue:
                logger.warning("No IPC queue available")
                return None
            
            message = {
                'type': message_type,
                'data': data or {},
                'response_queue': self.response_queue
            }
            
            self.main_process_queue.put(message)
            
            # Wait for response
            if self.response_queue:
                try:
                    response = self.response_queue.get(timeout=5)
                    return response
                except:
                    logger.warning("No response received from main process")
                    return None
            
        except Exception as e:
            logger.error(f"Error sending message to main process: {e}")
            return None
    
    def _main_loop(self):
        """Main renderer process loop."""
        logger.info("🔄 Renderer process loop started")
        
        while self.running:
            try:
                # Check if window is still open (for webview)
                if self.window and hasattr(self.window, 'closed'):
                    if self.window.closed:
                        logger.info("🪟 Window closed by user")
                        break
                
                # Send periodic status requests
                if time.time() % 30 < 1:  # Every 30 seconds
                    self.send_to_main('get_status')
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("🛑 Received interrupt signal")
                break
            except Exception as e:
                logger.error(f"❌ Error in renderer loop: {e}")
                break
        
        self.shutdown()
    
    def shutdown(self):
        """Shutdown the renderer process."""
        logger.info("🛑 Shutting down renderer process...")
        self.running = False
        
        # Close window if using webview
        if self.window and hasattr(self.window, 'destroy'):
            try:
                self.window.destroy()
                logger.info("✅ Window closed")
            except Exception as e:
                logger.error(f"❌ Error closing window: {e}")
        
        logger.info("👋 Renderer process shutdown complete")

class WebViewBridge:
    """Bridge for communication between webview and Python."""
    
    def __init__(self, renderer: RendererProcess):
        self.renderer = renderer
    
    def send_message(self, message_type: str, data: Dict[str, Any] = None):
        """Send message from webview to main process."""
        return self.renderer.send_to_main(message_type, data)
    
    def get_status(self):
        """Get current status from main process."""
        return self.renderer.send_to_main('get_status')
    
    def create_app(self, description: str, app_name: str = None, framework: str = "customtkinter"):
        """Create a desktop app."""
        data = {
            'description': description,
            'app_name': app_name,
            'framework': framework
        }
        return self.renderer.send_to_main('create_app', data)
    
    def list_projects(self):
        """List all projects."""
        return self.renderer.send_to_main('list_projects')
    
    def run_project(self, project_name: str):
        """Run a specific project."""
        data = {'project_name': project_name}
        return self.renderer.send_to_main('run_project', data)

def main():
    """Main entry point for renderer process."""
    print("🖥️ StableAgents Desktop App Generator - Renderer Process")
    print("=" * 60)
    
    # Check if we're running as a subprocess
    if 'STABLEAGENTS_IPC_QUEUE' not in os.environ:
        print("⚠️  This script should be started by the main process")
        print("💡 Run: python main_process.py")
        sys.exit(1)
    
    # Start renderer process
    renderer = RendererProcess()
    renderer.start()

if __name__ == "__main__":
    main() 