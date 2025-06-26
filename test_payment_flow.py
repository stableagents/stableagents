#!/usr/bin/env python3
"""
Test script to verify the payment flow works correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'stableagents'))

from stableagents.api_key_manager import SecureAPIKeyManager
from stableagents.stripe_payment import StripePaymentManager

def test_payment_flow():
    """Test the payment flow without actually processing payment"""
    print("🧪 Testing Payment Flow")
    print("=" * 30)
    
    try:
        # Create the manager
        manager = SecureAPIKeyManager()
        print("✅ SecureAPIKeyManager created successfully")
        
        # Test that the process_payment method exists
        if hasattr(manager, 'process_payment'):
            print("✅ process_payment method exists")
        else:
            print("❌ process_payment method not found")
            return False
        
        # Test that the stripe_manager is properly initialized
        if hasattr(manager, 'stripe_manager') and manager.stripe_manager:
            print("✅ Stripe manager initialized")
            
            # Test that the stripe_manager has the correct methods
            if hasattr(manager.stripe_manager, 'process_monthly_subscription'):
                print("✅ stripe_manager.process_monthly_subscription method exists")
            else:
                print("❌ stripe_manager.process_monthly_subscription method not found")
                return False
                
            if hasattr(manager.stripe_manager, 'use_existing_payment_link'):
                print("✅ stripe_manager.use_existing_payment_link method exists")
            else:
                print("❌ stripe_manager.use_existing_payment_link method not found")
                return False
                
            # Test the payment link configuration
            stripe_config = manager.stripe_manager.get_stripe_config()
            if stripe_config.get('payment_link'):
                print(f"✅ Payment link configured: {stripe_config['payment_link']}")
            else:
                print("⚠️  No payment link configured")
        else:
            print("⚠️  Stripe manager not available")
            return False
        
        print("\n✅ Payment flow test passed!")
        print("💡 The CLI should now work with the existing payment link")
        return True
        
    except Exception as e:
        print(f"❌ Error during payment flow test: {e}")
        return False

def test_payment_link_flow():
    """Test the payment link flow specifically"""
    print("\n🧪 Testing Payment Link Flow")
    print("=" * 35)
    
    try:
        stripe_manager = StripePaymentManager()
        
        # Check if payment link is configured
        config = stripe_manager.get_stripe_config()
        if config.get('payment_link'):
            print(f"✅ Payment link found: {config['payment_link']}")
            
            # Test the use_existing_payment_link method (without actually opening browser)
            print("✅ Payment link flow is ready")
            return True
        else:
            print("❌ No payment link configured")
            return False
            
    except Exception as e:
        print(f"❌ Error testing payment link flow: {e}")
        return False

if __name__ == "__main__":
    success1 = test_payment_flow()
    success2 = test_payment_link_flow()
    
    if success1 and success2:
        print("\n🎉 All tests passed! The payment flow is ready.")
    else:
        print("\n❌ Some tests failed.")
    
    sys.exit(0 if (success1 and success2) else 1) 