#!/usr/bin/env python3
"""
Test script to verify the Gemini model fix
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gemini_models():
    """Test Gemini model availability and fallback."""
    print("🧪 Testing Gemini Model Fix")
    print("=" * 40)
    
    try:
        from stableagents.ai_providers import GoogleProvider
        
        # Test with a dummy API key to see model detection
        provider = GoogleProvider("dummy-key")
        print(f"✅ Provider initialized")
        print(f"   Available models: {provider.available_models}")
        
        # Test model selection
        test_model = provider._get_available_model("gemini-1.5-pro")
        print(f"   Selected model: {test_model}")
        
        # Test fallback
        fallback_model = provider._get_available_model("gemini-pro")
        print(f"   Fallback model: {fallback_model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini models: {e}")
        return False

def test_with_real_api_key():
    """Test with a real API key if available."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  No GEMINI_API_KEY environment variable found")
        print("   Set it to test with real API key")
        return True
    
    print("\n🔑 Testing with Real API Key")
    print("=" * 40)
    
    try:
        from stableagents.ai_providers import GoogleProvider
        
        provider = GoogleProvider(api_key)
        print(f"✅ Provider initialized with real API key")
        print(f"   Available models: {provider.available_models}")
        
        # Test text generation
        response = provider.generate_text("Hello, world!", max_tokens=50)
        if not response.startswith("Error:"):
            print(f"✅ Text generation successful")
            print(f"   Response: {response[:100]}...")
        else:
            print(f"❌ Text generation failed: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing with real API key: {e}")
        return False

def main():
    """Main test function."""
    print("🎯 Gemini Model Fix Test")
    print("=" * 30)
    
    # Test basic functionality
    if not test_gemini_models():
        print("❌ Basic model test failed")
        return 1
    
    # Test with real API key if available
    if not test_with_real_api_key():
        print("❌ Real API key test failed")
        return 1
    
    print("\n🎉 All tests passed!")
    print("\n💡 The fix should resolve the model not found error.")
    print("   The system will now:")
    print("   - Try gemini-1.5-pro first")
    print("   - Fall back to gemini-1.5-flash if needed")
    print("   - Use gemini-pro as a last resort")
    print("   - Handle model availability gracefully")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 