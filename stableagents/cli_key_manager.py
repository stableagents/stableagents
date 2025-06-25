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

  # Switch to a different provider
  stableagents-keys switch --provider anthropic

  # Show payment options
  stableagents-keys options

  # Create Stripe payment link
  stableagents-keys payment-link
        """
    )
    
    parser.add_argument('command', choices=[
        'setup', 'status', 'reset', 'list', 'add', 'options', 'switch', 'payment-link'
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
    
    elif args.command == 'switch':
        # Switch active provider
        if not args.provider:
            print("❌ Provider required. Use --provider openai|anthropic|google")
            return 1
        
        password = args.password or getpass.getpass("Enter your encryption password: ")
        if not password:
            print("❌ Password required")
            return 1
        
        print(f"🔄 Switching to {args.provider.capitalize()}")
        print("=" * 40)
        
        if manager.switch_active_provider(args.provider, password):
            print(f"✅ Switched to {args.provider.capitalize()}")
        else:
            print(f"❌ Failed to switch to {args.provider.capitalize()}")
            return 1
    
    elif args.command == 'payment-link':
        # Create Stripe payment link
        print("💳 Creating Stripe Payment Link")
        print("=" * 35)
        
        try:
            from stableagents.stripe_payment import StripePaymentManager
            import webbrowser
            
            stripe_manager = StripePaymentManager()
            
            if not stripe_manager.stripe_secret_key:
                print("❌ STRIPE_SECRET_KEY is not set")
                print("Please set your Stripe secret key:")
                print("export STRIPE_SECRET_KEY='sk_test_...'")
                return 1
            
            print("🔗 Creating payment link for monthly subscription...")
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
                        password = getpass.getpass("Enter a password to encrypt your API keys: ")
                        if password:
                            # Provide API keys
                            if manager.provide_api_keys_after_payment(password):
                                print("✅ API keys have been securely stored and encrypted!")
                                print("🔒 Your keys are protected with your password")
                                print("💡 You can now use AI features in stableagents-ai")
                                print("📅 Your subscription will renew monthly")
                                print("💳 Manage your subscription: Check your email for account details")
                            else:
                                print("❌ Failed to provide API keys")
                                return 1
                        else:
                            print("❌ Password required for encryption")
                            return 1
                    else:
                        print("❌ Payment verification failed")
                        print("💡 You can still complete the payment manually and try again")
                        return 1
                else:
                    print("💡 Payment link created but not completed")
                    print("You can complete the payment later by visiting the URL above")
            else:
                print("❌ Failed to create payment link")
                print("Please check your Stripe configuration")
                return 1
                
        except ImportError:
            print("❌ Stripe integration not available")
            print("Please install the stripe package: pip install stripe")
            return 1
        except Exception as e:
            print(f"❌ Error creating payment link: {e}")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 