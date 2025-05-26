#!/usr/bin/env python3
"""
StableAgents Computer Control Example

This example demonstrates how to use StableAgents to control your computer
with natural language commands.
"""

import sys
import os
import time

# Add parent directory to path to import stableagents
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stableagents import StableAgents

def main():
    # Create a StableAgents instance
    agent = StableAgents()
    
    print("StableAgents Computer Control Example")
    print("====================================")
    
    # Example commands to demonstrate functionality
    commands = [
        "open calculator",
        "search for python documentation",
        "list .",
        "create file example.txt",
        "execute echo 'Hello from StableAgents' > example.txt",
        "find example.txt in .",
    ]
    
    for i, command in enumerate(commands, 1):
        print(f"\n[{i}/{len(commands)}] Executing: {command}")
        result = agent.control_computer(command)
        print(f"Result: {result}")
        time.sleep(2)  # Pause between commands
    
    # Interactive mode
    print("\nNow entering interactive mode. Type 'exit' to quit.")
    while True:
        command = input("\nEnter a command: ")
        if command.lower() in ['exit', 'quit']:
            break
            
        result = agent.control_computer(command)
        print(f"Result: {result}")
    
    print("\nThank you for using StableAgents!")
    
if __name__ == "__main__":
    main() 