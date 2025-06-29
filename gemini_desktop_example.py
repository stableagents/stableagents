#!/usr/bin/env python3
"""
Gemini Desktop App Generator Example

This example combines Google Gemini AI with natural language desktop app generation.
It demonstrates how to create desktop applications using simple text descriptions.
"""

import os
import sys
import json
from pathlib import Path

# Load environment variables from .env.local
def load_env_file(filepath=".env.local"):
    """Load environment variables from a .env file"""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value

# Load the environment variables
load_env_file()

def test_gemini_connection():
    """Test the Gemini API connection"""
    print("🔍 Testing Gemini API connection...")
    
    try:
        from google import genai
        client = genai.Client()
        
        # Test with a simple request
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents="Say 'Gemini is working!'"
        )
        print(f"✅ Gemini API test successful: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def create_desktop_app():
    """Create a desktop application using Gemini and natural language"""
    print("\n🚀 Gemini Desktop App Generator")
    print("=" * 50)
    print("Create beautiful desktop applications using natural language and Google Gemini AI!")
    print()
    
    # Test Gemini connection first
    if not test_gemini_connection():
        print("❌ Cannot proceed without working Gemini API")
        return False
    
    try:
        # Import the natural language desktop generator
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        # Get API key from environment
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment")
            print("Make sure your .env.local contains: GEMINI_API_KEY=your_key_here")
            return False
        
        # Initialize the generator
        print("🔧 Initializing Natural Language Desktop Generator...")
        generator = NaturalLanguageDesktopGenerator(api_key)
        print("✅ Generator initialized successfully!")
        
        # Get app description from user
        print("\n📝 Describe your desktop application:")
        print("💡 Be specific about features, UI elements, and functionality")
        print("💡 Examples:")
        print("   - 'Create a modern calculator with scientific functions, dark mode, and history'")
        print("   - 'Build a todo list app with categories, due dates, and priority levels'")
        print("   - 'Make a weather app that shows current conditions and 5-day forecast'")
        print("   - 'Create a note-taking app with rich text editing and file saving'")
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
        print("\n🎨 Choose UI Framework:")
        frameworks = generator.list_frameworks()
        framework_descriptions = generator.get_framework_descriptions()
        
        for i, (framework, desc) in enumerate(zip(frameworks, framework_descriptions), 1):
            print(f"  {i}. {framework} - {desc}")
        
        while True:
            try:
                choice = input(f"\nSelect framework (1-{len(frameworks)}): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(frameworks):
                    ui_framework = frameworks[choice_idx]
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
            except ValueError:
                print("❌ Please enter a number.")
        
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
            
            # Show project info
            project_info = generator.get_project_info(result['project_path'])
            print(f"\n📊 Project Information:")
            print(f"   Name: {project_info.get('name', 'Unknown')}")
            print(f"   Framework: {project_info.get('framework', 'Unknown')}")
            print(f"   Description: {project_info.get('description', 'No description')}")
            
            # Ask if user wants to run the app
            run_app = input("\nWould you like to run the application now? (y/n): ").strip().lower()
            if run_app in ['y', 'yes']:
                print("🚀 Starting application...")
                success = generator.run_app(result['project_path'])
                if success:
                    print("✅ Application started successfully!")
                else:
                    print("❌ Failed to start application")
            
            return True
        else:
            print(f"❌ Failed to create application: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def create_demo_app():
    """Create a demo application to showcase capabilities"""
    print("\n🎯 Creating Demo Application")
    print("=" * 40)
    
    # Test Gemini connection first
    if not test_gemini_connection():
        print("❌ Cannot proceed without working Gemini API")
        return False
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        # Get API key from environment
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment")
            return False
        
        # Initialize the generator
        generator = NaturalLanguageDesktopGenerator(api_key)
        
        # Create a demo app
        demo_description = """
        Create a modern scientific calculator with the following features:
        - Basic arithmetic operations (+, -, *, /)
        - Scientific functions (sin, cos, tan, log, sqrt, power)
        - Memory functions (M+, M-, MR, MC)
        - History of calculations
        - Dark mode toggle
        - Responsive design with CustomTkinter
        - Error handling for invalid operations
        - Clear and intuitive user interface
        """
        
        print("🚀 Creating Scientific Calculator Demo...")
        result = generator.create_app_from_description(
            description=demo_description,
            app_name="Scientific Calculator",
            ui_framework="customtkinter"
        )
        
        if result.get("success"):
            print("\n🎉 Demo application created successfully!")
            print(f"📁 Location: {result['project_path']}")
            print(f"🚀 To run: cd {result['project_path']} && python main.py")
            
            # Ask if user wants to run the demo
            run_demo = input("\nWould you like to run the demo application? (y/n): ").strip().lower()
            if run_demo in ['y', 'yes']:
                print("🚀 Starting demo application...")
                generator.run_app(result['project_path'])
            
            return True
        else:
            print(f"❌ Failed to create demo: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def show_setup_instructions():
    """Show setup instructions"""
    print("\n📚 Setup Instructions")
    print("=" * 30)
    print("1. Get a Google Gemini API key from: https://makersuite.google.com/app/apikey")
    print("2. Create a .env.local file in your project root")
    print("3. Add: GEMINI_API_KEY=your_actual_api_key_here")
    print("4. Install dependencies: pip install -r requirements.txt")
    print("5. Run this script to create desktop applications!")
    print()
    print("💡 Example .env.local file:")
    print("   GEMINI_API_KEY=AIzaSyC...")
    print()

def main():
    """Main function"""
    print("🤖 Gemini Desktop App Generator Example")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "demo":
            return create_demo_app()
        elif command == "setup":
            show_setup_instructions()
            return True
        elif command == "test":
            return test_gemini_connection()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: demo, setup, test")
            return False
    else:
        # Interactive mode
        print("Choose an option:")
        print("1. Create custom desktop app")
        print("2. Create demo app (Scientific Calculator)")
        print("3. Test Gemini connection")
        print("4. Show setup instructions")
        print("5. Exit")
        
        while True:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                return create_desktop_app()
            elif choice == "2":
                return create_demo_app()
            elif choice == "3":
                return test_gemini_connection()
            elif choice == "4":
                show_setup_instructions()
                return True
            elif choice == "5":
                print("👋 Goodbye!")
                return True
            else:
                print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 