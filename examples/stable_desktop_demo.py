#!/usr/bin/env python3
"""
Stable Desktop Demo - Showcase desktop software creation using GPT
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import stableagents
sys.path.insert(0, str(Path(__file__).parent.parent))

from stableagents import StableAgents
from stableagents.stable_desktop import DesktopBuilder


def demo_create_simple_app():
    """Demo creating a simple desktop application"""
    print("🚀 Stable Desktop Demo - Creating Simple App")
    print("=" * 50)
    
    # Initialize the agent
    agent = StableAgents()
    
    # Check if we have an AI provider
    if not agent.get_active_ai_provider():
        print("⚠️  No AI provider configured.")
        print("💡 Please run 'stableagents-ai setup' first to configure your AI provider.")
        return False
    
    # Create desktop builder
    ai_provider = agent.get_active_ai_provider()
    desktop_builder = DesktopBuilder(ai_provider)
    
    # Create a simple calculator app
    print("\n📱 Creating a simple calculator application...")
    
    result = desktop_builder.create_app(
        app_name="Simple Calculator",
        description="A basic calculator application with addition, subtraction, multiplication, and division",
        ui_framework="tkinter",
        features=["Basic arithmetic", "Clear function", "User-friendly interface"]
    )
    
    if result.get("success"):
        print("\n🎉 Calculator app created successfully!")
        print(f"📁 Project location: {result['project_path']}")
        print(f"🚀 To run: cd {result['project_path']} && python main.py")
        return True
    else:
        print(f"❌ Failed to create app: {result.get('error', 'Unknown error')}")
        return False


def demo_list_frameworks():
    """Demo listing available UI frameworks"""
    print("\n🎨 Available UI Frameworks")
    print("=" * 40)
    
    from stableagents.stable_desktop import UIFramework
    
    ui_framework = UIFramework()
    frameworks = ui_framework.list_frameworks()
    
    for framework in frameworks:
        print(f"\n📱 {framework['name']}")
        print(f"   📝 {framework['description']}")
        print(f"   ✅ Pros: {', '.join(framework['pros'])}")
        print(f"   ❌ Cons: {', '.join(framework['cons'])}")
        print(f"   🎯 Best for: {', '.join(framework['best_for'])}")
        
        # Check availability
        availability = ui_framework.check_framework_availability(framework['name'].lower())
        if availability['available']:
            print(f"   🔧 Status: Available")
        else:
            print(f"   🔧 Status: Not available - {availability.get('error', 'Unknown error')}")


def demo_create_modern_app():
    """Demo creating a modern app with CustomTkinter"""
    print("\n🚀 Creating Modern App with CustomTkinter")
    print("=" * 50)
    
    # Initialize the agent
    agent = StableAgents()
    
    # Check if we have an AI provider
    if not agent.get_active_ai_provider():
        print("⚠️  No AI provider configured.")
        print("💡 Please run 'stableagents-ai setup' first to configure your AI provider.")
        return False
    
    # Create desktop builder
    ai_provider = agent.get_active_ai_provider()
    desktop_builder = DesktopBuilder(ai_provider)
    
    # Create a modern task manager app
    print("\n📱 Creating a modern task manager application...")
    
    result = desktop_builder.create_app(
        app_name="Task Manager",
        description="A modern task management application with a beautiful UI for organizing and tracking tasks",
        ui_framework="customtkinter",
        features=["Add tasks", "Mark complete", "Delete tasks", "Modern UI", "Dark mode support"]
    )
    
    if result.get("success"):
        print("\n🎉 Task Manager app created successfully!")
        print(f"📁 Project location: {result['project_path']}")
        print(f"🚀 To run: cd {result['project_path']} && python main.py")
        return True
    else:
        print(f"❌ Failed to create app: {result.get('error', 'Unknown error')}")
        return False


def demo_list_projects():
    """Demo listing created projects"""
    print("\n📋 Listing Created Projects")
    print("=" * 40)
    
    # Initialize the agent
    agent = StableAgents()
    
    # Create desktop builder
    desktop_builder = DesktopBuilder()
    
    projects = desktop_builder.list_projects()
    if not projects:
        print("No projects found.")
        print("💡 Create your first project with the demo functions above")
        return
    
    for i, project in enumerate(projects, 1):
        print(f"\n{i}. {project['app_name']}")
        print(f"   📝 Description: {project['description']}")
        print(f"   🎨 Framework: {project['ui_framework']}")
        print(f"   📁 Location: {project['output_dir']}")
        print(f"   📅 Created: {project['created_at']}")
        if project['features']:
            print(f"   ⚡ Features: {', '.join(project['features'])}")


def main():
    """Main demo function"""
    print("🎯 Stable Desktop Demo")
    print("=" * 30)
    print("This demo showcases creating desktop software using GPT")
    print()
    
    while True:
        print("\nChoose a demo option:")
        print("1. 📱 Create Simple Calculator App (Tkinter)")
        print("2. 🎨 List Available UI Frameworks")
        print("3. 🚀 Create Modern Task Manager App (CustomTkinter)")
        print("4. 📋 List Created Projects")
        print("5. 🚪 Exit")
        print()
        
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                demo_create_simple_app()
            elif choice == "2":
                demo_list_frameworks()
            elif choice == "3":
                demo_create_modern_app()
            elif choice == "4":
                demo_list_projects()
            elif choice == "5":
                print("👋 Thanks for trying Stable Desktop!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 