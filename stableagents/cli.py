#!/usr/bin/env python3
"""
stableagents-ai CLI - Command Line Interface for stableagents-ai
"""

import argparse
import sys
import logging
import os
import json
import getpass
import webbrowser

# Import from the package
from stableagents import StableAgents
from stableagents.core import get_banner
from stableagents.desktop import DesktopAutomation, run_async

def setup_logging(verbose):
    """Configure logging based on verbosity level"""
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('stableagents-ai-cli')

def exit_cli(message="👋 Goodbye! Thanks for using stableagents-ai!"):
    """Clean exit function for the CLI"""
    print(f"\n{message}")
    sys.exit(0)

def check_exit_command(user_input):
    """Check if user input is an exit command"""
    if user_input.lower() in ['exit', 'quit', 'q']:
        return True
    return False

def show_preview_prompts_and_select_provider():
    """Show preview prompts and help user select a model provider before API setup"""
    print("\n🎯 WELCOME TO stableagents-ai!")
    print("=" * 50)
    print("Let's start by exploring what you can build with AI, then choose your provider.")
    print("💡 Type 'exit', 'quit', or 'q' at any time to cancel")
    print()
    
    # Create agent instance for prompt showcase
    agent = StableAgents()
    
    # Step 1: Show preview prompts
    print("📋 STEP 1: EXPLORE WHAT YOU CAN BUILD")
    print("=" * 50)
    print("Here are some examples of what you can create with stableagents-ai:")
    print()
    
    # Show quick preview of capabilities
    print("🖥️  Computer Control Examples:")
    print("   • 'Open my email and compose a new message'")
    print("   • 'Create a new folder and organize my files'")
    print("   • 'Search for Python tutorials and open the first 3 results'")
    print()
    
    print("🧠 AI Applications Examples:")
    print("   • 'Create a chatbot for customer support'")
    print("   • 'Build an app that reads PDFs and extracts key info'")
    print("   • 'Make an AI assistant that can identify objects in photos'")
    print()
    
    print("💻 Code Generation Examples:")
    print("   • 'Write a Python function to sort data'")
    print("   • 'Create a web scraper for e-commerce sites'")
    print("   • 'Generate code to integrate with REST APIs'")
    print()
    
    print("📝 Content Creation Examples:")
    print("   • 'Write a 500-word blog post about AI trends'")
    print("   • 'Create professional email templates'")
    print("   • 'Generate engaging social media posts'")
    print()
    
    print("📊 Data Analysis Examples:")
    print("   • 'Analyze monthly sales data and identify trends'")
    print("   • 'Process customer reviews and extract sentiment'")
    print("   • 'Build a model to predict customer churn'")
    print()
    
    print("⚡ Productivity Examples:")
    print("   • 'Automatically categorize emails and draft responses'")
    print("   • 'Create an AI assistant for meeting scheduling'")
    print("   • 'Build a system to prioritize tasks'")
    print()
    
    # Ask if they want to see more detailed examples
    try:
        see_more = input("\nWould you like to see more detailed examples? (y/n): ").strip().lower()
        if check_exit_command(see_more):
            exit_cli("👋 Setup cancelled.")
        if see_more in ['y', 'yes']:
            print("\n" + "="*60)
            print("📋 DETAILED PROMPT EXAMPLES")
            print("="*60)
            print(agent.show_prompts_showcase())
    except (KeyboardInterrupt, EOFError):
        exit_cli("👋 Setup cancelled.")
    
    # Step 2: Interactive prompt selection
    print("\n" + "="*60)
    print("🎯 STEP 2: SELECT A SPECIFIC PROMPT")
    print("="*60)
    print("Let's pick a specific prompt to work with:")
    print()
    
    try:
        # Use the agent's prompt selection functionality
        selected_prompt = agent.select_prompt_and_provider()
        if not selected_prompt:
            print("❌ Prompt selection cancelled.")
            return None, None
        
        prompt_info = selected_prompt.get("prompt", {})
        selected_provider = selected_prompt.get("provider")
        
        if not prompt_info or not selected_provider:
            print("❌ Incomplete selection.")
            return None, None
        
        print(f"\n✅ Selected Prompt: {prompt_info.get('name', 'Unknown')}")
        print(f"📋 Prompt: {prompt_info.get('prompt', 'Unknown')}")
        print(f"🎯 Category: {prompt_info.get('category', 'Unknown')}")
        print(f"📊 Difficulty: {prompt_info.get('difficulty', 'Unknown')}")
        print(f"🤖 Provider: {selected_provider.upper()}")
        
        # Get provider info for the next step
        providers = {
            'openai': {
                'name': 'OpenAI (GPT-4, GPT-3.5)',
                'pros': ['Fast response times', 'Good for general tasks', 'Wide model selection'],
                'cons': ['Higher cost for GPT-4', 'Rate limits'],
                'best_for': ['General AI tasks', 'Quick prototyping', 'Content creation'],
                'cost': 'GPT-3.5: ~$0.002/1K tokens, GPT-4: ~$0.03/1K tokens'
            },
            'anthropic': {
                'name': 'Anthropic (Claude)',
                'pros': ['Excellent reasoning', 'Long context windows', 'Safety-focused'],
                'cons': ['Slower response times', 'Higher cost'],
                'best_for': ['Complex reasoning', 'Code generation', 'Analysis tasks'],
                'cost': 'Claude: ~$0.008/1K tokens'
            },
            'google': {
                'name': 'Google (PaLM, Gemini)',
                'pros': ['Good performance', 'Competitive pricing', 'Integration with Google services'],
                'cons': ['Limited model selection', 'Newer to market'],
                'best_for': ['Google ecosystem integration', 'Cost-effective solutions'],
                'cost': 'PaLM: ~$0.001/1K tokens, Gemini: ~$0.002/1K tokens'
            },
            'local': {
                'name': 'Local Models (GGUF)',
                'pros': ['Privacy-focused', 'No API costs', 'Works offline'],
                'cons': ['Limited model quality', 'Requires setup', 'Resource intensive'],
                'best_for': ['Privacy-sensitive tasks', 'Offline use', 'Learning/experimentation'],
                'cost': 'Free (one-time model download)'
            }
        }
        
        provider_info = providers.get(selected_provider, {})
        
        return selected_provider, provider_info
        
    except (KeyboardInterrupt, EOFError):
        exit_cli("👋 Setup cancelled.")
    except Exception as e:
        print(f"\n❌ Error during prompt selection: {e}")
        return None, None

def check_secure_api_setup(selected_provider=None, provider_info=None):
    """Check if secure API key management is available and guide user through setup"""
    try:
        from stableagents.api_key_manager import SecureAPIKeyManager
        manager = SecureAPIKeyManager()
        
        # Check if user has already paid or set up keys
        status = manager.check_payment_status()
        
        if status.get('paid', False) and status.get('api_keys_provided'):
            print("✅ Secure API keys are configured")
            return True
            
        # No secure setup found, guide user through the process
        print("\n🔐 API KEY SETUP")
        print("=" * 40)
        
        # Show options
        print("You have three options:")
        print()
        print("1. 💳 Monthly Subscription ($20/month)")
        print("   - We provide working API keys")
        print("   - Keys are securely encrypted")
        print("   - Monthly recurring billing")
        print("   - Cancel anytime")
        print("   - No setup fees or hidden costs")
        print()
        print("2. 🔑 Bring your own API keys")
        print("   - Use your existing OpenAI, Anthropic, etc. keys")
        print("   - Keys are securely encrypted")
        print("   - No additional cost beyond your API usage")
        print()
        print("3. 🏠 Use local models only")
        print("   - Download GGUF models for local inference")
        print("   - No API keys or payment required")
        print("   - Works offline, privacy-focused")
        print()
        print("💡 Type 'exit', 'quit', or 'q' at any time to cancel setup")
        print()
        
        while True:
            try:
                choice = input("Enter your choice (1-3): ").strip()
                
                # Handle exit commands
                if check_exit_command(choice):
                    exit_cli("👋 Setup cancelled. You can run 'stableagents-ai setup' later.")
                
                if choice == "1":
                    return setup_payment_option(manager)
                elif choice == "2":
                    return setup_custom_keys(manager)
                elif choice == "3":
                    print("✅ Local model mode selected")
                    print("💡 To use local models, download GGUF files to ~/.stableagents/models/")
                    return True
                else:
                    print("Please enter 1, 2, or 3 (or 'exit' to cancel)")
            except KeyboardInterrupt:
                exit_cli("👋 Setup cancelled. You can run 'stableagents-ai setup' later.")
            except EOFError:
                exit_cli("👋 Setup cancelled. You can run 'stableagents-ai setup' later.")
                
    except ImportError:
        print("⚠️  Secure API key management not available")
        print("   Using legacy API key management")
        return False

