#!/usr/bin/env python3
"""
Test Generation Config Fix

This script tests that the generation_config parameter fix is working correctly
for the new Google Genai client.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_gemini_client_initialization():
    """Test that the Gemini client initializes correctly."""
    print("🧪 Testing Gemini Client Initialization")
    print("=" * 45)
    
    try:
        from stableagents.ai_providers import GoogleProvider
        
        # Check if API key is available
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY environment variable not set")
            print("💡 Set it with: export GEMINI_API_KEY='your-key'")
            return False
        
        # Initialize provider
        provider = GoogleProvider(api_key)
        
        if provider.available:
            print("✅ Gemini client initialized successfully")
            print(f"✅ Using new client: {provider._is_new_client()}")
            return True
        else:
            print("❌ Gemini client not available")
            return False
        
    except Exception as e:
        print(f"❌ Error initializing Gemini client: {str(e)}")
        return False


def test_generation_config_fix():
    """Test that the generation_config parameter fix works."""
    print("\n🧪 Testing Generation Config Fix")
    print("=" * 35)
    
    try:
        from stableagents.ai_providers import GoogleProvider
        
        # Check if API key is available
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY environment variable not set")
            print("💡 Set it with: export GEMINI_API_KEY='your-key'")
            return False
        
        # Initialize provider
        provider = GoogleProvider(api_key)
        
        if not provider.available:
            print("❌ Gemini client not available")
            return False
        
        # Test simple text generation (should not have generation_config error)
        test_prompt = "Say hello in one word"
        response = provider.generate_text(test_prompt)
        
        if response and not response.startswith("Error:"):
            print("✅ Text generation works without generation_config error")
            print(f"📝 Response: {response}")
            return True
        elif response and "generation_config" in response:
            print("❌ Still getting generation_config error")
            return False
        else:
            print(f"⚠️ Other error: {response}")
            return False
        
    except Exception as e:
        if "generation_config" in str(e):
            print("❌ Still getting generation_config error")
            return False
        else:
            print(f"⚠️ Other error: {str(e)}")
            return False


def test_natural_desktop_generation():
    """Test that natural desktop generation works without generation_config error."""
    print("\n🧪 Testing Natural Desktop Generation")
    print("=" * 40)
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        # Check if API key is available
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY environment variable not set")
            print("💡 Set it with: export GEMINI_API_KEY='your-key'")
            return False
        
        # Initialize generator
        generator = NaturalLanguageDesktopGenerator()
        
        # Test code generation (should not have generation_config error)
        test_prompt = "Create a simple button"
        code = generator.generate_code_from_prompt(test_prompt, "customtkinter")
        
        if code and not code.startswith("Error:"):
            print("✅ Code generation works without generation_config error")
            print(f"📝 Code length: {len(code)} characters")
            return True
        elif code and "generation_config" in code:
            print("❌ Still getting generation_config error in code generation")
            return False
        else:
            print(f"⚠️ Other error: {code[:100]}...")
            return False
        
    except Exception as e:
        if "generation_config" in str(e):
            print("❌ Still getting generation_config error")
            return False
        else:
            print(f"⚠️ Other error: {str(e)}")
            return False


def main():
    """Main test function."""
    print("🔧 Generation Config Fix Test Suite")
    print("=" * 50)
    print("Testing the generation_config parameter fix for the new Google Genai client")
    print()
    
    tests = [
        ("Gemini Client Initialization", test_gemini_client_initialization),
        ("Generation Config Fix", test_generation_config_fix),
        ("Natural Desktop Generation", test_natural_desktop_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {str(e)}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Generation config fix is working correctly!")
        print("🚀 You can now generate desktop applications without generation_config errors!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        print("💡 Note: API key issues are expected if GEMINI_API_KEY is not set or expired")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 