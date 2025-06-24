#!/usr/bin/env python3
"""
Stripe Payment Manager for StableAgents
Handles monthly subscription billing with Stripe Checkout
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
        """Initialize Stripe payment manager"""
        self.payment_config_file = Path.home() / ".stableagents" / "stripe_config.json"
        self.payment_status_file = Path.home() / ".stableagents" / "payment_status.json"
        
        # Ensure config directory exists
        self.payment_config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load or create configuration
        self.config = self._load_config()
        self.stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
        # Only set the API key if we have it, don't print warning on initialization
        if self.stripe_secret_key:
            stripe.api_key = self.stripe_secret_key
    
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
            'product_name': 'StableAgents Monthly Subscription',
            'product_description': 'Monthly access to managed API keys and features',
            'price_amount': 2000,  # $20.00 in cents
            'currency': 'usd',
            'billing_interval': 'month',
            'success_url': 'https://stableagents.ai/subscription-success?session_id={CHECKOUT_SESSION_ID}',
            'cancel_url': 'https://stableagents.ai/subscription-cancel'
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
    
    def process_monthly_subscription(self) -> bool:
        if not self.stripe_secret_key:
            print("❌ STRIPE_SECRET_KEY is not set. Cannot process payment.")
            return False
        print("\n💳 Monthly Subscription Setup")
        print("=" * 35)
        print(f"Product: {self.config['product_name']}")
        print(f"Amount: ${self.config['price_amount'] / 100:.2f} {self.config['currency'].upper()} per month")
        print(f"Billing: Monthly recurring")
        print()
        # Create product and price if not already created
        product_id = self._get_or_create_product()
        if not product_id:
            print("❌ Failed to create product")
            return False
        price_id = self._get_or_create_price(product_id)
        if not price_id:
            print("❌ Failed to create price")
            return False
        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=self.config['success_url'],
            cancel_url=self.config['cancel_url'],
            metadata={
                'product': 'stableagents_monthly_subscription',
                'version': '1.0'
            }
        )
        checkout_url = session.url
        print("🔗 Opening subscription page in your browser...")
        print(f"Subscription URL: {checkout_url}")
        print()
        print("📋 Instructions:")
        print("1. Complete subscription setup in your browser")
        print("2. After payment, you will be redirected to a success page with a session_id in the URL")
        print("3. Copy the session_id from the URL and paste it below")
        print()
        try:
            webbrowser.open(checkout_url)
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"Please manually visit: {checkout_url}")
        session_id = input("Paste the session_id from the success URL here: ").strip()
        if not session_id:
            print("❌ No session_id provided. Cannot verify payment.")
            return False
        print("\n🔍 Verifying payment with Stripe...")
        if self._verify_checkout_session(session_id):
            print("✅ Subscription active!")
            return True
        print("❌ Payment not completed or not found")
        return False
    
    def _get_or_create_product(self) -> Optional[str]:
        try:
            products = stripe.Product.list(limit=100)
            for product in products.data:
                if product.name == self.config['product_name']:
                    return product.id
            product = stripe.Product.create(
                name=self.config['product_name'],
                description=self.config['product_description']
            )
            return product.id
        except Exception as e:
            print(f"❌ Error creating product: {e}")
            return None
    
    def _get_or_create_price(self, product_id: str) -> Optional[str]:
        try:
            prices = stripe.Price.list(product=product_id, active=True, limit=100)
            for price in prices.data:
                if (price.unit_amount == self.config['price_amount'] and 
                    price.currency == self.config['currency'] and
                    price.recurring and 
                    price.recurring.interval == self.config['billing_interval']):
                    return price.id
            price = stripe.Price.create(
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
    
    def _verify_checkout_session(self, session_id: str) -> bool:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid' and session.subscription:
                subscription = stripe.Subscription.retrieve(session.subscription)
                if subscription.status in ['active', 'trialing']:
                    return True
            return False
        except Exception as e:
            print(f"❌ Error verifying session: {e}")
            return False
    
    def get_subscription_status(self) -> Dict[str, Any]:
        """Get current subscription status"""
        return self._load_payment_status()
    
    def cancel_subscription(self) -> bool:
        """Cancel the current subscription"""
        status = self._load_payment_status()
        
        if not status.get('subscribed'):
            print("❌ No active subscription found")
            return False
        
        print("📧 To cancel your subscription, please contact support or visit your Stripe dashboard.")
        print("   Your subscription will remain active until the end of the current billing period.")
        
        # Update local status
        status['status'] = 'canceling'
        self._save_payment_status(status)
        
        print("✅ Subscription cancellation requested")
        return True
    
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
        if safe_config.get('checkout_url'):
            safe_config['checkout_url'] = safe_config['checkout_url'][:30] + '...'
        return safe_config 