#!/usr/bin/env python3
"""
Natural Language Desktop App Generator

This module allows users to create desktop applications using natural language
descriptions and Google Gemini AI. It generates modern, native desktop apps
without using Electron.
"""

import os
import json
import subprocess
import tempfile
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from .ai_providers import GoogleProvider
from .stable_desktop.desktop_builder import DesktopBuilder


class NaturalLanguageDesktopGenerator:
    """
    Generates desktop applications from natural language descriptions using Google Gemini.
    
    Features:
    - Natural language to desktop app conversion
    - Modern UI frameworks (CustomTkinter, Tkinter, PyQt)
    - Code generation with Gemini AI
    - Automatic dependency management
    - Cross-platform support
    """
    
    def __init__(self, gemini_api_key: Optional[str] = None):
        """
        Initialize the natural language desktop generator.
        
        Args:
            gemini_api_key: Google Gemini API key
        """
        self.logger = logging.getLogger(__name__)
        self.gemini_provider = None
        self.desktop_builder = None
        
        # Initialize Gemini provider
        if gemini_api_key:
            self.gemini_provider = GoogleProvider(gemini_api_key)
            if self.gemini_provider.available:
                self.desktop_builder = DesktopBuilder(self.gemini_provider)
                self.logger.info("Natural Language Desktop Generator initialized with Gemini")
            else:
                self.logger.error("Failed to initialize Gemini provider")
        else:
            self.logger.warning("No Gemini API key provided. Some features may be limited.")
    
    def create_app_from_description(self, 
                                   description: str,
                                   app_name: Optional[str] = None,
                                   ui_framework: str = "customtkinter",
                                   output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """
        Create a desktop application from a natural language description.
        
        Args:
            description: Natural language description of the app
            app_name: Name for the application (auto-generated if not provided)
            ui_framework: UI framework to use (customtkinter, tkinter, pyqt)
            output_dir: Output directory for the project
            
        Returns:
            Dictionary with project information and status
        """
        if not self.gemini_provider or not self.gemini_provider.available:
            return {
                "success": False,
                "error": "Google Gemini not available. Please provide a valid API key."
            }
        
        try:
            # Generate app name if not provided
            if not app_name:
                app_name = self._generate_app_name(description)
            
            # Analyze description and extract features
            features = self._analyze_description(description)
            
            # Generate enhanced description
            enhanced_description = self._enhance_description(description, features)
            
            # Create the application
            result = self.desktop_builder.create_app(
                app_name=app_name,
                description=enhanced_description,
                ui_framework=ui_framework,
                features=features,
                output_dir=output_dir
            )
            
            if result.get("success"):
                # Add natural language metadata
                result["natural_language"] = {
                    "original_description": description,
                    "enhanced_description": enhanced_description,
                    "extracted_features": features,
                    "generated_name": app_name
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error creating app from description: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_app_name(self, description: str) -> str:
        """Generate an appropriate app name from the description."""
        prompt = f"""
        Based on this description, generate a short, catchy app name (2-3 words max):
        
        Description: {description}
        
        Return only the app name, nothing else.
        """
        
        try:
            name = self.gemini_provider.generate_text(prompt, max_tokens=50)
            # Clean up the name
            name = name.strip().replace('"', '').replace("'", "")
            if len(name) > 50:
                name = name[:50]
            return name or "MyApp"
        except Exception as e:
            self.logger.error(f"Error generating app name: {e}")
            return "MyApp"
    
    def _analyze_description(self, description: str) -> List[str]:
        """Analyze the description and extract features."""
        prompt = f"""
        Analyze this app description and extract the main features that should be implemented:
        
        Description: {description}
        
        Return a JSON array of feature strings. Focus on:
        - User interface elements (buttons, forms, lists, etc.)
        - Core functionality (data storage, calculations, file operations, etc.)
        - User interactions (clicking, typing, dragging, etc.)
        - Visual elements (charts, images, animations, etc.)
        
        Example: ["User authentication", "Data input forms", "File upload", "Data visualization", "Settings panel"]
        
        Return only valid JSON array.
        """
        
        try:
            response = self.gemini_provider.generate_text(prompt, max_tokens=500)
            features = json.loads(response)
            if isinstance(features, list):
                return features
            else:
                return []
        except Exception as e:
            self.logger.error(f"Error analyzing description: {e}")
            return ["Basic UI", "User input", "Data display"]
    
    def _enhance_description(self, description: str, features: List[str]) -> str:
        """Enhance the description with technical details."""
        prompt = f"""
        Enhance this app description with technical implementation details:
        
        Original Description: {description}
        Extracted Features: {', '.join(features)}
        
        Create a detailed technical description that includes:
        - Specific UI components needed
        - Data structures and storage requirements
        - User interaction patterns
        - Error handling considerations
        - Performance requirements
        
        Make it comprehensive for code generation.
        """
        
        try:
            enhanced = self.gemini_provider.generate_text(prompt, max_tokens=1000)
            return enhanced or description
        except Exception as e:
            self.logger.error(f"Error enhancing description: {e}")
            return description
    
    def generate_code_from_prompt(self, 
                                 prompt: str,
                                 code_type: str = "python",
                                 framework: str = "customtkinter") -> str:
        """
        Generate code from a natural language prompt.
        
        Args:
            prompt: Natural language description of the code needed
            code_type: Type of code to generate (python, javascript, etc.)
            framework: Framework to use (customtkinter, tkinter, pyqt)
            
        Returns:
            Generated code as string
        """
        if not self.gemini_provider or not self.gemini_provider.available:
            return "# Error: Google Gemini not available"
        
        code_prompt = f"""
        Generate {code_type} code using {framework} framework for:
        
        {prompt}
        
        Requirements:
        - Use {framework} for the UI
        - Include proper error handling
        - Add comments explaining the code
        - Make it production-ready
        - Follow Python best practices
        
        Return only the code, no explanations.
        """
        
        try:
            return self.gemini_provider.generate_text(code_prompt, max_tokens=2000)
        except Exception as e:
            self.logger.error(f"Error generating code: {e}")
            return f"# Error generating code: {e}"
    
    def create_interactive_demo(self) -> Dict[str, Any]:
        """Create an interactive demo application."""
        demo_description = """
        Create a modern task management application with the following features:
        - Beautiful modern UI with dark/light mode toggle
        - Add, edit, and delete tasks
        - Mark tasks as complete/incomplete
        - Task categories and priority levels
        - Search and filter tasks
        - Data persistence (save/load tasks)
        - Responsive design that works on different screen sizes
        - Professional animations and transitions
        """
        
        return self.create_app_from_description(
            description=demo_description,
            app_name="TaskMaster",
            ui_framework="customtkinter"
        )
    
    def list_supported_frameworks(self) -> List[Dict[str, Any]]:
        """List supported UI frameworks with descriptions."""
        return [
            {
                "name": "customtkinter",
                "display_name": "CustomTkinter",
                "description": "Modern and beautiful custom tkinter widgets",
                "pros": ["Modern look", "Easy to use", "Built on tkinter", "Beautiful widgets"],
                "cons": ["Newer library", "Limited widget set"],
                "best_for": ["Modern applications", "Professional look", "Quick development"],
                "recommended": True
            },
            {
                "name": "tkinter",
                "display_name": "Tkinter",
                "description": "Python's standard GUI toolkit",
                "pros": ["Built-in", "Simple", "Cross-platform", "No installation needed"],
                "cons": ["Basic styling", "Limited widgets", "Outdated look"],
                "best_for": ["Simple applications", "Quick prototypes", "Learning"],
                "recommended": False
            },
            {
                "name": "pyqt",
                "display_name": "PyQt",
                "description": "Qt framework for Python",
                "pros": ["Professional", "Rich widgets", "Modern look", "Extensive features"],
                "cons": ["Complex", "Large size", "License considerations"],
                "best_for": ["Professional applications", "Complex UIs", "Commercial software"],
                "recommended": False
            }
        ]
    
    def get_setup_instructions(self) -> str:
        """Get setup instructions for the natural language desktop generator."""
        return """
🎯 Natural Language Desktop App Generator Setup
===============================================

1. 🔑 Get Google Gemini API Key:
   • Visit: https://makersuite.google.com/app/apikey
   • Create a new API key
   • Copy the key for use in the application

2. 📦 Install Dependencies:
   • pip install google-generativeai
   • pip install customtkinter
   • pip install stableagents-ai

3. 🚀 Start Creating Apps:
   • Use the create_app_from_description() method
   • Provide natural language descriptions
   • Choose your preferred UI framework
   • Let Gemini generate the code for you!

4. 💡 Example Usage:
   ```python
   generator = NaturalLanguageDesktopGenerator("your-gemini-api-key")
   result = generator.create_app_from_description(
       "Create a calculator app with scientific functions"
   )
   ```

5. 🎨 Supported Frameworks:
   • CustomTkinter (Recommended) - Modern, beautiful UI
   • Tkinter - Built-in, simple
   • PyQt - Professional, feature-rich

6. 🔧 Advanced Features:
   • Code generation from prompts
   • Interactive demos
   • Framework recommendations
   • Automatic dependency management
        """ 