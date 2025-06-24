#!/usr/bin/env python3
"""
AI-Powered Computer Control Demo
Demonstrates using AI to interpret and execute natural language computer commands.
"""

import sys
import os
import time

# Add the parent directory to the path to import stableagents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stableagents import StableAgents

def main():
    print("🤖 AI-Powered Computer Control Demo")
    print("=" * 50)
    print("This demo shows how AI can interpret natural language commands")
    print("and convert them into specific computer actions.")
    print()
    
    # Initialize the agent
    agent = StableAgents()
    
    # Check if AI provider is configured
    if not agent.get_active_ai_provider():
        print("❌ No AI provider configured.")
        print("Please run 'stableagents-ai setup' to configure an AI provider first.")
        return 1
    
    print(f"✅ Using AI provider: {agent.get_active_ai_provider().capitalize()}")
    print()
    
    # Demo commands to test
    demo_commands = [
        "open youtube and search for the latest bruno mars song",
        "take a screenshot and save it to the desktop",
        "search for python tutorials and open the first result",
        "check system performance and show memory usage",
        "create a new folder called 'ai_demo' on the desktop",
        "open spotify and play some relaxing music"
    ]
    
    print("🎯 Demo Commands:")
    for i, command in enumerate(demo_commands, 1):
        print(f"  {i}. {command}")
    print()
    
    # Let user choose or run all
    try:
        choice = input("Enter a number (1-6) to test a specific command, or 'all' to run all: ").strip()
        
        if choice.lower() == 'all':
            commands_to_run = demo_commands
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(demo_commands):
                    commands_to_run = [demo_commands[index]]
                else:
                    print("❌ Invalid choice. Running first command.")
                    commands_to_run = [demo_commands[0]]
            except ValueError:
                print("❌ Invalid choice. Running first command.")
                commands_to_run = [demo_commands[0]]
        
        print(f"\n🚀 Running {len(commands_to_run)} command(s)...")
        print("=" * 60)
        
        for i, command in enumerate(commands_to_run, 1):
            print(f"\n🎯 Command {i}: {command}")
            print("-" * 40)
            
            # Use AI to interpret and execute the command
            result = agent.ai_control_computer(command)
            print(result)
            
            if i < len(commands_to_run):
                print("\n⏳ Waiting 3 seconds before next command...")
                time.sleep(3)
        
        print("\n" + "=" * 60)
        print("✅ Demo completed!")
        print("\n💡 Try these commands in interactive mode:")
        print("   stableagents-ai interactive")
        print("   Then use: ai-control [your natural language command]")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo cancelled.")
        return 0
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 