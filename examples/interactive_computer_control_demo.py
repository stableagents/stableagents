#!/usr/bin/env python3
"""
Interactive Computer Control Demo

This demo showcases the enhanced desktop automation capabilities of StableAgents,
including mouse control, keyboard input, screenshots, system monitoring, and more.
"""

import sys
import os
import time
import subprocess

# Add parent directory to path to import stableagents
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stableagents import StableAgents

def print_banner():
    """Print a banner for the demo."""
    print("=" * 60)
    print("🖥️  INTERACTIVE COMPUTER CONTROL DEMO")
    print("=" * 60)
    print("Experience the power of AI-driven desktop automation!")
    print("Control your computer with natural language commands.")
    print("=" * 60)

def print_menu():
    """Print the interactive menu."""
    print("\n🎮 Available Commands:")
    print("=" * 40)
    print("1. 🖱️  Mouse Control")
    print("   • click [coordinates] - Click at specific position")
    print("   • drag from x1,y1 to x2,y2 - Drag mouse")
    print("   • scroll up/down [amount] - Scroll mouse wheel")
    print()
    print("2. ⌨️  Keyboard Control")
    print("   • type [text] - Type text")
    print("   • key [keyname] - Press specific key")
    print()
    print("3. 📸 Screenshots & Media")
    print("   • screenshot - Take a screenshot")
    print()
    print("4. 💻 System Monitoring")
    print("   • monitor - Get system overview")
    print("   • monitor cpu - CPU information")
    print("   • monitor memory - Memory information")
    print("   • monitor disk - Disk information")
    print("   • monitor processes - Process information")
    print()
    print("5. 🔧 Process Control")
    print("   • process list - List running processes")
    print("   • process info [name/pid] - Get process details")
    print("   • process kill [name/pid] - Kill a process")
    print()
    print("6. 📁 File Operations")
    print("   • open [app] - Open application")
    print("   • browse [url] - Open website")
    print("   • search [query] - Search the web")
    print("   • list [path] - List directory contents")
    print("   • create file/folder [path] - Create file or folder")
    print()
    print("7. 🎯 Advanced Automation")
    print("   • window [action] [target] - Control windows")
    print("   • execute [command] - Run shell command")
    print()
    print("8. 📊 System Information")
    print("   • Get detailed system stats")
    print()
    print("0. 🚪 Exit")
    print("=" * 40)

def demo_mouse_control(agent):
    """Demonstrate mouse control capabilities."""
    print("\n🖱️  Mouse Control Demo")
    print("=" * 30)
    
    print("This demo will show you mouse control capabilities.")
    print("⚠️  WARNING: Mouse movements will be performed on your screen!")
    print("💡 Make sure you have a safe area to test mouse movements.")
    
    confirm = input("\nContinue with mouse control demo? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Mouse control demo skipped.")
        return
    
    # Get current mouse position
    print("\n📍 Getting current mouse position...")
    result = agent.control_computer("click")
    print(f"Result: {result}")
    
    # Test clicking at specific coordinates (safe area)
    print("\n🖱️  Testing click at position (100, 100)...")
    result = agent.control_computer("click 100,100")
    print(f"Result: {result}")
    
    # Test scrolling
    print("\n📜 Testing mouse scroll...")
    result = agent.control_computer("scroll down 3")
    print(f"Result: {result}")
    
    print("\n✅ Mouse control demo completed!")

def demo_keyboard_control(agent):
    """Demonstrate keyboard control capabilities."""
    print("\n⌨️  Keyboard Control Demo")
    print("=" * 30)
    
    print("This demo will show you keyboard control capabilities.")
    print("⚠️  WARNING: Keyboard input will be sent to the active window!")
    print("💡 Make sure you have a text editor or safe input field active.")
    
    confirm = input("\nContinue with keyboard control demo? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Keyboard control demo skipped.")
        return
    
    # Test typing text
    print("\n⌨️  Testing text input...")
    result = agent.control_computer("type Hello from StableAgents!")
    print(f"Result: {result}")
    
    # Test pressing specific keys
    print("\n🔑 Testing key press...")
    result = agent.control_computer("key enter")
    print(f"Result: {result}")
    
    print("\n✅ Keyboard control demo completed!")

def demo_screenshots(agent):
    """Demonstrate screenshot capabilities."""
    print("\n📸 Screenshot Demo")
    print("=" * 20)
    
    print("Taking a screenshot...")
    result = agent.control_computer("screenshot")
    print(f"Result: {result}")
    
    print("\n✅ Screenshot demo completed!")
    print("💡 Check the ~/.stableagents/screenshots/ directory for the saved image.")