def setup_payment_option(manager):
    """Setup monthly subscription option for managed API keys"""
    print("\n💳 Monthly Subscription Setup")
    print("=" * 30)
    print("Setting up monthly subscription for API key access...")
    print("Amount: $20.00 USD per month")
    print("Billing: Monthly recurring subscription")
    print("Payment: Credit card or PayPal")
    print("Cancellation: Cancel anytime from your account")
    print("\nType 'exit' at any time to quit the setup.")
    print()
    
    # Try to create a payment link first
    try:
        from stableagents.stripe_payment import StripePaymentManager
        stripe_manager = StripePaymentManager()
        
        if stripe_manager.stripe_secret_key:
            print("🔗 Creating Stripe payment link...")
            payment_url = stripe_manager.create_payment_link()
            
            if payment_url:
                print("✅ Payment link created successfully!")
                print(f"🔗 Payment URL: {payment_url}")
                print()
                print("📋 Instructions:")
                print("1. Click the payment link above or copy it to your browser")
                print("2. Complete the subscription setup")
                print("3. After payment, you'll be redirected to a success page")
                print("4. Copy the session_id from the URL and paste it below")
                print()
                
                # Try to open the payment link
                try:
                    webbrowser.open(payment_url)
                    print("🌐 Payment page opened in your browser")
                except Exception as e:
                    print(f"⚠️  Could not open browser automatically: {e}")
                    print("Please manually visit the payment URL above")
                
                print()
                session_id = input("Paste the session_id from the success URL here (or press Enter to skip): ").strip()
                
                if session_id:
                    print("\n🔍 Verifying payment with Stripe...")
                    if stripe_manager._verify_checkout_session(session_id):
                        print("✅ Subscription active!")
                        print("📅 Your subscription will automatically renew each month")
                        print("💳 You can manage your subscription anytime")
                        print()
                        
                        # Get password for encryption
                        while True:
                            try:
                                password = getpass.getpass("Enter a password to encrypt your API keys (or type 'exit'): ")
                                if check_exit_command(password):
                                    exit_cli("👋 Setup cancelled.")
                                if password:
                                    confirm = getpass.getpass("Confirm password (or type 'exit'): ")
                                    if check_exit_command(confirm):
                                        exit_cli("👋 Setup cancelled.")
                                    if password == confirm:
                                        break
                                    else:
                                        print("Passwords don't match. Please try again.")
                                else:
                                    print("Password cannot be empty.")
                            except (KeyboardInterrupt, EOFError):
                                exit_cli("👋 Setup cancelled.")
                        
                        # Provide API keys
                        if manager.provide_api_keys_after_payment(password):
                            print("✅ API keys have been securely stored and encrypted!")
                            print("🔒 Your keys are protected with your password")
                            print("💡 You can now use AI features in stableagents-ai")
                            print("📅 Your subscription will renew monthly")
                            print("💳 Manage your subscription: Check your email for account details")
                            return True
                        else:
                            print("❌ Failed to provide API keys")
                            return False
                    else:
                        print("❌ Payment verification failed")
                        print("💡 You can still complete the payment manually and try again")
                        return False
                else:
                    print("💡 Payment link created but not completed")
                    print("You can complete the payment later by visiting the URL above")
                    return False
            else:
                print("❌ Failed to create payment link")
                print("Falling back to manual payment process...")
        else:
            print("⚠️  Stripe not configured")
            print("Falling back to manual payment process...")
    except Exception as e:
        print(f"⚠️  Error with Stripe integration: {e}")
        print("Falling back to manual payment process...")
    
    # Fallback to original payment process
    if manager.process_payment():
        print("✅ Subscription active!")
        print("📅 Your subscription will automatically renew each month")
        print("💳 You can manage your subscription anytime")
        print()
        
        # Get password for encryption
        while True:
            try:
                password = getpass.getpass("Enter a password to encrypt your API keys (or type 'exit'): ")
                if check_exit_command(password):
                    exit_cli("👋 Setup cancelled.")
                if password:
                    confirm = getpass.getpass("Confirm password (or type 'exit'): ")
                    if check_exit_command(confirm):
                        exit_cli("👋 Setup cancelled.")
                    if password == confirm:
                        break
                    else:
                        print("Passwords don't match. Please try again.")
                else:
                    print("Password cannot be empty.")
            except (KeyboardInterrupt, EOFError):
                exit_cli("👋 Setup cancelled.")
        
        # Provide API keys
        if manager.provide_api_keys_after_payment(password):
            print("✅ API keys have been securely stored and encrypted!")
            print("🔒 Your keys are protected with your password")
            print("💡 You can now use AI features in stableagents-ai")
            print("📅 Your subscription will renew monthly")
            print("💳 Manage your subscription: Check your email for account details")
            return True
        else:
            print("❌ Failed to provide API keys")
            return False
    else:
        print("❌ Subscription setup failed")
        return False

def setup_custom_keys(manager):
    """Setup custom API keys"""
    print("\n🔑 Custom API Key Setup")
    print("=" * 25)
    print("Enter your API keys securely. They will be encrypted.")
    print("You must provide at least one API key to continue.")
    print("\nType 'exit' at any time to quit the setup.")
    print()
    
    # Get password for encryption
    while True:
        try:
            password = getpass.getpass("Enter a password to encrypt your API keys (or type 'exit'): ")
            if check_exit_command(password):
                exit_cli("👋 Setup cancelled.")
            if password:
                confirm = getpass.getpass("Confirm password (or type 'exit'): ")
                if check_exit_command(confirm):
                    exit_cli("👋 Setup cancelled.")
                if password == confirm:
                    break
                else:
                    print("Passwords don't match. Please try again.")
            else:
                print("Password cannot be empty.")
        except (KeyboardInterrupt, EOFError):
            exit_cli("👋 Setup cancelled.")
            return False
    
    # Reset encryption
    manager.reset_encryption()
    
    # Collect API keys
    providers = ["openai", "anthropic", "google"]
    keys_set = False
    
    print("\n🔑 API Key Entry")
    print("=" * 20)
    print("You must provide at least one API key to continue.")
    print("Get your API keys from:")
    print("  OpenAI: https://platform.openai.com/api-keys")
    print("  Anthropic: https://console.anthropic.com/")
    print("  Google: https://makersuite.google.com/app/apikey")
    print("\nType 'exit' at any time to quit the setup.")
    print()
    
    for provider in providers:
        try:
            print(f"\n{provider.capitalize()} API Key:")
            api_key = getpass.getpass("> ")
            
            # Check for exit command
            if check_exit_command(api_key):
                exit_cli("👋 Setup cancelled.")
            
            if api_key and api_key.strip():
                if manager.set_api_key(provider, api_key, password):
                    print(f"✅ {provider.capitalize()} key stored securely")
                    keys_set = True
                else:
                    print(f"❌ Failed to store {provider.capitalize()} key")
            else:
                print(f"⚠️  {provider.capitalize()} key skipped (optional)")
        except (KeyboardInterrupt, EOFError):
            print(f"\n👋 Setup cancelled.")
            return False
    
    if keys_set:
        print("\n✅ API keys have been securely stored and encrypted!")
        print("🔒 Your keys are protected with your password")
        print("💡 You can now use AI features in stableagents-ai")
        return True
    else:
        print("\n❌ No API keys were provided")
        print("You must provide at least one API key to use AI features.")
        return False

