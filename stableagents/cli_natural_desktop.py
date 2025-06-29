#!/usr/bin/env python3
"""
CLI for Natural Language Desktop App Generator

This module provides a command-line interface for creating desktop applications
using natural language descriptions and Google Gemini AI.
"""

import argparse
import sys
import os
import getpass
import json
from pathlib import Path
from typing import Optional

from .natural_language_desktop import NaturalLanguageDesktopGenerator


def get_gemini_api_key() -> Optional[str]:
    """Get Gemini API key from user input or environment."""
    # Try environment variable first
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key:
        return api_key
    
    # Try to get from user input
    try:
        print("🔑 Google Gemini API Key Required")
        print("=" * 40)
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        print()
        
        api_key = getpass.getpass("Enter your Gemini API key: ")
        if api_key.strip():
            return api_key.strip()
        else:
            print("❌ No API key provided")
            return None
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Setup cancelled.")
        return None


def save_api_key_to_config(api_key: str) -> bool:
    """Save API key to the stableagents configuration."""
    try:
        config_dir = os.path.expanduser("~/.stableagents")
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, "api_keys.json")
        
        # Load existing config or create new one
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        # Update with new API key
        config["gemini"] = api_key
        config["active_provider"] = "google"  # Set as active provider
        
        # Save updated config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ API key saved to configuration")
        return True
        
    except Exception as e:
        print(f"⚠️ Could not save API key to config: {e}")
        return False


def check_and_setup_api_key() -> Optional[str]:
    """Check if API key is available and working, prompt for new one if needed."""
    print("🔍 Checking API key...")
    
    # Try to get existing API key
    api_key = get_gemini_api_key()
    if not api_key:
        print("❌ No API key found")
        return None
    
    # Test the API key by trying to initialize the generator
    try:
        print("🧪 Testing API key...")
        generator = NaturalLanguageDesktopGenerator(api_key)
        
        # Try a simple test call
        test_response = generator.gemini.generate_text("Hello")
        if test_response and not test_response.startswith("Error:"):
            print("✅ API key is working!")
            
            # Try a more complex test to ensure it works for app generation
            print("🧪 Testing app generation capability...")
            complex_test = generator.gemini.generate_text("Create a simple Python function that adds two numbers")
            if complex_test and not complex_test.startswith("Error:"):
                print("✅ API key supports app generation!")
                return api_key
            else:
                print("❌ API key works for simple calls but fails for complex generation")
                raise ValueError("API key has limited capabilities")
        else:
            print("❌ API key test failed")
            raise ValueError("API key test failed")
            
    except Exception as e:
        print(f"❌ API key error: {str(e)}")
        print("\n🔄 Let's set up a new API key...")
        
        # Prompt for new API key
        new_api_key = get_gemini_api_key()
        if new_api_key:
            # Save to config
            save_api_key_to_config(new_api_key)
            return new_api_key
        else:
            return None


def create_app_interactive() -> bool:
    """Interactive app creation with enhanced Gemini integration."""
    print("\n🚀 Natural Language Desktop App Generator")
    print("=" * 50)
    print("Create beautiful desktop applications using natural language and Google Gemini AI!")
    print()
    
    # Check and setup API key
    api_key = check_and_setup_api_key()
    if not api_key:
        print("❌ Cannot proceed without a valid API key")
        return False
    
    try:
        # Initialize the generator with the verified API key
        generator = NaturalLanguageDesktopGenerator(api_key)
        print("✅ Gemini AI initialized successfully!")
        
        # Get app description
        print("\n📝 Describe your desktop application:")
        print("💡 Be specific about features, UI elements, and functionality")
        print("💡 Example: 'Create a modern calculator with scientific functions, dark mode, and history'")
        print()
        
        description = input("Description: ").strip()
        if not description:
            print("❌ Description is required")
            return False
        
        # Get app name (optional)
        print("\n📱 App Name (optional, will be generated if not provided):")
        app_name = input("Name: ").strip()
        if not app_name:
            app_name = None
        
        # Choose framework
        ui_framework = _select_framework(generator)
        
        print(f"\n🚀 Creating {ui_framework} application...")
        print("⏳ This may take a moment as Gemini AI generates your application...")
        
        # Create the application
        result = generator.create_app_from_description(
            description=description,
            app_name=app_name,
            ui_framework=ui_framework
        )
        
        if result.get("success"):
            print("\n🎉 Application created successfully!")
            print(f"📁 Location: {result['project_path']}")
            print(f"🚀 To run: cd {result['project_path']} && python main.py")
            
            # Ask if user wants to run the app
            run_app = input("\nWould you like to run the application now? (y/n): ").strip().lower()
            if run_app in ['y', 'yes']:
                print("🚀 Starting application...")
                generator.run_app(result['project_path'])
            
            return True
        else:
            print(f"❌ Failed to create application: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def create_enhanced_demo_app() -> bool:
    """Create an enhanced demo application showcasing the capabilities."""
    print("\n🎯 Enhanced Demo Application")
    print("=" * 40)
    print("Creating a comprehensive demo showcasing Natural Language Desktop capabilities...")
    
    # Check and setup API key
    api_key = check_and_setup_api_key()
    if not api_key:
        print("❌ Cannot proceed without a valid API key")
        return False
    
    try:
        generator = NaturalLanguageDesktopGenerator(api_key)
        
        # Create the demo app
        result = generator.create_interactive_demo()
        
        if result.get("success"):
            print("\n🎉 Enhanced demo application created successfully!")
            print(f"📁 Location: {result['project_path']}")
            print(f"🚀 To run: cd {result['project_path']} && python main.py")
            
            # Ask if user wants to run the demo
            run_demo = input("\nWould you like to run the demo application now? (y/n): ").strip().lower()
            if run_demo in ['y', 'yes']:
                print("🚀 Starting demo application...")
                generator.run_app(result['project_path'])
            
            return True
        else:
            print(f"❌ Failed to create demo app: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def list_frameworks() -> bool:
    """List supported UI frameworks."""
    print("🎨 Supported UI Frameworks")
    print("=" * 40)
    
    try:
        # Try to initialize generator, but don't fail if API key is missing
        api_key = get_gemini_api_key()
        if api_key:
            generator = NaturalLanguageDesktopGenerator(api_key)
            framework_descriptions = generator.get_framework_descriptions()
        else:
            # Fallback to hardcoded list if no API key
            framework_descriptions = [
                "customtkinter - Modern, beautiful UI with dark mode support",
                "tkinter - Standard Python GUI framework", 
                "pyqt - Professional Qt-based framework"
            ]
    except Exception as e:
        print(f"⚠️ Could not initialize generator: {e}")
        # Fallback to hardcoded list
        framework_descriptions = [
            "customtkinter - Modern, beautiful UI with dark mode support",
            "tkinter - Standard Python GUI framework",
            "pyqt - Professional Qt-based framework"
        ]
    
    for i, description in enumerate(framework_descriptions, 1):
        print(f"\n{i}. {description}")
    
    print("\n💡 Recommendation for beginners: CustomTkinter (modern and easy)")
    print("💡 Recommendation for simple apps: Tkinter (built-in)")
    print("💡 Recommendation for professional apps: PyQt (powerful)")
    
    return True


def _select_framework(generator) -> str:
    """Helper function to select a framework with descriptions."""
    print("\n🎨 Choose UI Framework:")
    framework_descriptions = generator.get_framework_descriptions()
    framework_names = generator.list_frameworks()
    
    for i, description in enumerate(framework_descriptions, 1):
        print(f"  {i}. {description}")
    
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(framework_names)}): ").strip()
            framework_index = int(choice) - 1
            if 0 <= framework_index < len(framework_names):
                return framework_names[framework_index]
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a number.")


