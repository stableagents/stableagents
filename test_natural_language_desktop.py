#!/usr/bin/env python3
"""
Test script for Natural Language Desktop Generator

This script tests the basic functionality of the natural language desktop generator
without requiring a Gemini API key.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        print("✅ NaturalLanguageDesktopGenerator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import NaturalLanguageDesktopGenerator: {e}")
        return False
    
    try:
        from stableagents.ai_providers import GoogleProvider
        print("✅ GoogleProvider imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import GoogleProvider: {e}")
        return False
    
    try:
        from stableagents.stable_desktop.desktop_builder import DesktopBuilder
        print("✅ DesktopBuilder imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import DesktopBuilder: {e}")
        return False
    
    return True


def test_generator_initialization():
    """Test generator initialization without API key."""
    print("\n🔍 Testing generator initialization...")
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        # Test initialization without API key
        generator = NaturalLanguageDesktopGenerator()
        print("✅ Generator initialized without API key")
        
        # Test framework listing
        frameworks = generator.list_supported_frameworks()
        if frameworks and len(frameworks) > 0:
            print(f"✅ Found {len(frameworks)} supported frameworks")
            for framework in frameworks:
                print(f"   - {framework['display_name']}")
        else:
            print("❌ No frameworks found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing generator: {e}")
        return False


def test_google_provider_stub():
    """Test Google provider stub functionality."""
    print("\n🔍 Testing Google provider stub...")
    
    try:
        from stableagents.ai_providers import GoogleProvider
        
        # Test initialization without API key
        provider = GoogleProvider("dummy-key")
        print("✅ Google provider initialized")
        
        # Test availability (should be False without proper API key)
        print(f"   Provider available: {provider.available}")
        
        # Test text generation (should return error message)
        response = provider.generate_text("Hello world")
        print(f"   Text generation response: {response[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Google provider: {e}")
        return False


def test_cli_imports():
    """Test CLI module imports."""
    print("\n🔍 Testing CLI imports...")
    
    try:
        from stableagents.cli_natural_desktop import (
            get_gemini_api_key,
            create_app_interactive,
            create_demo_app,
            list_frameworks,
            show_setup_instructions,
            generate_code_interactive
        )
        print("✅ CLI functions imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import CLI functions: {e}")
        return False


def test_dependencies():
    """Test that required dependencies are available."""
    print("\n🔍 Testing dependencies...")
    
    dependencies = [
        ("google.generativeai", "google-generativeai"),
        ("customtkinter", "customtkinter"),
        ("tkinter", "tkinter (built-in)"),
        ("pathlib", "pathlib (built-in)"),
        ("json", "json (built-in)"),
        ("logging", "logging (built-in)")
    ]
    
    all_available = True
    
    for module, package in dependencies:
        try:
            __import__(module)
            print(f"✅ {module} ({package})")
        except ImportError:
            print(f"❌ {module} ({package}) - not available")
            all_available = False
    
    return all_available


def test_setup_instructions():
    """Test setup instructions generation."""
    print("\n🔍 Testing setup instructions...")
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        generator = NaturalLanguageDesktopGenerator()
        instructions = generator.get_setup_instructions()
        
        if instructions and len(instructions) > 100:
            print("✅ Setup instructions generated successfully")
            print(f"   Length: {len(instructions)} characters")
            return True
        else:
            print("❌ Setup instructions too short or empty")
            return False
            
    except Exception as e:
        print(f"❌ Error testing setup instructions: {e}")
        return False


def main():
    """Main test function."""
    print("🧪 Natural Language Desktop Generator Tests")
    print("=" * 50)
    print("Testing basic functionality without API key...")
    print()
    
    tests = [
        ("Import Tests", test_imports),
        ("Generator Initialization", test_generator_initialization),
        ("Google Provider Stub", test_google_provider_stub),
        ("CLI Imports", test_cli_imports),
        ("Dependencies", test_dependencies),
        ("Setup Instructions", test_setup_instructions)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print(f"\n📊 Test Results")
    print("=" * 30)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        print("\n💡 Next steps:")
        print("   1. Get a Google Gemini API key from https://makersuite.google.com/app/apikey")
        print("   2. Run: stableagents-ai natural-desktop create")
        print("   3. Or try the demo: python examples/natural_language_desktop_demo.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 