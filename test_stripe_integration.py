#!/usr/bin/env python3
"""
Test script for Stripe payment integration in StableAgents
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_stripe_integration():
    """Test the Stripe payment integration"""
    print("💳 Testing Stripe Payment Integration")
    print("=" * 45)
    
    try:
        from stableagents.stripe_payment import StripePaymentManager
        from stableagents.api_key_manager import SecureAPIKeyManager
        
        # Test 1: Check if Stripe is available
        print("\n1. Testing Stripe availability...")
        stripe_manager = StripePaymentManager()
        print("✅ Stripe Payment Manager created")
        
        # Test 2: Check Stripe configuration
        print("\n2. Checking Stripe configuration...")
        config = stripe_manager.get_stripe_config()
        if config.get('stripe_secret_key'):
            print("✅ Stripe is configured")
            print(f"   Secret key: {config['stripe_secret_key']}")
            print(f"   Publishable key: {config['stripe_publishable_key']}")
        else:
            print("⚠️  Stripe not configured")
            print("   Set environment variables:")
            print("   export STRIPE_SECRET_KEY='sk_test_...'")
            print("   export STRIPE_PUBLISHABLE_KEY='pk_test_...'")
        
        # Test 3: Test payment link creation (if configured)
        if config.get('stripe_secret_key'):
            print("\n3. Testing payment link creation...")
            payment_url = stripe_manager.create_payment_link()
            if payment_url:
                print("✅ Payment link created successfully")
                print(f"   URL: {payment_url}")
            else:
                print("❌ Failed to create payment link")
        else:
            print("\n3. Skipping payment link test (Stripe not configured)")
        
        # Test 4: Test integration with API key manager
        print("\n4. Testing integration with API key manager...")
        api_manager = SecureAPIKeyManager()
        
        # Check if Stripe is available in API manager
        stripe_config = api_manager.get_stripe_config()
        if stripe_config.get('stripe_available'):
            print("✅ Stripe integration available in API key manager")
        else:
            print("❌ Stripe integration not available in API key manager")
        
        # Test 5: Test payment processing flow
        print("\n5. Testing payment processing flow...")
        payment_status = api_manager.check_payment_status()
        print(f"   Current payment status: {payment_status}")
        
        print("\n" + "=" * 45)
        print("🎉 Stripe integration test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test error: {e}")

def show_stripe_setup_instructions():
    """Show instructions for setting up Stripe"""
    print("\n🔧 Stripe Setup Instructions")
    print("=" * 30)
    
    print("\n1. Get Stripe API Keys:")
    print("   • Go to https://dashboard.stripe.com/")
    print("   • Sign up or log in")
    print("   • Go to Developers > API keys")
    print("   • Copy your Secret key and Publishable key")
    print()
    
    print("2. Set Environment Variables:")
    print("   export STRIPE_SECRET_KEY='sk_test_...'")
    print("   export STRIPE_PUBLISHABLE_KEY='pk_test_...'")
    print()
    
    print("3. Or use the CLI command:")
    print("   stableagents-keys stripe-setup --stripe-secret sk_test_... --stripe-publishable pk_test_...")
    print()
    
    print("4. Test the integration:")
    print("   python test_stripe_integration.py")
    print()

def show_usage_examples():
    """Show usage examples"""
    print("\n💡 Usage Examples")
    print("=" * 20)
    
    print("\n🔐 Setup Stripe keys:")
    print("   stableagents-keys stripe-setup --stripe-secret sk_test_... --stripe-publishable pk_test_...")
    print()
    
    print("📊 Check status:")
    print("   stableagents-keys status")
    print()
    
    print("💳 Setup with Stripe payment:")
    print("   stableagents-keys setup")
    print("   # Choose option 1 for Stripe payment")
    print()
    
    print("🚀 Start with Stripe payment:")
    print("   stableagents --start")
    print("   # Choose option 1 for Stripe payment")
    print()

if __name__ == "__main__":
    print("🧪 StableAgents Stripe Integration Test")
    print("=" * 50)
    
    test_stripe_integration()
    show_stripe_setup_instructions()
    show_usage_examples()
    
    print("\n" + "=" * 50)
    print("🎯 Ready to test Stripe integration!")
    print("\nTo enable Stripe payments:")
    print("1. Get your Stripe API keys")
    print("2. Set environment variables or use CLI setup")
    print("3. Run 'stableagents --start' and choose payment option") 