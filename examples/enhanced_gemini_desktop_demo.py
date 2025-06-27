#!/usr/bin/env python3
"""
Enhanced Gemini Desktop Application Demo

This example demonstrates the enhanced integration of Google Gemini AI
for creating desktop applications from natural language descriptions.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to import stableagents
sys.path.insert(0, str(Path(__file__).parent.parent))

from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator


def demo_calculator_app():
    """Demo: Create a modern calculator application."""
    print("\n🧮 Creating Modern Calculator App")
    print("=" * 40)
    
    description = """
    Create a modern calculator application with:
    - Beautiful modern UI with dark/light mode toggle
    - Basic arithmetic operations (add, subtract, multiply, divide)
    - Scientific functions (sin, cos, tan, log, sqrt, power)
    - Memory functions (store, recall, clear)
    - History of calculations with scrollable list
    - Keyboard shortcuts for all operations
    - Responsive design that works on different screen sizes
    - Professional animations and transitions
    - Error handling for invalid operations
    - Copy result to clipboard functionality
    """
    
    generator = NaturalLanguageDesktopGenerator()
    result = generator.create_app_from_description(
        description=description,
        app_name="SmartCalculator",
        ui_framework="customtkinter"
    )
    
    if result.get("success"):
        print("✅ Calculator app created successfully!")
        print(f"📁 Location: {result['project_path']}")
        return result['project_path']
    else:
        print(f"❌ Failed to create calculator app: {result.get('error', 'Unknown error')}")
        return None


def demo_task_manager():
    """Demo: Create a task management application."""
    print("\n📋 Creating Task Manager App")
    print("=" * 40)
    
    description = """
    Build a comprehensive task management application with:
    - Modern, intuitive user interface with dark/light theme toggle
    - Add, edit, and delete tasks with descriptions and due dates
    - Task categories and priority levels (High, Medium, Low)
    - Due dates with calendar picker and reminders
    - Mark tasks as complete/incomplete with visual indicators
    - Search and filter tasks by category, priority, or status
    - Data persistence - save tasks to local JSON file
    - Export tasks to different formats (CSV, JSON)
    - Statistics and progress tracking with charts
    - Responsive design for different window sizes
    - Drag and drop to reorder tasks
    - Bulk operations (delete multiple, change priority)
    """
    
    generator = NaturalLanguageDesktopGenerator()
    result = generator.create_app_from_description(
        description=description,
        app_name="TaskMaster",
        ui_framework="customtkinter"
    )
    
    if result.get("success"):
        print("✅ Task manager app created successfully!")
        print(f"📁 Location: {result['project_path']}")
        return result['project_path']
    else:
        print(f"❌ Failed to create task manager app: {result.get('error', 'Unknown error')}")
        return None


def demo_file_manager():
    """Demo: Create a file manager application."""
    print("\n📁 Creating File Manager App")
    print("=" * 40)
    
    description = """
    Create a modern file manager application with:
    - Dual-pane interface for easy file navigation
    - File and folder operations (copy, move, delete, rename)
    - File preview for common formats (text, images)
    - Search functionality with filters and regex support
    - File size and modification date display
    - Drag and drop support for file operations
    - Context menus for right-click operations
    - Keyboard shortcuts for common actions
    - Bookmark favorite locations
    - Modern UI with icons and visual feedback
    - Progress bars for file operations
    - Multiple view modes (list, grid, details)
    - File type associations and default programs
    """
    
    generator = NaturalLanguageDesktopGenerator()
    result = generator.create_app_from_description(
        description=description,
        app_name="FileExplorer",
        ui_framework="customtkinter"
    )
    
    if result.get("success"):
        print("✅ File manager app created successfully!")
        print(f"📁 Location: {result['project_path']}")
        return result['project_path']
    else:
        print(f"❌ Failed to create file manager app: {result.get('error', 'Unknown error')}")
        return None


def demo_code_generation():
    """Demo: Generate specific UI components."""
    print("\n🎨 Code Generation Examples")
    print("=" * 40)
    
    generator = NaturalLanguageDesktopGenerator()
    
    examples = [
        {
            "title": "Login Form",
            "prompt": "Create a modern login form with username and password fields, validation, and a submit button",
            "framework": "customtkinter"
        },
        {
            "title": "Data Visualization",
            "prompt": "Build a data visualization widget with bar charts, line charts, and pie charts using matplotlib",
            "framework": "customtkinter"
        },
        {
            "title": "File Upload",
            "prompt": "Create a file upload component with drag and drop support, progress bar, and file type validation",
            "framework": "customtkinter"
        }
    ]
    
    for example in examples:
        print(f"\n📝 Generating {example['title']}...")
        code = generator.generate_code_from_prompt(
            prompt=example['prompt'],
            framework=example['framework']
        )
        
        print(f"✅ {example['title']} code generated!")
        print("📋 Code preview (first 200 characters):")
        print(code[:200] + "..." if len(code) > 200 else code)
        print("-" * 50)


def demo_framework_comparison():
    """Demo: Show framework comparison."""
    print("\n🎨 Framework Comparison")
    print("=" * 40)
    
    generator = NaturalLanguageDesktopGenerator()
    frameworks = generator.list_frameworks()
    
    print("Available UI Frameworks:")
    for i, framework in enumerate(frameworks, 1):
        print(f"  {i}. {framework}")
    
    print("\n💡 Framework Recommendations:")
    print("  • CustomTkinter: Best for modern, beautiful applications")
    print("  • Tkinter: Best for simple applications and learning")
    print("  • PyQt: Best for professional, feature-rich applications")


def main():
    """Main demo function."""
    print("🚀 Enhanced Gemini Desktop Application Demo")
    print("=" * 60)
    print("This demo showcases the enhanced integration of Google Gemini AI")
    print("for creating desktop applications from natural language descriptions.")
    print()
    
    try:
        # Initialize the generator
        generator = NaturalLanguageDesktopGenerator()
        print("✅ Gemini AI initialized successfully!")
        
        while True:
            print("\nChoose a demo option:")
            print("1. 🧮 Create Calculator App")
            print("2. 📋 Create Task Manager App")
            print("3. 📁 Create File Manager App")
            print("4. 🎨 Code Generation Examples")
            print("5. 🎨 Framework Comparison")
            print("6. 🚀 Create Interactive Demo")
            print("7. 🚪 Exit")
            print()
            
            try:
                choice = input("Enter your choice (1-7): ").strip()
                
                if choice == "1":
                    demo_calculator_app()
                elif choice == "2":
                    demo_task_manager()
                elif choice == "3":
                    demo_file_manager()
                elif choice == "4":
                    demo_code_generation()
                elif choice == "5":
                    demo_framework_comparison()
                elif choice == "6":
                    print("\n🚀 Creating Interactive Demo")
                    print("=" * 40)
                    result = generator.create_interactive_demo()
                    if result.get("success"):
                        print("🎉 Interactive demo app created successfully!")
                        print(f"📁 Project location: {result['project_path']}")
                        print(f"🚀 To run: cd {result['project_path']} && python main.py")
                    else:
                        print(f"❌ Failed to create demo app: {result.get('error', 'Unknown error')}")
                elif choice == "7":
                    print("👋 Thanks for trying the Enhanced Gemini Desktop Demo!")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-7.")
                    
            except KeyboardInterrupt:
                print("\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
    except Exception as e:
        print(f"❌ Failed to initialize Gemini AI: {str(e)}")
        print("💡 Make sure you have set up your Gemini API key:")
        print("   1. Get a key from https://makersuite.google.com/app/apikey")
        print("   2. Set it as environment variable: export GEMINI_API_KEY='your-key'")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 