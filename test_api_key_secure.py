#!/usr/bin/env python3
"""
Secure API Key Testing Script

This script allows you to test API keys securely without exposing them publicly.
It uses the existing SecureAPIKeyManager for encrypted storage and testing.
"""

import sys
import os
import getpass
import json
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_key_secure():
    """Test an API key securely using the existing SecureAPIKeyManager"""
    print("🔐 Secure API Key Testing")
    print("=" * 40)
    print("This script will help you test your API key securely.")
    print("Your key will be encrypted and stored locally.")
    print()
    
    try:
        from stableagents.api_key_manager import SecureAPIKeyManager
        from stableagents import StableAgents
        
        # Initialize the secure manager
        manager = SecureAPIKeyManager()
        print("✅ Secure API Key Manager initialized")
        
        # Get the API key securely
        print("\n🔑 Enter your API key:")
        print("   (It will be encrypted and stored securely)")
        api_key = getpass.getpass("API Key: ")
        
        if not api_key or api_key.strip() == "":
            print("❌ No API key provided")
            return False
        
        # Get encryption password
        print("\n🔐 Set up encryption password:")
        print("   (This will be used to encrypt/decrypt your API key)")
        password = getpass.getpass("Encryption Password: ")
        
        if not password or password.strip() == "":
            print("❌ No password provided")
            return False
        
        # Confirm password
        confirm_password = getpass.getpass("Confirm Password: ")
        if password != confirm_password:
            print("❌ Passwords don't match")
            return False
        
        # Choose provider
        print("\n🤖 Choose your AI provider:")
        print("1. OpenAI (GPT-4, GPT-3.5)")
        print("2. Anthropic (Claude)")
        print("3. Google (Gemini)")
        
        provider_choice = input("Enter choice (1-3): ").strip()
        
        provider_map = {
            "1": "openai",
            "2": "anthropic", 
            "3": "google"
        }
        
        if provider_choice not in provider_map:
            print("❌ Invalid choice")
            return False
        
        provider = provider_map[provider_choice]
        
        # Store the API key securely
        print(f"\n💾 Storing {provider.capitalize()} API key securely...")
        if manager.set_api_key(provider, api_key, password):
            print("✅ API key stored securely")
        else:
            print("❌ Failed to store API key")
            return False
        
        # Test the API key
        print(f"\n🧪 Testing {provider.capitalize()} API key...")
        
        # Initialize StableAgents
        agent = StableAgents(enable_self_healing=True)
        
        # Set the API key
        agent.set_api_key(provider, api_key)
        agent.set_active_ai_provider(provider)
        
        # Test with a simple prompt
        test_prompt = "Hello! Please respond with 'API key test successful' if you can see this message."
        
        try:
            print("   Sending test request...")
            response = agent.generate_text(test_prompt, max_tokens=50)
            
            if response and "successful" in response.lower():
                print("✅ API key test successful!")
                print(f"   Response: {response}")
            else:
                print("⚠️  API key works but unexpected response:")
                print(f"   Response: {response}")
                
        except Exception as e:
            print(f"❌ API key test failed: {e}")
            print("\n💡 Common issues:")
            print("   - Invalid API key")
            print("   - Insufficient credits/quota")
            print("   - Network connectivity issues")
            print("   - Provider service down")
            return False
        
        # Show how to retrieve the key later
        print(f"\n📋 To retrieve your {provider.capitalize()} API key later:")
        print(f"   from stableagents.api_key_manager import SecureAPIKeyManager")
        print(f"   manager = SecureAPIKeyManager()")
        print(f"   key = manager.get_api_key('{provider}', 'your_password')")
        
        # Show current status
        print(f"\n📊 Current Status:")
        status = manager.check_payment_status()
        providers_with_keys = status.get('api_keys_provided', [])
        print(f"   Providers with keys: {', '.join(providers_with_keys) if providers_with_keys else 'None'}")
        
        print(f"\n🎉 API key testing completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the project directory and dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_existing_key():
    """Test an existing stored API key"""
    print("🔐 Test Existing API Key")
    print("=" * 30)
    
    try:
        from stableagents.api_key_manager import SecureAPIKeyManager
        from stableagents import StableAgents
        
        manager = SecureAPIKeyManager()
        
        # Check what providers have keys
        status = manager.check_payment_status()
        providers_with_keys = status.get('api_keys_provided', [])
        
        if not providers_with_keys:
            print("❌ No stored API keys found")
            print("   Run the main test function first to store a key")
            return False
        
        print(f"📋 Available providers: {', '.join(providers_with_keys)}")
        
        # Get password
        password = getpass.getpass("Enter your encryption password: ")
        
        # Test each provider
        for provider in providers_with_keys:
            if provider == "active_provider":
                continue
                
            print(f"\n🧪 Testing {provider.capitalize()}...")
            
            api_key = manager.get_api_key(provider, password)
            if not api_key:
                print(f"❌ Could not retrieve {provider} key")
                continue
            
            # Test the key
            agent = StableAgents(enable_self_healing=True)
            agent.set_api_key(provider, api_key)
            agent.set_active_ai_provider(provider)
            
            try:
                response = agent.generate_text("Test message", max_tokens=20)
                print(f"✅ {provider.capitalize()} API key works!")
                print(f"   Response: {response}")
            except Exception as e:
                print(f"❌ {provider.capitalize()} API key failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🔐 Secure API Key Testing Tool")
    print("=" * 40)
    print("1. Test a new API key")
    print("2. Test existing stored API keys")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        return test_api_key_secure()
    elif choice == "2":
        return test_existing_key()
    elif choice == "3":
        print("👋 Goodbye!")
        return True
    else:
        print("❌ Invalid choice")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 