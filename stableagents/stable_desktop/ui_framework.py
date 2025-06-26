"""
UI Framework - Handles different desktop UI frameworks.
"""

from typing import Dict, List, Any, Optional
from pathlib import Path


class UIFramework:
    """
    Manages different UI frameworks for desktop applications.
    
    Supports:
    - Tkinter (built-in)
    - PyQt5/PyQt6
    - Kivy
    - CustomTkinter
    - Custom frameworks
    """
    
    def __init__(self):
        """Initialize the UI framework manager."""
        self.frameworks = {
            "tkinter": {
                "name": "Tkinter",
                "description": "Python's standard GUI toolkit",
                "builtin": True,
                "dependencies": [],
                "pros": ["Built-in", "Simple", "Cross-platform", "No installation needed"],
                "cons": ["Basic styling", "Limited widgets", "Outdated look"],
                "best_for": ["Simple applications", "Quick prototypes", "Learning"],
                "template": "tkinter_template.py"
            },
            "customtkinter": {
                "name": "CustomTkinter",
                "description": "Modern and beautiful custom tkinter widgets",
                "builtin": False,
                "dependencies": ["customtkinter"],
                "pros": ["Modern look", "Easy to use", "Built on tkinter", "Beautiful widgets"],
                "cons": ["Newer library", "Limited widget set", "External dependency"],
                "best_for": ["Modern applications", "Professional look", "Easy development"],
                "template": "customtkinter_template.py"
            },
            "pyqt": {
                "name": "PyQt",
                "description": "Qt framework for Python",
                "builtin": False,
                "dependencies": ["PyQt5", "PyQt5-tools"],
                "pros": ["Professional", "Rich widgets", "Modern look", "Extensive features"],
                "cons": ["Complex", "Large size", "License considerations", "Steep learning curve"],
                "best_for": ["Complex applications", "Professional software", "Rich interfaces"],
                "template": "pyqt_template.py"
            },
            "kivy": {
                "name": "Kivy",
                "description": "Modern library for multi-touch applications",
                "builtin": False,
                "dependencies": ["kivy"],
                "pros": ["Modern", "Touch-friendly", "Cross-platform", "Mobile support"],
                "cons": ["Learning curve", "Different from traditional GUIs", "Complex setup"],
                "best_for": ["Touch applications", "Mobile-like interfaces", "Modern apps"],
                "template": "kivy_template.py"
            },
            "wxpython": {
                "name": "wxPython",
                "description": "Python bindings for wxWidgets",
                "builtin": False,
                "dependencies": ["wxPython"],
                "pros": ["Native look", "Mature", "Cross-platform", "Rich widgets"],
                "cons": ["Complex", "Large size", "Installation issues"],
                "best_for": ["Native-looking apps", "Traditional desktop apps"],
                "template": "wxpython_template.py"
            }
        }
    
    def get_framework_info(self, framework_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a UI framework.
        
        Args:
            framework_name: Name of the framework
            
        Returns:
            Framework information or None if not found
        """
        return self.frameworks.get(framework_name.lower())
    
    def list_frameworks(self) -> List[Dict[str, Any]]:
        """
        List all available UI frameworks.
        
        Returns:
            List of framework information
        """
        return list(self.frameworks.values())
    
    def check_framework_availability(self, framework_name: str) -> Dict[str, Any]:
        """
        Check if a framework is available and installed.
        
        Args:
            framework_name: Name of the framework
            
        Returns:
            Availability status
        """
        framework_info = self.get_framework_info(framework_name)
        if not framework_info:
            return {
                "available": False,
                "error": f"Framework '{framework_name}' not found"
            }
        
        # Check if it's built-in
        if framework_info["builtin"]:
            try:
                if framework_name == "tkinter":
                    import tkinter
                    return {
                        "available": True,
                        "builtin": True,
                        "version": "Built-in"
                    }
            except ImportError:
                return {
                    "available": False,
                    "error": "Built-in framework not available"
                }
        
        # Check external dependencies
        missing_deps = []
        for dep in framework_info["dependencies"]:
            try:
                __import__(dep.lower().replace("-", "_"))
            except ImportError:
                missing_deps.append(dep)
        
        if missing_deps:
            return {
                "available": False,
                "error": f"Missing dependencies: {', '.join(missing_deps)}",
                "missing_deps": missing_deps
            }
        
        return {
            "available": True,
            "builtin": False,
            "dependencies": framework_info["dependencies"]
        }
    
    def get_recommended_framework(self, 
                                 app_type: str = "general",
                                 complexity: str = "simple") -> str:
        """
        Get recommended framework based on app type and complexity.
        
        Args:
            app_type: Type of application (general, modern, professional, touch)
            complexity: Complexity level (simple, moderate, complex)
            
        Returns:
            Recommended framework name
        """
        recommendations = {
            "general": {
                "simple": "tkinter",
                "moderate": "customtkinter",
                "complex": "pyqt"
            },
            "modern": {
                "simple": "customtkinter",
                "moderate": "customtkinter",
                "complex": "kivy"
            },
            "professional": {
                "simple": "customtkinter",
                "moderate": "pyqt",
                "complex": "pyqt"
            },
            "touch": {
                "simple": "kivy",
                "moderate": "kivy",
                "complex": "kivy"
            }
        }
        
        return recommendations.get(app_type, {}).get(complexity, "tkinter")
    
    def generate_framework_template(self, 
                                   framework_name: str,
                                   app_name: str,
                                   features: List[str]) -> str:
        """
        Generate a template for a specific framework.
        
        Args:
            framework_name: Name of the framework
            app_name: Name of the application
            features: List of features
            
        Returns:
            Template code as string
        """
        framework_info = self.get_framework_info(framework_name)
        if not framework_info:
            return self._generate_generic_template(app_name, features)
        
        if framework_name == "tkinter":
            return self._generate_tkinter_template(app_name, features)
        elif framework_name == "customtkinter":
            return self._generate_customtkinter_template(app_name, features)
        elif framework_name == "pyqt":
            return self._generate_pyqt_template(app_name, features)
        elif framework_name == "kivy":
            return self._generate_kivy_template(app_name, features)
        else:
            return self._generate_generic_template(app_name, features)
    
    def _generate_tkinter_template(self, app_name: str, features: List[str]) -> str:
        """Generate Tkinter template."""
        return f'''#!/usr/bin/env python3
"""
{app_name} - Tkinter Application
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys

class {app_name.replace(" ", "")}App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("{app_name}")
        self.root.geometry("800x600")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="{app_name}", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Features
        for feature in {features}:
            feature_btn = ttk.Button(main_frame, text=feature, 
                                   command=lambda f=feature: self.handle_feature(f))
            feature_btn.pack(pady=5)
        
    def handle_feature(self, feature):
        messagebox.showinfo("Feature", f"Handling feature: {{feature}}")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = {app_name.replace(" ", "")}App()
    app.run()
'''
    
    def _generate_customtkinter_template(self, app_name: str, features: List[str]) -> str:
        """Generate CustomTkinter template."""
        return f'''#!/usr/bin/env python3
"""
{app_name} - CustomTkinter Application
"""

import customtkinter as ctk
import sys

# Configure appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class {app_name.replace(" ", "")}App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("{app_name}")
        self.root.geometry("900x600")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(main_frame, text="{app_name}", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(20, 30))
        
        # Features
        for feature in {features}:
            feature_btn = ctk.CTkButton(main_frame, text=feature,
                                      command=lambda f=feature: self.handle_feature(f))
            feature_btn.pack(pady=10)
        
    def handle_feature(self, feature):
        # Handle feature action
        print(f"Handling feature: {{feature}}")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = {app_name.replace(" ", "")}App()
    app.run()
'''
    
    def _generate_pyqt_template(self, app_name: str, features: List[str]) -> str:
        """Generate PyQt template."""
        return f'''#!/usr/bin/env python3
"""
{app_name} - PyQt Application
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class {app_name.replace(" ", "")}App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("{app_name}")
        self.setGeometry(100, 100, 800, 600)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel("{app_name}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Features
        for feature in {features}:
            feature_btn = QPushButton(feature)
            feature_btn.clicked.connect(lambda checked, f=feature: self.handle_feature(f))
            layout.addWidget(feature_btn)
        
    def handle_feature(self, feature):
        print(f"Handling feature: {{feature}}")
        
def main():
    app = QApplication(sys.argv)
    window = {app_name.replace(" ", "")}App()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
'''
    
    def _generate_kivy_template(self, app_name: str, features: List[str]) -> str:
        """Generate Kivy template."""
        return f'''#!/usr/bin/env python3
"""
{app_name} - Kivy Application
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class {app_name.replace(" ", "")}App(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(text="{app_name}", size_hint_y=None, height=50)
        title.font_size = '24sp'
        layout.add_widget(title)
        
        # Features
        for feature in {features}:
            feature_btn = Button(text=feature, size_hint_y=None, height=50)
            feature_btn.bind(on_press=lambda btn, f=feature: self.handle_feature(f))
            layout.add_widget(feature_btn)
        
        return layout
        
    def handle_feature(self, feature):
        print(f"Handling feature: {{feature}}")

if __name__ == "__main__":
    {app_name.replace(" ", "")}App().run()
'''
    
    def _generate_generic_template(self, app_name: str, features: List[str]) -> str:
        """Generate generic template."""
        return f'''#!/usr/bin/env python3
"""
{app_name} - Desktop Application
"""

import sys

class {app_name.replace(" ", "")}App:
    def __init__(self):
        self.app_name = "{app_name}"
        self.features = {features}
        
    def run(self):
        print(f"Starting {{self.app_name}}...")
        print(f"Features: {{', '.join(self.features)}}")
        print("This is a template application.")

if __name__ == "__main__":
    app = {app_name.replace(" ", "")}App()
    app.run()
''' 