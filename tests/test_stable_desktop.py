#!/usr/bin/env python3
"""
Test script for Stable Desktop functionality
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all stable desktop modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from stableagents.stable_desktop import DesktopBuilder, AppGenerator, UIFramework
        print("✅ All stable desktop modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_ui_framework():
    """Test UI framework functionality"""
    print("\n🧪 Testing UI framework...")
    
    try:
        from stableagents.stable_desktop import UIFramework
        
        ui_framework = UIFramework()
        
        # Test listing frameworks
        frameworks = ui_framework.list_frameworks()
        print(f"✅ Found {len(frameworks)} UI frameworks")
        
        # Test framework info
        tkinter_info = ui_framework.get_framework_info("tkinter")
        if tkinter_info:
            print(f"✅ Tkinter info retrieved: {tkinter_info['name']}")
        
        # Test availability check
        availability = ui_framework.check_framework_availability("tkinter")
        print(f"✅ Tkinter availability: {availability['available']}")
        
        return True
    except Exception as e:
        print(f"❌ UI framework test failed: {e}")
        return False

def test_desktop_builder():
    """Test desktop builder functionality"""
    print("\n🧪 Testing desktop builder...")
    
    try:
        from stableagents.stable_desktop import DesktopBuilder
        
        # Create builder without AI provider (for testing)
        desktop_builder = DesktopBuilder()
        
        # Test project listing
        projects = desktop_builder.list_projects()
        print(f"✅ Project listing works: {len(projects)} projects found")
        
        # Test project path creation
        project_path = desktop_builder.project_path
        print(f"✅ Project path: {project_path}")
        
        return True
    except Exception as e:
        print(f"❌ Desktop builder test failed: {e}")
        return False

def test_app_generator():
    """Test app generator functionality"""
    print("\n🧪 Testing app generator...")
    
    try:
        from stableagents.stable_desktop import AppGenerator
        
        # Create generator without AI provider (for testing)
        app_generator = AppGenerator()
        
        # Test requirements generation
        requirements = app_generator.generate_requirements("tkinter")
        print(f"✅ Requirements generated: {len(requirements.split())} lines")
        
        # Test setup files generation
        setup_files = app_generator.generate_setup_files("test_app")
        print(f"✅ Setup files generated: {len(setup_files)} files")
        
        return True
    except Exception as e:
        print(f"❌ App generator test failed: {e}")
        return False

def test_cli_commands():
    """Test CLI command structure"""
    print("\n🧪 Testing CLI commands...")
    
    try:
        import subprocess
        
        # Test help command
        result = subprocess.run([
            sys.executable, "-m", "stableagents.cli", "stable-desktop", "--help"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ CLI help command works")
        else:
            print(f"❌ CLI help command failed: {result.stderr}")
            return False
        
        # Test frameworks command
        result = subprocess.run([
            sys.executable, "-m", "stableagents.cli", "stable-desktop", "frameworks"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ CLI frameworks command works")
        else:
            print(f"❌ CLI frameworks command failed: {result.stderr}")
            return False
        
        # Test list command
        result = subprocess.run([
            sys.executable, "-m", "stableagents.cli", "stable-desktop", "list"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ CLI list command works")
        else:
            print(f"❌ CLI list command failed: {result.stderr}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Stable Desktop Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_ui_framework,
        test_desktop_builder,
        test_app_generator,
        test_cli_commands
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Stable Desktop is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 