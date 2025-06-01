#!/usr/bin/env python3
"""
Simple CLI for StableAgents that takes a model and API key.
Usage: python simple_cli.py <model> <api_key>
"""
import sys
import argparse
from stableagents import StableAgents
from stableagents.core import get_banner

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='StableAgents Simple CLI')
    parser.add_argument('model', choices=['openai', 'anthropic', 'google', 'custom'], 
                        help='AI provider model')
    parser.add_argument('api_key', help='API key for the model')
    
    args = parser.parse_args()
    
    # Display simple banner
    print(get_banner("simple"))
    
    # Initialize agent
    agent = StableAgents()
    
    # Set API key and activate provider
    success = agent.set_api_key(args.model, args.api_key)
    if not success:
        print(f"Failed to set API key for {args.model}")
        return 1
    
    agent.set_active_ai_provider(args.model)
    print(f"Using AI provider: {args.model}")
    
    # Enter interactive loop
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                break
                
            # Simple help command
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  <message> - Send a message to the AI")
                print("  exit/quit - Exit the program")
                continue
            
            # Chat with the AI
            messages = [{"role": "user", "content": user_input}]
            result = agent.generate_chat(messages)
            print(f"AI: {result}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 