#!/usr/bin/env python3
"""
Secure API Setup Demo

This example demonstrates how to use StableAgents with secure API key management.
"""

import sys
import os
import getpass

# Add parent directory to path to import stableagents
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stableagents import StableAgents
from stableagents.api_key_manager import SecureAPIKeyManager

def demo_secure_setup():
    """Demonstrate secure API key setup."""
    print("🔐 StableAgents Secure API Setup Demo")
    print("=" * 50)
    print("This demo shows how to securely manage API keys with encryption.")
    print()
    
    # Initialize the secure manager
    manager = SecureAPIKeyManager()
    
    # Check current status
    status = manager.check_payment_status()
    print("📊 Current Status:")
    print(f"   Payment: {'✅ Paid' if status.get('paid') else '❌ Not paid'}")
    print(f"   API Keys: {', '.join(status.get('api_keys_provided', ['None']))}")
    print()
    
    # Show payment options
    manager.show_payment_options()
    
    # Get user choice
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        # Process payment
        print("\n💳 Processing Payment...")
        if manager.process_payment():
            password = getpass.getpass("Enter a password to encrypt your API keys: ")
            if password:
                if manager.provide_api_keys_after_payment(password):
                    print("\n✅ Payment and setup successful!")
                    demo_usage_with_secure_keys(manager, password)
                else:
                    print("❌ Setup failed")
            else:
                print("❌ Password required")
        else:
            print("❌ Payment failed")
    
    elif choice == "2":
        # Custom API keys
        print("\n🔑 Custom API Key Setup...")
        password = getpass.getpass("Enter a password to encrypt your API keys: ")
        if password:
            if manager.setup_custom_api_keys(password):
                print("\n✅ Custom API key setup successful!")
                demo_usage_with_secure_keys(manager, password)
            else:
                print("❌ Setup failed")
        else:
            print("❌ Password required")
    
    elif choice == "3":
        # Local models only
        print("\n🏠 Local Models Setup...")
        print("Great choice! You can use StableAgents with local models.")
        print("Download GGUF models and place them in ~/.stableagents/models/")
        demo_local_usage()
    
    else:
        print("❌ Invalid choice")

def demo_usage_with_secure_keys(manager, password):
    """Demonstrate usage with secure API keys."""
    print("\n🚀 Using StableAgents with Secure API Keys")
    print("=" * 50)
    
    # Initialize StableAgents
    agent = StableAgents(enable_self_healing=True)
    
    # Get API keys securely
    providers = ["openai", "anthropic"]
    for provider in providers:
        api_key = manager.get_api_key(provider, password)
        if api_key:
            print(f"✅ {provider.capitalize()} API key retrieved securely")
            # Set the API key in the agent
            agent.set_api_key(provider, api_key)
            agent.set_active_ai_provider(provider)
            break
    
    # Test the agent
    print("\n🧪 Testing AI Generation...")
    try:
        response = agent.generate_text("Hello, StableAgents!", max_tokens=20)
        print(f"✅ AI Response: {response}")
    except Exception as e:
        print(f"❌ AI Generation failed: {e}")
        print("   This is expected with demo keys. Contact support for real keys.")
    
    # Test memory
    print("\n🧠 Testing Memory...")
    agent.add_to_memory("short_term", "demo", {"message": "Hello from secure demo"})
    memory = agent.get_from_memory("short_term", "demo")
    print(f"✅ Memory test: {memory}")
    
    # Test self-healing
    print("\n🔄 Testing Self-Healing...")
    health = agent.get_health_report()
    print(f"✅ Health status: {health.get('status', 'unknown')}")
    
    print("\n🎉 Secure API setup demo completed!")

def demo_local_usage():
    """Demonstrate local model usage."""
    print("\n🚀 Using StableAgents with Local Models")
    print("=" * 50)
    
    # Initialize StableAgents
    agent = StableAgents(enable_self_healing=True)
    
    # Check for local models
    models_dir = os.path.join(os.path.expanduser("~"), ".stableagents", "models")
    if os.path.exists(models_dir):
        gguf_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]
        if gguf_files:
            print(f"📁 Found {len(gguf_files)} local model(s):")
            for model in gguf_files:
                print(f"   - {model}")
            
            # Try to use the first model
            model_path = os.path.join(models_dir, gguf_files[0])
            if agent.set_local_model(model_path):
                print(f"✅ Local model loaded: {gguf_files[0]}")
                
                # Test local generation
                try:
                    response = agent.generate_text("Hello from local model!", max_tokens=20)
                    print(f"✅ Local AI Response: {response}")
                except Exception as e:
                    print(f"❌ Local generation failed: {e}")
            else:
                print("❌ Failed to load local model")
        else:
            print("📁 No GGUF models found")
            print("   Download models from: https://huggingface.co/TheBloke")
    else:
        print("📁 Models directory not found")
        print("   Creating: ~/.stableagents/models/")
        os.makedirs(models_dir, exist_ok=True)
        print("   Download GGUF models and place them in this directory")
    
    # Test other features
    print("\n🧠 Testing Memory...")
    agent.add_to_memory("short_term", "demo", {"message": "Hello from local demo"})
    memory = agent.get_from_memory("short_term", "demo")
    print(f"✅ Memory test: {memory}")
    
    print("\n🎉 Local model demo completed!")

def main():
    """Main function."""
    try:
        demo_secure_setup()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 