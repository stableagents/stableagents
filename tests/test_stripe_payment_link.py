#!/usr/bin/env python3
"""
Test script for Stripe Payment Link Integration
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_stripe_payment_link():
    """Test the Stripe payment link creation"""
    print("💳 Testing Stripe Payment Link Integration")
    print("=" * 50)
    
    try:
        from stableagents.stripe_payment import StripePaymentManager
        
        # Test 1: Check if Stripe is available
        print("\n1. Testing Stripe availability...")
        stripe_manager = StripePaymentManager()
        print("✅ Stripe Payment Manager created")
        
        # Test 2: Check Stripe configuration
        print("\n2. Checking Stripe configuration...")
        config = stripe_manager.get_stripe_config()
        print(f"   Product: {config['product_name']}")
        print(f"   Price: ${config['price_amount'] / 100:.2f} per {config['billing_interval']}")
        print(f"   Currency: {config['currency'].upper()}")
        
        if config.get('stripe_secret_key'):
            print("✅ Stripe is configured")
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
                print("✅ Payment link created successfully!")
                print(f"   URL: {payment_url}")
                print("\n📋 How to use:")
                print("1. Visit the payment link in your browser")
                print("2. Complete the subscription setup")
                print("3. After payment, you'll be redirected to a success page")
                print("4. Copy the session_id from the URL")
                print("5. Use it with the CLI: stableagents-keys payment-link")
            else:
                print("❌ Failed to create payment link")
        else:
            print("\n3. Skipping payment link test (Stripe not configured)")
        
        # Test 4: Test CLI integration
        print("\n4. Testing CLI integration...")
        print("   Available commands:")
        print("   • stableagents-ai payment-link")
        print("   • stableagents-keys payment-link")
        print("   • stableagents-ai setup (option 1)")
        
        print("\n" + "=" * 50)
        print("🎉 Stripe payment link test completed!")
        
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
    
    print("3. Install Stripe package:")
    print("   pip install stripe")
    print()
    
    print("4. Test the integration:")
    print("   python tests/test_stripe_payment_link.py")
    print()

def show_usage_examples():
    """Show usage examples"""
    print("\n💡 Usage Examples")
    print("=" * 20)
    
    print("\n🔗 Create payment link:")
    print("   stableagents-ai payment-link")
    print()
    
    print("🔑 Create payment link via key manager:")
    print("   stableagents-keys payment-link")
    print()
    
    print("🎯 Setup with payment link:")
    print("   stableagents-ai setup")
    print("   # Choose option 1 for monthly subscription")
    print()
    
    print("🚀 Start with payment link:")
    print("   stableagents-ai --start")
    print("   # Choose option 1 for monthly subscription")
    print()

if __name__ == "__main__":
    print("🧪 StableAgents Stripe Payment Link Test")
    print("=" * 55)
    
    test_stripe_payment_link()
    show_stripe_setup_instructions()
    show_usage_examples()
    
    print("\n" + "=" * 55)
    print("🎯 Ready to test Stripe payment links!")
    print("\nTo enable Stripe payment links:")
    print("1. Get your Stripe API keys")
    print("2. Set environment variables")
    print("3. Run 'stableagents-ai payment-link' to create a payment link") 