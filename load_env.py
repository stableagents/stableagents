#!/usr/bin/env python3
"""
Utility to load environment variables from .env.local
"""

import os
import sys

def load_env_file(filepath=".env.local"):
    """Load environment variables from a .env file"""
    if not os.path.exists(filepath):
        print(f"❌ {filepath} not found")
        return False
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value
                    print(f"✅ Loaded: {key}")
        return True
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return False

def main():
    """Load .env.local and test Gemini API"""
    print("🔧 Loading environment variables...")
    
    if load_env_file():
        print("\n🚀 Testing Gemini API...")
        
        # Check if API key is loaded
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env.local")
            print("Make sure your .env.local contains: GEMINI_API_KEY=your_key_here")
            return False
        
        print(f"✅ API key loaded (length: {len(api_key)} characters)")
        
        # Test the API
        try:
            from google import genai
            client = genai.Client()
            
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents="Say 'Environment loading successful!'"
            )
            print(f"✅ API test successful: {response.text}")
            return True
            
        except Exception as e:
            print(f"❌ API test failed: {e}")
            return False
    else:
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 