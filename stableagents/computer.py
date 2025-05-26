import os
import subprocess
import platform
import webbrowser
import logging
import shutil
import time
import re
from typing import List, Dict, Any, Optional, Union

class ComputerControl:
    """Module for controlling computer actions based on natural language commands."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.os_type = platform.system().lower()
        self.registered_actions = {
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
            "screenshot": self.take_screenshot
        }
        
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
        """Simulate typing text."""
        # This is a stub - actual implementation would depend on OS and available tools
        return f"Typed: {text} (simulated)"
    
    def take_screenshot(self, params: str = "") -> str:
        """Take a screenshot."""
        # This is a stub - actual implementation would depend on OS and available tools
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshot-{timestamp}.png"
        
        return f"Screenshot taken: {filename} (simulated)" 