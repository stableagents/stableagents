import os
import subprocess
import platform
import webbrowser
import logging
import shutil
import time
import re
import json
import psutil
import tempfile
from typing import List, Dict, Any, Optional, Union

# Try to import advanced automation libraries
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

class ComputerControl:
    """Enhanced module for controlling computer actions and building desktop applications."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.os_type = platform.system().lower()
        self.registered_actions = {
            # Basic operations
            "open": self.open_application,
            "browse": self.browse_web,
            "search": self.search_web,
            "create": self.create_file_or_folder,
            "list": self.list_directory,
            "find": self.find_files,
            "move": self.move_file,
            "copy": self.copy_file,
            "delete": self.delete_file,
            "execute": self.execute_command,
            "type": self.type_text,
            "screenshot": self.take_screenshot,
            
            # Advanced operations
            "click": self.mouse_click,
            "drag": self.mouse_drag,
            "scroll": self.mouse_scroll,
            "key": self.keyboard_input,
            "window": self.window_control,
            "monitor": self.system_monitor,
            "process": self.process_control,
            "build": self.build_application,
            "gui": self.gui_automation,
            "network": self.network_operations,
            "database": self.database_operations
        }
        
        # Initialize pyautogui if available
        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1
        
    def parse_command(self, command: str) -> Dict[str, Any]:
        """Parse a natural language command into actionable parts."""
        command = command.strip().lower()
        
        # Basic parsing - this could be enhanced with NLP
        for action_key in self.registered_actions.keys():
            if command.startswith(action_key):
                return {
                    "action": action_key,
                    "params": command[len(action_key):].strip()
                }
        
        # If no matching action is found, use a simple heuristic
        words = command.split()
        if words:
            potential_action = words[0]
            closest_action = self._find_closest_action(potential_action)
            return {
                "action": closest_action,
                "params": command[len(words[0]):].strip()
            }
        
        return {"action": None, "params": command}
    
    def _find_closest_action(self, action: str) -> str:
        """Find the closest matching registered action."""
        actions = list(self.registered_actions.keys())
        if action in actions:
            return action
        
        # Simple string similarity
        for registered_action in actions:
            if action in registered_action or registered_action in action:
                return registered_action
        
        # Default to execute for unrecognized commands
        return "execute"
    
    def execute(self, command: str) -> str:
        """Execute a natural language command."""
        parsed = self.parse_command(command)
        action = parsed.get("action")
        params = parsed.get("params", "")
        
        if not action or action not in self.registered_actions:
            return f"Unknown action: {command}"
        
        try:
            result = self.registered_actions[action](params)
            return result
        except Exception as e:
            self.logger.error(f"Error executing command '{command}': {str(e)}")
            return f"Error: {str(e)}"
    
    def open_application(self, app_name: str) -> str:
        """Open an application by name."""
        app_name = app_name.strip()
        
        if self.os_type == "darwin":  # macOS
            try:
                subprocess.Popen(["open", "-a", app_name])
                return f"Opened {app_name}"
            except Exception:
                # Try alternative methods
                try:
                    subprocess.Popen(["osascript", "-e", f'tell application "{app_name}" to activate'])
                    return f"Activated {app_name}"
                except Exception as e:
                    return f"Failed to open {app_name}: {str(e)}"
                
        elif self.os_type == "windows":
            try:
                subprocess.Popen([app_name], shell=True)
                return f"Opened {app_name}"
            except Exception as e:
                return f"Failed to open {app_name}: {str(e)}"
                
        elif self.os_type == "linux":
            try:
                subprocess.Popen([app_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return f"Opened {app_name}"
            except Exception as e:
                return f"Failed to open {app_name}: {str(e)}"
                
        return f"Unsupported OS: {self.os_type}"
    
    def browse_web(self, url: str) -> str:
        """Open a URL in the default web browser."""
        url = url.strip()
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
        
        try:
            webbrowser.open(url)
            return f"Opened {url} in browser"
        except Exception as e:
            return f"Failed to open {url}: {str(e)}"
    
    def search_web(self, query: str) -> str:
        """Search the web for a query."""
        query = query.strip()
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        try:
            webbrowser.open(search_url)
            return f"Searched for '{query}'"
        except Exception as e:
            return f"Failed to search for '{query}': {str(e)}"
    
    def create_file_or_folder(self, params: str) -> str:
        """Create a file or folder."""
        parts = params.split()
        if not parts:
            return "Please specify what to create (file/folder) and path"
        
        create_type = parts[0].lower()
        if create_type not in ["file", "folder", "directory"]:
            return f"Unknown creation type: {create_type}. Use 'file' or 'folder'."
        
        path = " ".join(parts[1:]).strip()
        if not path:
            return f"Please specify a path for the {create_type}"
        
        try:
            if create_type == "file":
                # Create an empty file
                with open(path, 'w') as f:
                    pass
                return f"Created file: {path}"
            else:  # folder/directory
                os.makedirs(path, exist_ok=True)
                return f"Created directory: {path}"
        except Exception as e:
            return f"Failed to create {create_type} at '{path}': {str(e)}"
    
    def list_directory(self, path: str) -> str:
        """List the contents of a directory."""
        path = path.strip() or "."  # Default to current directory
        
        try:
            items = os.listdir(path)
            if not items:
                return f"Directory '{path}' is empty"
            
            files = [f for f in items if os.path.isfile(os.path.join(path, f))]
            directories = [d for d in items if os.path.isdir(os.path.join(path, d))]
            
            result = f"Contents of '{path}':\n"
            if directories:
                result += "Directories:\n" + "\n".join(f"  {d}/" for d in sorted(directories)) + "\n"
            if files:
                result += "Files:\n" + "\n".join(f"  {f}" for f in sorted(files))
            
            return result
        except Exception as e:
            return f"Failed to list directory '{path}': {str(e)}"
    
    def find_files(self, pattern: str) -> str:
        """Find files matching a pattern."""
        pattern = pattern.strip()
        if not pattern:
            return "Please specify a search pattern"
        
        # Split into directory and pattern
        parts = pattern.split(" in ")
        search_pattern = parts[0].strip()
        directory = parts[1].strip() if len(parts) > 1 else "."
        
        try:
            results = []
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    if search_pattern.lower() in filename.lower():
                        results.append(os.path.join(root, filename))
            
            if not results:
                return f"No files matching '{search_pattern}' found in '{directory}'"
            
            return "Found:\n" + "\n".join(results)
        except Exception as e:
            return f"Error searching for '{search_pattern}': {str(e)}"
    
    def move_file(self, params: str) -> str:
        """Move a file from source to destination."""
        parts = params.split(" to ")
        if len(parts) != 2:
            return "Usage: move [source] to [destination]"
        
        source = parts[0].strip()
        destination = parts[1].strip()
        
        try:
            shutil.move(source, destination)
            return f"Moved '{source}' to '{destination}'"
        except Exception as e:
            return f"Failed to move '{source}' to '{destination}': {str(e)}"
    
    def copy_file(self, params: str) -> str:
        """Copy a file from source to destination."""
        parts = params.split(" to ")
        if len(parts) != 2:
            return "Usage: copy [source] to [destination]"
        
        source = parts[0].strip()
        destination = parts[1].strip()
        
        try:
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            return f"Copied '{source}' to '{destination}'"
        except Exception as e:
            return f"Failed to copy '{source}' to '{destination}': {str(e)}"
    
    def delete_file(self, path: str) -> str:
        """Delete a file or directory."""
        path = path.strip()
        if not path:
            return "Please specify a path to delete"
        
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
                return f"Deleted directory: {path}"
            else:
                os.remove(path)
                return f"Deleted file: {path}"
        except Exception as e:
            return f"Failed to delete '{path}': {str(e)}"
    
    def execute_command(self, command: str) -> str:
        """Execute a shell command."""
        command = command.strip()
        if not command:
            return "Please specify a command to execute"
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            output = result.stdout
            error = result.stderr
            
            response = f"Command executed: {command}\n"
            if output:
                response += f"Output:\n{output}\n"
            if error:
                response += f"Error:\n{error}\n"
            
            return response
        except Exception as e:
            return f"Failed to execute '{command}': {str(e)}"
    
    def type_text(self, text: str) -> str:
        """Simulate typing text using pyautogui."""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available. Install with: pip install pyautogui"
        
        try:
            # Give user time to focus on the target window
            time.sleep(2)
            pyautogui.typewrite(text)
            return f"Typed: {text}"
        except Exception as e:
            return f"Failed to type text: {str(e)}"
    
    def take_screenshot(self, params: str = "") -> str:
        """Take a screenshot using pyautogui."""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available. Install with: pip install pyautogui"
        
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"screenshot-{timestamp}.png"
            
            # Create screenshots directory if it doesn't exist
            screenshots_dir = os.path.join(os.path.expanduser("~"), ".stableagents", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            filepath = os.path.join(screenshots_dir, filename)
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            return f"Screenshot saved: {filepath}"
        except Exception as e:
            return f"Failed to take screenshot: {str(e)}"

    def mouse_click(self, params: str) -> str:
        """Simulate a mouse click using pyautogui."""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available. Install with: pip install pyautogui"
        
        try:
            # Parse coordinates or use current position
            if params.strip():
                # Try to parse coordinates like "100,200" or "x=100 y=200"
                coords = self._parse_coordinates(params)
                if coords:
                    x, y = coords
                    pyautogui.click(x, y)
                    return f"Clicked at position ({x}, {y})"
                else:
                    # Try to click on text or element
                    return self._click_on_text(params)
            else:
                # Click at current mouse position
                x, y = pyautogui.position()
                pyautogui.click()
                return f"Clicked at current position ({x}, {y})"
        except Exception as e:
            return f"Failed to click: {str(e)}"

    def mouse_drag(self, params: str) -> str:
        """Simulate a mouse drag using pyautogui."""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available. Install with: pip install pyautogui"
        
        try:
            # Parse drag parameters: "from x1,y1 to x2,y2"
            if "from" in params and "to" in params:
                parts = params.split("to")
                from_part = parts[0].replace("from", "").strip()
                to_part = parts[1].strip()
                
                start_coords = self._parse_coordinates(from_part)
                end_coords = self._parse_coordinates(to_part)
                
                if start_coords and end_coords:
                    x1, y1 = start_coords
                    x2, y2 = end_coords
                    pyautogui.drag(x2 - x1, y2 - y1, duration=0.5)
                    return f"Dragged from ({x1}, {y1}) to ({x2}, {y2})"
            
            return "Usage: drag from x1,y1 to x2,y2"
        except Exception as e:
            return f"Failed to drag: {str(e)}"

    def mouse_scroll(self, params: str) -> str:
        """Simulate a mouse scroll using pyautogui."""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available. Install with: pip install pyautogui"
        
        try:
            # Parse scroll parameters: "up 3" or "down 5"
            parts = params.strip().split()
            if len(parts) >= 2:
                direction = parts[0].lower()
                amount = int(parts[1])
                
                if direction == "up":
                    pyautogui.scroll(amount)
                    return f"Scrolled up {amount} units"
                elif direction == "down":
                    pyautogui.scroll(-amount)
                    return f"Scrolled down {amount} units"
            
            return "Usage: scroll up/down [amount]"
        except Exception as e:
            return f"Failed to scroll: {str(e)}"

    def keyboard_input(self, params: str) -> str:
        """Simulate keyboard input using pyautogui."""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available. Install with: pip install pyautogui"
        
        try:
            # Parse special keys or text
            if params.strip().startswith("key "):
                key = params.replace("key ", "").strip()
                pyautogui.press(key)
                return f"Pressed key: {key}"
            else:
                # Type text
                pyautogui.typewrite(params)
                return f"Typed: {params}"
        except Exception as e:
            return f"Failed keyboard input: {str(e)}"

    def window_control(self, params: str) -> str:
        """Control windows using platform-specific methods."""
        try:
            parts = params.strip().split()
            if not parts:
                return "Usage: window [action] [target]"
            
            action = parts[0].lower()
            target = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            if self.os_type == "darwin":  # macOS
                return self._macos_window_control(action, target)
            elif self.os_type == "windows":
                return self._windows_window_control(action, target)
            elif self.os_type == "linux":
                return self._linux_window_control(action, target)
            else:
                return f"Window control not supported on {self.os_type}"
        except Exception as e:
            return f"Failed window control: {str(e)}"

    def system_monitor(self, params: str) -> str:
        """Monitor system resources using psutil."""
        try:
            if not params.strip():
                # Return comprehensive system info
                return self._get_system_info()
            
            # Parse specific monitoring request
            parts = params.strip().split()
            metric = parts[0].lower()
            
            if metric == "cpu":
                return self._get_cpu_info()
            elif metric == "memory":
                return self._get_memory_info()
            elif metric == "disk":
                return self._get_disk_info()
            elif metric == "network":
                return self._get_network_info()
            elif metric == "processes":
                return self._get_processes_info()
            else:
                return f"Unknown metric: {metric}. Available: cpu, memory, disk, network, processes"
        except Exception as e:
            return f"Failed system monitoring: {str(e)}"

    def process_control(self, params: str) -> str:
        """Control processes using psutil."""
        try:
            parts = params.strip().split()
            if not parts:
                return "Usage: process [action] [target]"
            
            action = parts[0].lower()
            target = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            if action == "list":
                return self._list_processes()
            elif action == "kill":
                return self._kill_process(target)
            elif action == "start":
                return self._start_process(target)
            elif action == "info":
                return self._get_process_info(target)
            else:
                return f"Unknown action: {action}. Available: list, kill, start, info"
        except Exception as e:
            return f"Failed process control: {str(e)}"

    def build_application(self, params: str) -> str:
        """Build a desktop application using tkinter."""
        if not TKINTER_AVAILABLE:
            return "Tkinter not available for GUI building"
        
        try:
            # Parse application parameters
            parts = params.strip().split()
            if not parts:
                return "Usage: build [app_type] [name] [options]"
            
            app_type = parts[0].lower()
            app_name = parts[1] if len(parts) > 1 else "App"
            
            if app_type == "calculator":
                return self._build_calculator(app_name)
            elif app_type == "notepad":
                return self._build_notepad(app_name)
            elif app_type == "file_manager":
                return self._build_file_manager(app_name)
            else:
                return f"Unknown app type: {app_type}. Available: calculator, notepad, file_manager"
        except Exception as e:
            return f"Failed to build application: {str(e)}"

    def gui_automation(self, params: str) -> str:
        """Automate GUI interactions using pyautogui."""
        if not PYAUTOGUI_AVAILABLE:
            return "PyAutoGUI not available. Install with: pip install pyautogui"
        
        try:
            parts = params.strip().split()
            if not parts:
                return "Usage: gui [action] [target]"
            
            action = parts[0].lower()
            target = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            if action == "find":
                return self._find_and_click(target)
            elif action == "fill":
                return self._fill_form(target)
            elif action == "navigate":
                return self._navigate_ui(target)
            else:
                return f"Unknown GUI action: {action}. Available: find, fill, navigate"
        except Exception as e:
            return f"Failed GUI automation: {str(e)}"

    def network_operations(self, params: str) -> str:
        """Perform network operations."""
        try:
            parts = params.strip().split()
            if not parts:
                return "Usage: network [action] [target]"
            
            action = parts[0].lower()
            target = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            if action == "ping":
                return self._ping_host(target)
            elif action == "download":
                return self._download_file(target)
            elif action == "upload":
                return self._upload_file(target)
            else:
                return f"Unknown network action: {action}. Available: ping, download, upload"
        except Exception as e:
            return f"Failed network operation: {str(e)}"

    def database_operations(self, params: str) -> str:
        """Perform database operations."""
        try:
            parts = params.strip().split()
            if not parts:
                return "Usage: database [action] [target]"
            
            action = parts[0].lower()
            target = " ".join(parts[1:]) if len(parts) > 1 else ""
            
            if action == "connect":
                return self._connect_database(target)
            elif action == "query":
                return self._query_database(target)
            elif action == "backup":
                return self._backup_database(target)
            else:
                return f"Unknown database action: {action}. Available: connect, query, backup"
        except Exception as e:
            return f"Failed database operation: {str(e)}"

    def open_media_service(self, service: str, action: str = "") -> str:
        """Open media services like YouTube, Spotify, etc."""
        service = service.lower().strip()
        action = action.strip()
        
        service_urls = {
            "youtube": "https://www.youtube.com",
            "spotify": "https://open.spotify.com",
            "netflix": "https://www.netflix.com",
            "amazon": "https://www.amazon.com",
            "apple music": "https://music.apple.com",
            "soundcloud": "https://soundcloud.com",
            "vimeo": "https://vimeo.com",
            "twitch": "https://www.twitch.tv"
        }
        
        if service in service_urls:
            url = service_urls[service]
            if action:
                # Add search parameters for specific actions
                if "search" in action or "play" in action:
                    search_query = action.replace("search", "").replace("play", "").strip()
                    if search_query:
                        if service == "youtube":
                            url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
                        elif service == "spotify":
                            url = f"https://open.spotify.com/search/{search_query.replace(' ', '%20')}"
            
            try:
                webbrowser.open(url)
                return f"Opened {service} - {action if action else 'main page'}"
            except Exception as e:
                return f"Failed to open {service}: {str(e)}"
        else:
            return f"Unknown media service: {service}"
    
    def search_and_play_media(self, query: str, service: str = "youtube") -> str:
        """Search for and play media content."""
        service = service.lower().strip()
        
        if service == "youtube":
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        elif service == "spotify":
            search_url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
        else:
            return f"Unsupported service for media search: {service}"
        
        try:
            webbrowser.open(search_url)
            return f"Searched for '{query}' on {service}"
        except Exception as e:
            return f"Failed to search {service} for '{query}': {str(e)}"

    # Helper methods for the above functions
    def _parse_coordinates(self, coord_str: str) -> Optional[tuple]:
        """Parse coordinate string into (x, y) tuple."""
        try:
            # Handle formats like "100,200" or "x=100 y=200"
            if "," in coord_str:
                x, y = map(int, coord_str.split(","))
                return (x, y)
            elif "x=" in coord_str and "y=" in coord_str:
                x = int(coord_str.split("x=")[1].split()[0])
                y = int(coord_str.split("y=")[1].split()[0])
                return (x, y)
        except:
            pass
        return None

    def _click_on_text(self, text: str) -> str:
        """Click on text using image recognition (basic implementation)."""
        # This is a simplified implementation
        # In a real scenario, you'd use OCR or image recognition
        return f"Would click on text: {text} (requires OCR implementation)"

    def _macos_window_control(self, action: str, target: str) -> str:
        """Control windows on macOS using AppleScript."""
        try:
            if action == "minimize":
                script = f'tell application "System Events" to set visible of process "{target}" to false'
            elif action == "maximize":
                script = f'tell application "{target}" to activate'
            elif action == "close":
                script = f'tell application "{target}" to quit'
            else:
                return f"Unknown action: {action}"
            
            subprocess.run(["osascript", "-e", script])
            return f"Window {action} for {target}"
        except Exception as e:
            return f"Failed macOS window control: {str(e)}"

    def _windows_window_control(self, action: str, target: str) -> str:
        """Control windows on Windows."""
        # Windows implementation would use win32api or similar
        return f"Windows window control not yet implemented for {action} {target}"

    def _linux_window_control(self, action: str, target: str) -> str:
        """Control windows on Linux."""
        # Linux implementation would use wmctrl or similar
        return f"Linux window control not yet implemented for {action} {target}"

    def _get_system_info(self) -> str:
        """Get comprehensive system information."""
        info = []
        info.append("=== SYSTEM INFORMATION ===")
        info.append(f"OS: {platform.system()} {platform.release()}")
        info.append(f"Architecture: {platform.machine()}")
        info.append(f"Python: {platform.python_version()}")
        info.append("")
        
        # CPU info
        cpu_info = self._get_cpu_info()
        info.append(cpu_info)
        info.append("")
        
        # Memory info
        memory_info = self._get_memory_info()
        info.append(memory_info)
        info.append("")
        
        # Disk info
        disk_info = self._get_disk_info()
        info.append(disk_info)
        
        return "\n".join(info)

    def _get_cpu_info(self) -> str:
        """Get CPU information."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            info = ["=== CPU INFORMATION ==="]
            info.append(f"CPU Usage: {cpu_percent}%")
            info.append(f"CPU Cores: {cpu_count}")
            if cpu_freq:
                info.append(f"CPU Frequency: {cpu_freq.current:.1f} MHz")
            
            return "\n".join(info)
        except Exception as e:
            return f"Failed to get CPU info: {str(e)}"

    def _get_memory_info(self) -> str:
        """Get memory information."""
        try:
            memory = psutil.virtual_memory()
            
            info = ["=== MEMORY INFORMATION ==="]
            info.append(f"Total Memory: {memory.total / (1024**3):.1f} GB")
            info.append(f"Available Memory: {memory.available / (1024**3):.1f} GB")
            info.append(f"Memory Usage: {memory.percent}%")
            info.append(f"Used Memory: {memory.used / (1024**3):.1f} GB")
            
            return "\n".join(info)
        except Exception as e:
            return f"Failed to get memory info: {str(e)}"

    def _get_disk_info(self) -> str:
        """Get disk information."""
        try:
            info = ["=== DISK INFORMATION ==="]
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    info.append(f"Drive {partition.device}:")
                    info.append(f"  Total: {usage.total / (1024**3):.1f} GB")
                    info.append(f"  Used: {usage.used / (1024**3):.1f} GB")
                    info.append(f"  Free: {usage.free / (1024**3):.1f} GB")
                    info.append(f"  Usage: {usage.percent}%")
                except:
                    continue
            
            return "\n".join(info)
        except Exception as e:
            return f"Failed to get disk info: {str(e)}"

    def _get_network_info(self) -> str:
        """Get network information."""
        try:
            info = ["=== NETWORK INFORMATION ==="]
            
            # Network interfaces
            for interface, addresses in psutil.net_if_addrs().items():
                info.append(f"Interface: {interface}")
                for addr in addresses:
                    if addr.family == psutil.AF_INET:
                        info.append(f"  IPv4: {addr.address}")
                    elif addr.family == psutil.AF_INET6:
                        info.append(f"  IPv6: {addr.address}")
            
            return "\n".join(info)
        except Exception as e:
            return f"Failed to get network info: {str(e)}"

    def _get_processes_info(self) -> str:
        """Get information about running processes."""
        try:
            info = ["=== PROCESSES INFORMATION ==="]
            
            # Get top 10 processes by CPU usage
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            info.append("Top 10 processes by CPU usage:")
            for i, proc in enumerate(processes[:10]):
                info.append(f"{i+1}. {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']:.1f}%")
            
            return "\n".join(info)
        except Exception as e:
            return f"Failed to get processes info: {str(e)}"

    def _list_processes(self) -> str:
        """List running processes."""
        try:
            info = ["=== RUNNING PROCESSES ==="]
            
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                try:
                    info.append(f"{proc.info['pid']}: {proc.info['name']} ({proc.info['status']})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return "\n".join(info[:50])  # Limit to first 50 processes
        except Exception as e:
            return f"Failed to list processes: {str(e)}"

    def _kill_process(self, target: str) -> str:
        """Kill a process by name or PID."""
        try:
            if target.isdigit():
                # Kill by PID
                pid = int(target)
                proc = psutil.Process(pid)
                proc.terminate()
                return f"Terminated process with PID {pid}"
            else:
                # Kill by name
                killed = 0
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        if proc.info['name'].lower() == target.lower():
                            proc.terminate()
                            killed += 1
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                
                if killed > 0:
                    return f"Terminated {killed} process(es) named '{target}'"
                else:
                    return f"No processes found with name '{target}'"
        except Exception as e:
            return f"Failed to kill process: {str(e)}"

    def _start_process(self, target: str) -> str:
        """Start a process."""
        try:
            subprocess.Popen(target, shell=True)
            return f"Started process: {target}"
        except Exception as e:
            return f"Failed to start process: {str(e)}"

    def _get_process_info(self, target: str) -> str:
        """Get detailed information about a process."""
        try:
            if target.isdigit():
                proc = psutil.Process(int(target))
            else:
                # Find process by name
                for p in psutil.process_iter(['pid', 'name']):
                    if p.info['name'].lower() == target.lower():
                        proc = p
                        break
                else:
                    return f"Process '{target}' not found"
            
            info = [f"=== PROCESS INFO: {proc.name()} ==="]
            info.append(f"PID: {proc.pid}")
            info.append(f"Status: {proc.status()}")
            info.append(f"CPU Percent: {proc.cpu_percent()}")
            info.append(f"Memory Percent: {proc.memory_percent():.1f}%")
            info.append(f"Memory RSS: {proc.memory_info().rss / (1024**2):.1f} MB")
            info.append(f"Create Time: {time.ctime(proc.create_time())}")
            
            return "\n".join(info)
        except Exception as e:
            return f"Failed to get process info: {str(e)}"

    def _build_calculator(self, name: str) -> str:
        """Build a simple calculator application."""
        try:
            # This would create a tkinter calculator
            # For now, return a placeholder
            return f"Calculator '{name}' would be built (tkinter implementation needed)"
        except Exception as e:
            return f"Failed to build calculator: {str(e)}"

    def _build_notepad(self, name: str) -> str:
        """Build a simple notepad application."""
        try:
            # This would create a tkinter notepad
            # For now, return a placeholder
            return f"Notepad '{name}' would be built (tkinter implementation needed)"
        except Exception as e:
            return f"Failed to build notepad: {str(e)}"

    def _build_file_manager(self, name: str) -> str:
        """Build a simple file manager application."""
        try:
            # This would create a tkinter file manager
            # For now, return a placeholder
            return f"File Manager '{name}' would be built (tkinter implementation needed)"
        except Exception as e:
            return f"Failed to build file manager: {str(e)}"

    def _find_and_click(self, target: str) -> str:
        """Find and click on an element in the GUI."""
        # This would use image recognition or OCR
        return f"Would find and click on '{target}' (image recognition needed)"

    def _fill_form(self, target: str) -> str:
        """Fill a form in the GUI."""
        # This would automate form filling
        return f"Would fill form '{target}' (form automation needed)"

    def _navigate_ui(self, target: str) -> str:
        """Navigate through UI elements."""
        # This would navigate through UI
        return f"Would navigate to '{target}' (UI navigation needed)"

    def _ping_host(self, host: str) -> str:
        """Ping a host."""
        try:
            result = subprocess.run(['ping', '-c', '4', host], capture_output=True, text=True)
            return f"Ping result for {host}:\n{result.stdout}"
        except Exception as e:
            return f"Failed to ping {host}: {str(e)}"

    def _download_file(self, url: str) -> str:
        """Download a file from URL."""
        try:
            import requests
            response = requests.get(url)
            filename = url.split('/')[-1]
            with open(filename, 'wb') as f:
                f.write(response.content)
            return f"Downloaded {filename}"
        except Exception as e:
            return f"Failed to download {url}: {str(e)}"

    def _upload_file(self, target: str) -> str:
        """Upload a file."""
        # This would implement file upload
        return f"Would upload file to '{target}' (upload implementation needed)"

    def _connect_database(self, connection_string: str) -> str:
        """Connect to a database."""
        # This would implement database connection
        return f"Would connect to database '{connection_string}' (database implementation needed)"

    def _query_database(self, query: str) -> str:
        """Query a database."""
        # This would implement database querying
        return f"Would execute query '{query}' (database implementation needed)"

    def _backup_database(self, target: str) -> str:
        """Backup a database."""
        # This would implement database backup
        return f"Would backup database '{target}' (database implementation needed)" 