#!/usr/bin/env python3
"""
Test script to compare our GoogleProvider implementation with the new Google GenAI client.
"""

import os
import sys
import logging

# Add the stableagents package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'stableagents'))

from stableagents.ai_providers import GoogleProvider

def test_our_implementation():
    """Test our current GoogleProvider implementation."""
    print("Testing our GoogleProvider implementation...")
    
    # Get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set")
        return False
    
    try:
        # Initialize our provider
        provider = GoogleProvider(api_key)
        
        if not provider.available:
            print("❌ GoogleProvider not available")
            return False
        
        print(f"✅ GoogleProvider initialized successfully")
        print(f"   Using new client: {provider._is_new_client()}")
        print(f"   Available models: {provider.available_models[:5]}...")  # Show first 5
        
        # Test text generation
        print("\nTesting text generation...")
        response = provider.generate_text(
            "Explain how AI works in a few words",
            model="gemini-2.5-flash"
        )
        print(f"✅ Response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing our implementation: {e}")
        return False

def test_user_example():
    """Test the user's example code."""
    print("\nTesting user's example code...")
    
    # Get API key from environment
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set")
        return False
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Explain how AI works in a few words",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disables thinking
            ),
        )
        print(f"✅ User example response: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error testing user example: {e}")
        return False

def compare_implementations():
    """Compare our implementation with the user's example."""
    print("=" * 60)
    print("COMPARING GOOGLE GENAI IMPLEMENTATIONS")
    print("=" * 60)
    
    # Test both implementations
    our_success = test_our_implementation()
    user_success = test_user_example()
    
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    
    if our_success and user_success:
        print("✅ Both implementations work correctly")
        print("\nKey differences:")
        print("1. Our implementation supports both new and legacy clients")
        print("2. Our implementation has fallback model logic")
        print("3. Our implementation includes error handling and logging")
        print("4. User's example uses the config parameter for thinking_config")
        print("5. Our implementation doesn't currently use the config parameter")
        
    elif our_success and not user_success:
        print("✅ Our implementation works, but user's example failed")
        print("   This suggests our implementation is more robust")
        
    elif not our_success and user_success:
        print("❌ Our implementation failed, but user's example works")
        print("   This suggests we need to update our implementation")
        
    else:
        print("❌ Both implementations failed")
        print("   This suggests an API key or network issue")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    compare_implementations() 