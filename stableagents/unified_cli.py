#!/usr/bin/env python3
"""
Unified CLI for StableAgents that provides simple access to all framework features.
"""
import sys
import os
import argparse

class UnifiedCLI:
    def __init__(self):
        # Lazy load heavy modules
        self.agent = None
        self.log_manager = None
        self.commands = {
            "help": self.show_help,
            "exit": self.exit,
            "quit": self.exit,
            "ai": self.ai_command,
            "memory": self.memory_command,
            "control": self.control_command,
            "provider": self.provider_command,
            "providers": self.providers_command,
            "clear": self.clear_screen,
            "health": self.health_command,
            "setup": self.setup_command
        }
        self.use_local_model = False
        self.local_model_path = None
        self.self_healing_enabled = False
        self.auto_recovery = False
        
    def _lazy_load_agent(self):
        """Lazy load the StableAgents instance"""
        if self.agent is None:
            from stableagents import StableAgents
            self.agent = StableAgents()
        return self.agent
        
    def _lazy_load_logging(self):
        """Lazy load the logging manager"""
        if self.log_manager is None:
            from stableagents.core import LogManager
            self.log_manager = LogManager()
        return self.log_manager
        
    def start(self, model=None, api_key=None, use_local=False, model_path=None, 
              enable_self_healing=False, auto_recovery=False, show_banner=True):
        """Start the CLI interface"""
        # Display banner only if requested
        if show_banner:
            from stableagents.core import get_banner
            print(get_banner("simple"))
        
        # Set up local or remote provider
        self.use_local_model = use_local
        self.local_model_path = model_path
        self.self_healing_enabled = enable_self_healing
        self.auto_recovery = auto_recovery
        
        # Initialize the agent with self-healing if enabled
        agent = self._lazy_load_agent()
        
        if self.self_healing_enabled:
            # Re-create the agent with self-healing enabled
            from stableagents import StableAgents
            self.agent = StableAgents(enable_self_healing=True)
            
            if self.auto_recovery:
                self.agent.self_healing.set_config({
                    "auto_recovery": True,
                    "min_severity_for_recovery": "medium"
                })
                print("Self-healing enabled with automatic recovery")
            else:
                print("Self-healing enabled (manual recovery)")
        
        # Check for secure API setup if not using local models
        if not use_local and not model and not api_key:
            self._check_secure_api_setup()
        
        if use_local:
            print("Using local model")
            if model_path:
                print(f"Model path: {model_path}")
                self.agent.set_local_model(model_path)
            else:
                self.agent.set_local_model()
        elif model and api_key:
            success = self.agent.set_api_key(model, api_key)
            if success:
                self.agent.set_active_ai_provider(model)
                print(f"Using AI provider: {model}")
            else:
                print(f"Failed to set API key for {model}")
                
        # Print welcome message
        print("\nStableAgents CLI - Type 'help' for available commands")
        
        # Main loop
        while True:
            try:
                user_input = input("\n> ").strip()
                if not user_input:
                    continue
                    
                # Parse the command
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                # Execute the command
                if command in self.commands:
                    self.commands[command](args)
                else:
                    # Default to sending to AI
                    self.ai_command(user_input)
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                log_manager = self._lazy_load_logging()
                log_manager.logger.error(f"Error in command execution: {e}")
    
    def _check_secure_api_setup(self):
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
            print("\n🔐 Welcome to StableAgents!")
            print("=" * 40)
            print("To use AI features, you need to set up API keys securely.")
            print()
            
            # Show options
            print("You have three options:")
            print()
            print("1. 💳 Pay $20 for managed API keys")
            print("   - We provide working API keys")
            print("   - Keys are securely encrypted")
            print("   - One-time payment, no recurring charges")
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
            
            while True:
                try:
                    choice = input("Enter your choice (1-3): ").strip()
                    
                    if choice == "1":
                        return self._setup_payment_option(manager)
                    elif choice == "2":
                        return self._setup_custom_keys(manager)
                    elif choice == "3":
                        print("✅ Local model mode selected")
                        print("💡 To use local models, download GGUF files to ~/.stableagents/models/")
                        return True
                    else:
                        print("Please enter 1, 2, or 3")
                except KeyboardInterrupt:
                    print("\nSetup cancelled. You can run 'setup' command later.")
                    return False
                    
        except ImportError:
            print("⚠️  Secure API key management not available")
            print("   Using legacy API key management")
            return False
    
    def _setup_payment_option(self, manager):
        """Setup payment option for managed API keys"""
        import getpass
        
        print("\n💳 Payment Setup")
        print("=" * 20)
        print("Processing payment for API key access...")
        print("Amount: $20.00 USD")
        print()
        
        if manager.process_payment():
            print("✅ Payment successful!")
            print()
            
            # Get password for encryption
            while True:
                password = getpass.getpass("Enter a password to encrypt your API keys: ")
                if password:
                    confirm = getpass.getpass("Confirm password: ")
                    if password == confirm:
                        break
                    else:
                        print("Passwords don't match. Please try again.")
                else:
                    print("Password cannot be empty.")
            
            # Provide API keys
            if manager.provide_api_keys_after_payment(password):
                print("✅ API keys have been securely stored and encrypted!")
                print("🔒 Your keys are protected with your password")
                print("💡 You can now use AI features in StableAgents")
                return True
            else:
                print("❌ Failed to provide API keys")
                return False
        else:
            print("❌ Payment failed")
            return False
    
    def _setup_custom_keys(self, manager):
        """Setup custom API keys"""
        import getpass
        
        print("\n🔑 Custom API Key Setup")
        print("=" * 25)
        print("Enter your API keys securely. They will be encrypted.")
        print()
        
        # Get password for encryption
        while True:
            password = getpass.getpass("Enter a password to encrypt your API keys: ")
            if password:
                confirm = getpass.getpass("Confirm password: ")
                if password == confirm:
                    break
                else:
                    print("Passwords don't match. Please try again.")
            else:
                print("Password cannot be empty.")
        
        # Reset encryption
        manager.reset_encryption()
        
        # Collect API keys
        providers = ["openai", "anthropic", "google"]
        keys_set = False
        
        for provider in providers:
            print(f"\n{provider.capitalize()} API Key (press Enter to skip):")
            api_key = getpass.getpass("> ")
            
            if api_key:
                if manager.set_api_key(provider, api_key, password):
                    print(f"✅ {provider.capitalize()} key stored securely")
                    keys_set = True
                else:
                    print(f"❌ Failed to store {provider.capitalize()} key")
        
        if keys_set:
            print("\n✅ API keys have been securely stored and encrypted!")
            print("🔒 Your keys are protected with your password")
            print("💡 You can now use AI features in StableAgents")
            return True
        else:
            print("\n⚠️  No API keys were set")
            return False
    
    def show_help(self, args):
        """Show help information"""
        print("\nAvailable commands:")
        print("  ai <prompt>       - Generate text using AI")
        print("  memory add <type> <key> <value> - Add to memory")
        print("  memory get <type> [key]        - Get from memory")
        print("  control <command> - Control computer with natural language")
        print("  provider list     - List available AI providers")
        print("  provider set <n> <key> - Set provider and API key")
        print("  setup             - Setup secure API keys")
        print("  health            - Show system health report")
        print("  clear             - Clear the screen")
        print("  help              - Show this help message")
        print("  exit/quit         - Exit the program")
        
        if self.use_local_model:
            print("\nRunning with local model")
            if self.local_model_path:
                print(f"Model path: {self.local_model_path}")
                
        if self.self_healing_enabled:
            if self.auto_recovery:
                print("\nSelf-healing enabled with automatic recovery")
            else:
                print("\nSelf-healing enabled (manual recovery)")
        
        print("\nDefault: Any text not matching a command is sent to the AI")
    
    def exit(self, args):
        """Exit the program"""
        print("Goodbye!")
        sys.exit(0)
    
    def ai_command(self, prompt):
        """Generate text using AI"""
        agent = self._lazy_load_agent()
        
        # Check if AI provider is configured
        if not self.use_local_model and not agent.get_active_ai_provider():
            print("No active AI provider. Please set one with 'provider set <n> <key>'")
            return
            
        # If this is a chat-style message (not a command prefix), use chat mode
        if " " not in prompt or prompt.split()[0] not in self.commands:
            messages = [{"role": "user", "content": prompt}]
            result = agent.generate_chat(messages)
        else:
            result = agent.generate_text(prompt)
            
        print(f"AI: {result}")
    
    def memory_command(self, args):
        """Memory operations"""
        if not args:
            print("Usage: memory add <type> <key> <value> or memory get <type> [key]")
            return
            
        parts = args.split(maxsplit=3)
        sub_command = parts[0].lower() if parts else ""
        
        agent = self._lazy_load_agent()
        
        if sub_command == "add" and len(parts) >= 4:
            mem_type, key, value = parts[1], parts[2], parts[3]
            agent.add_to_memory(mem_type, key, value)
            print(f"Added to {mem_type} memory: {key} = {value}")
        elif sub_command == "get" and len(parts) >= 2:
            mem_type = parts[1]
            key = parts[2] if len(parts) > 2 else None
            result = agent.get_from_memory(mem_type, key)
            print(f"Memory ({mem_type}, {key}):", result)
        else:
            print("Usage: memory add <type> <key> <value> or memory get <type> [key]")
    
    def control_command(self, args):
        """Control computer with natural language"""
        if not args:
            print("Please provide a command after 'control'")
            return
            
        agent = self._lazy_load_agent()
        result = agent.control_computer(args)
        print(result)
    
    def provider_command(self, args):
        """Provider operations"""
        if not args:
            print("Usage: provider list or provider set <n> <key>")
            return
            
        parts = args.split(maxsplit=2)
        sub_command = parts[0].lower() if parts else ""
        
        agent = self._lazy_load_agent()
        
        if sub_command == "list":
            providers = agent.list_ai_providers()
            print("\nAvailable AI providers:")
            for provider in providers:
                status = "ACTIVE" if provider["is_active"] else ""
                key_status = "✓" if provider["has_key"] else "✗"
                print(f"  {provider['name']} {status} [Key: {key_status}]")
        elif sub_command == "set" and len(parts) >= 3:
            provider, key = parts[1], parts[2]
            success = agent.set_api_key(provider, key)
            if success:
                agent.set_active_ai_provider(provider)
                print(f"Set {provider} as active provider")
            else:
                print(f"Failed to set API key for {provider}")
        else:
            print("Usage: provider list or provider set <n> <key>")
    
    def providers_command(self, args):
        """List available AI providers"""
        print("\nAvailable AI providers:")
        print("  openai - OpenAI's GPT models")
        print("  anthropic - Anthropic's Claude models")
        print("\nTo set up a provider, use: provider set [PROVIDER] [KEY]")
        print("Example: provider set openai sk-...")
    
    def clear_screen(self, args):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(get_banner("simple"))
    
    def health_command(self, args):
        """Show system health report"""
        agent = self._lazy_load_agent()
        
        print("\n🏥 StableAgents Health Report")
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
        
        # Check self-healing if enabled
        if self.self_healing_enabled:
            print("\n🔧 Self-Healing Status:")
            try:
                health = agent.self_healing.get_health_status()
                print(f"  Status: {health.get('status', 'Unknown')}")
                print(f"  Issues: {health.get('issue_count', 0)}")
                print(f"  Auto-recovery: {'✅' if self.auto_recovery else '❌'}")
            except Exception as e:
                print(f"  ❌ Error checking self-healing: {e}")
        
        # Check local model if enabled
        if self.use_local_model:
            print("\n🏠 Local Model Status:")
            if self.local_model_path:
                if os.path.exists(self.local_model_path):
                    print(f"  ✅ Model file exists: {self.local_model_path}")
                else:
                    print(f"  ❌ Model file not found: {self.local_model_path}")
            else:
                print("  ⚠️  No specific model path set")
        
        print("\n" + "=" * 30)
    
    def setup_command(self, args):
        """Setup secure API keys"""
        print("🔐 Secure API Key Setup")
        print("=" * 25)
        setup_success = self._check_secure_api_setup()
        if setup_success:
            print("\n✅ Setup completed successfully!")
        else:
            print("\n⚠️  Setup was not completed.")
        return setup_success

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='StableAgents Unified CLI')
    parser.add_argument('--model', help='AI model to use (openai, anthropic, google, etc.)')
    parser.add_argument('--api-key', help='API key for the model')
    parser.add_argument('--local', action='store_true', help='Use local model')
    parser.add_argument('--model-path', help='Path to local model file')
    parser.add_argument('--self-healing', action='store_true', help='Enable self-healing')
    parser.add_argument('--auto-recovery', action='store_true', help='Enable automatic recovery')
    parser.add_argument('--no-banner', action='store_true', help='Hide banner')
    parser.add_argument('--start', action='store_true', help='Start with secure API setup')
    
    args = parser.parse_args()
    
    # Create CLI instance
    cli = UnifiedCLI()
    
    # Handle --start flag
    if args.start:
        print("🚀 Starting StableAgents with secure setup...")
        print()
        
        # Run secure setup
        setup_success = cli._check_secure_api_setup()
        
        if setup_success:
            print("\n" + "="*50)
            print("🎉 Setup complete! Starting interactive mode...")
            print("="*50)
            print()
        else:
            print("\n⚠️  Setup incomplete. You can still use StableAgents with limited features.")
            print("💡 Run 'setup' command to configure API keys later.")
            print()
    
    # Start the CLI
    cli.start(
        model=args.model,
        api_key=args.api_key,
        use_local=args.local,
        model_path=args.model_path,
        enable_self_healing=args.self_healing,
        auto_recovery=args.auto_recovery,
        show_banner=not args.no_banner
    )

if __name__ == '__main__':
    main() 