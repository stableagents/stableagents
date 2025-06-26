#!/usr/bin/env python3
"""
Script to set up a new Gemini API key
"""

import os
import getpass
import subprocess
from pathlib import Path

def setup_new_api_key():
    """Set up a new Gemini API key."""
    print("🔑 Setting up New Gemini API Key")
    print("=" * 40)
    print()
    print("📋 Instructions:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key' or 'Create another key'")
    print("4. Copy the new API key")
    print()
    
    # Get the new API key
    try:
        new_api_key = getpass.getpass("Enter your new Gemini API key: ")
        if not new_api_key.strip():
            print("❌ No API key provided")
            return False
        
        new_api_key = new_api_key.strip()
        
        # Test the new API key
        print("\n🧪 Testing new API key...")
        try:
            from stableagents.ai_providers import GoogleProvider
            provider = GoogleProvider(new_api_key)
            response = provider.generate_text("Hello")
            print("✅ New API key works!")
        except Exception as e:
            print(f"❌ New API key test failed: {e}")
            return False
        
        # Update the .zshrc file
        print("\n📝 Updating .zshrc file...")
        zshrc_path = Path.home() / ".zshrc"
        
        # Read current content
        with open(zshrc_path, 'r') as f:
            content = f.read()
        
        # Remove old API key lines
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if not line.strip().startswith('export GEMINI_API_KEY'):
                new_lines.append(line)
        
        # Add new API key
        new_lines.append(f'export GEMINI_API_KEY="{new_api_key}"')
        
        # Write back to file
        with open(zshrc_path, 'w') as f:
            f.write('\n'.join(new_lines))
        
        print("✅ .zshrc file updated successfully!")
        
        # Set environment variable for current session
        os.environ['GEMINI_API_KEY'] = new_api_key
        print("✅ Environment variable set for current session")
        
        print("\n🔄 To apply changes to new terminal sessions, run:")
        print("   source ~/.zshrc")
        
        return True
        
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled.")
        return False
    except Exception as e:
        print(f"❌ Error setting up API key: {e}")
        return False

if __name__ == "__main__":
    setup_new_api_key() 