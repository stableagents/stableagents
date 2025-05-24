#!/usr/bin/env python3
import argparse
import sys
import logging
import os
import importlib.util

# Handle import whether run as a script or as part of package
try:
    from stableagents import StableAgents
except ImportError:
    # Try relative import
    try:
        from .main import StableAgents
    except ImportError:
        # Direct import for when running script directly
        from main import StableAgents

def setup_logging(verbose):
    """Configure logging based on verbosity level"""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('stableagents-cli')

def interactive_mode(agent):
    """Run an interactive session with the agent"""
    print("Starting interactive StableAgents session. Type 'exit' or 'quit' to end.")
    print("Commands: memory.add TYPE KEY VALUE, memory.get TYPE [KEY], reset, help")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                break
                
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  memory.add TYPE KEY VALUE - Add to memory (TYPE: short_term, long_term, context)")
                print("  memory.get TYPE [KEY] - Get from memory")
                print("  reset - Reset the agent")
                print("  exit/quit - Exit the program")
                continue
                
            if user_input.lower() == 'reset':
                agent.reset()
                print("Agent has been reset.")
                continue
                
            if user_input.startswith('memory.add '):
                parts = user_input.split(' ', 3)
                if len(parts) < 4:
                    print("Usage: memory.add TYPE KEY VALUE")
                else:
                    _, mem_type, key, value = parts
                    agent.add_to_memory(mem_type, key, value)
                    print(f"Added to {mem_type} memory: {key} = {value}")
                continue
                
            if user_input.startswith('memory.get '):
                parts = user_input.split(' ')
                if len(parts) < 2:
                    print("Usage: memory.get TYPE [KEY]")
                else:
                    key = parts[2] if len(parts) > 2 else None
                    result = agent.get_from_memory(parts[1], key)
                    print(f"Memory ({parts[1]}, {key}):", result)
                continue
                
            # Default: display as message
            agent.display_messages(user_input)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='StableAgents CLI')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Interactive mode
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive session')
    
    # Memory commands
    memory_parser = subparsers.add_parser('memory', help='Memory operations')
    memory_subparsers = memory_parser.add_subparsers(dest='memory_command', help='Memory command')
    
    # Add to memory
    add_parser = memory_subparsers.add_parser('add', help='Add to memory')
    add_parser.add_argument('type', choices=['short_term', 'long_term', 'context'], help='Memory type')
    add_parser.add_argument('key', help='Memory key')
    add_parser.add_argument('value', help='Memory value')
    
    # Get from memory
    get_parser = memory_subparsers.add_parser('get', help='Get from memory')
    get_parser.add_argument('type', choices=['short_term', 'long_term', 'context'], help='Memory type')
    get_parser.add_argument('key', nargs='?', help='Memory key (optional)')
    
    args = parser.parse_args()
    logger = setup_logging(args.verbose)
    
    # Create agent instance
    agent = StableAgents()
    logger.debug("StableAgents initialized")
    
    # Process commands
    if args.command == 'interactive' or not args.command:
        interactive_mode(agent)
    elif args.command == 'memory':
        if args.memory_command == 'add':
            agent.add_to_memory(args.type, args.key, args.value)
            print(f"Added to {args.type} memory: {args.key} = {args.value}")
        elif args.memory_command == 'get':
            result = agent.get_from_memory(args.type, args.key)
            print(result)
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 