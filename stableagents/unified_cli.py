#!/usr/bin/env python3
"""
Unified CLI for StableAgents that provides simple access to all framework features.
"""
import sys
import os
import argparse
from stableagents import StableAgents
from stableagents.core import get_banner, LogManager

# Set up logging
log_manager = LogManager()
logger = log_manager.logger

class UnifiedCLI:
    def __init__(self):
        self.agent = StableAgents()
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
            "health": self.health_command
        }
        self.use_local_model = False
        self.local_model_path = None
        self.self_healing_enabled = False
        self.auto_recovery = False
        
    def start(self, model=None, api_key=None, use_local=False, model_path=None, 
              enable_self_healing=False, auto_recovery=False):
        """Start the CLI interface"""
        # Display banner
        print(get_banner("simple"))
        
        # Set up local or remote provider
        self.use_local_model = use_local
        self.local_model_path = model_path
        self.self_healing_enabled = enable_self_healing
        self.auto_recovery = auto_recovery
        
        # Initialize the agent with self-healing if enabled
        if self.self_healing_enabled:
            # Re-create the agent with self-healing enabled
            self.agent = StableAgents(enable_self_healing=True)
            
            if self.auto_recovery:
                self.agent.self_healing.set_config({
                    "auto_recovery": True,
                    "min_severity_for_recovery": "medium"
                })
                print("Self-healing enabled with automatic recovery")
            else:
                print("Self-healing enabled (manual recovery)")
        
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
                logger.error(f"Error in command execution: {e}")
    
    def show_help(self, args):
        """Show help information"""
        print("\nAvailable commands:")
        print("  ai <prompt>       - Generate text using AI")
        print("  memory add <type> <key> <value> - Add to memory")
        print("  memory get <type> [key]        - Get from memory")
        print("  control <command> - Control computer with natural language")
        print("  provider list     - List available AI providers")
        print("  provider set <n> <key> - Set provider and API key")
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
        # Check if AI provider is configured
        if not self.use_local_model and not self.agent.get_active_ai_provider():
            print("No active AI provider. Please set one with 'provider set <n> <key>'")
            return
            
        # If this is a chat-style message (not a command prefix), use chat mode
        if " " not in prompt or prompt.split()[0] not in self.commands:
            messages = [{"role": "user", "content": prompt}]
            result = self.agent.generate_chat(messages)
        else:
            result = self.agent.generate_text(prompt)
            
        print(f"AI: {result}")
    
    def memory_command(self, args):
        """Memory operations"""
        if not args:
            print("Usage: memory add <type> <key> <value> or memory get <type> [key]")
            return
            
        parts = args.split(maxsplit=3)
        sub_command = parts[0].lower() if parts else ""
        
        if sub_command == "add" and len(parts) >= 4:
            mem_type, key, value = parts[1], parts[2], parts[3]
            self.agent.add_to_memory(mem_type, key, value)
            print(f"Added to {mem_type} memory: {key} = {value}")
        elif sub_command == "get" and len(parts) >= 2:
            mem_type = parts[1]
            key = parts[2] if len(parts) > 2 else None
            result = self.agent.get_from_memory(mem_type, key)
            print(f"Memory ({mem_type}, {key}):", result)
        else:
            print("Usage: memory add <type> <key> <value> or memory get <type> [key]")
    
    def control_command(self, args):
        """Control computer with natural language"""
        if not args:
            print("Please provide a command after 'control'")
            return
            
        result = self.agent.control_computer(args)
        print(result)
    
    def provider_command(self, args):
        """Provider operations"""
        if not args:
            print("Usage: provider list or provider set <n> <key>")
            return
            
        parts = args.split(maxsplit=2)
        sub_command = parts[0].lower() if parts else ""
        
        if sub_command == "list":
            providers = self.agent.list_ai_providers()
            print("\nAvailable AI providers:")
            for provider in providers:
                status = "ACTIVE" if provider["is_active"] else ""
                key_status = "✓" if provider["has_key"] else "✗"
                print(f"  {provider['name']} {status} [Key: {key_status}]")
        elif sub_command == "set" and len(parts) >= 3:
            provider, key = parts[1], parts[2]
            success = self.agent.set_api_key(provider, key)
            if success:
                self.agent.set_active_ai_provider(provider)
                print(f"Active provider set to {provider}")
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
        """Show system health information"""
        if not self.agent.self_healing_enabled:
            print("Self-healing is not enabled. Start with --self-healing to enable.")
            return
            
        health_report = self.agent.get_health_report()
        
        print("\nSystem Health Report:")
        print(f"Status: {health_report.get('status', 'unknown')}")
        
        # Show components health
        if "components" in health_report:
            print("\nComponents:")
            for comp_id, comp_data in health_report["components"].items():
                status = "✓ Healthy" if comp_data.get("healthy", False) else "✗ Unhealthy"
                print(f"  {comp_id}: {status}")
                
                # Show metrics for unhealthy components
                if not comp_data.get("healthy", False):
                    for metric in comp_data.get("metrics", []):
                        if not metric.get("healthy", True):
                            print(f"    - {metric['name']}: {metric['value']} (unhealthy)")
        
        # Show active issues
        active_issues = health_report.get("active_issues", [])
        if active_issues:
            print(f"\nActive Issues ({len(active_issues)}):")
            for issue in active_issues:
                print(f"  - {issue['severity'].upper()}: {issue['component']} - {issue['description']}")
                
                # Show recovery plan if available
                if "recovery_plans" in health_report and issue["id"] in health_report["recovery_plans"]:
                    plan = health_report["recovery_plans"][issue["id"]]
                    status = "Succeeded" if plan["success"] else "Failed"
                    print(f"    Recovery: {status} ({plan['actions_executed']} actions)")
        else:
            print("\nNo active issues detected")
            
        # Show recovery status
        print(f"\nAutomatic Recovery: {'Enabled' if health_report.get('auto_recovery', False) else 'Disabled'}")
        print(f"Monitoring Interval: {health_report.get('monitoring_interval', 'unknown')} seconds")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='StableAgents Unified CLI')
    parser.add_argument('--model', choices=['openai', 'anthropic', 'google', 'custom'], 
                        help='AI provider model (optional)')
    parser.add_argument('--key', help='API key for the model (optional)')
    parser.add_argument('--local', action='store_true', help='Use local model instead of remote')
    parser.add_argument('--model-path', help='Path to a local model file (optional, used with --local)')
    parser.add_argument('--self-healing', action='store_true', help='Enable self-healing capabilities')
    parser.add_argument('--auto-recovery', action='store_true', 
                      help='Enable automatic recovery (implies --self-healing)')
    
    args = parser.parse_args()
    
    # If auto-recovery is enabled, also enable self-healing
    enable_self_healing = args.self_healing or args.auto_recovery
    
    # Start the CLI
    cli = UnifiedCLI()
    cli.start(args.model, args.key, args.local, args.model_path, enable_self_healing, args.auto_recovery)
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 