def show_setup_instructions() -> bool:
    """Show setup instructions."""
    try:
        api_key = get_gemini_api_key()
        if api_key:
            generator = NaturalLanguageDesktopGenerator(api_key)
            print(generator.get_setup_instructions())
        else:
            # Show basic setup instructions without generator
            print("""
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
Run the CLI and it will prompt you for the API key automatically.

Option 3: Manual Configuration
Edit ~/.stableagents/api_keys.json and add:
{
  "gemini": "your-api-key-here",
  "active_provider": "google"
}

📦 Installation:
```bash
pip install stableagents
```

🎯 Usage:
```bash
python -m stableagents.cli natural-desktop create
```
            """)
    except Exception as e:
        print(f"⚠️ Could not load setup instructions: {e}")
        print("Please check your API key configuration.")
    
    return True


def generate_code_interactive() -> bool:
    """Interactive code generation for specific UI components."""
    print("\n🎨 Code Generation Tool")
    print("=" * 30)
    print("Generate specific UI components or functionality using natural language!")
    print()
    
    # Check and setup API key
    api_key = check_and_setup_api_key()
    if not api_key:
        print("❌ Cannot proceed without a valid API key")
        return False
    
    try:
        generator = NaturalLanguageDesktopGenerator(api_key)
        
        # Get code prompt
        print("📝 Describe the UI component or functionality you want to generate:")
        print("💡 Examples:")
        print("  - 'Create a login form with username and password fields'")
        print("  - 'Build a data visualization widget with charts'")
        print("  - 'Make a file upload component with drag and drop'")
        print()
        
        prompt = input("Description: ").strip()
        if not prompt:
            print("❌ Description is required")
            return False
        
        # Choose framework
        ui_framework = _select_framework(generator)
        
        print(f"\n🎨 Generating {ui_framework} code...")
        print("⏳ This may take a moment...")
        
        # Generate the code
        code = generator.generate_code_from_prompt(prompt, ui_framework)
        
        print("\n✅ Code generated successfully!")
        print("\n📋 Generated Code:")
        print("=" * 50)
        print(code)
        print("=" * 50)
        
        # Ask if user wants to save the code
        save_code = input("\nWould you like to save this code to a file? (y/n): ").strip().lower()
        if save_code in ['y', 'yes']:
            filename = input("Enter filename (e.g., my_component.py): ").strip()
            if not filename.endswith('.py'):
                filename += '.py'
            
            try:
                with open(filename, 'w') as f:
                    f.write(code)
                print(f"✅ Code saved to {filename}")
            except Exception as e:
                print(f"❌ Error saving file: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Natural Language Desktop App Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s create          # Interactive app creation
  %(prog)s demo            # Create demo application
  %(prog)s frameworks      # List supported frameworks
  %(prog)s setup           # Show setup instructions
  %(prog)s code            # Generate code from description
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create app command
    create_parser = subparsers.add_parser('create', help='Create a new desktop application')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Create a demo application')
    
    # Frameworks command
    frameworks_parser = subparsers.add_parser('frameworks', help='List supported UI frameworks')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Show setup instructions')
    
    # Code generation command
    code_parser = subparsers.add_parser('code', help='Generate code from description')
    
    args = parser.parse_args()
    
    if not args.command:
        # No command provided, run interactive mode
        return 0 if create_app_interactive() else 1
    
    # Handle commands
    if args.command == 'create':
        return 0 if create_app_interactive() else 1
    elif args.command == 'demo':
        return 0 if create_enhanced_demo_app() else 1
    elif args.command == 'frameworks':
        return 0 if list_frameworks() else 1
    elif args.command == 'setup':
        return 0 if show_setup_instructions() else 1
    elif args.command == 'code':
        return 0 if generate_code_interactive() else 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main()) 