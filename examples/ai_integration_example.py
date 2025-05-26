#!/usr/bin/env python3
"""
StableAgents AI Integration Example

This example demonstrates how to use StableAgents with AI providers
like OpenAI, Anthropic, and others.
"""

import sys
import os
import getpass

# Add parent directory to path to import stableagents
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stableagents import StableAgents

def get_api_key(provider="openai"):
    """Prompt for API key if needed"""
    print(f"\nThis example requires a {provider.capitalize()} API key.")
    print(f"Enter your {provider.capitalize()} API key (or press Enter to skip):")
    api_key = getpass.getpass("> ")
    return api_key

def main():
    # Create a StableAgents instance
    agent = StableAgents()
    
    print("StableAgents AI Integration Example")
    print("====================================")
    
    # Check for existing API key, or prompt for one
    provider = "openai"  # Default provider
    api_key = agent.get_api_key(provider)
    
    if not api_key:
        api_key = get_api_key(provider)
        if api_key:
            agent.set_api_key(provider, api_key)
        else:
            print("No API key provided. Exiting example.")
            return
    
    print(f"\nUsing {provider.capitalize()} as the AI provider")
    
    # Example 1: Generate text with a prompt
    print("\n1. Text Generation Example")
    prompt = "Write a short poem about artificial intelligence."
    print(f"Prompt: {prompt}")
    
    response = agent.generate_text(prompt)
    print("\nAI Response:")
    print(response)
    
    # Example 2: Chat conversation
    print("\n2. Chat Conversation Example")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that specializes in computer science."},
        {"role": "user", "content": "What is a neural network in simple terms?"}
    ]
    
    print("User: What is a neural network in simple terms?")
    response = agent.generate_chat(messages)
    print(f"AI: {response}")
    
    # Add the assistant's response to the conversation
    messages.append({"role": "assistant", "content": response})
    
    # Continue the conversation
    messages.append({"role": "user", "content": "Can you give an example of how they're used?"})
    print("\nUser: Can you give an example of how they're used?")
    
    response = agent.generate_chat(messages)
    print(f"AI: {response}")
    
    # Example 3: Integration with computer control
    print("\n3. AI + Computer Control Integration")
    
    prompt = "Suggest a terminal command to list all Python files in the current directory."
    print(f"Prompt: {prompt}")
    
    response = agent.generate_text(prompt)
    print(f"AI Suggestion: {response}")
    
    execute = input("\nWould you like to execute this command? (y/n) ")
    if execute.lower() == 'y':
        # Extract command from the AI's response (simple heuristic)
        import re
        command_match = re.search(r'`(.*?)`', response)
        command = command_match.group(1) if command_match else response.strip()
        
        print(f"Executing: {command}")
        result = agent.control_computer(f"execute {command}")
        print(f"Result: {result}")
    
    # Interactive mode
    print("\nNow entering interactive chat mode. Type 'exit' to quit.")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages.append({"role": "user", "content": user_input})
        response = agent.generate_chat(messages)
        
        print(f"AI: {response}")
        messages.append({"role": "assistant", "content": response})
    
    print("\nThank you for using StableAgents!")
    
if __name__ == "__main__":
    main() 