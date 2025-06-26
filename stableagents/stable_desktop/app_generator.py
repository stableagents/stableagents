"""
App Generator - Uses GPT to generate desktop application code.
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path

from ..ai_providers import AIProvider


class AppGenerator:
    """
    Generates desktop application code using GPT.
    
    Handles:
    - Main application structure
    - UI components
    - Requirements and dependencies
    - Setup files
    """
    
    def __init__(self, ai_provider: Optional[AIProvider] = None):
        """
        Initialize the app generator.
        
        Args:
            ai_provider: AI provider for code generation
        """
        self.ai_provider = ai_provider
        
        # UI framework templates
        self.framework_templates = {
            "tkinter": {
                "name": "Tkinter",
                "description": "Python's standard GUI toolkit",
                "dependencies": ["tkinter"],
                "pros": ["Built-in", "Simple", "Cross-platform"],
                "cons": ["Basic styling", "Limited widgets"]
            },
            "pyqt": {
                "name": "PyQt",
                "description": "Qt framework for Python",
                "dependencies": ["PyQt5", "PyQt5-tools"],
                "pros": ["Professional", "Rich widgets", "Modern look"],
                "cons": ["Complex", "Large size", "License considerations"]
            },
            "kivy": {
                "name": "Kivy",
                "description": "Modern library for multi-touch applications",
                "dependencies": ["kivy"],
                "pros": ["Modern", "Touch-friendly", "Cross-platform"],
                "cons": ["Learning curve", "Different from traditional GUIs"]
            },
            "customtkinter": {
                "name": "CustomTkinter",
                "description": "Modern and beautiful custom tkinter widgets",
                "dependencies": ["customtkinter"],
                "pros": ["Modern look", "Easy to use", "Built on tkinter"],
                "cons": ["Newer library", "Limited widget set"]
            }
        }
    
    def generate_app_structure(self,
                              app_name: str,
                              description: str,
                              ui_framework: str,
                              features: List[str]) -> Dict[str, Any]:
        """
        Generate the overall application structure.
        
        Args:
            app_name: Name of the application
            description: Description of what the app should do
            ui_framework: UI framework to use
            features: List of features to include
            
        Returns:
            Application structure information
        """
        if not self.ai_provider:
            return self._generate_default_structure(app_name, description, ui_framework, features)
        
        prompt = f"""
        Generate a desktop application structure for:
        
        App Name: {app_name}
        Description: {description}
        UI Framework: {ui_framework}
        Features: {', '.join(features)}
        
        Please provide a JSON structure with:
        1. Main application class structure
        2. UI component organization
        3. File structure recommendations
        4. Key functions and methods needed
        
        Return only valid JSON.
        """
        
        try:
            response = self.ai_provider.generate_text(prompt, max_tokens=1000)
            return json.loads(response)
        except:
            return self._generate_default_structure(app_name, description, ui_framework, features)
    
    def generate_main_app(self,
                         app_name: str,
                         description: str,
                         ui_framework: str,
                         features: List[str]) -> str:
        """
        Generate the main application file.
        
        Args:
            app_name: Name of the application
            description: Description of what the app should do
            ui_framework: UI framework to use
            features: List of features to include
            
        Returns:
            Main application code as string
        """
        if not self.ai_provider:
            return self._generate_default_main_app(app_name, description, ui_framework, features)
        
        prompt = f"""
        Generate a complete Python desktop application using {ui_framework}.
        
        App Name: {app_name}
        Description: {description}
        Features: {', '.join(features)}
        
        Requirements:
        1. Create a complete, runnable application
        2. Use {ui_framework} for the UI
        3. Include proper error handling
        4. Add comments explaining the code
        5. Make it user-friendly and modern looking
        6. Include the features: {', '.join(features)}
        
        Return only the Python code, no explanations.
        """
        
        try:
            return self.ai_provider.generate_text(prompt, max_tokens=2000)
        except:
            return self._generate_default_main_app(app_name, description, ui_framework, features)
    
    def generate_ui_components(self,
                              app_name: str,
                              description: str,
                              ui_framework: str,
                              features: List[str]) -> Dict[str, str]:
        """
        Generate UI components for the application.
        
        Args:
            app_name: Name of the application
            description: Description of what the app should do
            ui_framework: UI framework to use
            features: List of features to include
            
        Returns:
            Dictionary of component names to code
        """
        if not self.ai_provider:
            return self._generate_default_ui_components(app_name, description, ui_framework, features)
        
        components = {}
        
        # Generate main window component
        main_window_prompt = f"""
        Generate a main window component for a {ui_framework} application.
        
        App Name: {app_name}
        Description: {description}
        Features: {', '.join(features)}
        
        Create a main window class that:
        1. Sets up the primary application window
        2. Handles window management (resize, close, etc.)
        3. Provides a clean, modern interface
        4. Is ready to integrate with other components
        
        Return only the Python code.
        """
        
        try:
            components["main_window"] = self.ai_provider.generate_text(main_window_prompt, max_tokens=1000)
        except:
            components["main_window"] = self._generate_default_main_window(app_name, ui_framework)
        
        # Generate additional components based on features
        for feature in features:
            feature_prompt = f"""
            Generate a UI component for the feature: {feature}
            
            App Name: {app_name}
            UI Framework: {ui_framework}
            
            Create a component that:
            1. Implements the {feature} functionality
            2. Uses {ui_framework} widgets
            3. Has a clean, user-friendly interface
            4. Can be easily integrated into the main application
            
            Return only the Python code.
            """
            
            try:
                component_name = f"{feature.lower().replace(' ', '_')}_component"
                components[component_name] = self.ai_provider.generate_text(feature_prompt, max_tokens=1000)
            except:
                components[component_name] = self._generate_default_feature_component(feature, ui_framework)
        
        return components
    
    def generate_requirements(self, ui_framework: str) -> str:
        """
        Generate requirements.txt file.
        
        Args:
            ui_framework: UI framework being used
            
        Returns:
            Requirements file content
        """
        base_requirements = [
            "pillow>=8.0.0",  # For image handling
            "requests>=2.25.0",  # For HTTP requests
        ]
        
        # Add framework-specific requirements
        if ui_framework in self.framework_templates:
            framework_deps = self.framework_templates[ui_framework]["dependencies"]
            base_requirements.extend(framework_deps)
        
        # Add common desktop app requirements
        additional_requirements = [
            "pyinstaller>=4.0",  # For creating executables
            "setuptools>=45.0.0",  # For packaging
        ]
        
        all_requirements = base_requirements + additional_requirements
        
        return "\n".join(all_requirements)
    
    def generate_setup_files(self, app_name: str) -> Dict[str, str]:
        """
        Generate setup and configuration files.
        
        Args:
            app_name: Name of the application
            
        Returns:
            Dictionary of filename to content
        """
        setup_files = {}
        
        # Setup.py
        setup_py = f'''from setuptools import setup, find_packages

setup(
    name="{app_name.lower().replace(' ', '-')}",
    version="1.0.0",
    description="A desktop application created with Stable Desktop",
    author="Stable Desktop",
    packages=find_packages(),
    install_requires=[
        "pillow>=8.0.0",
        "requests>=2.25.0",
    ],
    entry_points={{
        "console_scripts": [
            "{app_name.lower().replace(' ', '-')}=main:main",
        ],
    }},
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)'''
        
        setup_files["setup.py"] = setup_py
        
        # PyInstaller spec file
        spec_file = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{app_name.lower().replace(" ", "_")}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)'''
        
        setup_files[f"{app_name.lower().replace(' ', '_')}.spec"] = spec_file
        
        return setup_files
    
    def _generate_default_structure(self,
                                   app_name: str,
                                   description: str,
                                   ui_framework: str,
                                   features: List[str]) -> Dict[str, Any]:
        """Generate default application structure."""
        return {
            "app_name": app_name,
            "ui_framework": ui_framework,
            "main_class": f"{app_name.replace(' ', '')}App",
            "components": ["main_window"] + [f"{f.lower().replace(' ', '_')}_component" for f in features],
            "file_structure": [
                "main.py",
                "ui/",
                "ui/main_window.py",
                "requirements.txt",
                "README.md"
            ]
        }
    
    def _generate_default_main_app(self,
                                  app_name: str,
                                  description: str,
                                  ui_framework: str,
                                  features: List[str]) -> str:
        """Generate default main application code."""
        
        if ui_framework == "tkinter":
            return f'''#!/usr/bin/env python3
"""
{app_name} - A desktop application created with Stable Desktop
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

