#!/usr/bin/env python3
"""
Environment-based API Key Testing Script

This script tests API keys using environment variables for maximum security.
Your API key is never stored on disk and is only kept in memory.
"""

import sys
import os
import getpass
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api_key_from_env():
    """Test API key from environment variable"""
    print("🔐 Environment-based API Key Testing")
    print("=" * 45)
    print("This method uses environment variables for maximum security.")
    print("Your API key will NOT be stored on disk.")
    print()
    
    try:
        from stableagents import StableAgents
        
        # Check if API key is already in environment
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY", 
            "google": "GOOGLE_API_KEY"
        }
        
        available_providers = []
        for provider, env_var in env_vars.items():
            if os.getenv(env_var):
                available_providers.append(provider)
                print(f"✅ Found {provider.capitalize()} API key in {env_var}")
        
        if not available_providers:
            print("❌ No API keys found in environment variables")
            print("\n💡 To set environment variables:")
            print("   export OPENAI_API_KEY='your-key-here'")
            print("   export ANTHROPIC_API_KEY='your-key-here'")
            print("   export GOOGLE_API_KEY='your-key-here'")
            
            # Offer to set them temporarily
            print("\n🔑 Would you like to set an API key temporarily? (y/n): ", end="")
            choice = input().strip().lower()
            
            if choice == 'y':
                return set_and_test_temp_key()
            else:
                return False
        
        # Test available providers
        print(f"\n🧪 Testing {len(available_providers)} provider(s)...")
        
        agent = StableAgents(enable_self_healing=True)
        
        for provider in available_providers:
            print(f"\n📡 Testing {provider.capitalize()}...")
            
            # Set the provider as active
            agent.set_active_ai_provider(provider)
            
            try:
                # Test with a simple prompt
                test_prompt = f"Hello! This is a test of the {provider.capitalize()} API. Please respond with 'Test successful' if you can see this message."
                
                print("   Sending test request...")
                response = agent.generate_text(test_prompt, max_tokens=50)
                
                if response:
                    print(f"✅ {provider.capitalize()} API key works!")
                    print(f"   Response: {response}")
                else:
                    print(f"⚠️  {provider.capitalize()} returned empty response")
                    
            except Exception as e:
                print(f"❌ {provider.capitalize()} API key failed: {e}")
                print("\n💡 Common issues:")
                print("   - Invalid API key")
                print("   - Insufficient credits/quota")
                print("   - Network connectivity issues")
        
        print(f"\n🎉 Environment-based testing completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the project directory and dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def set_and_test_temp_key():
    """Set a temporary API key and test it"""
    print("\n🔑 Temporary API Key Setup")
    print("=" * 30)
    
    # Choose provider
    print("🤖 Choose your AI provider:")
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
    env_var = f"{provider.upper()}_API_KEY"
    
    # Get API key securely
    print(f"\n🔑 Enter your {provider.capitalize()} API key:")
    print("   (It will be stored temporarily in memory only)")
    api_key = getpass.getpass("API Key: ")
    
    if not api_key or api_key.strip() == "":
        print("❌ No API key provided")
        return False
    
    # Set environment variable temporarily
    os.environ[env_var] = api_key
    print(f"✅ API key set in {env_var} (temporary)")
    
    # Test the key
    try:
        from stableagents import StableAgents
        
        agent = StableAgents(enable_self_healing=True)
        agent.set_active_ai_provider(provider)
        
        test_prompt = f"Hello! This is a test of the {provider.capitalize()} API. Please respond with 'Test successful' if you can see this message."
        
        print(f"\n🧪 Testing {provider.capitalize()} API key...")
        print("   Sending test request...")
        
        response = agent.generate_text(test_prompt, max_tokens=50)
        
        if response and "successful" in response.lower():
            print("✅ API key test successful!")
            print(f"   Response: {response}")
        else:
            print("⚠️  API key works but unexpected response:")
            print(f"   Response: {response}")
        
        # Clean up environment variable
        if env_var in os.environ:
            del os.environ[env_var]
            print(f"✅ Cleaned up {env_var} from environment")
        
        print(f"\n🎉 Temporary API key testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        
        # Clean up environment variable even on failure
        if env_var in os.environ:
            del os.environ[env_var]
        
        return False

def main():
    """Main function"""
    print("🔐 Environment-based API Key Testing")
    print("=" * 45)
    print("This tool tests API keys using environment variables.")
    print("Your keys are never stored on disk - maximum security!")
    print()
    
    return test_api_key_from_env()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 