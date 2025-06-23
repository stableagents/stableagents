#!/usr/bin/env python3
"""
Stripe Payment Manager for StableAgents
Handles monthly subscription billing with Stripe
"""
import os
import time
import webbrowser
import stripe
from typing import Optional, Dict, Any
import json
from pathlib import Path

class StripePaymentManager:
    def __init__(self):
        self.stripe = None
        self.payment_config_file = Path.home() / ".stableagents" / "stripe_config.json"
        self.payment_status_file = Path.home() / ".stableagents" / "payment_status.json"
        
        # Ensure config directory exists
        self.payment_config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load or create configuration
        self.config = self._load_config()
        
        # Initialize Stripe if API key is available
        if self.config.get('stripe_secret_key'):
            stripe.api_key = self.config['stripe_secret_key']
            self.stripe = stripe
    
    def _load_config(self) -> Dict[str, Any]:
        """Load Stripe configuration from file"""
        if self.payment_config_file.exists():
            try:
                with open(self.payment_config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default configuration for monthly subscription
        return {
            'stripe_secret_key': os.getenv('STRIPE_SECRET_KEY'),
            'stripe_publishable_key': os.getenv('STRIPE_PUBLISHABLE_KEY'),
            'product_name': 'StableAgents Monthly Subscription',
            'product_description': 'Monthly access to managed API keys and features',
            'price_amount': 2000,  # $20.00 in cents
            'currency': 'usd',
            'billing_interval': 'month'
        }
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.payment_config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")
    
    def _save_payment_status(self, status: Dict[str, Any]):
        """Save payment status to file"""
        try:
            with open(self.payment_status_file, 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save payment status: {e}")
    
    def _load_payment_status(self) -> Dict[str, Any]:
        """Load payment status from file"""
        if self.payment_status_file.exists():
            try:
                with open(self.payment_status_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            'subscribed': False, 
            'subscription_id': None, 
            'customer_id': None,
            'subscription_date': None,
            'next_billing_date': None,
            'status': 'inactive'
        }
    
    def setup_stripe_keys(self, secret_key: str, publishable_key: str):
        """Setup Stripe API keys"""
        self.config['stripe_secret_key'] = secret_key
        self.config['stripe_publishable_key'] = publishable_key
        self._save_config()
        
        # Initialize Stripe
        stripe.api_key = secret_key
        self.stripe = stripe
        
        print("✅ Stripe keys configured successfully")
    
    def check_stripe_configured(self) -> bool:
        """Check if Stripe is properly configured"""
        if not self.config.get('stripe_secret_key'):
            print("❌ Stripe not configured. Please set up Stripe keys first.")
            print("💡 You can set environment variables:")
            print("   export STRIPE_SECRET_KEY='sk_test_...'")
            print("   export STRIPE_PUBLISHABLE_KEY='pk_test_...'")
            print("   Or use the setup_stripe_keys() method")
            return False
        
        if not self.stripe:
            stripe.api_key = self.config['stripe_secret_key']
            self.stripe = stripe
        
        return True
    
    def create_or_get_product(self) -> Optional[str]:
        """Create or get the product ID for StableAgents subscription"""
        if not self.check_stripe_configured():
            return None
        
        try:
            # Check if product already exists
            products = self.stripe.Product.list(limit=100)
            for product in products.data:
                if product.name == self.config['product_name']:
                    return product.id
            
            # Create new product
            product = self.stripe.Product.create(
                name=self.config['product_name'],
                description=self.config['product_description']
            )
            return product.id
            
        except Exception as e:
            print(f"❌ Error creating product: {e}")
            return None
    
    def create_or_get_price(self, product_id: str) -> Optional[str]:
        """Create or get the price ID for the subscription"""
        if not self.check_stripe_configured():
            return None
        
        try:
            # Check if price already exists
            prices = self.stripe.Price.list(
                product=product_id,
                active=True,
                limit=100
            )
            
            for price in prices.data:
                if (price.unit_amount == self.config['price_amount'] and 
                    price.currency == self.config['currency'] and
                    price.recurring and 
                    price.recurring.interval == self.config['billing_interval']):
                    return price.id
            
            # Create new price
            price = self.stripe.Price.create(
                product=product_id,
                unit_amount=self.config['price_amount'],
                currency=self.config['currency'],
                recurring={
                    'interval': self.config['billing_interval']
                }
            )
            return price.id
            
        except Exception as e:
            print(f"❌ Error creating price: {e}")
            return None
    
    def create_checkout_session(self, price_id: str) -> Optional[str]:
        """Create a Stripe checkout session for subscription"""
        if not self.check_stripe_configured():
            return None
        
        try:
            checkout_session = self.stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url='https://stableagents.ai/subscription-success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://stableagents.ai/subscription-cancel',
                metadata={
                    'product': 'stableagents_monthly_subscription',
                    'version': '1.0'
                }
            )
            
            return checkout_session.url
            
        except Exception as e:
            print(f"❌ Error creating checkout session: {e}")
            return None
    
    def check_subscription_status(self, session_id: str) -> bool:
        """Check if subscription was created successfully"""
        if not self.check_stripe_configured():
            return False
        
        try:
            # Get the checkout session
            session = self.stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid' and session.subscription:
                subscription = self.stripe.Subscription.retrieve(session.subscription)
                
                if subscription.status in ['active', 'trialing']:
                    # Save subscription status
                    status = {
                        'subscribed': True,
                        'subscription_id': subscription.id,
                        'customer_id': subscription.customer,
                        'subscription_date': time.strftime('%Y-%m-%dT%H:%M:%S'),
                        'next_billing_date': time.strftime('%Y-%m-%dT%H:%M:%S', 
                                                          time.localtime(subscription.current_period_end)),
                        'status': subscription.status
                    }
                    self._save_payment_status(status)
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error checking subscription status: {e}")
            return False
    
    def process_monthly_subscription(self) -> bool:
        """Process monthly subscription signup"""
        if not self.check_stripe_configured():
            return False
        
        print("\n💳 Monthly Subscription Setup")
        print("=" * 35)
        print(f"Product: {self.config['product_name']}")
        print(f"Amount: ${self.config['price_amount'] / 100:.2f} {self.config['currency'].upper()} per month")
        print(f"Billing: Monthly recurring")
        print()
        
        # Create product and price
        print("🔧 Setting up subscription product...")
        product_id = self.create_or_get_product()
        if not product_id:
            print("❌ Failed to create product")
            return False
        
        price_id = self.create_or_get_price(product_id)
        if not price_id:
            print("❌ Failed to create price")
            return False
        
        # Create checkout session
        checkout_url = self.create_checkout_session(price_id)
        if not checkout_url:
            print("❌ Failed to create checkout session")
            return False
        
        # Extract session ID from URL
        session_id = checkout_url.split('session_id=')[-1] if 'session_id=' in checkout_url else None
        
        print("🔗 Opening subscription page in your browser...")
        print(f"Subscription URL: {checkout_url}")
        print()
        print("📋 Instructions:")
        print("1. Complete subscription setup in your browser")
        print("2. Return to this terminal")
        print("3. Press Enter to check subscription status")
        print()
        
        # Open browser
        try:
            webbrowser.open(checkout_url)
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"Please manually visit: {checkout_url}")
        
        # Wait for user to complete subscription
        input("Press Enter after completing subscription...")
        
        # Check subscription status
        if session_id:
            print("\n🔍 Checking subscription status...")
            max_attempts = 5
            for attempt in range(max_attempts):
                if self.check_subscription_status(session_id):
                    print("✅ Subscription active!")
                    return True
                
                if attempt < max_attempts - 1:
                    print(f"⏳ Subscription not found yet... (attempt {attempt + 1}/{max_attempts})")
                    time.sleep(2)
        
        print("❌ Subscription not completed or not found")
        return False
    
    def get_subscription_status(self) -> Dict[str, Any]:
        """Get current subscription status"""
        status = self._load_payment_status()
        
        # If we have a subscription ID, check with Stripe
        if status.get('subscription_id') and self.check_stripe_configured():
            try:
                subscription = self.stripe.Subscription.retrieve(status['subscription_id'])
                status['status'] = subscription.status
                status['next_billing_date'] = time.strftime('%Y-%m-%dT%H:%M:%S', 
                                                          time.localtime(subscription.current_period_end))
                self._save_payment_status(status)
            except Exception as e:
                print(f"Warning: Could not check subscription status: {e}")
        
        return status
    
    def cancel_subscription(self) -> bool:
        """Cancel the current subscription"""
        status = self._load_payment_status()
        
        if not status.get('subscription_id') or not self.check_stripe_configured():
            print("❌ No active subscription found")
            return False
        
        try:
            subscription = self.stripe.Subscription.retrieve(status['subscription_id'])
            subscription.cancel_at_period_end = True
            subscription.save()
            
            # Update local status
            status['status'] = 'canceled'
            self._save_payment_status(status)
            
            print("✅ Subscription will be canceled at the end of the current period")
            return True
            
        except Exception as e:
            print(f"❌ Error canceling subscription: {e}")
            return False
    
    def reset_subscription_status(self):
        """Reset subscription status (for testing)"""
        status = {
            'subscribed': False, 
            'subscription_id': None, 
            'customer_id': None,
            'subscription_date': None,
            'next_billing_date': None,
            'status': 'inactive'
        }
        self._save_payment_status(status)
        print("✅ Subscription status reset")
    
    def get_stripe_config(self) -> Dict[str, Any]:
        """Get Stripe configuration (without sensitive keys)"""
        safe_config = self.config.copy()
        if safe_config.get('stripe_secret_key'):
            safe_config['stripe_secret_key'] = safe_config['stripe_secret_key'][:8] + '...'
        if safe_config.get('stripe_publishable_key'):
            safe_config['stripe_publishable_key'] = safe_config['stripe_publishable_key'][:8] + '...'
        return safe_config 