def setup_ai_provider(agent):
    """Interactive setup for AI provider and API key"""
    # First check if secure API management is available
    if check_secure_api_setup():
        # Try to get keys from secure manager
        try:
            from stableagents.api_key_manager import SecureAPIKeyManager
            manager = SecureAPIKeyManager()
            status = manager.check_payment_status()
            
            if status.get('paid', False) and status.get('api_keys_provided'):
                # User has secure keys, try to use them
                password = getpass.getpass("Enter your encryption password (or type 'exit' to quit): ")
                if check_exit_command(password):
                    exit_cli("👋 Setup cancelled.")
                
                # Try to get keys for each provider
                providers = ["openai", "anthropic", "google"]
                for provider in providers:
                    key = manager.get_api_key(provider, password)
                    if key:
                        agent.set_api_key(provider, key)
                        agent.set_active_ai_provider(provider)
                        print(f"✅ Using {provider.capitalize()} from secure storage")
                        return True
        except Exception as e:
            print(f"⚠️  Error accessing secure keys: {e}")
    
    # Fallback to legacy setup
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
    print("\n🔑 API KEY SETUP REQUIRED")
    print("=" * 30)
    print("To use AI features, you must configure an API key.")
    print("Please select a provider (or type 'exit' to quit):")
    for i, provider in enumerate(providers, 1):
        print(f"  {i}. {provider['name']}")
    
    while True:
        choice = input(f"\nSelect a provider (1-{len(providers)}) or type 'exit': ").strip()
        
        # Handle exit commands
        if check_exit_command(choice):
            exit_cli("👋 Setup cancelled.")
        
        try:
            choice_num = int(choice)
            if choice_num < 1 or choice_num > len(providers):
                print(f"Please enter a number between 1 and {len(providers)} or type 'exit'")
                continue
                
            provider_name = providers[choice_num-1]["name"]
            break
        except ValueError:
            print("Please enter a valid number or type 'exit'")
            continue
    
    # Ask for API key - REQUIRED, no skipping allowed
    print(f"\n🔑 {provider_name.capitalize()} API Key Required")
    print("=" * 40)
    print("You must provide an API key to continue.")
    print("Get your API key from:")
    
    if provider_name == "openai":
        print("   https://platform.openai.com/api-keys")
    elif provider_name == "anthropic":
        print("   https://console.anthropic.com/")
    elif provider_name == "google":
        print("   https://makersuite.google.com/app/apikey")
    else:
        print(f"   {provider_name} provider website")
    
    print("\nType 'exit' at any time to quit the setup.")
    print()
    
    while True:
        try:
            api_key = getpass.getpass(f"Enter your {provider_name.capitalize()} API key (or type 'exit'): ")
            
            # Check for exit command
            if check_exit_command(api_key):
                exit_cli("👋 Setup cancelled.")
            
            if api_key and api_key.strip():
                if agent.set_api_key(provider_name, api_key):
                    agent.set_active_ai_provider(provider_name)
                    print(f"✅ {provider_name.capitalize()} API key configured successfully.")
                    return True
                else:
                    print(f"❌ Failed to configure {provider_name.capitalize()} API key.")
                    print("Please check your API key and try again.")
                    continue
            else:
                print("❌ API key is required. Please enter a valid API key or type 'exit'.")
            continue
        except (KeyboardInterrupt, EOFError):
            exit_cli("👋 Setup cancelled.")
            
    return False

