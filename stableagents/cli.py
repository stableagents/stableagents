#!/usr/bin/env python3
import argparse
import sys
import logging
import os
import json
import getpass

# Import from the package
from stableagents import StableAgents
from stableagents.core import get_banner

def setup_logging(verbose):
    """Configure logging based on verbosity level"""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('stableagents-cli')

def setup_ai_provider(agent):
    """Interactive setup for AI provider and API key"""
    providers = agent.list_ai_providers()
    
    # Get providers with keys
    providers_with_keys = [p for p in providers if p["has_key"]]
    
    # If we have an active provider with a key, use it
    active_provider = next((p for p in providers_with_keys if p["is_active"]), None)
    if active_provider:
        print(f"Using active AI provider: {active_provider['name']}")
        return True
        
    # If we have providers with keys but none is active, select the first one
    if providers_with_keys:
        provider_name = providers_with_keys[0]["name"]
        agent.set_active_ai_provider(provider_name)
        print(f"Selected AI provider: {provider_name}")
        return True
        
    # No providers with keys, ask user to choose one
    print("\nNo AI provider configured. Please select a provider:")
    for i, provider in enumerate(providers, 1):
        print(f"  {i}. {provider['name']}")
    
    try:
        choice = input("Enter number (or press Enter to skip): ")
        if not choice:
            print("AI setup skipped.")
            return False
            
        choice = int(choice)
        if choice < 1 or choice > len(providers):
            print("Invalid choice. AI setup skipped.")
            return False
            
        provider_name = providers[choice-1]["name"]
        
        # Ask for API key
        print(f"\nPlease enter your {provider_name.capitalize()} API key:")
        api_key = getpass.getpass("> ")
        
        if api_key:
            agent.set_api_key(provider_name, api_key)
            agent.set_active_ai_provider(provider_name)
            print(f"AI provider {provider_name} configured successfully.")
            return True
        else:
            print("No API key provided. AI setup skipped.")
            return False
            
    except (ValueError, IndexError):
        print("Invalid input. AI setup skipped.")
        return False

