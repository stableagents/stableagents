#!/usr/bin/env python3
"""
Test script for StableAgents Monthly Subscription System
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_monthly_subscription():
    """Test the monthly subscription system"""
    print("💳 Testing Monthly Subscription System")
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
            print(f"   Product: {config['product_name']}")
            print(f"   Price: ${config['price_amount'] / 100:.2f} per {config['billing_interval']}")
        else:
            print("⚠️  Stripe not configured")
            print("   Set environment variables:")
            print("   export STRIPE_SECRET_KEY='sk_test_...'")
            print("   export STRIPE_PUBLISHABLE_KEY='pk_test_...'")
        
        # Test 3: Test product and price creation (if configured)
        if config.get('stripe_secret_key'):
            print("\n3. Testing product and price creation...")
            product_id = stripe_manager.create_or_get_product()
            if product_id:
                print(f"✅ Product created/retrieved: {product_id}")
                
                price_id = stripe_manager.create_or_get_price(product_id)
                if price_id:
                    print(f"✅ Price created/retrieved: {price_id}")
                else:
                    print("❌ Failed to create price")
            else:
                print("❌ Failed to create product")
        else:
            print("\n3. Skipping product/price test (Stripe not configured)")
        
        # Test 4: Test integration with API key manager
        print("\n4. Testing integration with API key manager...")
        api_manager = SecureAPIKeyManager()
        
        # Check subscription status
        subscription_status = api_manager.check_payment_status()
        print(f"   Current subscription status: {subscription_status}")
        
        # Test 5: Test subscription flow
        print("\n5. Testing subscription flow...")
        if subscription_status.get('subscribed'):
            print("✅ User has active subscription")
            if subscription_status.get('next_billing_date'):
                print(f"   Next billing: {subscription_status['next_billing_date']}")
        else:
            print("❌ No active subscription")
        
        print("\n" + "=" * 45)
        print("🎉 Monthly subscription test completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Test error: {e}")

def show_subscription_benefits():
    """Show the benefits of the monthly subscription"""
    print("\n🚀 Monthly Subscription Benefits")
    print("=" * 35)
    
    benefits = [
        "💳 $20/month for managed API keys",
        "🔄 Automatic monthly billing",
        "🔑 Access to OpenAI, Anthropic, and Google APIs",
        "🔒 Secure encryption of all API keys",
        "📅 Cancel anytime",
        "🛡️  Professional payment processing",
        "📱 Works on all devices",
        "⚡ Instant access after payment"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    print("\n💡 Subscription includes:")
    print("   • Managed API keys for all major providers")
    print("   • Secure key storage and encryption")
    print("   • Automatic billing and renewal")
    print("   • Easy cancellation process")

def show_usage_instructions():
    """Show usage instructions"""
    print("\n📋 Usage Instructions")
    print("=" * 25)
    
    print("\n🔐 Setup Stripe for subscriptions:")
    print("   export STRIPE_SECRET_KEY='sk_test_...'")
    print("   export STRIPE_PUBLISHABLE_KEY='pk_test_...'")
    print()
    
    print("💳 Start subscription process:")
    print("   stableagents --start")
    print("   # Choose option 1 for monthly subscription")
    print()
    
    print("📊 Check subscription status:")
    print("   stableagents-keys status")
    print()
    
    print("🚫 Cancel subscription:")
    print("   stableagents-keys cancel")
    print()
    
    print("🔧 Setup custom keys (no subscription):")
    print("   stableagents-keys setup")
    print("   # Choose option 2 for custom keys")

if __name__ == "__main__":
    print("🧪 StableAgents Monthly Subscription Test")
    print("=" * 55)
    
    test_monthly_subscription()
    show_subscription_benefits()
    show_usage_instructions()
    
    print("\n" + "=" * 55)
    print("🎯 Ready to test monthly subscriptions!")
    print("\nTo enable Stripe subscriptions:")
    print("1. Get your Stripe API keys")
    print("2. Set environment variables")
    print("3. Run 'stableagents --start' and choose subscription option") 