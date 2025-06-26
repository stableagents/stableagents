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
from pathlib import Path
from typing import Optional

from .natural_language_desktop import NaturalLanguageDesktopGenerator


def get_gemini_api_key() -> Optional[str]:
    """Get Gemini API key from user input or environment."""
    # Try environment variable first
    api_key = os.getenv("GEMINI_API_KEY")
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


def create_app_interactive() -> bool:
    """Interactive app creation process."""
    print("🎯 Natural Language Desktop App Creator")
    print("=" * 50)
    print("Create desktop applications using natural language descriptions!")
    print()
    
    # Get API key
    api_key = get_gemini_api_key()
    if not api_key:
        return False
    
    # Initialize generator
    try:
        generator = NaturalLanguageDesktopGenerator(api_key)
        if not generator.gemini_provider or not generator.gemini_provider.available:
            print("❌ Failed to initialize Gemini provider")
            return False
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return False
    
    print("✅ Gemini API connected successfully!")
    print()
    
    # Get app description
    print("📝 Describe your application:")
    print("Example: 'Create a calculator app with scientific functions and a modern UI'")
    print("Example: 'Build a task manager with dark mode and data persistence'")
    print()
    
    try:
        description = input("Description: ").strip()
        if not description:
            print("❌ Description is required")
            return False
    except (KeyboardInterrupt, EOFError):
        print("\n👋 App creation cancelled.")
        return False
    
    # Get app name (optional)
    app_name = None
    try:
        app_name_input = input("App name (press Enter for auto-generate): ").strip()
        if app_name_input:
            app_name = app_name_input
    except (KeyboardInterrupt, EOFError):
        pass
    
    # Choose UI framework
    print("\n🎨 Choose UI Framework:")
    frameworks = generator.list_supported_frameworks()
    
    for i, framework in enumerate(frameworks, 1):
        status = "⭐ RECOMMENDED" if framework["recommended"] else ""
        print(f"{i}. {framework['display_name']} {status}")
        print(f"   {framework['description']}")
        print(f"   ✅ Pros: {', '.join(framework['pros'])}")
        print(f"   ❌ Cons: {', '.join(framework['cons'])}")
        print()
    
    try:
        choice = input("Enter your choice (1-3, default 1): ").strip()
        if not choice:
            choice = "1"
        
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(frameworks):
            ui_framework = frameworks[choice_idx]["name"]
        else:
            print("❌ Invalid choice, using CustomTkinter")
            ui_framework = "customtkinter"
    except (ValueError, KeyboardInterrupt, EOFError):
        print("❌ Invalid choice, using CustomTkinter")
        ui_framework = "customtkinter"
    
    # Create the app
    print(f"\n🚀 Creating '{app_name or 'Your App'}' with {ui_framework}...")
    print("This may take a few moments...")
    print()
    
    try:
        result = generator.create_app_from_description(
            description=description,
            app_name=app_name,
            ui_framework=ui_framework
        )
        
        if result.get("success"):
            print("🎉 App created successfully!")
            print(f"📁 Project location: {result['project_path']}")
            print(f"🚀 To run: cd {result['project_path']} && python main.py")
            
            # Show extracted features
            if "natural_language" in result:
                nl_data = result["natural_language"]
                print(f"\n📋 Generated name: {nl_data.get('generated_name', 'N/A')}")
                print(f"🔍 Extracted features: {', '.join(nl_data.get('extracted_features', []))}")
            
            # Ask if user wants to run the app
            try:
                run_app = input("\n🚀 Run the app now? (y/n): ").strip().lower()
                if run_app == 'y':
                    project_path = Path(result['project_path'])
                    if generator.desktop_builder:
                        success = generator.desktop_builder.run_app(project_path)
                        if success:
                            print("✅ App ran successfully!")
                        else:
                            print("❌ Failed to run app")
            except (KeyboardInterrupt, EOFError):
                pass
            
            return True
        else:
            print(f"❌ Failed to create app: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating app: {e}")
        return False