def demo_system_monitoring(agent):
    """Demonstrate system monitoring capabilities."""
    print("\n💻 System Monitoring Demo")
    print("=" * 30)
    
    print("Getting comprehensive system information...")
    result = agent.control_computer("monitor")
    print(f"\n{result}")
    
    print("\nGetting CPU information...")
    result = agent.control_computer("monitor cpu")
    print(f"\n{result}")
    
    print("\nGetting memory information...")
    result = agent.control_computer("monitor memory")
    print(f"\n{result}")
    
    print("\nGetting disk information...")
    result = agent.control_computer("monitor disk")
    print(f"\n{result}")
    
    print("\n✅ System monitoring demo completed!")

def demo_process_control(agent):
    """Demonstrate process control capabilities."""
    print("\n🔧 Process Control Demo")
    print("=" * 30)
    
    print("Listing running processes...")
    result = agent.control_computer("process list")
    print(f"\n{result}")
    
    # Get info about Python process
    print("\nGetting information about Python processes...")
    result = agent.control_computer("process info python")
    print(f"\n{result}")
    
    print("\n✅ Process control demo completed!")

def demo_file_operations(agent):
    """Demonstrate file operation capabilities."""
    print("\n📁 File Operations Demo")
    print("=" * 30)
    
    print("Listing current directory...")
    result = agent.control_computer("list .")
    print(f"\n{result}")
    
    print("\nCreating a test file...")
    result = agent.control_computer("create file test_demo.txt")
    print(f"Result: {result}")
    
    print("\nOpening a web browser...")
    result = agent.control_computer("browse https://www.google.com")
    print(f"Result: {result}")
    
    print("\n✅ File operations demo completed!")

def demo_advanced_automation(agent):
    """Demonstrate advanced automation capabilities."""
    print("\n🎯 Advanced Automation Demo")
    print("=" * 35)
    
    print("Getting system information via shell command...")
    result = agent.control_computer("execute uname -a")
    print(f"\n{result}")
    
    print("\nGetting current working directory...")
    result = agent.control_computer("execute pwd")
    print(f"\n{result}")
    
    print("\n✅ Advanced automation demo completed!")

def interactive_mode(agent):
    """Run interactive mode for user commands."""
    print("\n🎮 Interactive Mode")
    print("=" * 20)
    print("Enter natural language commands to control your computer.")
    print("Type 'help' for available commands, 'menu' to see the menu, or 'exit' to quit.")
    print()
    
    while True:
        try:
            command = input("🤖 Command: ").strip()
            
            if command.lower() in ['exit', 'quit', 'q']:
                print("👋 Exiting interactive mode.")
                break
            elif command.lower() == 'help':
                print_menu()
                continue
            elif command.lower() == 'menu':
                print_menu()
                continue
            elif not command:
                continue
            
            print(f"🔄 Executing: {command}")
            result = agent.control_computer(command)
            print(f"📋 Result: {result}")
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Exiting interactive mode.")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def main():
    """Main demo function."""
    print_banner()
    
    # Create StableAgents instance
    print("🚀 Initializing StableAgents...")
    agent = StableAgents()
    print("✅ StableAgents initialized successfully!")
    
    while True:
        print_menu()
        
        try:
            choice = input("\n🎯 Select an option (0-8): ").strip()
            
            if choice == "0":
                print("👋 Thanks for trying the Interactive Computer Control Demo!")
                break
            elif choice == "1":
                demo_mouse_control(agent)
            elif choice == "2":
                demo_keyboard_control(agent)
            elif choice == "3":
                demo_screenshots(agent)
            elif choice == "4":
                demo_system_monitoring(agent)
            elif choice == "5":
                demo_process_control(agent)
            elif choice == "6":
                demo_file_operations(agent)
            elif choice == "7":
                demo_advanced_automation(agent)
            elif choice == "8":
                print("\n📊 System Information")
                print("=" * 25)
                result = agent.control_computer("monitor")
                print(f"\n{result}")
            elif choice.lower() == "interactive":
                interactive_mode(agent)
            else:
                print("❌ Invalid choice. Please select 0-8 or type 'interactive' for interactive mode.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Thanks for trying!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying the Interactive Computer Control Demo!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your installation and try again.") 