def interactive_mode(agent, setup_ai=True, banner_style="default"):
    """Run an interactive session with the agent"""
    # Display ASCII art banner
    print(get_banner(banner_style))
    
    print("Starting interactive stableagents-ai session.")
    print("Commands: memory.add TYPE KEY VALUE, memory.get TYPE [KEY], control [COMMAND], ai [PROMPT], apikey [PROVIDER] [KEY], help")
    print("New AI Commands: showcase, guided-setup, select-prompt, ai-capabilities")
    print("💡 Type 'exit', 'quit', or 'q' to exit the program")
    
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
            
            if check_exit_command(user_input):
                exit_cli("👋 Goodbye! Thanks for using stableagents-ai!")
                
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  memory.add TYPE KEY VALUE - Add to memory (TYPE: short_term, long_term, context)")
                print("  memory.get TYPE [KEY] - Get from memory")
                print("  control [COMMAND] - Control computer with natural language")
                print("  ai-control [NATURAL COMMAND] - Use AI to interpret and execute complex commands")
                print("  ai [PROMPT] - Generate text using the active AI provider")
                print("  chat [MESSAGE] - Chat with the AI provider")
                print("  apikey [PROVIDER] [KEY] - Set API key for a provider")
                print("  providers - List available AI providers")
                print("  provider list - Show detailed provider status")
                print("  provider [PROVIDER] - Set the active AI provider")
                print("  showcase [CATEGORY] - Show AI functionality examples")
                print("  guided-setup - Start guided setup with prompt selection")
                print("  select-prompt - Select a prompt and provider")
                print("  ai-capabilities - Check available AI capabilities")
                print("  health - Show system health report")
                print("  keys - Show API key management options")
                print("  add-key [PROVIDER] - Add a new API key")
                print("  remove-key [PROVIDER] - Remove an API key")
                print("  list-keys - List all configured providers")
                print("  change-password - Change encryption password")
                print("  switch-provider [PROVIDER] - Switch to a different AI provider")
                print("  current-provider - Show the current active AI provider")
                print("  reset - Reset the agent")
                print("  reconfigure - Reconfigure AI provider settings")
                print("  exit/quit/q - Exit the program")
                print()
                print("💡 AI Control Examples:")
                print("  ai-control open youtube and search for the latest bruno mars song")
                print("  ai-control search for python tutorials and open the first result")
                print("  ai-control take a screenshot and save it to desktop")
                print("  ai-control check system performance and show memory usage")
                print()
                print("💡 Type 'exit', 'quit', or 'q' to exit the program")
                continue
                
            if user_input.lower() == 'showcase':
                print(agent.show_prompts_showcase())
                continue
                
            if user_input.startswith('showcase '):
                category = user_input[9:].strip()
                print(agent.show_prompts_showcase(category))
                continue
                
            if user_input.lower() == 'guided-setup':
                print("🎯 Starting guided setup with prompt selection...")
                result = agent.show_guided_setup()
                print(f"Setup result: {result}")
                continue
                
            if user_input.lower() == 'select-prompt':
                print("🎯 Starting prompt and provider selection...")
                result = agent.select_prompt_and_provider()
                if result:
                    print("✅ Selection completed successfully!")
                else:
                    print("❌ Selection was cancelled.")
                continue
                
            if user_input.lower() == 'ai-capabilities':
                capabilities = agent.get_ai_capabilities()
                print("\n🔧 AI Capabilities:")
                for capability, available in capabilities.items():
                    status = "✅ Available" if available else "❌ Not Available"
                    print(f"   {capability}: {status}")
                continue
                
            if user_input.lower() == 'health':
                print("\n🏥 stableagents-ai Health Report")
                print("=" * 30)
                
                # Check AI providers
                providers = agent.list_ai_providers()
                print("\n🤖 AI Providers:")
                for provider in providers:
                    status = "✅" if provider["has_key"] else "❌"
                    active = " (active)" if provider["is_active"] else ""
                    print(f"  {status} {provider['name']}{active}")
                
                # Check memory
                print("\n🧠 Memory Status:")
                try:
                    short_term = agent.get_from_memory("short_term")
                    long_term = agent.get_from_memory("long_term")
                    context = agent.get_from_memory("context")
                    
                    print(f"  Short-term: {len(short_term)} items")
                    print(f"  Long-term: {len(long_term)} items")
                    print(f"  Context: {len(context)} items")
                except Exception as e:
                    print(f"  ❌ Error accessing memory: {e}")
                
                # Check self-healing if available
                try:
                    if hasattr(agent, 'self_healing') and agent.self_healing:
                        print("\n🔧 Self-Healing Status:")
                        health = agent.self_healing.get_health_status()
                        print(f"  Status: {health.get('status', 'Unknown')}")
                        print(f"  Issues: {health.get('issue_count', 0)}")
                except Exception as e:
                    pass  # Self-healing not available
                
                print("\n" + "=" * 30)
                continue
                
            if user_input.lower() == 'keys':
                print("🔐 API Key Management")
                print("=" * 25)
                print("Available commands:")
                print("  list-keys     - List all configured providers")
                print("  add-key       - Add a new API key")
                print("  remove-key    - Remove an API key")
                print("  change-password - Change encryption password")
                print("  status        - Check payment status")
                print()
                print("Or use: stableagents-keys --help for more options")
                continue
                
            if user_input.startswith('add-key '):
                parts = user_input.split(' ', 1)
                if len(parts) < 2:
                    print("Usage: add-key <provider>")
                    print("Providers: openai, anthropic, google")
                    continue
                
                provider = parts[1].lower()
                if provider not in ['openai', 'anthropic', 'google']:
                    print("❌ Invalid provider. Use: openai, anthropic, google")
                    continue
                
                print(f"🔑 Adding {provider.capitalize()} API Key")
                print("=" * 40)
                
                try:
                    import getpass
                    api_key = getpass.getpass(f"Enter your {provider.capitalize()} API key: ")
                    if api_key:
                        if agent.set_api_key(provider, api_key):
                            print(f"✅ {provider.capitalize()} API key stored")
                            
                            # Ask if user wants to set as active
                            set_active = input(f"Set {provider.capitalize()} as active provider? (y/n): ").strip().lower()
                            if set_active == 'y':
                                agent.set_active_ai_provider(provider)
                                print(f"✅ {provider.capitalize()} is now the active provider")
                        else:
                            print(f"❌ Failed to store {provider.capitalize()} API key")
                    else:
                        print("❌ API key required")
                except Exception as e:
                    print(f"❌ Error: {e}")
                continue
                
            if user_input.startswith('remove-key '):
                parts = user_input.split(' ', 1)
                if len(parts) < 2:
                    print("Usage: remove-key <provider>")
                    print("Providers: openai, anthropic, google")
                    continue
                
                provider = parts[1].lower()
                if provider not in ['openai', 'anthropic', 'google']:
                    print("❌ Invalid provider. Use: openai, anthropic, google")
                    continue
                
                print(f"🗑️  Removing {provider.capitalize()} API Key")
                print("=" * 40)
                
                # Confirm removal
                confirm = input(f"Are you sure you want to remove {provider.capitalize()} API key? (y/n): ").strip().lower()
                if confirm == 'y':
                    if agent.set_api_key(provider, ""):
                        print(f"✅ {provider.capitalize()} API key removed")
                    else:
                        print(f"❌ Failed to remove {provider.capitalize()} API key")
                else:
                    print("❌ Removal cancelled")
                continue
                
            if user_input.lower() == 'list-keys':
                print("📡 API Key Status")
                print("=" * 20)
                
                providers = agent.list_ai_providers()
                for provider in providers:
                    status = "✅" if provider["has_key"] else "❌"
                    active = " (active)" if provider["is_active"] else ""
                    print(f"  {status} {provider['name']}{active}")
                continue
                
            if user_input.lower() == 'change-password':
                print("🔐 Change Encryption Password")
                print("=" * 30)
                print("⚠️  Password change functionality not yet implemented")
                print("   This will be available in a future update")
                continue
                
            if user_input.startswith('switch-provider '):
                parts = user_input.split(' ', 1)
                if len(parts) < 2:
                    print("Usage: switch-provider <provider>")
                    print("Providers: openai, anthropic, google, local")
                    continue
                
                provider = parts[1].lower()
                if provider not in ['openai', 'anthropic', 'google', 'local']:
                    print("❌ Invalid provider. Use: openai, anthropic, google, local")
                    continue
                
                print(f"🔄 Switching to {provider.capitalize()}")
                print("=" * 40)
                
                if provider == 'local':
                    print("✅ Switched to local model mode")
                    print("💡 Make sure you have GGUF models in ~/.stableagents/models/")
                    agent.set_active_ai_provider("local")
                else:
                    # Check if provider has a key configured
                    providers = agent.list_ai_providers()
                    provider_info = next((p for p in providers if p['name'] == provider), None)
                    
                    if not provider_info or not provider_info['has_key']:
                        print(f"❌ No API key configured for {provider.capitalize()}")
                        print(f"   Use 'add-key {provider}' to add an API key first")
                    else:
                        if agent.set_active_ai_provider(provider):
                            print(f"✅ Switched to {provider.capitalize()}")
                        else:
                            print(f"❌ Failed to switch to {provider.capitalize()}")
                continue
                
            if user_input.lower() == 'current-provider':
                print("🤖 Current AI Provider")
                print("=" * 25)
                
                current_provider = agent.get_active_ai_provider()
                if current_provider:
                    print(f"✅ Active: {current_provider.capitalize()}")
                    
                    # Show provider details
                    providers = agent.list_ai_providers()
                    for provider in providers:
                        if provider['name'] == current_provider:
                            status = "✅" if provider['has_key'] else "❌"
                            print(f"   Status: {status} API key configured")
                            break
                else:
                    print("❌ No active provider")
                    print("   Use 'switch-provider <provider>' to set one")
                
                # Show available providers
                print("\n📡 Available Providers:")
                print("   openai    - OpenAI GPT models")
                print("   anthropic - Anthropic Claude models")
                print("   google    - Google AI models")
                print("   local     - Local GGUF models")
                continue
                
            if user_input.lower() == 'reset':
                agent.reset()
                print("Agent has been reset.")
                continue
                
            if user_input.lower() == 'reconfigure':
                print("🔧 Reconfiguring AI Provider")
                print("=" * 30)
                if agent.reconfigure_ai_provider():
                    print("✅ AI provider reconfigured successfully!")
                else:
                    print("❌ AI provider reconfiguration failed.")
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
                
            if user_input.startswith('ai-control '):
                command = user_input[11:].strip()
                if not command:
                    print("Please provide a natural language command after 'ai-control'")
                    print("Example: ai-control open youtube and play the latest bruno mars song")
                else:
                    print(f"🤖 Using AI to interpret: '{command}'")
                    print("⏳ Processing...")
                    result = agent.ai_control_computer(command)
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
                    print("Usage: apikey [PROVIDER] [KEY]")
                else:
                    provider_name = parts[1]
                    api_key = parts[2]
                    if agent.set_api_key(provider_name, api_key):
                        print(f"API key set for {provider_name}")
                        agent.set_active_ai_provider(provider_name)
                        print(f"Set {provider_name} as active provider")
                    else:
                        print(f"Failed to set API key for {provider_name}")
                continue
                
            if user_input.lower() == 'providers':
                providers = agent.list_ai_providers()
                print("\nAvailable AI providers:")
                for provider in providers:
                    status = "✓" if provider["has_key"] else "✗"
                    active = " (active)" if provider["is_active"] else ""
                    print(f"  {status} {provider['name']}{active}")
                print("\nTo set up a provider, use: apikey [PROVIDER] [KEY]")
                print("Example: apikey openai sk-...")
                continue
                
            if user_input.startswith('provider '):
                parts = user_input.split(' ', 1)
                if len(parts) < 2:
                    print("Usage: provider [PROVIDER] or provider list")
                    continue
                    
                subcommand = parts[1].strip()
                
                if subcommand.lower() == 'list':
                    providers = agent.list_ai_providers()
                    print("\nAI Provider Status:")
                    print("=" * 30)
                    for provider in providers:
                        status = "✅" if provider["has_key"] else "❌"
                        active = " (ACTIVE)" if provider["is_active"] else ""
                        print(f"  {status} {provider['name']}{active}")
                        
                        if provider["has_key"]:
                            # Show masked key for security
                            key = agent.get_api_key(provider["name"])
                            if key:
                                masked_key = key[:8] + "****" + key[-4:] if len(key) > 12 else "****"
                                print(f"      Key: {masked_key}")
                    print()
                    continue
                else:
                    # Set active provider
                    success = agent.set_active_ai_provider(subcommand)
                    if success:
                        print(f"Active provider set to {subcommand}")
                    else:
                        print(f"Failed to set active provider to {subcommand}")
                    continue
            
            # Default: display as message
            agent.display_messages(user_input)
            
        except KeyboardInterrupt:
            exit_cli("👋 Goodbye! Thanks for using stableagents-ai!")
        except EOFError:
            exit_cli("👋 Goodbye! Thanks for using stableagents-ai!")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Type 'help' for available commands or 'exit' to quit")
            continue

