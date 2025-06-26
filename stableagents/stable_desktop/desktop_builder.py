"""
Desktop Builder - Main class for creating desktop software using GPT.
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..ai_providers import AIProvider
from .app_generator import AppGenerator
from .ui_framework import UIFramework


class DesktopBuilder:
    """
    Main class for building desktop applications using GPT.
    
    Provides functionality to:
    - Generate application code using AI
    - Create UI frameworks (Tkinter, PyQt, etc.)
    - Build and package applications
    - Deploy desktop software
    """
    
    def __init__(self, ai_provider: Optional[AIProvider] = None):
        """
        Initialize the desktop builder.
        
        Args:
            ai_provider: AI provider instance for code generation
        """
        self.ai_provider = ai_provider
        self.app_generator = AppGenerator(ai_provider)
        self.ui_framework = UIFramework()
        
        # Project structure
        self.project_path = Path.cwd() / "stable_desktop_projects"
        self.project_path.mkdir(exist_ok=True)
        
        # Templates and configurations
        self.templates_path = Path(__file__).parent / "templates"
        self.templates_path.mkdir(exist_ok=True)
        
    def create_app(self, 
                   app_name: str,
                   description: str,
                   ui_framework: str = "tkinter",
                   features: List[str] = None,
                   output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Create a new desktop application using GPT.
        
        Args:
            app_name: Name of the application
            description: Description of what the app should do
            ui_framework: UI framework to use (tkinter, pyqt, kivy, etc.)
            features: List of specific features to include
            output_dir: Output directory (default: project_path/app_name)
            
        Returns:
            Dictionary with project information and status
        """
        if not self.ai_provider:
            raise ValueError("AI provider is required for app generation")
        
        # Validate inputs
        if not app_name or not description:
            raise ValueError("App name and description are required")
        
        # Set output directory
        if not output_dir:
            output_dir = self.project_path / app_name
        
        # Clean app name for file system
        safe_app_name = self._sanitize_name(app_name)
        
        print(f"🚀 Creating desktop app: {app_name}")
        print(f"📝 Description: {description}")
        print(f"🎨 UI Framework: {ui_framework}")
        print(f"📁 Output: {output_dir}")
        print()
        
        try:
            # Generate application structure
            app_structure = self.app_generator.generate_app_structure(
                app_name=safe_app_name,
                description=description,
                ui_framework=ui_framework,
                features=features or []
            )
            
            # Create project directory
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate main application file
            main_file = self.app_generator.generate_main_app(
                app_name=safe_app_name,
                description=description,
                ui_framework=ui_framework,
                features=features or []
            )
            
            # Generate UI components
            ui_components = self.app_generator.generate_ui_components(
                app_name=safe_app_name,
                description=description,
                ui_framework=ui_framework,
                features=features or []
            )
            
            # Generate requirements and setup files
            requirements = self.app_generator.generate_requirements(ui_framework)
            setup_files = self.app_generator.generate_setup_files(safe_app_name)
            
            # Write files to disk
            self._write_project_files(
                output_dir=output_dir,
                app_name=safe_app_name,
                main_file=main_file,
                ui_components=ui_components,
                requirements=requirements,
                setup_files=setup_files
            )
            
            # Create project metadata
            metadata = {
                "app_name": app_name,
                "safe_name": safe_app_name,
                "description": description,
                "ui_framework": ui_framework,
                "features": features or [],
                "created_at": datetime.now().isoformat(),
                "output_dir": str(output_dir),
                "status": "created"
            }
            
            # Save metadata
            with open(output_dir / "project.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ Desktop app created successfully!")
            print(f"📁 Project location: {output_dir}")
            print(f"🚀 To run: cd {output_dir} && python main.py")
            print()
            
            return {
                "success": True,
                "project_path": str(output_dir),
                "metadata": metadata,
                "files_created": self._list_created_files(output_dir)
            }
            
        except Exception as e:
            print(f"❌ Error creating desktop app: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def build_app(self, project_path: Path) -> Dict[str, Any]:
        """
        Build a desktop application for distribution.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            Build status and information
        """
        print(f"🔨 Building desktop app: {project_path}")
        
        try:
            # Load project metadata
            metadata_file = project_path / "project.json"
            if not metadata_file.exists():
                raise FileNotFoundError("Project metadata not found")
            
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Check if main.py exists
            main_file = project_path / "main.py"
            if not main_file.exists():
                raise FileNotFoundError("main.py not found")
            
            # Install dependencies
            requirements_file = project_path / "requirements.txt"
            if requirements_file.exists():
                print("📦 Installing dependencies...")
                subprocess.run([
                    "pip", "install", "-r", str(requirements_file)
                ], check=True, capture_output=True)
            
            # Create build directory
            build_dir = project_path / "build"
            build_dir.mkdir(exist_ok=True)
            
            # Copy project files to build directory
            self._copy_project_files(project_path, build_dir)
            
            # Generate executable (if pyinstaller is available)
            try:
                import PyInstaller
                print("📦 Creating executable...")
                subprocess.run([
                    "pyinstaller", "--onefile", "--windowed", 
                    str(main_file), "--distpath", str(build_dir)
                ], check=True, capture_output=True)
                
                executable_created = True
            except ImportError:
                print("⚠️  PyInstaller not available, skipping executable creation")
                executable_created = False
            
            print(f"✅ Build completed!")
            print(f"📁 Build location: {build_dir}")
            
            return {
                "success": True,
                "build_path": str(build_dir),
                "executable_created": executable_created,
                "metadata": metadata
            }
            
        except Exception as e:
            print(f"❌ Error building app: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_app(self, project_path: Path) -> bool:
        """
        Run a desktop application.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            True if successful, False otherwise
        """
        print(f"🚀 Running desktop app: {project_path}")
        
        try:
            main_file = project_path / "main.py"
            if not main_file.exists():
                print(f"❌ main.py not found in {project_path}")
                return False
            
            # Install dependencies if needed
            requirements_file = project_path / "requirements.txt"
            if requirements_file.exists():
                print("📦 Installing dependencies...")
                subprocess.run([
                    "pip", "install", "-r", str(requirements_file)
                ], check=True, capture_output=True)
            
            # Run the application
            print("🎯 Starting application...")
            subprocess.run(["python", str(main_file)], check=True)
            
            return True
            
        except Exception as e:
            print(f"❌ Error running app: {e}")
            return False
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all created desktop projects.
        
        Returns:
            List of project metadata
        """
        projects = []
        
        for project_dir in self.project_path.iterdir():
            if project_dir.is_dir():
                metadata_file = project_dir / "project.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                        projects.append(metadata)
                    except:
                        continue
        
        return projects
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize app name for file system use."""
        import re
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9\s]', '', name)
        sanitized = re.sub(r'\s+', '_', sanitized).lower()
        return sanitized
    
    def _write_project_files(self, 
                            output_dir: Path,
                            app_name: str,
                            main_file: str,
                            ui_components: Dict[str, str],
                            requirements: str,
                            setup_files: Dict[str, str]):
        """Write all project files to disk."""
        
        # Write main application file
        with open(output_dir / "main.py", 'w') as f:
            f.write(main_file)
        
        # Write UI components
        ui_dir = output_dir / "ui"
        ui_dir.mkdir(exist_ok=True)
        
        for component_name, component_code in ui_components.items():
            with open(ui_dir / f"{component_name}.py", 'w') as f:
                f.write(component_code)
        
        # Write requirements
        with open(output_dir / "requirements.txt", 'w') as f:
            f.write(requirements)
        
        # Write setup files
        for filename, content in setup_files.items():
            with open(output_dir / filename, 'w') as f:
                f.write(content)
        
        # Create README
        readme_content = f"""# {app_name}

A desktop application created with Stable Desktop.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Building for Distribution

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## Features

- Desktop application created with AI assistance
- Modern UI framework
- Cross-platform compatibility

## Project Structure

- `main.py` - Main application entry point
- `ui/` - UI components and layouts
- `requirements.txt` - Python dependencies
- `project.json` - Project metadata
"""
        
        with open(output_dir / "README.md", 'w') as f:
            f.write(readme_content)
    
    def _list_created_files(self, project_dir: Path) -> List[str]:
        """List all files created in the project."""
        files = []
        for file_path in project_dir.rglob("*"):
            if file_path.is_file():
                files.append(str(file_path.relative_to(project_dir)))
        return files
    
    def _copy_project_files(self, source_dir: Path, dest_dir: Path):
        """Copy project files to build directory."""
        import shutil
        
        # Copy all files except build artifacts
        for item in source_dir.iterdir():
            if item.name in ['build', 'dist', '__pycache__', '.pyc']:
                continue
            
            if item.is_file():
                shutil.copy2(item, dest_dir)
            elif item.is_dir():
                shutil.copytree(item, dest_dir / item.name, dirs_exist_ok=True) 