class {app_name.replace(" ", "")}App:
    """Main application class for {app_name}"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("{app_name}")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        self.setup_style()
        
        # Create main interface
        self.create_widgets()
        
        # Center window
        self.center_window()
        
    def setup_style(self):
        """Configure application styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
    def create_widgets(self):
        """Create the main application widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="{app_name}", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(main_frame, text="{description}", wraplength=600)
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Features section
        if {features}:
            features_label = ttk.Label(main_frame, text="Features:", style='Header.TLabel')
            features_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
            
            for i, feature in enumerate({features}):
                feature_label = ttk.Label(main_frame, text=f"• {{feature}}")
                feature_label.grid(row=3+i, column=0, columnspan=2, sticky=tk.W, padx=(20, 0))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=100, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{{width}}x{{height}}+{{x}}+{{y}}')
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\nApplication interrupted by user")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {{e}}")
            print(f"Error: {{e}}")

def main():
    """Main entry point"""
    try:
        app = {app_name.replace(" ", "")}App()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        elif ui_framework == "customtkinter":
            return f'''#!/usr/bin/env python3
"""
{app_name} - A desktop application created with Stable Desktop
"""

import customtkinter as ctk
import sys
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class {app_name.replace(" ", "")}App:
    """Main application class for {app_name}"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("{app_name}")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)
        
        # Create main interface
        self.create_widgets()
        
        # Center window
        self.center_window()
        
    def create_widgets(self):
        """Create the main application widgets"""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="{app_name}", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Description
        desc_label = ctk.CTkLabel(main_frame, text="{description}", 
                                 wraplength=700, font=ctk.CTkFont(size=14))
        desc_label.pack(pady=(0, 20))
        
        # Features section
        if {features}:
            features_label = ctk.CTkLabel(main_frame, text="Features:", 
                                        font=ctk.CTkFont(size=16, weight="bold"))
            features_label.pack(pady=(0, 10))
            
            for feature in {features}:
                feature_label = ctk.CTkLabel(main_frame, text=f"• {{feature}}", 
                                           font=ctk.CTkFont(size=12))
                feature_label.pack(pady=2)
        
        # Status bar
        self.status_var = ctk.StringVar()
        self.status_var.set("Ready")
        status_bar = ctk.CTkLabel(main_frame, textvariable=self.status_var, 
                                 font=ctk.CTkFont(size=10))
        status_bar.pack(side="bottom", pady=(20, 0))
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{{width}}x{{height}}+{{x}}+{{y}}')
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\nApplication interrupted by user")
        except Exception as e:
            print(f"Error: {{e}}")