def run_examples(agent, banner_style="default"):
    """Run a guided example of AI capabilities"""
    # Display ASCII art banner for examples
    print(get_banner(banner_style))
    
    print("\nstableagents-ai AI Integration Example")
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

def interactive_prompt_selection():
    """Interactive prompt selection using the PromptsShowcase functionality"""
    print("\n🎯 INTERACTIVE PROMPT SELECTION")
    print("=" * 50)
    print("Let's pick a specific prompt to work with:")
    print("💡 Type 'exit', 'quit', or 'q' at any time to cancel")
    print()
    
    # Create agent instance
    agent = StableAgents()
    
    try:
        # Use the agent's prompt selection functionality
        result = agent.select_prompt_and_provider()
        if not result:
            print("❌ Prompt selection cancelled.")
            return None, None, None
        
        prompt_info = result.get("prompt", {})
        selected_provider = result.get("provider")
        
        if not prompt_info or not selected_provider:
            print("❌ Incomplete selection.")
            return None, None, None
        
        print(f"\n✅ Selected Prompt: {prompt_info.get('name', 'Unknown')}")
        print(f"📋 Prompt: {prompt_info.get('prompt', 'Unknown')}")
        print(f"🎯 Category: {prompt_info.get('category', 'Unknown')}")
        print(f"📊 Difficulty: {prompt_info.get('difficulty', 'Unknown')}")
        print(f"🤖 Provider: {selected_provider.upper()}")
        
        # Get provider info
        providers = {
            'openai': {
                'name': 'OpenAI (GPT-4, GPT-3.5)',
                'pros': ['Fast response times', 'Good for general tasks', 'Wide model selection'],
                'cons': ['Higher cost for GPT-4', 'Rate limits'],
                'best_for': ['General AI tasks', 'Quick prototyping', 'Content creation'],
                'cost': 'GPT-3.5: ~$0.002/1K tokens, GPT-4: ~$0.03/1K tokens'
            },
            'anthropic': {
                'name': 'Anthropic (Claude)',
                'pros': ['Excellent reasoning', 'Long context windows', 'Safety-focused'],
                'cons': ['Slower response times', 'Higher cost'],
                'best_for': ['Complex reasoning', 'Code generation', 'Analysis tasks'],
                'cost': 'Claude: ~$0.008/1K tokens'
            },
            'google': {
                'name': 'Google (PaLM, Gemini)',
                'pros': ['Good performance', 'Competitive pricing', 'Integration with Google services'],
                'cons': ['Limited model selection', 'Newer to market'],
                'best_for': ['Google ecosystem integration', 'Cost-effective solutions'],
                'cost': 'PaLM: ~$0.001/1K tokens, Gemini: ~$0.002/1K tokens'
            },
            'local': {
                'name': 'Local Models (GGUF)',
                'pros': ['Privacy-focused', 'No API costs', 'Works offline'],
                'cons': ['Limited model quality', 'Requires setup', 'Resource intensive'],
                'best_for': ['Privacy-sensitive tasks', 'Offline use', 'Learning/experimentation'],
                'cost': 'Free (one-time model download)'
            }
        }
        
        provider_info = providers.get(selected_provider, {})
        
        return selected_provider, provider_info, prompt_info
        
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Setup cancelled.")
        return None, None, None
    except Exception as e:
        print(f"\n❌ Error during prompt selection: {e}")
        return None, None, None