def interactive_mode(agent, setup_ai=True, banner_style="default"):
    """Run an interactive session with the agent"""
    # Display ASCII art banner
    print(get_banner(banner_style))
    
    print("Starting interactive StableAgents session. Type 'exit' or 'quit' to end.")
    print("Commands: memory.add TYPE KEY VALUE, memory.get TYPE [KEY], control [COMMAND], ai [PROMPT], apikey [PROVIDER] [KEY], help")
    
    # Setup AI provider if requested
    if setup_ai:
        ai_configured = setup_ai_provider(agent)
        if ai_configured:
            print("\nAI provider configured. You can use 'ai' and 'chat' commands.")
        else:
            print("\nAI provider not configured. Use 'apikey' command to set up.")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                break
                
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  memory.add TYPE KEY VALUE - Add to memory (TYPE: short_term, long_term, context)")
                print("  memory.get TYPE [KEY] - Get from memory")
                print("  control [COMMAND] - Control computer with natural language")
                print("  ai [PROMPT] - Generate text using the active AI provider")
                print("  chat [MESSAGE] - Chat with the AI provider")
                print("  apikey [PROVIDER] [KEY] - Set API key for a provider")
                print("  providers - List available AI providers")
                print("  provider [PROVIDER] - Set the active AI provider")
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
                
            if user_input.startswith('control '):
                command = user_input[8:].strip()
                if not command:
                    print("Please provide a command after 'control'")
                else:
                    result = agent.control_computer(command)
                    print(result)
                continue
                
            if user_input.startswith('ai '):
                prompt = user_input[3:].strip()
                if not prompt:
                    print("Please provide a prompt after 'ai'")
                else:
                    # Check if AI provider is configured
                    if not agent.get_active_ai_provider():
                        print("No active AI provider. Setting up now...")
                        if not setup_ai_provider(agent):
                            print("AI setup failed. Please use 'apikey' command to set up.")
                            continue
                    
                    result = agent.generate_text(prompt)
                    print(result)
                continue
                
            if user_input.startswith('chat '):
                message = user_input[5:].strip()
                if not message:
                    print("Please provide a message after 'chat'")
                else:
                    # Check if AI provider is configured
                    if not agent.get_active_ai_provider():
                        print("No active AI provider. Setting up now...")
                        if not setup_ai_provider(agent):
                            print("AI setup failed. Please use 'apikey' command to set up.")
                            continue
                    
                    # Get previous messages from memory, if any
                    prev_messages = agent.get_from_memory("short_term", "chat_history")
                    if not prev_messages:
                        messages = []
                    else:
                        messages = prev_messages[0]["value"] if prev_messages else []
                    
                    # Add user message
                    messages.append({"role": "user", "content": message})
                    
                    # Generate response
                    result = agent.generate_chat(messages)
                    print(f"AI: {result}")
                    
                    # Add assistant message
                    messages.append({"role": "assistant", "content": result})
                    
                    # Store in memory
                    agent.add_to_memory("short_term", "chat_history", messages)
                continue
                
            if user_input.startswith('apikey '):
                parts = user_input.split(' ', 2)
                if len(parts) < 3:
                    print("Usage: apikey PROVIDER KEY")
                else:
                    _, provider, key = parts
                    success = agent.set_api_key(provider, key)
                    if success:
                        print(f"API key set for {provider}")
                        # Set as active provider if no active provider
                        if not agent.get_active_ai_provider():
                            agent.set_active_ai_provider(provider)
                            print(f"Active provider set to {provider}")
                    else:
                        print(f"Failed to set API key for {provider}")
                continue
                
            if user_input.lower() == 'providers':
                providers = agent.list_ai_providers()
                print("\nAvailable AI providers:")
                for provider in providers:
                    status = "ACTIVE" if provider["is_active"] else ""
                    key_status = "✓" if provider["has_key"] else "✗"
                    print(f"  {provider['name']} {status} [Key: {key_status}]")
                continue
                
            if user_input.startswith('provider '):
                provider = user_input[9:].strip()
                if not provider:
                    print("Please specify a provider")
                else:
                    success = agent.set_active_ai_provider(provider)
                    if success:
                        print(f"Active provider set to {provider}")
                    else:
                        print(f"Failed to set active provider to {provider}")
                continue
                
            # Default: display as message
            agent.display_messages(user_input)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def run_examples(agent, banner_style="default"):
    """Run a guided example of AI capabilities"""
    # Display ASCII art banner for examples
    print(get_banner(banner_style))
    
    print("\nStableAgents AI Integration Example")
    print("====================================")
    
    # Setup AI provider
    if not setup_ai_provider(agent):
        print("AI setup required to run examples. Exiting.")
        return 1
    
    print(f"\nUsing {agent.get_active_ai_provider().capitalize()} as the AI provider")
    
    # Example 1: Generate text with a prompt
    print("\n1. Text Generation Example")
    print("==========================")
    
    example_prompt = "Write a short poem about artificial intelligence."
    print(f"Default prompt: {example_prompt}")
    
    user_prompt = input("Enter your own prompt (or press Enter to use default): ").strip()
    prompt = user_prompt or example_prompt
    
    print(f"\nGenerating text for: {prompt}")
    response = agent.generate_text(prompt)
    print("\nAI Response:")
    print(response)
    
    input("\nPress Enter to continue to the next example...")
    
    # Example 2: Chat conversation
    print("\n2. Chat Conversation Example")
    print("===========================")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that specializes in computer science."},
        {"role": "user", "content": "What is a neural network in simple terms?"}
    ]
    
    print("Starting a chat with the AI...")
    print("System: You are a helpful assistant that specializes in computer science.")
    print("User: What is a neural network in simple terms?")
    
    response = agent.generate_chat(messages)
    print(f"AI: {response}")
    
    # Add the assistant's response to the conversation
    messages.append({"role": "assistant", "content": response})
    
    # Continue the conversation
    next_question = "Can you give an example of how they're used?"
    print(f"\nDefault next question: {next_question}")
    
    user_question = input("Enter your own follow-up question (or press Enter to use default): ").strip()
    question = user_question or next_question
    
    messages.append({"role": "user", "content": question})
    print(f"\nUser: {question}")
    
    response = agent.generate_chat(messages)
    print(f"AI: {response}")
    
    input("\nPress Enter to continue to the next example...")
    
    # Example 3: AI + Computer Control Integration
    print("\n3. AI + Computer Control Integration")
    print("==================================")
    
    example_prompt = "Suggest a terminal command to list all Python files in the current directory."
    print(f"Default prompt: {example_prompt}")
    
    user_prompt = input("Enter your own prompt (or press Enter to use default): ").strip()
    prompt = user_prompt or example_prompt
    
    print(f"\nGenerating suggestion for: {prompt}")
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
    
    print("\nExample run complete!")
    
    # Ask if user wants to continue to interactive mode
    continue_interactive = input("\nWould you like to continue in interactive mode? (y/n) ")
    if continue_interactive.lower() == 'y':
        interactive_mode(agent, setup_ai=False, banner_style=banner_style)
    
    return 0

