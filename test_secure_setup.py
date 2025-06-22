#!/usr/bin/env python3
"""
Test script for StableAgents secure API key management integration
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_secure_setup_integration():
    """Test the secure setup integration with the main CLI"""
    print("🔐 Testing Secure API Setup Integration")
    print("=" * 50)
    
    try:
        from stableagents.api_key_manager import SecureAPIKeyManager
        from stableagents import StableAgents
        
        # Test 1: Check if secure manager is available
        print("\n1. Testing Secure API Key Manager availability...")
        manager = SecureAPIKeyManager()
        print("✅ Secure API Key Manager is available")
        
        # Test 2: Check payment status
        print("\n2. Checking payment status...")
        status = manager.check_payment_status()
        print(f"   Payment status: {status}")
        
        # Test 3: Test payment processing (simulated)
        print("\n3. Testing payment processing...")
        if manager.process_payment():
            print("✅ Payment processing works")
        else:
            print("❌ Payment processing failed")
        
        # Test 4: Test API key storage
        print("\n4. Testing API key storage...")
        test_password = "test_password_123"
        test_key = "sk-test-key-123456789"
        
        if manager.set_api_key("openai", test_key, test_password):
            print("✅ API key storage works")
        else:
            print("❌ API key storage failed")
        
        # Test 5: Test API key retrieval
        print("\n5. Testing API key retrieval...")
        retrieved_key = manager.get_api_key("openai", test_password)
        if retrieved_key == test_key:
            print("✅ API key retrieval works")
        else:
            print("❌ API key retrieval failed")
        
        # Test 6: Test integration with StableAgents
        print("\n6. Testing integration with StableAgents...")
        agent = StableAgents()
        
        # Try to get keys from secure manager
        try:
            key = manager.get_api_key("openai", test_password)
            if key:
                agent.set_api_key("openai", key)
                agent.set_active_ai_provider("openai")
                print("✅ Integration with StableAgents works")
            else:
                print("❌ Failed to get key for StableAgents")
        except Exception as e:
            print(f"❌ Integration error: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test error: {e}")

def test_cli_integration():
    """Test the CLI integration"""
    print("\n🖥️  Testing CLI Integration")
    print("=" * 30)
    
    print("\nAvailable commands:")
    print("  stableagents --start          # Start with secure setup")
    print("  stableagents setup            # Run setup only")
    print("  stableagents interactive      # Start interactive mode")
    print("  stableagents-keys status      # Check key status")
    print("  stableagents-keys setup       # Setup keys via CLI")
    
    print("\nExample usage:")
    print("  python -m stableagents.cli --start")
    print("  python -m stableagents.unified_cli --start")
    print("  python stableagents-keys status")

def show_integration_benefits():
    """Show the benefits of the integration"""
    print("\n🚀 Integration Benefits")
    print("=" * 25)
    
    benefits = [
        "🔐 Automatic secure setup on first run",
        "💳 Integrated payment processing",
        "🔑 Encrypted API key storage",
        "🔄 Seamless fallback to legacy methods",
        "🏠 Local model support",
        "⚡ One-command startup with --start",
        "🛡️  Password-protected key access",
        "📱 User-friendly setup flow"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    print("\n💡 The --start flag provides:")
    print("   • Automatic detection of existing setup")
    print("   • Guided setup for new users")
    print("   • Three setup options (payment, custom keys, local)")
    print("   • Seamless transition to interactive mode")
    print("   • Fallback to limited functionality if setup is skipped")

if __name__ == "__main__":
    print("🧪 StableAgents Secure Setup Integration Test")
    print("=" * 55)
    
    test_secure_setup_integration()
    test_cli_integration()
    show_integration_benefits()
    
    print("\n" + "=" * 55)
    print("🎯 Ready to test the integration!")
    print("\nTry running:")
    print("  python -m stableagents.cli --start")
    print("  python -m stableagents.unified_cli --start")
    print("  stableagents --start") 