def guided_setup_with_prompt_selection():
    """Guided setup that includes payment options first, then prompt and provider selection"""
    print("\n🎯 GUIDED SETUP")
    print("=" * 50)
    print("This enhanced setup will help you:")
    print("1. 💳 Choose your payment/API key option")
    print("2. 📋 Explore what you can build with AI")
    print("3. 🤖 Choose your preferred AI provider (if needed)")
    print("4. 🔧 Get step-by-step setup instructions")
    print("5. 🚀 Start building immediately")
    print()
    print("💡 Type 'exit', 'quit', or 'q' at any time to cancel setup")
    print()
    
    # Step 1: Ask about payment/API key options FIRST
    print("💳 STEP 1: CHOOSE YOUR PAYMENT/API KEY OPTION")
    print("=" * 60)
    print("You have three options:")
    print()
    print("1. 💳 Monthly Subscription ($20/month)")
    print("   - We provide working API keys")
    print("   - Keys are securely encrypted")
    print("   - Monthly recurring billing")
    print("   - Cancel anytime")
    print("   - No setup fees or hidden costs")
    print()
    print("2. 🔑 Bring your own API keys")
    print("   - Use your existing OpenAI, Anthropic, etc. keys")
    print("   - Keys are securely encrypted")
    print("   - No additional cost beyond your API usage")
    print()
    print("3. 🏠 Use local models only")
    print("   - Download GGUF models for local inference")
    print("   - No API keys or payment required")
    print("   - Works offline, privacy-focused")
    print()
    print("💡 Type 'exit', 'quit', or 'q' at any time to cancel")
    print()
    
    try:
        payment_choice = input("Enter your choice (1-3): ").strip()
        
        if check_exit_command(payment_choice):
            exit_cli("👋 Setup cancelled.")
        
        if payment_choice == "1":
            # Monthly subscription - proceed with payment
            print("\n" + "="*60)
            print("💳 MONTHLY SUBSCRIPTION SETUP")
            print("="*60)
            
            try:
                from stableagents.api_key_manager import SecureAPIKeyManager
                from stableagents.stripe_payment import StripePaymentManager
                
                manager = SecureAPIKeyManager()
                stripe_manager = StripePaymentManager()
                
                if stripe_manager.process_monthly_subscription():
                    print("✅ Subscription active!")
                    print("📅 Your subscription will automatically renew each month")
                    print("💳 You can manage your subscription anytime")
                    print()
                    
                    # Get password for encryption
                    while True:
                        try:
                            password = getpass.getpass("Enter a password to encrypt your API keys (or type 'exit'): ")
                            if check_exit_command(password):
                                exit_cli("👋 Setup cancelled.")
                            if password:
                                confirm = getpass.getpass("Confirm password (or type 'exit'): ")
                                if check_exit_command(confirm):
                                    exit_cli("👋 Setup cancelled.")
                                if password == confirm:
                                    break
                                else:
                                    print("Passwords don't match. Please try again.")
                            else:
                                print("Password cannot be empty.")
                        except (KeyboardInterrupt, EOFError):
                            exit_cli("👋 Setup cancelled.")
                    
                    # Provide API keys
                    if manager.provide_api_keys_after_payment(password):
                        print("✅ API keys have been securely stored and encrypted!")
                        print("🔒 Your keys are protected with your password")
                        print("💡 You can now use AI features in stableagents-ai")
                        print("📅 Your subscription will renew monthly")
                        print("💳 Manage your subscription: Check your email for account details")
                        
                        # Now show what they can build
                        print("\n" + "="*60)
                        print("🚀 READY TO BUILD!")
                        print("="*60)
                        print("Your subscription is active! Here's what you can build:")
                        print()
                        print("🖥️  Computer Control Examples:")
                        print("   • 'Open my email and compose a new message'")
                        print("   • 'Create a new folder and organize my files'")
                        print("   • 'Search for Python tutorials and open the first 3 results'")
                        print()
                        print("🧠 AI Applications Examples:")
                        print("   • 'Create a chatbot for customer support'")
                        print("   • 'Build an app that reads PDFs and extracts key info'")
                        print("   • 'Make an AI assistant that can identify objects in photos'")
                        print()
                        print("💻 Code Generation Examples:")
                        print("   • 'Write a Python function to sort data'")
                        print("   • 'Create a web scraper for e-commerce sites'")
                        print("   • 'Generate code to integrate with REST APIs'")
                        print()
                        print("📝 Content Creation Examples:")
                        print("   • 'Write a 500-word blog post about AI trends'")
                        print("   • 'Create professional email templates'")
                        print("   • 'Generate engaging social media posts'")
                        print()
                        print("📊 Data Analysis Examples:")
                        print("   • 'Analyze monthly sales data and identify trends'")
                        print("   • 'Process customer reviews and extract sentiment'")
                        print("   • 'Build a model to predict customer churn'")
                        print()
                        print("⚡ Productivity Examples:")
                        print("   • 'Automatically categorize emails and draft responses'")
                        print("   • 'Create an AI assistant for meeting scheduling'")
                        print("   • 'Build a system to prioritize tasks'")
                        print()
                        
                        print("🎯 Ready to start building? Run: stableagents-ai interactive")
                        return True
                    else:
                        print("❌ Failed to provide API keys")
                        return False
                else:
                    print("❌ Subscription setup failed")
                    return False
            except Exception as e:
                print(f"❌ Error during subscription setup: {e}")
                return False
                
        elif payment_choice == "2":
            # Bring your own API keys - now ask which provider
            print("\n" + "="*60)
            print("🔑 BRING YOUR OWN API KEYS")
            print("="*60)
            print("Great! Let's set up your API keys. First, let's explore what you can build,")
            print("then choose which provider you'd like to use.")
            print()
            
            # Step 2: Show preview prompts and select provider
            selected_provider, provider_info, prompt_info = interactive_prompt_selection()
            
            if not selected_provider:
                return False
            
            # Step 3: Show setup instructions for the selected provider
            print("\n" + "="*60)
            print("🔧 SETUP INSTRUCTIONS")
            print("="*60)
            
            if selected_provider == 'local':
                instructions = f"""
🎯 Setup Instructions for Local Models
🤖 Provider: {provider_info['name']}

📋 NEXT STEPS:

1. 📥 Download GGUF Models:
   • Visit https://huggingface.co/TheBloke
   • Download a model like: llama-2-7b-chat.Q4_K_M.gguf
   • Place it in: ~/.stableagents/models/

2. 🔧 Configure Local Model:
   • Run: stableagents-ai setup
   • Choose "Local models only"
   • Point to your downloaded model

3. 🚀 Start Building:
   • Run: stableagents-ai interactive
   • Try your first AI prompt!
"""
            else:
                instructions = f"""
🎯 Setup Instructions for {provider_info['name']}
🤖 Provider: {selected_provider.upper()}

📋 NEXT STEPS:

1. 🔑 Get API Key:
   • Visit: {get_provider_url(selected_provider)}
   • Create account and get API key
   • Note: {provider_info['cost']}

2. 🔧 Configure API Key:
   • Run: stableagents-ai setup
   • Choose "Bring your own API keys"
   • Enter your {selected_provider.upper()} API key

3. 🚀 Start Building:
   • Run: stableagents-ai interactive
   • Try your first AI prompt!
"""
            
            print(instructions)
            
            # Step 4: Ask if they want to proceed with setup
            try:
                print("💡 Type 'exit', 'quit', or 'q' to cancel, or 'y' to continue")
                proceed = input("\nWould you like to proceed with the setup now? (y/n): ").strip().lower()
                
                if check_exit_command(proceed):
                    exit_cli("👋 Setup cancelled.")
                
                if proceed in ['y', 'yes']:
                    print("\n" + "="*60)
                    print("🔧 READY FOR API KEY SETUP")
                    print("="*60)
                    print("Now let's set up your API keys to start building!")
                    print()
                    
                    # Proceed with API key setup using the selected provider
                    return check_secure_api_setup(selected_provider, provider_info)
                else:
                    print("\n✅ Perfect! You now know what you can build and which provider to use.")
                    print("💡 When you're ready, run 'stableagents-ai setup' to configure your API keys.")
                    return True
            except (KeyboardInterrupt, EOFError):
                exit_cli("👋 Setup cancelled.")
                
        elif payment_choice == "3":
            # Local models only
            print("\n" + "="*60)
            print("🏠 LOCAL MODELS SETUP")
            print("="*60)
            print("Great choice! You can use StableAgents with local models.")
            print("Download GGUF models and place them in ~/.stableagents/models/")
            print("No API keys or payment required.")
            print()
            print("📋 NEXT STEPS:")
            print("1. Download GGUF models from https://huggingface.co/TheBloke")
            print("2. Place models in ~/.stableagents/models/")
            print("3. Run: stableagents-ai interactive")
            print("4. Start building with local AI!")
            print()
            print("🎉 Setup complete! You can now use StableAgents with local models.")
            return True
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
            return False
            
    except (KeyboardInterrupt, EOFError):
        exit_cli("👋 Setup cancelled.")
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False

def get_provider_url(provider: str) -> str:
    """Get signup URL for provider."""
    urls = {
        'openai': 'https://platform.openai.com/signup',
        'anthropic': 'https://console.anthropic.com/',
        'google': 'https://makersuite.google.com/app/apikey'
    }
    return urls.get(provider, 'https://example.com')

