#!/usr/bin/env python3
"""
Main Process - StableAgents Desktop App Generator

This is the main process that handles:
- API server management
- Renderer process management
- Inter-process communication
- System-level operations
"""

import os
import sys
import time
import signal
import subprocess
import threading
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import multiprocessing as mp

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MainProcess')

class MainProcess:
    """Main process manager for the desktop app generator."""
    
    def __init__(self):
        self.api_process: Optional[subprocess.Popen] = None
        self.renderer_process: Optional[subprocess.Popen] = None
        self.frontend_process: Optional[subprocess.Popen] = None
        self.running = False
        self.processes = {}
        
        # IPC communication
        self.ipc_queue = mp.Queue()
        self.message_handlers = {
            'start_api': self._handle_start_api,
            'stop_api': self._handle_stop_api,
            'restart_api': self._handle_restart_api,
            'start_renderer': self._handle_start_renderer,
            'stop_renderer': self._handle_stop_renderer,
            'restart_renderer': self._handle_restart_renderer,
            'get_status': self._handle_get_status,
            'create_app': self._handle_create_app,
            'list_projects': self._handle_list_projects,
            'run_project': self._handle_run_project,
        }
    
    def start(self):
        """Start the main process and all sub-processes."""
        logger.info("🚀 Starting Main Process...")
        self.running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            # Start API server
            self._start_api_server()
            
            # Start frontend server
            self._start_frontend_server()
            
            # Start renderer process
            self._start_renderer_process()
            
            # Start IPC message handler
            self._start_ipc_handler()
            
            logger.info("✅ Main process started successfully")
            logger.info("📱 Renderer process should open automatically")
            logger.info("🔗 API server running on http://localhost:8000")
            logger.info("🌐 Frontend server running on http://localhost:3000")
            
            # Keep main process running
            self._main_loop()
            
        except Exception as e:
            logger.error(f"❌ Error starting main process: {e}")
            self.shutdown()
    
    def _start_api_server(self):
        """Start the API server process."""
        logger.info("🔧 Starting API server...")
        
        api_script = Path(__file__).parent / "stableagents" / "api_server.py"
        if not api_script.exists():
            raise FileNotFoundError(f"API server script not found: {api_script}")
        
        try:
            self.api_process = subprocess.Popen([
                sys.executable, str(api_script)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for API server to start
            time.sleep(3)
            
            if self.api_process.poll() is None:
                logger.info("✅ API server started successfully")
                self.processes['api'] = self.api_process
            else:
                stdout, stderr = self.api_process.communicate()
                raise RuntimeError(f"API server failed to start: {stderr}")
                
        except Exception as e:
            logger.error(f"❌ Failed to start API server: {e}")
            raise
    
    def _start_frontend_server(self):
        """Start the frontend server process."""
        logger.info("🌐 Starting frontend server...")
        
        frontend_script = Path(__file__).parent / "frontend" / "server.py"
        if not frontend_script.exists():
            raise FileNotFoundError(f"Frontend server script not found: {frontend_script}")
        
        try:
            self.frontend_process = subprocess.Popen([
                sys.executable, str(frontend_script)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for frontend server to start
            time.sleep(2)
            
            if self.frontend_process.poll() is None:
                logger.info("✅ Frontend server started successfully")
                self.processes['frontend'] = self.frontend_process
            else:
                stdout, stderr = self.frontend_process.communicate()
                raise RuntimeError(f"Frontend server failed to start: {stderr}")
                
        except Exception as e:
            logger.error(f"❌ Failed to start frontend server: {e}")
            raise
    
    def _start_renderer_process(self):
        """Start the renderer process (Electron-like window)."""
        logger.info("🖥️ Starting renderer process...")
        
        renderer_script = Path(__file__).parent / "renderer_process.py"
        if not renderer_script.exists():
            raise FileNotFoundError(f"Renderer script not found: {renderer_script}")
        
        try:
            # Pass IPC queue to renderer process
            env = os.environ.copy()
            env['STABLEAGENTS_IPC_QUEUE'] = str(self.ipc_queue)
            
            self.renderer_process = subprocess.Popen([
                sys.executable, str(renderer_script)
            ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for renderer process to start
            time.sleep(2)
            
            if self.renderer_process.poll() is None:
                logger.info("✅ Renderer process started successfully")
                self.processes['renderer'] = self.renderer_process
            else:
                stdout, stderr = self.renderer_process.communicate()
                raise RuntimeError(f"Renderer process failed to start: {stderr}")
                
        except Exception as e:
            logger.error(f"❌ Failed to start renderer process: {e}")
            raise
    
    def _start_ipc_handler(self):
        """Start the IPC message handler thread."""
        logger.info("📡 Starting IPC message handler...")
        
        def ipc_handler():
            while self.running:
                try:
                    # Check for messages from renderer process
                    if not self.ipc_queue.empty():
                        message = self.ipc_queue.get_nowait()
                        self._handle_ipc_message(message)
                    time.sleep(0.1)
                except Exception as e:
                    logger.error(f"Error in IPC handler: {e}")
        
        ipc_thread = threading.Thread(target=ipc_handler, daemon=True)
        ipc_thread.start()
        logger.info("✅ IPC message handler started")
    
    def _handle_ipc_message(self, message: Dict[str, Any]):
        """Handle IPC messages from renderer process."""
        try:
            msg_type = message.get('type')
            handler = self.message_handlers.get(msg_type)
            
            if handler:
                response = handler(message)
                # Send response back to renderer if needed
                if 'response_queue' in message:
                    response_queue = message['response_queue']
                    response_queue.put(response)
            else:
                logger.warning(f"Unknown message type: {msg_type}")
                
        except Exception as e:
            logger.error(f"Error handling IPC message: {e}")
    
    def _handle_start_api(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle start API request."""
        try:
            if self.api_process and self.api_process.poll() is None:
                return {'success': True, 'message': 'API server already running'}
            
            self._start_api_server()
            return {'success': True, 'message': 'API server started'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_stop_api(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle stop API request."""
        try:
            if self.api_process:
                self.api_process.terminate()
                self.api_process.wait(timeout=5)
                self.api_process = None
                return {'success': True, 'message': 'API server stopped'}
            return {'success': True, 'message': 'API server not running'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_restart_api(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle restart API request."""
        try:
            self._handle_stop_api({})
            time.sleep(1)
            self._handle_start_api({})
            return {'success': True, 'message': 'API server restarted'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_start_renderer(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle start renderer request."""
        try:
            if self.renderer_process and self.renderer_process.poll() is None:
                return {'success': True, 'message': 'Renderer already running'}
            
            self._start_renderer_process()
            return {'success': True, 'message': 'Renderer started'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_stop_renderer(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle stop renderer request."""
        try:
            if self.renderer_process:
                self.renderer_process.terminate()
                self.renderer_process.wait(timeout=5)
                self.renderer_process = None
                return {'success': True, 'message': 'Renderer stopped'}
            return {'success': True, 'message': 'Renderer not running'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_restart_renderer(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle restart renderer request."""
        try:
            self._handle_stop_renderer({})
            time.sleep(1)
            self._handle_start_renderer({})
            return {'success': True, 'message': 'Renderer restarted'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_get_status(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get status request."""
        status = {
            'api_server': {
                'running': self.api_process and self.api_process.poll() is None,
                'pid': self.api_process.pid if self.api_process else None
            },
            'frontend_server': {
                'running': self.frontend_process and self.frontend_process.poll() is None,
                'pid': self.frontend_process.pid if self.frontend_process else None
            },
            'renderer': {
                'running': self.renderer_process and self.renderer_process.poll() is None,
                'pid': self.renderer_process.pid if self.renderer_process else None
            }
        }
        return {'success': True, 'status': status}
    
    def _handle_create_app(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create app request."""
        try:
            # This would integrate with the existing desktop generator
            # For now, return a placeholder response
            return {
                'success': True, 
                'message': 'App creation request received',
                'data': message.get('data', {})
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_list_projects(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list projects request."""
        try:
            # This would integrate with the existing project management
            projects_dir = Path("stable_desktop_projects")
            if projects_dir.exists():
                projects = [p.name for p in projects_dir.iterdir() if p.is_dir()]
                return {'success': True, 'projects': projects}
            return {'success': True, 'projects': []}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _handle_run_project(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle run project request."""
        try:
            project_name = message.get('project_name')
            if not project_name:
                return {'success': False, 'error': 'Project name required'}
            
            # This would integrate with the existing project runner
            return {
                'success': True, 
                'message': f'Project {project_name} started',
                'project_name': project_name
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _main_loop(self):
        """Main process loop."""
        logger.info("🔄 Main process loop started")
        
        while self.running:
            try:
                # Check if any processes have died
                for name, process in self.processes.items():
                    if process and process.poll() is not None:
                        logger.warning(f"⚠️ {name} process has died")
                        # Could restart the process here if needed
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("🛑 Received interrupt signal")
                break
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}")
                break
        
        self.shutdown()
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown."""
        logger.info(f"📡 Received signal {signum}")
        self.shutdown()
    
    def shutdown(self):
        """Shutdown all processes gracefully."""
        logger.info("🛑 Shutting down main process...")
        self.running = False
        
        # Shutdown processes in reverse order
        processes_to_shutdown = [
            ('renderer', self.renderer_process),
            ('frontend', self.frontend_process),
            ('api', self.api_process)
        ]
        
        for name, process in processes_to_shutdown:
            if process:
                logger.info(f"🛑 Stopping {name} process...")
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    logger.info(f"✅ {name} process stopped")
                except subprocess.TimeoutExpired:
                    logger.warning(f"⚠️ Force killing {name} process")
                    process.kill()
                except Exception as e:
                    logger.error(f"❌ Error stopping {name} process: {e}")
        
        logger.info("👋 Main process shutdown complete")

def main():
    """Main entry point."""
    print("🚀 StableAgents Desktop App Generator - Main Process")
    print("=" * 60)
    
    # Check dependencies
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI and Uvicorn available")
    except ImportError:
        print("❌ FastAPI or Uvicorn not found")
        print("Please install: pip install fastapi uvicorn")
        sys.exit(1)
    
    try:
        import google.genai
        print("✅ Google Genai available")
    except ImportError:
        print("❌ Google Genai not found")
        print("Please install: pip install google-genai")
        sys.exit(1)
    
    # Start main process
    main_process = MainProcess()
    main_process.start()

if __name__ == "__main__":
    main() 