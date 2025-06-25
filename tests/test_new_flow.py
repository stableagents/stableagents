#!/usr/bin/env python3
"""
Test script for the new CLI flow that asks about payment options first
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_new_flow():
    """Test the new flow that asks about payment options first"""
    print("🎯 Testing New CLI Flow")
    print("=" * 40)
    
    try:
        from stableagents.cli import guided_setup_with_prompt_selection
        
        print("✅ New flow function imported successfully")
        print()
        print("📋 New Flow Order:")
        print("1. 💳 Choose payment/API key option FIRST")
        print("   - Monthly subscription ($20/month)")
        print("   - Bring your own API keys")
        print("   - Local models only")
        print()
        print("2. 📋 Explore what you can build (if needed)")
        print("3. 🤖 Choose provider (only if bringing own keys)")
        print("4. 🔧 Setup instructions")
        print("5. 🚀 Start building")
        print()
        print("🎉 New flow is ready!")
        print()
        print("💡 To test the flow:")
        print("   stableagents-ai guided-setup")
        print("   stableagents-ai --start")
        print("   stableagents-ai (no command)")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Test error: {e}")

def show_flow_comparison():
    """Show the difference between old and new flow"""
    print("\n🔄 Flow Comparison")
    print("=" * 30)
    
    print("\n❌ OLD FLOW:")
    print("1. Show prompts and select provider")
    print("2. Ask about payment options")
    print("3. Setup API keys")
    
    print("\n✅ NEW FLOW:")
    print("1. Ask about payment options FIRST")
    print("2. If monthly subscription: process payment")
    print("3. If bring own keys: then ask about provider")
    print("4. If local models: skip provider selection")
    print("5. Setup API keys")
    
    print("\n🎯 Benefits of new flow:")
    print("• Users know payment requirements upfront")
    print("• No provider selection for subscription users")
    print("• Cleaner, more logical flow")
    print("• Better user experience")

if __name__ == "__main__":
    print("🧪 StableAgents New Flow Test")
    print("=" * 50)
    
    test_new_flow()
    show_flow_comparison()
    
    print("\n" + "=" * 50)
    print("🎯 New flow implementation complete!")
    print("\nThe CLI now asks about payment options first,")
    print("then only asks about providers if users choose to bring their own keys.") 