def main():
    parser = argparse.ArgumentParser(description='stableagents-ai CLI')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--banner', choices=['default', 'simple', 'compact'], default='default', 
                      help='Select ASCII art banner style (default, simple, compact)')
    parser.add_argument('--start', action='store_true', help='Start stableagents-ai with secure API setup')
    parser.add_argument('--model', help='AI model to use (openai, anthropic, google, etc.)')
    parser.add_argument('--api-key', help='API key for the model')
    parser.add_argument('--local', action='store_true', help='Use local model')
    parser.add_argument('--model-path', help='Path to local model file')
    parser.add_argument('--self-healing', action='store_true', help='Enable self-healing')
    parser.add_argument('--auto-recovery', action='store_true', help='Enable automatic recovery')
    parser.add_argument('--no-banner', action='store_true', help='Hide banner')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Interactive mode
    interactive_parser = subparsers.add_parser('interactive', help='Start interactive session')
    
    # Examples mode
    examples_parser = subparsers.add_parser('examples', help='Run guided AI examples')
    
    # Setup mode
    setup_parser = subparsers.add_parser('setup', help='Setup secure API keys')
    
    # Guided setup mode
    guided_parser = subparsers.add_parser('guided-setup', help='Guided setup with prompt and provider selection')
    
    # Prompt setup mode (NEW)
    prompt_setup_parser = subparsers.add_parser('prompt-setup', help='Interactive prompt and provider selection (new prompt setup)')
    
    # Payment link mode (NEW)
    payment_link_parser = subparsers.add_parser('payment-link', help='Create Stripe payment link for monthly subscription')
    
    # Prompts showcase mode
    showcase_parser = subparsers.add_parser('showcase', help='Show AI functionality examples and prompts')
    showcase_parser.add_argument('category', nargs='?', 
                                choices=['all', 'computer_control', 'desktop_applications', 'quick_start', 
                                       'help', 'beginner', 'intermediate', 'advanced'],
                                help='Category to show (default: welcome message)')
    
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
    
    # AI-powered computer control
    ai_control_parser = subparsers.add_parser('ai-control', help='Use AI to interpret and execute complex computer commands')
    ai_control_parser.add_argument('command', nargs='+', help='Natural language command for AI interpretation')
    
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
    provider_subparsers = provider_parser.add_subparsers(dest='provider_command', help='Provider command')
    
    # List providers
    list_parser = provider_subparsers.add_parser('list', help='List all providers with status')
    
    # Set active provider
    set_parser = provider_subparsers.add_parser('set', help='Set active AI provider')
    set_parser.add_argument('name', choices=['openai', 'anthropic', 'google', 'custom'], help='Provider name')
    
    # Desktop automation commands
    desktop_parser = subparsers.add_parser('desktop', help='Desktop automation commands')
    desktop_subparsers = desktop_parser.add_subparsers(dest='desktop_command', help='Desktop command')
    
    # Navigate command
    navigate_parser = desktop_subparsers.add_parser('navigate', help='Navigate to a URL')
    navigate_parser.add_argument('url', help='URL to navigate to')
    
    # Click command
    click_parser = desktop_subparsers.add_parser('click', help='Click an element')
    click_parser.add_argument('selector', help='CSS selector of the element to click')
    
    # Type command
    type_parser = desktop_subparsers.add_parser('type', help='Type text into an input field')
    type_parser.add_argument('selector', help='CSS selector of the input field')
    type_parser.add_argument('text', help='Text to type')
    
    # Screenshot command
    screenshot_parser = desktop_subparsers.add_parser('screenshot', help='Take a screenshot')
    screenshot_parser.add_argument('path', help='Path to save the screenshot')
    
    args = parser.parse_args()
    logger = setup_logging(args.verbose)
    
    # Display banner for all commands (unless --no-banner is specified)
    if args.command != 'interactive' and not args.no_banner:
        print(get_banner(args.banner))
    
    # Create agent instance
    agent = StableAgents()
    logger.debug("stableagents-ai initialized")
    
    # Handle --start flag
    if args.start:
        print("🚀 Starting stableagents-ai with secure setup...")
        print()
        
        # Run the new guided setup flow
        selected_provider, provider_info, prompt_info = interactive_prompt_selection()
        
        if selected_provider:
            # Proceed with API key setup using the selected provider
            setup_success = check_secure_api_setup(selected_provider, provider_info)
        else:
            setup_success = False
        
        if setup_success:
            print("\n" + "="*50)
            print("🎉 Setup complete! Starting interactive mode...")
            print("="*50)
            print()
            
            # Start interactive mode
            interactive_mode(agent, setup_ai=False, banner_style=args.banner)
            return 0
        else:
            print("\n⚠️  Setup incomplete. You can still use stableagents-ai with limited features.")
            print("💡 Run 'stableagents-ai setup' to configure API keys later.")
            print()
            
            # Start interactive mode anyway
            interactive_mode(agent, setup_ai=False, banner_style=args.banner)
            return 0
    
    # Handle direct model/API key arguments
    if args.model and args.api_key:
        success = agent.set_api_key(args.model, args.api_key)
        if success:
            agent.set_active_ai_provider(args.model)
            print(f"✅ Configured with {args.model.capitalize()}")
        else:
            print(f"❌ Failed to configure {args.model.capitalize()}")
    
    if args.local:
        print("🏠 Using local model mode")
        if args.model_path:
            print(f"Model path: {args.model_path}")
            agent.set_local_model(args.model_path)
        else:
            agent.set_local_model()
    
    if args.self_healing:
        agent.enable_self_healing(args.auto_recovery)
        if args.auto_recovery:
            print("🔧 Self-healing enabled with automatic recovery")
        else:
            print("🔧 Self-healing enabled (manual recovery)")
    
    # Process commands
    if args.command == 'interactive' or not args.command:
        # If no command specified, offer guided setup first
        if not args.command:
            print("🎯 Welcome to stableagents-ai!")
            print("=" * 40)
            print("Would you like to:")
            print("1. 🎯 Start guided setup (recommended for new users)")
            print("2. 🚀 Go directly to interactive mode")
            print("3. 📋 Explore examples and prompts")
            print()
            print("💡 Type 'exit', 'quit', or 'q' to exit")
            print()
            
            try:
                choice = input("Enter your choice (1-3): ").strip()
                
                # Handle exit commands
                if check_exit_command(choice):
                    exit_cli("👋 Goodbye!")
                
                if choice == "1":
                    print("\n🎯 Starting guided setup...")
                    setup_success = guided_setup_with_prompt_selection()
                    if setup_success:
                        print("\n✅ Guided setup completed successfully!")
                        print("🚀 Starting interactive mode...")
                        print("=" * 50)
                        print()
                        interactive_mode(agent, setup_ai=False, banner_style=args.banner)
                    else:
                        print("\n⚠️  Guided setup was not completed.")
                        print("🚀 Starting interactive mode anyway...")
                        print("=" * 50)
                        print()
                        interactive_mode(agent, setup_ai=False, banner_style=args.banner)
                    return 0
                elif choice == "2":
                    print("\n🚀 Starting interactive mode...")
                    interactive_mode(agent, banner_style=args.banner)
                elif choice == "3":
                    print("\n📋 Exploring examples and prompts...")
                    print(agent.show_prompts_showcase())
                    print("\n" + "="*60)
                    print("🚀 Ready to get started?")
                    print("="*60)
                    print("🎯 For new users: Run 'stableagents-ai guided-setup' for step-by-step setup")
                    print("🔧 For setup: Run 'stableagents-ai setup' to configure your AI provider")
                    print("🚀 For building: Run 'stableagents-ai interactive' to start building with AI")
                    print("💡 For examples: Run 'stableagents-ai examples' to see AI in action")
                    print()
                    print("💡 Type 'exit', 'quit', or 'q' to exit the program")
                    return 0
                else:
                    print("Invalid choice. Starting interactive mode...")
                    interactive_mode(agent, banner_style=args.banner)
            except (KeyboardInterrupt, EOFError):
                exit_cli("👋 Goodbye!")
        else:
            interactive_mode(agent, banner_style=args.banner)
    elif args.command == 'setup':
        print("🔐 Secure API Key Setup")
        print("=" * 25)
        setup_success = check_secure_api_setup()
        if setup_success:
            print("\n✅ Setup completed successfully!")
            print("🚀 Starting interactive mode...")
            print("=" * 50)
            print()
            interactive_mode(agent, setup_ai=False, banner_style=args.banner)
        else:
            print("\n⚠️  Setup was not completed.")
            print("🚀 Starting interactive mode anyway...")
            print("=" * 50)
            print()
            interactive_mode(agent, setup_ai=False, banner_style=args.banner)
        return 0
    elif args.command == 'guided-setup':
        print("🎯 Guided Setup with Prompt Selection")
        print("=" * 40)
        setup_success = guided_setup_with_prompt_selection()
        if setup_success:
            print("\n✅ Guided setup completed successfully!")
            print("🚀 Starting interactive mode...")
            print("=" * 50)
            print()
            interactive_mode(agent, setup_ai=False, banner_style=args.banner)
        else:
            print("\n⚠️  Guided setup was not completed.")
            print("🚀 Starting interactive mode anyway...")
            print("=" * 50)
            print()
            interactive_mode(agent, setup_ai=False, banner_style=args.banner)
        return 0
    elif args.command == 'examples':
        return run_examples(agent, args.banner)
    elif args.command == 'showcase':
        print("🎯 AI Functionality Showcase")
        print("=" * 40)
        if args.category:
            print(agent.show_prompts_showcase(args.category))
        else:
            print(agent.show_prompts_showcase())
        
        print("\n" + "="*60)
        print("🚀 Ready to get started?")
        print("="*60)
        print("🎯 For new users: Run 'stableagents-ai guided-setup' for step-by-step setup")
        print("🔧 For setup: Run 'stableagents-ai setup' to configure your AI provider")
        print("🚀 For building: Run 'stableagents-ai interactive' to start building with AI")
        print("💡 For examples: Run 'stableagents-ai examples' to see AI in action")
        print()
        print("💡 Type 'exit', 'quit', or 'q' to exit the program")
        return 0
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
    elif args.command == 'ai-control':
        # Check if we have an active provider with key
        if not agent.get_active_ai_provider():
            print("No active AI provider. Setting up now...")
            if not setup_ai_provider(agent):
                print("AI setup failed. Exiting.")
                return 1
        
        command = ' '.join(args.command)
        print(f"🤖 Using AI to interpret: '{command}'")
        print("⏳ Processing...")
        result = agent.ai_control_computer(command)
        print(result)
    elif args.command == 'ai':
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
            status = "✓" if provider["has_key"] else "✗"
            active = " (active)" if provider["is_active"] else ""
            print(f"  {status} {provider['name']}{active}")
    elif args.command == 'provider':
        if args.provider_command == 'list':
            providers = agent.list_ai_providers()
            print("\nAI Provider Status:")
            print("=" * 30)
            for provider in providers:
                status = "✅" if provider["has_key"] else "❌"
                active = " (ACTIVE)" if provider["is_active"] else ""
                print(f"  {status} {provider['name']}{active}")
                
                if provider["has_key"]:
                    # Show masked key for security
                    key = agent.get_api_key(provider["name"])
                    if key:
                        masked_key = key[:8] + "****" + key[-4:] if len(key) > 12 else "****"
                        print(f"      Key: {masked_key}")
            print()
        elif args.provider_command == 'set':
            success = agent.set_active_ai_provider(args.name)
            if success:
                print(f"Active provider set to {args.name}")
            else:
                print(f"Failed to set active provider to {args.name}")
        else:
            print("Usage: provider list or provider set [PROVIDER]")
    elif args.command == 'desktop':
        desktop = DesktopAutomation()
        try:
            if args.desktop_command == 'navigate':
                run_async(desktop.navigate(args.url))
                print(f"Navigated to {args.url}")
            elif args.desktop_command == 'click':
                run_async(desktop.click(args.selector))
                print(f"Clicked element: {args.selector}")
            elif args.desktop_command == 'type':
                run_async(desktop.type_text(args.selector, args.text))
                print(f"Typed text into: {args.selector}")
            elif args.desktop_command == 'screenshot':
                run_async(desktop.screenshot(args.path))
                print(f"Screenshot saved to: {args.path}")
            else:
                print("Unknown desktop command. Use --help for available commands.")
        finally:
            run_async(desktop.close())
    elif args.command == 'prompt-setup':
        print("\n🎯 Interactive Prompt and Provider Setup")
        print("=" * 50)
        print("💡 Type 'exit', 'quit', or 'q' at any time to cancel")
        print()
        selected_provider, provider_info, prompt_info = interactive_prompt_selection()
        if not selected_provider:
            print("❌ Prompt setup was cancelled.")
            return 1
        print("\n" + "="*60)
        print("📋 SETUP INSTRUCTIONS")
        print("="*60)
        # Print setup instructions for the selected prompt and provider
        instructions = agent.prompts_showcase.get_setup_instructions(prompt_info, selected_provider)
        print(instructions)
        print("\nNext steps:")
        print("1. Get your API key from the selected provider (if needed)")
        print("2. Run 'stableagents-ai setup' to configure your keys")
        print("3. Run 'stableagents-ai interactive' to start building with your selected prompt!")
        print()
        print("💡 Type 'exit', 'quit', or 'q' to exit the program")
        return 0
    elif args.command == 'payment-link':
        print("\n💳 Creating Stripe payment link...")
        try:
            from stableagents.stripe_payment import StripePaymentManager
            from stableagents.api_key_manager import SecureAPIKeyManager
            
            stripe_manager = StripePaymentManager()
            manager = SecureAPIKeyManager()
            
            payment_url = stripe_manager.create_payment_link()
            
            if payment_url:
                print("✅ Payment link created successfully!")
                print(f"🔗 Payment URL: {payment_url}")
                print()
                print("📋 Instructions:")
                print("1. Click the payment link above or copy it to your browser")
                print("2. Complete the subscription setup")
                print("3. After payment, you'll be redirected to a success page")
                print("4. Copy the session_id from the URL and paste it below")
                print()
                
                # Try to open the payment link
                try:
                    webbrowser.open(payment_url)
                    print("🌐 Payment page opened in your browser")
                except Exception as e:
                    print(f"⚠️  Could not open browser automatically: {e}")
                    print("Please manually visit the payment URL above")
                
                print()
                session_id = input("Paste the session_id from the success URL here (or press Enter to skip): ").strip()
                
                if session_id:
                    print("\n🔍 Verifying payment with Stripe...")
                    if stripe_manager._verify_checkout_session(session_id):
                        print("✅ Subscription active!")
                        print("📅 Your subscription will automatically renew each month")
                        print("💳 You can manage your subscription anytime")
                        print()
                        
                        # Get password for encryption
                        while True:
                            try:
                                password = getpass.getpass("Enter a password to encrypt your API keys (or type 'exit'): ")
                                if check_exit_command(password):
                                    exit_cli("👋 Setup cancelled.")
                                if password:
                                    confirm = getpass.getpass("Confirm password (or type 'exit'): ")
                                    if check_exit_command(confirm):
                                        exit_cli("👋 Setup cancelled.")
                                    if password == confirm:
                                        break
                                    else:
                                        print("Passwords don't match. Please try again.")
                                else:
                                    print("Password cannot be empty.")
                            except (KeyboardInterrupt, EOFError):
                                exit_cli("👋 Setup cancelled.")
                        
                        # Provide API keys
                        if manager.provide_api_keys_after_payment(password):
                            print("✅ API keys have been securely stored and encrypted!")
                            print("🔒 Your keys are protected with your password")
                            print("💡 You can now use AI features in stableagents-ai")
                            print("📅 Your subscription will renew monthly")
                            print("💳 Manage your subscription: Check your email for account details")
                            return 0
                        else:
                            print("❌ Failed to provide API keys")
                            return 1
                    else:
                        print("❌ Payment verification failed")
                        print("💡 You can still complete the payment manually and try again")
                        return 1
                else:
                    print("💡 Payment link created but not completed")
                    print("You can complete the payment later by visiting the URL above")
                    return 0
            else:
                print("❌ Failed to create payment link")
                print("Please check your Stripe configuration")
                return 1
        except Exception as e:
            print(f"❌ Error with Stripe integration: {e}")
            print("Please check your Stripe configuration and try again")
            return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 