def main():
    parser = argparse.ArgumentParser(description='StableAgents CLI')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--banner', choices=['default', 'simple', 'compact'], default='default', 
                      help='Select ASCII art banner style (default, simple, compact)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Interactive mode
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive session')
    
    # Examples mode
    examples_parser = subparsers.add_parser('examples', help='Run guided AI examples')
    
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
    
    # Computer control
    control_parser = subparsers.add_parser('control', help='Control computer with natural language')
    control_parser.add_argument('command', nargs='+', help='Natural language command')
    
    # AI commands
    ai_parser = subparsers.add_parser('ai', help='AI text generation')
    ai_parser.add_argument('prompt', nargs='+', help='Text prompt')
    ai_parser.add_argument('--model', help='Model to use (provider-specific)')
    ai_parser.add_argument('--max-tokens', type=int, default=500, help='Maximum tokens to generate')
    
    # Chat commands
    chat_parser = subparsers.add_parser('chat', help='Chat with AI')
    chat_parser.add_argument('message', nargs='+', help='Chat message')
    chat_parser.add_argument('--model', help='Model to use (provider-specific)')
    chat_parser.add_argument('--max-tokens', type=int, default=500, help='Maximum tokens to generate')
    
    # API key management
    apikey_parser = subparsers.add_parser('apikey', help='API key management')
    apikey_subparsers = apikey_parser.add_subparsers(dest='apikey_command', help='API key command')
    
    # Set API key
    set_parser = apikey_subparsers.add_parser('set', help='Set API key')
    set_parser.add_argument('provider', choices=['openai', 'anthropic', 'google', 'custom'], help='Provider name')
    set_parser.add_argument('key', help='API key')
    
    # Get API key (for testing only)
    get_parser = apikey_subparsers.add_parser('get', help='Get API key (for testing only)')
    get_parser.add_argument('provider', choices=['openai', 'anthropic', 'google', 'custom'], help='Provider name')
    
    # List providers
    providers_parser = subparsers.add_parser('providers', help='List available AI providers')
    
    # Set active provider
    provider_parser = subparsers.add_parser('provider', help='Set active AI provider')
    provider_parser.add_argument('name', choices=['openai', 'anthropic', 'google', 'custom'], help='Provider name')
    
    args = parser.parse_args()
    logger = setup_logging(args.verbose)
    
    # Display banner for all commands
    if args.command != 'interactive':  # Skip here as interactive mode already shows the banner
        print(get_banner(args.banner))
    
    # Create agent instance
    agent = StableAgents()
    logger.debug("StableAgents initialized")
    
    # Process commands
    if args.command == 'interactive' or not args.command:
        interactive_mode(agent, banner_style=args.banner)
    elif args.command == 'examples':
        return run_examples(agent, args.banner)
    elif args.command == 'memory':
        if args.memory_command == 'add':
            agent.add_to_memory(args.type, args.key, args.value)
            print(f"Added to {args.type} memory: {args.key} = {args.value}")
        elif args.memory_command == 'get':
            result = agent.get_from_memory(args.type, args.key)
            print(result)
    elif args.command == 'control':
        command = ' '.join(args.command)
        result = agent.control_computer(command)
        print(result)
    elif args.command == 'ai':
        # Check if we have an active provider with key
        if not agent.get_active_ai_provider():
            print("No active AI provider. Setting up now...")
            if not setup_ai_provider(agent):
                print("AI setup failed. Exiting.")
                return 1
        
        prompt = ' '.join(args.prompt)
        kwargs = {}
        if args.model:
            kwargs['model'] = args.model
        if args.max_tokens:
            kwargs['max_tokens'] = args.max_tokens
        
        result = agent.generate_text(prompt, **kwargs)
        print(result)
    elif args.command == 'chat':
        # Check if we have an active provider with key
        if not agent.get_active_ai_provider():
            print("No active AI provider. Setting up now...")
            if not setup_ai_provider(agent):
                print("AI setup failed. Exiting.")
                return 1
        
        message = ' '.join(args.message)
        kwargs = {}
        if args.model:
            kwargs['model'] = args.model
        if args.max_tokens:
            kwargs['max_tokens'] = args.max_tokens
        
        # Simple one-off chat message
        messages = [{"role": "user", "content": message}]
        result = agent.generate_chat(messages, **kwargs)
        print(result)
    elif args.command == 'apikey':
        if args.apikey_command == 'set':
            success = agent.set_api_key(args.provider, args.key)
            if success:
                print(f"API key set for {args.provider}")
                # Set as active if no active provider
                if not agent.get_active_ai_provider():
                    agent.set_active_ai_provider(args.provider)
                    print(f"Active provider set to {args.provider}")
            else:
                print(f"Failed to set API key for {args.provider}")
        elif args.apikey_command == 'get':
            key = agent.get_api_key(args.provider)
            # Show only first few characters for security
            masked_key = key[:4] + '****' + key[-4:] if key else "No key set"
            print(f"API key for {args.provider}: {masked_key}")
    elif args.command == 'providers':
        providers = agent.list_ai_providers()
        print("Available AI providers:")
        for provider in providers:
            status = "ACTIVE" if provider["is_active"] else ""
            key_status = "✓" if provider["has_key"] else "✗"
            print(f"  {provider['name']} {status} [Key: {key_status}]")
    elif args.command == 'provider':
        success = agent.set_active_ai_provider(args.name)
        if success:
            print(f"Active provider set to {args.name}")
        else:
            print(f"Failed to set active provider to {args.name}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 