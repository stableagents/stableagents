#!/usr/bin/env python3
"""
Simple test of AI-powered computer control
"""

import sys
import os

# Add the stableagents directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'stableagents'))

from stableagents import StableAgents

def test_ai_control():
    print("🤖 Testing AI-Powered Computer Control")
    print("=" * 50)
    
    # Initialize agent
    agent = StableAgents()
    
    # Check if AI provider is configured
    if not agent.get_active_ai_provider():
        print("❌ No AI provider configured.")
        print("Please configure an AI provider first.")
        return
    
    print(f"✅ Using AI provider: {agent.get_active_ai_provider().capitalize()}")
    print()
    
    # Test commands
    test_commands = [
        "open youtube and search for the latest bruno mars song",
        "take a screenshot",
        "search for python tutorials",
        "check system memory usage"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n🎯 Test {i}: {command}")
        print("-" * 40)
        
        try:
            result = agent.ai_control_computer(command)
            print(result)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_ai_control() 