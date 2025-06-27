#!/usr/bin/env python3
"""
Natural Language Desktop Application Generator

Generates desktop applications from natural language descriptions using Google Gemini API.
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import re

# Import the configuration manager
from .config_manager import ConfigManager, setup_gemini_api_key, get_gemini_api_key
from .ai_providers import GoogleProvider


class NaturalLanguageDesktopGenerator:
    """Generates desktop applications from natural language descriptions."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the generator with optional API key."""
        self.config_manager = ConfigManager()
        
        # Set up API key
        if api_key:
            self.config_manager.set_api_key("gemini", api_key)
        else:
            # Try to get existing key
            api_key = get_gemini_api_key()
            if not api_key:
                print("🔑 No Gemini API key found. Let's set one up...")
                if not setup_gemini_api_key():
                    raise ValueError("Gemini API key is required")
                api_key = get_gemini_api_key()
        
        self.gemini = GoogleProvider(api_key)
        self.projects_dir = Path("stable_desktop_projects")
        self.projects_dir.mkdir(exist_ok=True)
    
    def generate_app(self, description: str, framework: str = "customtkinter") -> Dict[str, Any]:
        """Generate a desktop application from natural language description."""
        print(f"🚀 Generating {framework} app from description...")
        print(f"📝 Description: {description}")
        
        # Extract app name and features
        app_info = self._extract_app_info(description)
        app_name = app_info["name"]
        features = app_info["features"]
        
        print(f"📱 App Name: {app_name}")
        print(f"✨ Features: {', '.join(features)}")
        
        # Generate the application code
        code = self._generate_app_code(description, framework, app_name, features)
        
        # Create project structure
        project_path = self._create_project_structure(app_name, framework)
        
        # Write the generated code
        self._write_app_code(project_path, code, framework)
        
        # Create additional project files
        self._create_project_files(project_path, app_name, description, framework)
        
        print(f"✅ App generated successfully at: {project_path}")
        
        return {
            "name": app_name,
            "path": str(project_path),
            "framework": framework,
            "features": features,
            "description": description
        }
    
    def _extract_app_info(self, description: str) -> Dict[str, Any]:
        """Extract app name and features from description using AI."""
        prompt = f"""
        Extract the application name and key features from this description:
        "{description}"
        
        Return a JSON object with:
        - "name": A short, descriptive name for the app (max 3 words)
        - "features": List of main features/functionality
        
        Example:
        {{
            "name": "Calculator App",
            "features": ["basic arithmetic", "scientific functions", "history"]
        }}
        
        Only return the JSON object, nothing else.
        """
        
        try:
            response = self.gemini.generate_text(prompt)
            # Clean up the response to extract JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            app_info = json.loads(response)
            return app_info
        except Exception as e:
            print(f"⚠️ Error extracting app info: {e}")
            # Fallback: generate a simple name
            words = description.split()[:3]
            app_name = " ".join(words).title()
            return {
                "name": app_name,
                "features": ["basic functionality"]
            }
    
    def _generate_app_code(self, description: str, framework: str, app_name: str, features: List[str]) -> str:
        """Generate the main application code."""
        if framework == "customtkinter":
            return self._generate_customtkinter_code(description, app_name, features)
        elif framework == "tkinter":
            return self._generate_tkinter_code(description, app_name, features)
        elif framework == "pyqt":
            return self._generate_pyqt_code(description, app_name, features)
        else:
            raise ValueError(f"Unsupported framework: {framework}")
    
    def _generate_customtkinter_code(self, description: str, app_name: str, features: List[str]) -> str:
        """Generate CustomTkinter application code."""
        prompt = f"""
        Create a modern CustomTkinter desktop application based on this description:
        "{description}"
        
        App Name: {app_name}
        Features: {', '.join(features)}
        
        Requirements:
        1. Use CustomTkinter for modern UI
        2. Include proper imports and setup
        3. Create a main window with title "{app_name}"
        4. Add functionality based on the description
        5. Include error handling
        6. Add comments explaining the code
        7. Make the UI responsive and user-friendly
        8. Use modern styling with CustomTkinter themes
        
        Return only the complete Python code, no explanations.
        """
        
        try:
            code = self.gemini.generate_text(prompt)
            if not code or code.startswith("Error:"):
                raise ValueError(f"Failed to generate code: {code}")
            return code
        except Exception as e:
            print(f"❌ Error generating CustomTkinter code: {e}")
            print("   Please check your API key and try again.")
            raise
    
    def _generate_tkinter_code(self, description: str, app_name: str, features: List[str]) -> str:
        """Generate Tkinter application code."""
        prompt = f"""
        Create a Tkinter desktop application based on this description:
        "{description}"
        
        App Name: {app_name}
        Features: {', '.join(features)}
        
        Requirements:
        1. Use standard Tkinter
        2. Include proper imports and setup
        3. Create a main window with title "{app_name}"
        4. Add functionality based on the description
        5. Include error handling
        6. Add comments explaining the code
        7. Make the UI responsive and user-friendly
        
        Return only the complete Python code, no explanations.
        """
        
        try:
            code = self.gemini.generate_text(prompt)
            if not code or code.startswith("Error:"):
                raise ValueError(f"Failed to generate code: {code}")
            return code
        except Exception as e:
            print(f"❌ Error generating Tkinter code: {e}")
            print("   Please check your API key and try again.")
            raise
    
    def _generate_pyqt_code(self, description: str, app_name: str, features: List[str]) -> str:
        """Generate PyQt application code."""
        prompt = f"""
        Create a PyQt6 desktop application based on this description:
        "{description}"
        
        App Name: {app_name}
        Features: {', '.join(features)}
        
        Requirements:
        1. Use PyQt6 for modern UI
        2. Include proper imports and setup
        3. Create a main window with title "{app_name}"
        4. Add functionality based on the description
        5. Include error handling
        6. Add comments explaining the code
        7. Make the UI responsive and user-friendly
        8. Use modern styling
        
        Return only the complete Python code, no explanations.
        """
        
        return self.gemini.generate_text(prompt)
    
    def _create_project_structure(self, app_name: str, framework: str) -> Path:
        """Create the project directory structure."""
        # Clean app name for directory
        clean_name = re.sub(r'[^a-zA-Z0-9\s-]', '', app_name).replace(' ', '_')
        project_path = self.projects_dir / clean_name
        
        # Remove existing directory if it exists
        if project_path.exists():
            shutil.rmtree(project_path)
        
        # Create project structure
        project_path.mkdir(parents=True)
        
        # Create UI components directory for modular apps
        ui_dir = project_path / "ui"
        ui_dir.mkdir(exist_ok=True)
        
        return project_path
    
    def _write_app_code(self, project_path: Path, code: str, framework: str):
        """Write the generated code to the project."""
        main_file = project_path / "main.py"
        
        # Check if the code looks like valid Python (not an error message)
        if code.startswith("Error:") or code.startswith("❌") or "INVALID_ARGUMENT" in code:
            print(f"❌ Error: Generated code contains an error message:")
            print(f"   {code[:200]}...")
            print("   Please check your API key and try again.")
            raise ValueError("Failed to generate valid Python code")
        
        # Basic validation that it looks like Python code
        if not any(keyword in code for keyword in ["import", "def ", "class ", "if __name__"]):
            print(f"❌ Error: Generated code doesn't appear to be valid Python:")
            print(f"   {code[:200]}...")
            raise ValueError("Generated code is not valid Python")
        
        with open(main_file, 'w') as f:
            f.write(code)
        
        print(f"📄 Main app code written to: {main_file}")
    
    def _create_project_files(self, project_path: Path, app_name: str, description: str, framework: str):
        """Create additional project files (README, requirements, etc.)."""
        # Create README
        readme_content = f"""# {app_name}

A desktop application generated from natural language description.

## Description
{description}

## Framework
Built with {framework}

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## Features
- Generated from natural language description
- Modern UI with {framework}
- Cross-platform compatibility
"""
        
        with open(project_path / "README.md", 'w') as f:
            f.write(readme_content)
        
        # Create requirements.txt
        requirements = self._get_framework_requirements(framework)
        with open(project_path / "requirements.txt", 'w') as f:
            f.write(requirements)
        
        # Create project.json for metadata
        project_metadata = {
            "name": app_name,
            "description": description,
            "framework": framework,
            "generated_by": "StableAgents Natural Language Desktop Generator",
            "version": "1.0.0"
        }
        
        with open(project_path / "project.json", 'w') as f:
            json.dump(project_metadata, f, indent=2)
        
        # Create setup.py
        setup_content = f"""#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="{app_name.lower().replace(' ', '-')}",
    version="1.0.0",
    description="{description}",
    packages=find_packages(),
    install_requires=[
        {', '.join(f'"{req}"' for req in requirements.split('\\n') if req.strip())}
    ],
    entry_points={{
        'console_scripts': [
            '{app_name.lower().replace(" ", "-")}=main:main',
        ],
    }},
)
"""
        
        with open(project_path / "setup.py", 'w') as f:
            f.write(setup_content)
    
    def _get_framework_requirements(self, framework: str) -> str:
        """Get requirements for the specified framework."""
        requirements = {
            "customtkinter": "customtkinter>=5.2.0",
            "tkinter": "# tkinter is included with Python",
            "pyqt": "PyQt6>=6.4.0"
        }
        
        return requirements.get(framework, "customtkinter>=5.2.0")
    
    def run_app(self, project_path: str) -> bool:
        """Run the generated application."""
        project_path = Path(project_path).resolve()  # Ensure absolute path
        main_file = project_path / "main.py"
        
        if not main_file.exists():
            print(f"❌ Main file not found: {main_file}")
            return False
        
        print(f"🚀 Running app: {project_path.name}")
        print(f"📁 Project path: {project_path}")
        print(f"📄 Main file: {main_file}")
        
        try:
            # Install requirements first
            requirements_file = project_path / "requirements.txt"
            if requirements_file.exists():
                print("📦 Installing requirements...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ], check=True)
            
            # Run the app - use the main file path directly, not with cwd
            result = subprocess.run([
                sys.executable, str(main_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ App ran successfully")
                return True
            else:
                print(f"❌ Error running app: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running app: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def list_frameworks(self) -> List[str]:
        """List available UI framework names."""
        return ["customtkinter", "tkinter", "pyqt"]
    
    def get_framework_descriptions(self) -> List[str]:
        """List available UI frameworks with descriptions."""
        return [
            "customtkinter - Modern, beautiful UI with dark mode support",
            "tkinter - Standard Python GUI framework",
            "pyqt - Professional Qt-based framework"
        ]
    
    def get_project_info(self, project_path: str) -> Dict[str, Any]:
        """Get information about a generated project."""
        project_path = Path(project_path)
        
        if not project_path.exists():
            raise ValueError(f"Project not found: {project_path}")
        
        # Read project metadata
        project_file = project_path / "project.json"
        if project_file.exists():
            with open(project_file, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {"name": project_path.name}
        
        # Get file structure
        files = []
        for file_path in project_path.rglob("*"):
            if file_path.is_file():
                files.append(str(file_path.relative_to(project_path)))
        
        return {
            "path": str(project_path),
            "metadata": metadata,
            "files": files,
            "main_file": str(project_path / "main.py")
        }
    
    def get_setup_instructions(self) -> str:
        """Get setup instructions for the natural language desktop generator."""
        return """
🔧 Natural Language Desktop Generator Setup
==========================================

📋 Prerequisites:
1. Python 3.8 or higher
2. Google Gemini API key
3. Internet connection

🔑 Getting a Gemini API Key:
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click 'Create API Key'
4. Copy the API key

🚀 Setting up the API Key:

Option 1: Environment Variable (Recommended)
```bash
export GEMINI_API_KEY="your-api-key-here"
```

Option 2: Interactive Setup
```bash
stableagents-ai natural-desktop create
# This will prompt you for the API key
```

Option 3: Python Code
```python
import os
os.environ["GEMINI_API_KEY"] = "your-api-key-here"

from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
generator = NaturalLanguageDesktopGenerator("your-api-key-here")
```

📦 Installing Dependencies:
```bash
# For CustomTkinter (recommended)
pip install customtkinter

# For PyQt (optional)
pip install PyQt6

# Tkinter comes with Python
```

🎯 Quick Start:
```bash
# Create your first app
stableagents-ai natural-desktop create

# Or create a demo app
stableagents-ai natural-desktop demo

# List supported frameworks
stableagents-ai natural-desktop frameworks
```

💡 Tips:
- Be specific in your descriptions for better results
- CustomTkinter is recommended for modern, beautiful UIs
- Tkinter is good for simple, quick prototypes
- PyQt is best for professional, complex applications

🔍 Troubleshooting:
- If you get API key errors, make sure your key is valid and has sufficient credits
- If imports fail, install the required dependencies
- For UI issues, try a different framework
"""

    def create_app_from_description(self, description: str, app_name: str = None, ui_framework: str = "customtkinter") -> Dict[str, Any]:
        """Create a desktop application from natural language description using enhanced Gemini prompts."""
        print(f"🚀 Creating {ui_framework} desktop application...")
        print(f"📝 Description: {description}")
        
        # Extract app name if not provided
        if not app_name:
            app_info = self._extract_app_info(description)
            app_name = app_info["name"]
        
        print(f"📱 App Name: {app_name}")
        
        # Generate enhanced application code with better prompts
        code = self._generate_enhanced_app_code(description, ui_framework, app_name)
        
        # Create project structure
        project_path = self._create_project_structure(app_name, ui_framework)
        
        # Write the generated code
        self._write_app_code(project_path, code, ui_framework)
        
        # Create additional project files
        self._create_project_files(project_path, app_name, description, ui_framework)
        
        print(f"✅ Desktop application created successfully!")
        print(f"📁 Project location: {project_path}")
        print(f"🚀 To run: cd {project_path} && python main.py")
        
        return {
            "success": True,
            "name": app_name,
            "project_path": str(project_path),
            "framework": ui_framework,
            "description": description
        }
    
    def _generate_enhanced_app_code(self, description: str, framework: str, app_name: str) -> str:
        """Generate enhanced application code with better prompts for desktop applications."""
        if framework == "customtkinter":
            return self._generate_enhanced_customtkinter_code(description, app_name)
        elif framework == "tkinter":
            return self._generate_enhanced_tkinter_code(description, app_name)
        elif framework == "pyqt":
            return self._generate_enhanced_pyqt_code(description, app_name)
        else:
            raise ValueError(f"Unsupported framework: {framework}")
    
    def _generate_enhanced_customtkinter_code(self, description: str, app_name: str) -> str:
        """Generate enhanced CustomTkinter application code with modern UI patterns."""
        prompt = f"""
        Create a modern, professional CustomTkinter desktop application based on this description:
        "{description}"
        
        App Name: {app_name}
        
        Requirements:
        1. Use CustomTkinter for a modern, beautiful UI
        2. Include proper imports: import customtkinter as ctk, tkinter as tk
        3. Create a main application class with proper structure
        4. Set up modern theming with dark/light mode support
        5. Create a responsive layout that works on different screen sizes
        6. Add proper error handling and user feedback
        7. Include comprehensive comments explaining the code
        8. Make the UI intuitive and user-friendly
        9. Add proper window management (minimize, maximize, close)
        10. Include a main() function and proper entry point
        
        Code Structure:
        - Import statements
        - Main application class
        - UI setup and layout
        - Event handlers and functionality
        - Main function with proper entry point
        
        Return only the complete, runnable Python code. No explanations or markdown formatting.
        """
        
        return self.gemini.generate_text(prompt, model="gemini-2.5-flash", max_tokens=2000)
    
    def _generate_enhanced_tkinter_code(self, description: str, app_name: str) -> str:
        """Generate enhanced Tkinter application code."""
        prompt = f"""
        Create a professional Tkinter desktop application based on this description:
        "{description}"
        
        App Name: {app_name}
        
        Requirements:
        1. Use standard Tkinter with modern styling
        2. Include proper imports: import tkinter as tk, from tkinter import ttk
        3. Create a main application class with proper structure
        4. Use ttk widgets for better appearance
        5. Create a responsive layout with proper padding and spacing
        6. Add proper error handling and user feedback
        7. Include comprehensive comments explaining the code
        8. Make the UI intuitive and user-friendly
        9. Add proper window management
        10. Include a main() function and proper entry point
        
        Code Structure:
        - Import statements
        - Main application class
        - UI setup and layout
        - Event handlers and functionality
        - Main function with proper entry point
        
        Return only the complete, runnable Python code. No explanations or markdown formatting.
        """
        
        return self.gemini.generate_text(prompt, model="gemini-2.5-flash", max_tokens=2000)
    
    def _generate_enhanced_pyqt_code(self, description: str, app_name: str) -> str:
        """Generate enhanced PyQt application code."""
        prompt = f"""
        Create a professional PyQt6 desktop application based on this description:
        "{description}"
        
        App Name: {app_name}
        
        Requirements:
        1. Use PyQt6 for modern UI
        2. Include proper imports: from PyQt6.QtWidgets import *, from PyQt6.QtCore import *
        3. Create a main application class inheriting from QMainWindow
        4. Use modern Qt styling and themes
        5. Create a responsive layout with proper spacing
        6. Add proper error handling and user feedback
        7. Include comprehensive comments explaining the code
        8. Make the UI intuitive and user-friendly
        9. Add proper window management and menu system
        10. Include a main() function with QApplication setup
        
        Code Structure:
        - Import statements
        - Main application class (QMainWindow)
        - UI setup and layout
        - Event handlers and functionality
        - Main function with QApplication
        
        Return only the complete, runnable Python code. No explanations or markdown formatting.
        """
        
        return self.gemini.generate_text(prompt, model="gemini-2.5-flash", max_tokens=2000)
    
    def generate_code_from_prompt(self, prompt: str, framework: str = "customtkinter") -> str:
        """Generate specific UI code from a prompt."""
        print(f"🎨 Generating {framework} code from prompt...")
        
        enhanced_prompt = f"""
        Generate {framework} code for this specific UI component or functionality:
        "{prompt}"
        
        Requirements:
        1. Use {framework} framework
        2. Create complete, runnable code
        3. Include proper imports
        4. Add error handling
        5. Include comments explaining the code
        6. Make it reusable and modular
        
        Return only the complete Python code. No explanations or markdown formatting.
        """
        
        return self.gemini.generate_text(enhanced_prompt, model="gemini-2.5-flash", max_tokens=1500)
    
    def create_interactive_demo(self) -> Dict[str, Any]:
        """Create an interactive demo application showcasing the natural desktop capabilities."""
        demo_description = """
        Create an interactive demo application that showcases the Natural Language Desktop Generator capabilities.
        
        Features to include:
        1. Modern, beautiful UI with CustomTkinter
        2. Dark/light mode toggle
        3. Interactive sections demonstrating different UI components
        4. Sample applications showcase (calculator, task manager, file browser)
        5. Code generation examples
        6. Framework comparison information
        7. Setup instructions display
        8. Responsive design that works on different screen sizes
        9. Professional animations and transitions
        10. Helpful tooltips and user guidance
        
        The app should be educational and demonstrate the power of natural language to desktop app conversion.
        """
        
        return self.create_app_from_description(
            description=demo_description,
            app_name="NaturalDesktopDemo",
            ui_framework="customtkinter"
        )


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate desktop apps from natural language")
    parser.add_argument("description", help="Natural language description of the app")
    parser.add_argument("--framework", "-f", default="customtkinter", 
                       choices=["customtkinter", "tkinter", "pyqt"],
                       help="UI framework to use")
    parser.add_argument("--run", "-r", action="store_true", 
                       help="Run the generated app")
    
    args = parser.parse_args()
    
    try:
        generator = NaturalLanguageDesktopGenerator()
        result = generator.generate_app(args.description, args.framework)
        
        if args.run:
            generator.run_app(result["path"])
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 