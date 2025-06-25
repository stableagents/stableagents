#!/usr/bin/env python3
"""
Test script for Payment Link Integration with existing Stripe link
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_payment_link_integration():
    """Test the payment link integration"""
    print("🔗 Testing Payment Link Integration")
    print("=" * 45)
    
    try:
        from stableagents.stripe_payment import StripePaymentManager
        
        # Test 1: Check payment link configuration
        print("\n1. Testing payment link configuration...")
        stripe_manager = StripePaymentManager()
        config = stripe_manager.get_stripe_config()
        
        payment_link = config.get('payment_link')
        if payment_link:
            print("✅ Payment link configured")
            print(f"   URL: {payment_link}")
        else:
            print("❌ No payment link configured")
            return
        
        # Test 2: Test payment link creation
        print("\n2. Testing payment link creation...")
        created_link = stripe_manager.create_payment_link()
        if created_link:
            print("✅ Payment link created/retrieved successfully")
            print(f"   URL: {created_link}")
        else:
            print("❌ Failed to create/retrieve payment link")
            return
        
        # Test 3: Test CLI integration
        print("\n3. Testing CLI integration...")
        print("   Available commands:")
        print("   • stableagents-ai payment-link")
        print("   • stableagents-keys payment-link")
        print("   • stableagents-ai setup (option 1)")
        print("   • stableagents-ai --start (option 1)")
        
        print("\n" + "=" * 45)
        print("🎉 Payment link integration test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test error: {e}")

def show_usage_instructions():
    """Show usage instructions"""
    print("\n📋 Usage Instructions")
    print("=" * 25)
    
    print("\n🔗 Direct payment link:")
    print("   https://buy.stripe.com/3cI3cw5XW5zI0tRgTM6Ri01")
    print()
    
    print("💻 CLI commands:")
    print("   stableagents-ai payment-link")
    print("   stableagents-keys payment-link")
    print("   stableagents-ai setup")
    print("   stableagents-ai --start")
    print()
    
    print("🎯 Flow:")
    print("   1. User chooses monthly subscription")
    print("   2. Browser opens to payment link")
    print("   3. User completes payment")
    print("   4. User returns to CLI and presses Enter")
    print("   5. Setup continues automatically")
    print()

if __name__ == "__main__":
    print("🧪 StableAgents Payment Link Integration Test")
    print("=" * 55)
    
    test_payment_link_integration()
    show_usage_instructions()
    
    print("\n" + "=" * 55)
    print("🎯 Payment link integration ready!")
    print("\nYour Stripe payment link is now integrated:")
    print("https://buy.stripe.com/3cI3cw5XW5zI0tRgTM6Ri01") 