def main():
    """Main entry point"""
    try:
        app = {app_name.replace(" ", "")}App()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        else:
            # Generic template for other frameworks
            return f'''#!/usr/bin/env python3
"""
{app_name} - A desktop application created with Stable Desktop
"""

import sys
import os

class {app_name.replace(" ", "")}App:
    """Main application class for {app_name}"""
    
    def __init__(self):
        self.app_name = "{app_name}"
        self.description = "{description}"
        self.features = {features}
        
    def run(self):
        """Start the application"""
        print(f"Starting {{self.app_name}}...")
        print(f"Description: {{self.description}}")
        print(f"Features: {{', '.join(self.features)}}")
        print("Application framework: {ui_framework}")
        print("\\nThis is a template application. Please implement your specific functionality.")

def main():
    """Main entry point"""
    try:
        app = {app_name.replace(" ", "")}App()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    def _generate_default_ui_components(self,
                                       app_name: str,
                                       description: str,
                                       ui_framework: str,
                                       features: List[str]) -> Dict[str, str]:
        """Generate default UI components."""
        components = {}
        
        # Main window component
        components["main_window"] = self._generate_default_main_window(app_name, ui_framework)
        
        # Feature components
        for feature in features:
            component_name = f"{feature.lower().replace(' ', '_')}_component"
            components[component_name] = self._generate_default_feature_component(feature, ui_framework)
        
        return components
    
    def _generate_default_main_window(self, app_name: str, ui_framework: str) -> str:
        """Generate default main window component."""
        return f'''"""
Main window component for {app_name}
"""

class MainWindow:
    """Main window component"""
    
    def __init__(self, parent):
        self.parent = parent
        self.setup_window()
        
    def setup_window(self):
        """Setup the main window"""
        pass
        
    def create_menu(self):
        """Create application menu"""
        pass
        
    def create_toolbar(self):
        """Create application toolbar"""
        pass
'''
    
    def _generate_default_feature_component(self, feature: str, ui_framework: str) -> str:
        """Generate default feature component."""
        return f'''"""
{feature} component
"""

class {feature.replace(" ", "")}Component:
    """Component for {feature} functionality"""
    
    def __init__(self, parent):
        self.parent = parent
        self.setup_component()
        
    def setup_component(self):
        """Setup the component"""
        pass
        
    def handle_{feature.lower().replace(" ", "_")}_action(self):
        """Handle {feature} actions"""
        pass
''' 