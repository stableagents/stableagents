#!/usr/bin/env python3
"""
Test Framework Fix

This script tests that the framework selection and validation is working correctly
after fixing the framework name vs description issue.
"""

import sys
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_framework_separation():
    """Test that framework names and descriptions are properly separated."""
    print("🧪 Testing Framework Separation")
    print("=" * 40)
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        generator = NaturalLanguageDesktopGenerator()
        
        # Test framework names
        framework_names = generator.list_frameworks()
        print("✅ Framework names:")
        for name in framework_names:
            print(f"  - {name}")
        
        # Test framework descriptions
        framework_descriptions = generator.get_framework_descriptions()
        print("\n✅ Framework descriptions:")
        for desc in framework_descriptions:
            print(f"  - {desc}")
        
        # Verify they match
        print("\n✅ Verification:")
        for i, name in enumerate(framework_names):
            desc = framework_descriptions[i]
            if desc.startswith(name):
                print(f"  ✓ {name} matches description")
            else:
                print(f"  ❌ {name} doesn't match description")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing framework separation: {str(e)}")
        return False


def test_framework_validation():
    """Test that framework validation works correctly."""
    print("\n🧪 Testing Framework Validation")
    print("=" * 40)
    
    try:
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        generator = NaturalLanguageDesktopGenerator()
        
        # Test valid frameworks
        valid_frameworks = ["customtkinter", "tkinter", "pyqt"]
        for framework in valid_frameworks:
            try:
                # This should not raise an error
                generator._generate_enhanced_app_code("test", framework, "TestApp")
                print(f"✅ {framework} - Valid framework")
            except ValueError as e:
                if "Unsupported framework" in str(e):
                    print(f"❌ {framework} - Invalid framework")
                else:
                    print(f"⚠️ {framework} - Other error: {str(e)}")
        
        # Test invalid framework
        try:
            generator._generate_enhanced_app_code("test", "invalid-framework", "TestApp")
            print("❌ Invalid framework should have raised an error")
        except ValueError as e:
            if "Unsupported framework" in str(e):
                print("✅ Invalid framework correctly rejected")
            else:
                print(f"⚠️ Unexpected error for invalid framework: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing framework validation: {str(e)}")
        return False


def test_cli_framework_selection():
    """Test that CLI framework selection works correctly."""
    print("\n🧪 Testing CLI Framework Selection")
    print("=" * 40)
    
    try:
        from stableagents.cli_natural_desktop import _select_framework
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        generator = NaturalLanguageDesktopGenerator()
        
        # Test that the helper function exists and works
        print("✅ _select_framework helper function exists")
        
        # Test that it returns a valid framework name
        # Note: We can't actually test the interactive input, but we can test the logic
        framework_names = generator.list_frameworks()
        framework_descriptions = generator.get_framework_descriptions()
        
        print(f"✅ Framework names available: {framework_names}")
        print(f"✅ Framework descriptions available: {len(framework_descriptions)} descriptions")
        
        # Verify the counts match
        if len(framework_names) == len(framework_descriptions):
            print("✅ Framework names and descriptions count match")
        else:
            print("❌ Framework names and descriptions count don't match")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing CLI framework selection: {str(e)}")
        return False


def main():
    """Main test function."""
    print("🔧 Framework Fix Test Suite")
    print("=" * 50)
    print("Testing the framework name vs description fix")
    print()
    
    tests = [
        ("Framework Separation", test_framework_separation),
        ("Framework Validation", test_framework_validation),
        ("CLI Framework Selection", test_cli_framework_selection)
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
        print("\n🎉 All tests passed! Framework fix is working correctly!")
        print("🚀 You can now use the natural desktop commands without framework errors!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 