def create_demo_app() -> bool:
    """Create a demo application."""
    print("🎯 Creating Demo Application")
    print("=" * 40)
    
    # Get API key
    api_key = get_gemini_api_key()
    if not api_key:
        return False
    
    # Initialize generator
    try:
        generator = NaturalLanguageDesktopGenerator(api_key)
        if not generator.gemini_provider or not generator.gemini_provider.available:
            print("❌ Failed to initialize Gemini provider")
            return False
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return False
    
    print("✅ Gemini API connected successfully!")
    print("🚀 Creating TaskMaster demo application...")
    print("This may take a few moments...")
    print()
    
    try:
        result = generator.create_interactive_demo()
        
        if result.get("success"):
            print("🎉 Demo app created successfully!")
            print(f"📁 Project location: {result['project_path']}")
            print(f"🚀 To run: cd {result['project_path']} && python main.py")
            
            # Ask if user wants to run the app
            try:
                run_app = input("\n🚀 Run the demo app now? (y/n): ").strip().lower()
                if run_app == 'y':
                    project_path = Path(result['project_path'])
                    if generator.desktop_builder:
                        success = generator.desktop_builder.run_app(project_path)
                        if success:
                            print("✅ Demo app ran successfully!")
                        else:
                            print("❌ Failed to run demo app")
            except (KeyboardInterrupt, EOFError):
                pass
            
            return True
        else:
            print(f"❌ Failed to create demo app: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating demo app: {e}")
        return False


def list_frameworks() -> bool:
    """List supported UI frameworks."""
    print("🎨 Supported UI Frameworks")
    print("=" * 40)
    
    generator = NaturalLanguageDesktopGenerator()
    frameworks = generator.list_supported_frameworks()
    
    for framework in frameworks:
        status = "⭐ RECOMMENDED" if framework["recommended"] else ""
        print(f"\n📱 {framework['display_name']} {status}")
        print(f"   📝 {framework['description']}")
        print(f"   ✅ Pros: {', '.join(framework['pros'])}")
        print(f"   ❌ Cons: {', '.join(framework['cons'])}")
        print(f"   🎯 Best for: {', '.join(framework['best_for'])}")
    
    print(f"\n💡 Recommendation for beginners: CustomTkinter")
    print(f"💡 Recommendation for simple apps: Tkinter")
    print(f"💡 Recommendation for professional apps: PyQt")
    
    return True


def show_setup_instructions() -> bool:
    """Show setup instructions."""
    generator = NaturalLanguageDesktopGenerator()
    print(generator.get_setup_instructions())
    return True


def generate_code_interactive() -> bool:
    """Interactive code generation."""
    print("💻 Natural Language Code Generator")
    print("=" * 40)
    
    # Get API key
    api_key = get_gemini_api_key()
    if not api_key:
        return False
    
    # Initialize generator
    try:
        generator = NaturalLanguageDesktopGenerator(api_key)
        if not generator.gemini_provider or not generator.gemini_provider.available:
            print("❌ Failed to initialize Gemini provider")
            return False
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return False
    
    print("✅ Gemini API connected successfully!")
    print()
    
    # Get code description
    print("📝 Describe the code you want to generate:")
    print("Example: 'Create a login form with validation'")
    print("Example: 'Build a data visualization widget'")
    print()
    
    try:
        description = input("Description: ").strip()
        if not description:
            print("❌ Description is required")
            return False
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Code generation cancelled.")
        return False
    
    # Choose framework
    print("\n🎨 Choose Framework:")
    frameworks = generator.list_supported_frameworks()
    
    for i, framework in enumerate(frameworks, 1):
        print(f"{i}. {framework['display_name']}")
    
    try:
        choice = input("Enter your choice (1-3, default 1): ").strip()
        if not choice:
            choice = "1"
        
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(frameworks):
            framework = frameworks[choice_idx]["name"]
        else:
            print("❌ Invalid choice, using CustomTkinter")
            framework = "customtkinter"
    except (ValueError, KeyboardInterrupt, EOFError):
        print("❌ Invalid choice, using CustomTkinter")
        framework = "customtkinter"
    
    # Generate code
    print(f"\n🚀 Generating code with {framework}...")
    print("This may take a few moments...")
    print()
    
    try:
        code = generator.generate_code_from_prompt(
            prompt=description,
            framework=framework
        )
        
        print("🎉 Code generated successfully!")
        print("=" * 50)
        print(code)
        print("=" * 50)
        
        # Ask if user wants to save the code
        try:
            save_code = input("\n💾 Save code to file? (y/n): ").strip().lower()
            if save_code == 'y':
                filename = input("Filename (default: generated_code.py): ").strip()
                if not filename:
                    filename = "generated_code.py"
                
                with open(filename, 'w') as f:
                    f.write(code)
                print(f"✅ Code saved to {filename}")
        except (KeyboardInterrupt, EOFError):
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating code: {e}")
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
        return 0 if create_demo_app() else 1
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