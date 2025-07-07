#!/usr/bin/env python3
"""
Test script for the new API + JavaScript architecture.
Tests the API endpoints and verifies the integration works correctly.
"""

import requests
import json
import time
import sys
from pathlib import Path

# API base URL
API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test the API health endpoint."""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is healthy: {data['status']}")
            print(f"📊 Version: {data['version']}")
            print(f"🤖 Active provider: {data.get('active_provider', 'None')}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print("💡 Make sure the API server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error testing API health: {e}")
        return False

def test_desktop_frameworks():
    """Test the desktop frameworks endpoint."""
    print("\n🎨 Testing desktop frameworks...")
    try:
        response = requests.get(f"{API_BASE_URL}/desktop/frameworks")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                frameworks = data['frameworks']
                print(f"✅ Found {len(frameworks)} frameworks:")
                for fw in frameworks:
                    print(f"   • {fw['name']}: {fw['description']}")
                return True
            else:
                print(f"❌ Failed to get frameworks: {data.get('detail', 'Unknown error')}")
                return False
        else:
            print(f"❌ Frameworks request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing frameworks: {e}")
        return False

def test_projects_list():
    """Test the projects list endpoint."""
    print("\n📁 Testing projects list...")
    try:
        response = requests.get(f"{API_BASE_URL}/desktop/projects")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                projects = data['projects']
                print(f"✅ Found {len(projects)} projects")
                for project in projects[:3]:  # Show first 3 projects
                    name = project.get('metadata', {}).get('name', project['path'].split('/')[-1])
                    framework = project.get('metadata', {}).get('framework', 'Unknown')
                    print(f"   • {name} ({framework})")
                return True
            else:
                print(f"❌ Failed to get projects: {data.get('detail', 'Unknown error')}")
                return False
        else:
            print(f"❌ Projects request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing projects: {e}")
        return False

def test_code_generation():
    """Test the code generation endpoint."""
    print("\n💻 Testing code generation...")
    try:
        test_data = {
            "prompt": "Create a simple button with CustomTkinter",
            "framework": "customtkinter"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/desktop/generate-code",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                code = data['code']
                print(f"✅ Code generation successful!")
                print(f"📝 Generated {len(code)} characters of code")
                print(f"🎨 Framework: {data['framework']}")
                return True
            else:
                print(f"❌ Code generation failed: {data.get('detail', 'Unknown error')}")
                return False
        else:
            print(f"❌ Code generation request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing code generation: {e}")
        return False

def test_app_creation():
    """Test the desktop app creation endpoint."""
    print("\n🚀 Testing app creation...")
    try:
        test_data = {
            "description": "Create a simple calculator with basic arithmetic operations",
            "app_name": "TestCalculator",
            "ui_framework": "customtkinter"
        }
        
        print("⏳ Creating test app (this may take a moment)...")
        response = requests.post(
            f"{API_BASE_URL}/desktop/create",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                app = data['app']
                print(f"✅ App creation successful!")
                print(f"📱 App name: {app['name']}")
                print(f"🎨 Framework: {app['framework']}")
                print(f"📁 Location: {app['project_path']}")
                return True
            else:
                print(f"❌ App creation failed: {data.get('detail', 'Unknown error')}")
                return False
        else:
            print(f"❌ App creation request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing app creation: {e}")
        return False

def test_providers():
    """Test the providers endpoint."""
    print("\n🔑 Testing providers...")
    try:
        response = requests.get(f"{API_BASE_URL}/providers")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                providers = data['providers']
                print(f"✅ Found {len(providers)} providers:")
                for provider in providers:
                    print(f"   • {provider}")
                return True
            else:
                print(f"❌ Failed to get providers: {data.get('detail', 'Unknown error')}")
                return False
        else:
            print(f"❌ Providers request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing providers: {e}")
        return False

def test_text_generation():
    """Test the text generation endpoint."""
    print("\n📝 Testing text generation...")
    try:
        test_data = {
            "prompt": "Write a short poem about artificial intelligence",
            "max_tokens": 50,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{API_BASE_URL}/generate",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                text = data['text']
                print(f"✅ Text generation successful!")
                print(f"📝 Generated text: {text[:100]}...")
                return True
            else:
                print(f"❌ Text generation failed: {data.get('detail', 'Unknown error')}")
                return False
        else:
            print(f"❌ Text generation request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing text generation: {e}")
        return False

def main():
    """Run all API tests."""
    print("🧪 StableAgents API Integration Test")
    print("=" * 50)
    
    tests = [
        ("API Health", test_api_health),
        ("Desktop Frameworks", test_desktop_frameworks),
        ("Projects List", test_projects_list),
        ("Code Generation", test_code_generation),
        ("App Creation", test_app_creation),
        ("Providers", test_providers),
        ("Text Generation", test_text_generation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API integration is working correctly.")
        print("🚀 You can now use the frontend at http://localhost:3000")
    else:
        print("⚠️  Some tests failed. Please check the API server and try again.")
        print("💡 Make sure the API server is running: python -m stableagents.api_server")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 