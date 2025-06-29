#!/usr/bin/env python3
"""
Test script to verify Gemini API key setup
"""

import os
import sys

def test_env_file():
    """Test if .env.local file exists and has the API key"""
    print("🔍 Checking .env.local file...")
    
    if os.path.exists(".env.local"):
        print("✅ .env.local file found")
        try:
            with open(".env.local", "r") as f:
                content = f.read()
                if "GEMINI_API_KEY" in content:
                    print("✅ GEMINI_API_KEY found in .env.local")
                    # Extract the key (simple parsing)
                    for line in content.split('\n'):
                        if line.startswith('GEMINI_API_KEY='):
                            key = line.split('=', 1)[1].strip().strip('"').strip("'")
                            if key:
                                print(f"✅ API key found (length: {len(key)} characters)")
                                return key
                            else:
                                print("❌ API key appears to be empty")
                                return None
                else:
                    print("❌ GEMINI_API_KEY not found in .env.local")
                    return None
        except Exception as e:
            print(f"❌ Error reading .env.local: {e}")
            return None
    else:
        print("❌ .env.local file not found")
        return None

def test_environment_variable():
    """Test if GEMINI_API_KEY is set in environment"""
    print("\n🔍 Checking environment variable...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print(f"✅ GEMINI_API_KEY found in environment (length: {len(api_key)} characters)")
        return api_key
    else:
        print("❌ GEMINI_API_KEY not found in environment")
        return None

def test_google_genai_import():
    """Test if google.genai can be imported"""
    print("\n🔍 Testing Google GenAI import...")
    
    try:
        from google import genai
        print("✅ google.genai imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import google.genai: {e}")
        return False

def test_legacy_import():
    """Test if legacy google.generativeai can be imported"""
    print("\n🔍 Testing legacy Google GenerativeAI import...")
    
    try:
        import google.generativeai as genai
        print("✅ google.generativeai imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import google.generativeai: {e}")
        return False

def test_new_client(api_key):
    """Test the new Google GenAI client"""
    print("\n🔍 Testing new Google GenAI client...")
    
    try:
        from google import genai
        
        # Set the environment variable
        os.environ["GEMINI_API_KEY"] = api_key
        
        # Create client
        client = genai.Client()
        print("✅ Client created successfully")
        
        # Test a simple request
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents="Say 'Hello, this is a test!'"
        )
        print("✅ API request successful")
        print(f"Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ New client test failed: {e}")
        return False

def test_legacy_client(api_key):
    """Test the legacy Google GenerativeAI client"""
    print("\n🔍 Testing legacy Google GenerativeAI client...")
    
    try:
        import google.generativeai as genai
        
        # Configure with API key
        genai.configure(api_key=api_key)
        print("✅ Legacy client configured successfully")
        
        # Test a simple request
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say 'Hello, this is a test!'")
        print("✅ Legacy API request successful")
        print(f"Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Legacy client test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Gemini API Key Test Suite")
    print("=" * 40)
    
    # Test environment file
    env_key = test_env_file()
    
    # Test environment variable
    env_var_key = test_environment_variable()
    
    # Use the first available key
    api_key = env_key or env_var_key
    
    if not api_key:
        print("\n❌ No API key found!")
        print("\nTo fix this:")
        print("1. Create a .env.local file in your project root")
        print("2. Add: GEMINI_API_KEY=your_actual_api_key_here")
        print("3. Or set the environment variable: export GEMINI_API_KEY=your_key")
        return False
    
    # Test imports
    new_import_ok = test_google_genai_import()
    legacy_import_ok = test_legacy_import()
    
    if not new_import_ok and not legacy_import_ok:
        print("\n❌ No Google AI libraries found!")
        print("Install with: pip install google-genai google-generativeai")
        return False
    
    # Test clients
    new_client_ok = False
    legacy_client_ok = False
    
    if new_import_ok:
        new_client_ok = test_new_client(api_key)
    
    if legacy_import_ok:
        legacy_client_ok = test_legacy_client(api_key)
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Summary:")
    print(f"API Key: {'✅ Found' if api_key else '❌ Missing'}")
    print(f"New Client: {'✅ Working' if new_client_ok else '❌ Failed'}")
    print(f"Legacy Client: {'✅ Working' if legacy_client_ok else '❌ Failed'}")
    
    if new_client_ok or legacy_client_ok:
        print("\n🎉 Gemini API is working!")
        return True
    else:
        print("\n❌ Gemini API is not working")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 