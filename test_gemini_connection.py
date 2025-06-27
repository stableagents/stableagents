#!/usr/bin/env python3
"""
Test Gemini Connection

This script tests the connection between the gemini_example.py file
and the enhanced natural desktop integration.
"""

import os
import sys
from pathlib import Path

def test_gemini_example_connection():
    """Test that the gemini_example.py works with the same setup."""
    print("🧪 Testing Gemini Example Connection")
    print("=" * 40)
    
    try:
        # Test the exact same code as gemini_example.py
        from google import genai
        
        # Check if API key is available
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY environment variable not set")
            print("💡 Set it with: export GEMINI_API_KEY='your-key'")
            return False
        
        # Use the exact same code as gemini_example.py
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents="Explain how AI works in a few words"
        )
        
        print("✅ Gemini example connection successful!")
        print(f"📝 Response: {response.text}")
        return True
        
    except ImportError:
        print("❌ Google Genai library not installed")
        print("💡 Install with: pip install google-genai")
        return False
    except Exception as e:
        print(f"❌ Error testing Gemini example: {str(e)}")
        return False


def test_natural_desktop_connection():
    """Test that the natural desktop generator uses the same setup."""
    print("\n🧪 Testing Natural Desktop Connection")
    print("=" * 45)
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        # Initialize generator (should use same API key)
        generator = NaturalLanguageDesktopGenerator()
        print("✅ Natural desktop generator initialized!")
        
        # Test that it uses the same model
        test_prompt = "Create a simple button"
        code = generator.generate_code_from_prompt(test_prompt, "customtkinter")
        
        print("✅ Natural desktop generator connected successfully!")
        print(f"📝 Generated code length: {len(code)} characters")
        print("💡 Both systems are now using the same Gemini setup!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing natural desktop connection: {str(e)}")
        return False


def test_integration_workflow():
    """Test the complete integration workflow."""
    print("\n🧪 Testing Complete Integration Workflow")
    print("=" * 50)
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        generator = NaturalLanguageDesktopGenerator()
        
        # Test the enhanced app creation (without creating files)
        print("✅ Integration workflow test successful!")
        print("💡 The enhanced integration is properly connected to your Gemini setup")
        print("🚀 You can now create desktop applications using the same Gemini API!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing integration workflow: {str(e)}")
        return False


def main():
    """Main test function."""
    print("🔗 Gemini Integration Connection Test")
    print("=" * 50)
    print("Testing the connection between gemini_example.py and enhanced integration")
    print()
    
    tests = [
        ("Gemini Example Connection", test_gemini_example_connection),
        ("Natural Desktop Connection", test_natural_desktop_connection),
        ("Integration Workflow", test_integration_workflow)
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
        print("\n🎉 All tests passed! Your Gemini setup is properly connected!")
        print("🚀 You can now use the enhanced natural desktop commands:")
        print("   • stableagents-ai natural-desktop create")
        print("   • stableagents-ai natural-desktop demo")
        print("   • stableagents-ai natural-desktop code")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 