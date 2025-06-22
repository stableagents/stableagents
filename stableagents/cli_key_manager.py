#!/usr/bin/env python3
"""
StableAgents CLI Key Manager

A command-line interface for securely managing API keys with payment processing.
"""

import sys
import os
import argparse
import getpass

# Add parent directory to path to import stableagents
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stableagents.api_key_manager import SecureAPIKeyManager

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='StableAgents Secure API Key Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Set up API keys with payment
  stableagents-keys setup

  # Check payment status
  stableagents-keys status

  # Reset encryption (for testing)
  stableagents-keys reset

  # List providers
  stableagents-keys list

  # Add a specific API key
  stableagents-keys add openai

  # Show payment options
  stableagents-keys options
        """
    )
    
    parser.add_argument('command', choices=[
        'setup', 'status', 'reset', 'list', 'add', 'options'
    ], help='Command to execute')
    
    parser.add_argument('--provider', choices=['openai', 'anthropic', 'google'],
                       help='Provider for add command')
    
    parser.add_argument('--password', help='Password for encryption (not recommended)')
    
    args = parser.parse_args()
    
    # Initialize the secure manager
    manager = SecureAPIKeyManager()
    
    if args.command == 'setup':
        # Set up API keys
        print("🔐 StableAgents API Key Setup")
        print("=" * 40)
        
        # Check if already set up
        status = manager.check_payment_status()
        if status.get("paid") or status.get("api_keys_provided"):
            print("✅ API keys already configured")
            print(f"   Payment status: {'Paid' if status.get('paid') else 'Not paid'}")
            print(f"   Providers: {', '.join(status.get('api_keys_provided', []))}")
            
            change = input("\nWould you like to reconfigure? (y/n): ").strip().lower()
            if change != 'y':
                return 0
        
        # Show payment options
        manager.show_payment_options()
        
        # Get user choice
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Process payment
            if manager.process_payment():
                password = getpass.getpass("Enter a password to encrypt your API keys: ")
                if password:
                    manager.provide_api_keys_after_payment(password)
                    print("\n🎉 Setup complete! You can now use StableAgents with AI providers.")
                else:
                    print("❌ Password required for encryption")
                    return 1
            else:
                print("❌ Payment failed")
                return 1
        
        elif choice == "2":
            # Custom API keys
            password = getpass.getpass("Enter a password to encrypt your API keys: ")
            if password:
                if manager.setup_custom_api_keys(password):
                    print("\n🎉 Setup complete! You can now use StableAgents with your API keys.")
                else:
                    print("❌ Setup failed")
                    return 1
            else:
                print("❌ Password required for encryption")
                return 1
        
        elif choice == "3":
            # Local models only
            print("\n🏠 Local Models Setup")
            print("=" * 30)
            print("Great choice! You can use StableAgents with local models.")
            print("Download GGUF models and place them in ~/.stableagents/models/")
            print("No API keys or payment required.")
            print("\n🎉 Setup complete! You can now use StableAgents with local models.")
        
        else:
            print("❌ Invalid choice")
            return 1
    
    elif args.command == 'status':
        # Check payment status
        status = manager.check_payment_status()
        print("📊 Payment Status")
        print("=" * 20)
        print(f"Paid: {'✅ Yes' if status.get('paid') else '❌ No'}")
        if status.get('payment_date'):
            print(f"Payment Date: {status.get('payment_date')}")
        print(f"API Keys: {', '.join(status.get('api_keys_provided', ['None']))}")
    
    elif args.command == 'reset':
        # Reset encryption
        confirm = input("⚠️  This will delete all encrypted API keys. Continue? (y/n): ").strip().lower()
        if confirm == 'y':
            manager.reset_encryption()
            print("✅ Encryption reset complete")
        else:
            print("❌ Reset cancelled")
    
    elif args.command == 'list':
        # List providers
        password = args.password or getpass.getpass("Enter your encryption password: ")
        if password:
            providers = manager.list_providers(password)
            print("📡 Available Providers")
            print("=" * 25)
            for provider in providers:
                status = "✅" if provider['has_key'] else "❌"
                active = " (active)" if provider['is_active'] else ""
                print(f"{status} {provider['name'].capitalize()}{active}")
        else:
            print("❌ Password required")
            return 1
    
    elif args.command == 'add':
        # Add specific API key
        if not args.provider:
            print("❌ Provider required. Use --provider openai|anthropic|google")
            return 1
        
        password = args.password or getpass.getpass("Enter your encryption password: ")
        if not password:
            print("❌ Password required")
            return 1
        
        print(f"🔑 Adding {args.provider.capitalize()} API Key")
        print("=" * 40)
        print(f"Get your key from: https://platform.{args.provider}.com/account/api-keys")
        
        api_key = getpass.getpass(f"Enter your {args.provider.capitalize()} API key: ")
        if api_key:
            if manager.set_api_key(args.provider, api_key, password):
                print(f"✅ {args.provider.capitalize()} API key stored securely")
            else:
                print(f"❌ Failed to store {args.provider.capitalize()} API key")
                return 1
        else:
            print("❌ No API key provided")
            return 1
    
    elif args.command == 'options':
        # Show payment options
        manager.show_payment_options()
    
    return 0

if __name__ == "__main__":
    exit(main()) 