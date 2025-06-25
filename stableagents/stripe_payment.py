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
        self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
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
            'payment_link': 'https://buy.stripe.com/3cI3cw5XW5zI0tRgTM6Ri01',
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
    
    def create_payment_link(self) -> Optional[str]:
        """Create a Stripe payment link for the monthly subscription"""
        # First check if we have an existing payment link
        existing_link = self.config.get('payment_link')
        if existing_link:
            return existing_link
        
        # Fallback to creating a new payment link
        if not self.stripe_secret_key:
            print("❌ STRIPE_SECRET_KEY is not set. Cannot create payment link.")
            return None
        
        try:
            # Create product and price if not already created
            product_id = self._get_or_create_product()
            if not product_id:
                print("❌ Failed to create product")
                return None
                
            price_id = self._get_or_create_price(product_id)
            if not price_id:
                print("❌ Failed to create price")
                return None
            
            # Create payment link
            payment_link = stripe.PaymentLink.create(
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                after_completion={
                    'type': 'redirect',
                    'redirect': {
                        'url': self.config['success_url']
                    }
                },
                metadata={
                    'product': 'stableagents_monthly_subscription',
                    'version': '1.0'
                }
            )
            
            return payment_link.url
            
        except Exception as e:
            print(f"❌ Error creating payment link: {e}")
            return None
    
    def use_existing_payment_link(self) -> bool:
        """Use the existing Stripe payment link for subscription"""
        payment_link = self.config.get('payment_link')
        if not payment_link:
            print("❌ No payment link configured")
            return False
            
        print("\n💳 Monthly Subscription Setup")
        print("=" * 35)
        print(f"Product: {self.config['product_name']}")
        print(f"Amount: ${self.config['price_amount'] / 100:.2f} {self.config['currency'].upper()} per month")
        print(f"Billing: Monthly recurring")
        print()
        print("🔗 Opening subscription page in your browser...")
        print(f"Payment URL: {payment_link}")
        print()
        print("📋 Instructions:")
        print("1. Complete subscription setup in your browser")
        print("2. After payment, you will be redirected to a success page")
        print("3. Return to this terminal window when payment is complete")
        print()
        
        try:
            webbrowser.open(payment_link)
            print("🌐 Payment page opened in your browser")
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"Please manually visit: {payment_link}")
        
        print("\n⏳ Please complete your payment in the browser.")
        print("💡 After payment, return here and press Enter to continue...")
        
        try:
            input("Press Enter when payment is complete (or Ctrl+C to cancel): ")
            print("✅ Payment completed! Setting up your subscription...")
            return True
        except KeyboardInterrupt:
            print("\n👋 Setup cancelled.")
            return False

    def process_monthly_subscription(self) -> bool:
        """Process monthly subscription using existing payment link or create new checkout session"""
        # First try to use existing payment link
        if self.config.get('payment_link'):
            return self.use_existing_payment_link()
        
        # Fallback to creating new checkout session
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
        session_id = session.id
        print("🔗 Opening subscription page in your browser...")
        print(f"Subscription URL: {checkout_url}")
        print()
        print("📋 Instructions:")
        print("1. Complete subscription setup in your browser")
        print("2. After payment, you will be redirected to a success page")
        print("3. Return to this terminal window; payment will be detected automatically.")
        print()

        try:
            webbrowser.open(checkout_url)
        except Exception as e:
            print(f"⚠️  Could not open browser automatically: {e}")
            print(f"Please manually visit: {checkout_url}")

        print("⏳ Waiting for payment confirmation from Stripe...")
        while True:
            try:
                session = stripe.checkout.Session.retrieve(session_id)
                if session.payment_status == 'paid' and session.subscription:
                    subscription = stripe.Subscription.retrieve(session.subscription)
                    if subscription.status in ['active', 'trialing']:
                        # Save subscription details
                        status = {
                            'subscribed': True,
                            'subscription_id': subscription.id,
                            'customer_id': subscription.customer,
                            'subscription_date': time.time(),
                            'next_billing_date': subscription.current_period_end,
                            'status': subscription.status
                        }
                        self._save_payment_status(status)
                        print("\n✅ Subscription active! Payment confirmed.")
                        return True
                time.sleep(3)  # Poll every 3 seconds
            except KeyboardInterrupt:
                print("\n👋 Cancelled by user.")
                return False
            except Exception as e:
                print(f"❌ Error while polling Stripe: {e}")
                time.sleep(5)
        # Should never reach here
        return False
    
    def create_or_get_product(self) -> Optional[str]:
        """Create or get existing product (alias for _get_or_create_product)"""
        return self._get_or_create_product()
    
    def create_or_get_price(self, product_id: str) -> Optional[str]:
        """Create or get existing price (alias for _get_or_create_price)"""
        return self._get_or_create_price(product_id)
    
    def _get_or_create_product(self) -> Optional[str]:
        """Get existing product or create new one"""
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
        """Get existing price or create new one"""
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
        """Verify that a checkout session was completed successfully"""
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid' and session.subscription:
                subscription = stripe.Subscription.retrieve(session.subscription)
                if subscription.status in ['active', 'trialing']:
                    # Save subscription details
                    status = {
                        'subscribed': True,
                        'subscription_id': subscription.id,
                        'customer_id': subscription.customer,
                        'subscription_date': time.time(),
                        'next_billing_date': subscription.current_period_end,
                        'status': subscription.status
                    }
                    self._save_payment_status(status)
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
        safe_config['stripe_secret_key'] = bool(self.stripe_secret_key)
        safe_config['stripe_publishable_key'] = bool(self.stripe_publishable_key)
        if safe_config.get('checkout_url'):
            safe_config['checkout_url'] = safe_config['checkout_url'][:30] + '...'
        return safe_config 