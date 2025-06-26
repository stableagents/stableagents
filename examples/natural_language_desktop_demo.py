#!/usr/bin/env python3
"""
Natural Language Desktop App Generator Demo

This demo showcases creating desktop applications using natural language
descriptions and Google Gemini AI.
"""

import os
import sys
import getpass
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator


def get_gemini_api_key():
    """Get Gemini API key from user."""
    print("🔑 Google Gemini API Key Required")
    print("=" * 40)
    print("Get your API key from: https://makersuite.google.com/app/apikey")
    print()
    
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


def demo_create_calculator_app(generator):
    """Demo creating a calculator app."""
    print("\n🧮 Creating Calculator App")
    print("=" * 40)
    
    description = """
    Create a modern calculator application with the following features:
    - Beautiful modern UI with dark/light mode toggle
    - Basic arithmetic operations (add, subtract, multiply, divide)
    - Scientific functions (sin, cos, tan, log, sqrt, power)
    - Memory functions (store, recall, clear)
    - History of calculations
    - Keyboard shortcuts for all operations
    - Responsive design that works on different screen sizes
    - Professional animations and transitions
    """
    
    result = generator.create_app_from_description(
        description=description,
        app_name="SmartCalculator",
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
        print(f"❌ Failed to create calculator app: {result.get('error', 'Unknown error')}")
        return False


def demo_create_task_manager(generator):
    """Demo creating a task manager app."""
    print("\n📋 Creating Task Manager App")
    print("=" * 40)
    
    description = """
    Build a comprehensive task management application with:
    - Modern, intuitive user interface with dark/light theme
    - Add, edit, and delete tasks with descriptions
    - Task categories and priority levels (High, Medium, Low)
    - Due dates and reminders
    - Mark tasks as complete/incomplete with visual indicators
    - Search and filter tasks by category, priority, or status
    - Data persistence - save tasks to local file
    - Export tasks to different formats (CSV, JSON)
    - Statistics and progress tracking
    - Responsive design for different window sizes
    """
    
    result = generator.create_app_from_description(
        description=description,
        app_name="TaskMaster",
        ui_framework="customtkinter"
    )
    
    if result.get("success"):
        print("🎉 Task manager app created successfully!")
        print(f"📁 Project location: {result['project_path']}")
        print(f"🚀 To run: cd {result['project_path']} && python main.py")
        
        # Show extracted features
        if "natural_language" in result:
            nl_data = result["natural_language"]
            print(f"\n📋 Generated name: {nl_data.get('generated_name', 'N/A')}")
            print(f"🔍 Extracted features: {', '.join(nl_data.get('extracted_features', []))}")
        
        return True
    else:
        print(f"❌ Failed to create task manager app: {result.get('error', 'Unknown error')}")
        return False


def demo_create_file_manager(generator):
    """Demo creating a file manager app."""
    print("\n📁 Creating File Manager App")
    print("=" * 40)
    
    description = """
    Create a modern file manager application with:
    - Dual-pane interface for easy file navigation
    - File and folder operations (copy, move, delete, rename)
    - File preview for common formats (text, images)
    - Search functionality with filters
    - File size and modification date display
    - Drag and drop support
    - Context menus for right-click operations
    - Keyboard shortcuts for common actions
    - Bookmark favorite locations
    - Modern UI with icons and visual feedback
    """
    
    result = generator.create_app_from_description(
        description=description,
        app_name="FileExplorer",
        ui_framework="customtkinter"
    )
    
    if result.get("success"):
        print("🎉 File manager app created successfully!")
        print(f"📁 Project location: {result['project_path']}")
        print(f"🚀 To run: cd {result['project_path']} && python main.py")
        
        # Show extracted features
        if "natural_language" in result:
            nl_data = result["natural_language"]
            print(f"\n📋 Generated name: {nl_data.get('generated_name', 'N/A')}")
            print(f"🔍 Extracted features: {', '.join(nl_data.get('extracted_features', []))}")
        
        return True
    else:
        print(f"❌ Failed to create file manager app: {result.get('error', 'Unknown error')}")
        return False


def demo_code_generation(generator):
    """Demo code generation from natural language."""
    print("\n💻 Code Generation Demo")
    print("=" * 40)
    
    # Example prompts for code generation
    prompts = [
        {
            "description": "Create a login form with username and password fields, validation, and a submit button",
            "framework": "customtkinter"
        },
        {
            "description": "Build a data visualization widget that displays a bar chart with sample data",
            "framework": "customtkinter"
        },
        {
            "description": "Create a settings panel with checkboxes, radio buttons, and a save button",
            "framework": "customtkinter"
        }
    ]
    
    for i, prompt_info in enumerate(prompts, 1):
        print(f"\n📝 Example {i}: {prompt_info['description']}")
        print("-" * 60)
        
        try:
            code = generator.generate_code_from_prompt(
                prompt=prompt_info["description"],
                framework=prompt_info["framework"]
            )
            
            print("Generated Code:")
            print("=" * 40)
            print(code)
            print("=" * 40)
            
            # Ask if user wants to continue
            if i < len(prompts):
                try:
                    continue_demo = input("\nContinue to next example? (y/n): ").strip().lower()
                    if continue_demo != 'y':
                        break
                except (KeyboardInterrupt, EOFError):
                    break
                    
        except Exception as e:
            print(f"❌ Error generating code: {e}")
    
    return True


def demo_framework_comparison():
    """Demo framework comparison."""
    print("\n🎨 Framework Comparison")
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


def main():
    """Main demo function."""
    print("🎯 Natural Language Desktop App Generator Demo")
    print("=" * 60)
    print("This demo showcases creating desktop applications using natural language")
    print("descriptions and Google Gemini AI.")
    print()
    
    # Get API key
    api_key = get_gemini_api_key()
    if not api_key:
        print("❌ API key required to run demo")
        return 1
    
    # Initialize generator
    try:
        generator = NaturalLanguageDesktopGenerator(api_key)
        if not generator.gemini_provider or not generator.gemini_provider.available:
            print("❌ Failed to initialize Gemini provider")
            return 1
    except Exception as e:
        print(f"❌ Error initializing generator: {e}")
        return 1
    
    print("✅ Gemini API connected successfully!")
    print()
    
    while True:
        print("\nChoose a demo option:")
        print("1. 🧮 Create Calculator App")
        print("2. 📋 Create Task Manager App")
        print("3. 📁 Create File Manager App")
        print("4. 💻 Code Generation Examples")
        print("5. 🎨 Framework Comparison")
        print("6. 🚀 Create Interactive Demo")
        print("7. 📋 Show Setup Instructions")
        print("8. 🚪 Exit")
        print()
        
        try:
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == "1":
                demo_create_calculator_app(generator)
            elif choice == "2":
                demo_create_task_manager(generator)
            elif choice == "3":
                demo_create_file_manager(generator)
            elif choice == "4":
                demo_code_generation(generator)
            elif choice == "5":
                demo_framework_comparison()
            elif choice == "6":
                print("\n🚀 Creating Interactive Demo")
                print("=" * 40)
                result = generator.create_interactive_demo()
                if result.get("success"):
                    print("🎉 Demo app created successfully!")
                    print(f"📁 Project location: {result['project_path']}")
                    print(f"🚀 To run: cd {result['project_path']} && python main.py")
                else:
                    print(f"❌ Failed to create demo app: {result.get('error', 'Unknown error')}")
            elif choice == "7":
                print("\n📋 Setup Instructions")
                print("=" * 40)
                print(generator.get_setup_instructions())
            elif choice == "8":
                print("👋 Thanks for trying the Natural Language Desktop Generator!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-8.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 