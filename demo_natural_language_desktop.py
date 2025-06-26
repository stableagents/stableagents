#!/usr/bin/env python3
"""
Natural Language Desktop App Generator - Complete Demo

This script demonstrates the complete workflow of creating desktop applications
using natural language descriptions and Google Gemini AI.
"""

import os
import sys
import getpass
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    """Print a beautiful banner."""
    print("🎯" + "="*60 + "🎯")
    print("🚀 Natural Language Desktop App Generator Demo")
    print("🎯" + "="*60 + "🎯")
    print()
    print("✨ Create desktop applications using plain English descriptions")
    print("🤖 Powered by Google Gemini AI")
    print("🎨 Modern UI frameworks (CustomTkinter, Tkinter, PyQt)")
    print("⚡ No Electron required - lightweight native Python apps")
    print()

def get_gemini_api_key():
    """Get Gemini API key from user."""
    print("🔑 Google Gemini API Key Required")
    print("=" * 40)
    print("Get your API key from: https://makersuite.google.com/app/apikey")
    print()
    
    # Try environment variable first
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("✅ Found API key in environment variable")
        return api_key
    
    try:
        api_key = getpass.getpass("Enter your Gemini API key: ")
        if api_key.strip():
            return api_key.strip()
        else:
            print("❌ No API key provided")
            return None
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Demo cancelled.")
        return None

def demo_basic_functionality():
    """Demo basic functionality without API key."""
    print("🔍 Basic Functionality Demo (No API Key Required)")
    print("=" * 50)
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        # Initialize without API key
        generator = NaturalLanguageDesktopGenerator()
        print("✅ Generator initialized successfully")
        
        # List supported frameworks
        frameworks = generator.list_supported_frameworks()
        print(f"✅ Found {len(frameworks)} supported frameworks:")
        for framework in frameworks:
            status = "⭐ RECOMMENDED" if framework["recommended"] else ""
            print(f"   - {framework['display_name']} {status}")
        
        # Show setup instructions
        instructions = generator.get_setup_instructions()
        print(f"✅ Setup instructions available ({len(instructions)} characters)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in basic functionality demo: {e}")
        return False

def demo_with_api_key(api_key):
    """Demo with actual API key."""
    print("\n🚀 Full Functionality Demo (With API Key)")
    print("=" * 50)
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        # Initialize with API key
        generator = NaturalLanguageDesktopGenerator(api_key)
        print("✅ Generator initialized with API key")
        
        if not generator.gemini_provider or not generator.gemini_provider.available:
            print("❌ Gemini provider not available")
            return False
        
        print("✅ Gemini API connected successfully")
        
        # Test code generation
        print("\n💻 Testing Code Generation...")
        code = generator.generate_code_from_prompt(
            prompt="Create a simple login form with username and password fields",
            framework="customtkinter"
        )
        
        if code and not code.startswith("# Error"):
            print("✅ Code generation successful")
            print("Generated code preview:")
            print("-" * 40)
            lines = code.split('\n')[:10]  # Show first 10 lines
            for line in lines:
                print(f"  {line}")
            if len(code.split('\n')) > 10:
                print("  ...")
            print("-" * 40)
        else:
            print("❌ Code generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error in full functionality demo: {e}")
        return False

def demo_app_creation(api_key):
    """Demo creating a complete application."""
    print("\n🎯 Application Creation Demo")
    print("=" * 40)
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        generator = NaturalLanguageDesktopGenerator(api_key)
        
        # Simple calculator app description
        description = """
        Create a simple calculator application with:
        - Modern UI with dark/light mode toggle
        - Basic arithmetic operations (add, subtract, multiply, divide)
        - Clear and equals buttons
        - Number display
        - Responsive design
        """
        
        print("📝 Creating calculator app from description...")
        print(f"Description: {description.strip()}")
        print()
        
        result = generator.create_app_from_description(
            description=description,
            app_name="SimpleCalculator",
            ui_framework="customtkinter"
        )
        
        if result.get("success"):
            print("🎉 Calculator app created successfully!")
            print(f"📁 Project location: {result['project_path']}")
            print(f"🚀 To run: cd {result['project_path']} && python main.py")
            
            # Show extracted features
            if "natural_language" in result:
                nl_data = result["natural_language"]
                print(f"\n📋 Generated name: {nl_data.get('generated_name', 'N/A')}")
                print(f"🔍 Extracted features: {', '.join(nl_data.get('extracted_features', []))}")
            
            return True
        else:
            print(f"❌ Failed to create app: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error in app creation demo: {e}")
        return False

def show_usage_examples():
    """Show usage examples."""
    print("\n📚 Usage Examples")
    print("=" * 30)
    
    examples = [
        {
            "title": "CLI Usage",
            "commands": [
                "stableagents-ai natural-desktop create",
                "stableagents-ai natural-desktop demo",
                "stableagents-ai natural-desktop frameworks",
                "stableagents-ai natural-desktop setup"
            ]
        },
        {
            "title": "Python API Usage",
            "code": '''
from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator

# Initialize generator
generator = NaturalLanguageDesktopGenerator("your-api-key")

# Create app from description
result = generator.create_app_from_description(
    description="Create a modern task manager with dark mode",
    app_name="TaskMaster",
    ui_framework="customtkinter"
)

# Generate code component
code = generator.generate_code_from_prompt(
    prompt="Create a data visualization widget",
    framework="customtkinter"
)
'''
        }
    ]
    
    for example in examples:
        print(f"\n📖 {example['title']}")
        print("-" * 20)
        
        if "commands" in example:
            for cmd in example["commands"]:
                print(f"  $ {cmd}")
        
        if "code" in example:
            print(example["code"])

def main():
    """Main demo function."""
    print_banner()
    
    # Demo basic functionality (no API key required)
    if not demo_basic_functionality():
        print("❌ Basic functionality demo failed")
        return 1
    
    # Ask if user wants to continue with API key
    try:
        continue_demo = input("\n🚀 Continue with API key demo? (y/n): ").strip().lower()
        if continue_demo != 'y':
            show_usage_examples()
            return 0
    except (KeyboardInterrupt, EOFError):
        show_usage_examples()
        return 0
    
    # Get API key
    api_key = get_gemini_api_key()
    if not api_key:
        print("❌ API key required for full demo")
        show_usage_examples()
        return 1
    
    # Demo with API key
    if not demo_with_api_key(api_key):
        print("❌ Full functionality demo failed")
        return 1
    
    # Ask if user wants to create an app
    try:
        create_app = input("\n🎯 Create a demo application? (y/n): ").strip().lower()
        if create_app == 'y':
            if not demo_app_creation(api_key):
                print("❌ App creation demo failed")
                return 1
    except (KeyboardInterrupt, EOFError):
        pass
    
    # Show usage examples
    show_usage_examples()
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 Next steps:")
    print("   1. Get your own API key from https://makersuite.google.com/app/apikey")
    print("   2. Try: stableagents-ai natural-desktop create")
    print("   3. Explore the examples in examples/natural_language_desktop_demo.py")
    print("   4. Read the full documentation in NATURAL_LANGUAGE_DESKTOP.md")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 