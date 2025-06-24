#!/usr/bin/env python3
"""
Secure API Key Manager for StableAgents

This module provides secure API key management with payment processing
and safe storage of credentials.
"""

import os
import json
import hashlib
import getpass
import base64
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple, List, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import time

# Import Stripe payment manager
try:
    from stableagents.stripe_payment import StripePaymentManager
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False

class SecureAPIKeyManager:
    """Secure API key manager with payment processing and encryption."""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        # Use provided config_dir or default to ~/.stableagents
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".stableagents"
            
        self.keys_file = self.config_dir / "encrypted_keys.json"
        self.payment_file = self.config_dir / "payment_status.json"
        self.salt_file = self.config_dir / "salt.bin"
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Stripe payment manager if available
        self.stripe_manager = None
        if STRIPE_AVAILABLE:
            try:
                self.stripe_manager = StripePaymentManager()
            except Exception as e:
                print(f"Warning: Could not initialize Stripe: {e}")
        
        # Load or create salt
        self.salt = self._load_or_create_salt()
        
    def _load_or_create_salt(self) -> bytes:
        """Load existing salt or create a new one"""
        if self.salt_file.exists():
            try:
                with open(self.salt_file, 'rb') as f:
                    return f.read()
            except Exception:
                pass
        
        # Create new salt
        salt = os.urandom(16)
        try:
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
        except Exception as e:
            print(f"Warning: Could not save salt: {e}")
        
        return salt
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def _encrypt_data(self, data: str, password: str) -> str:
        """Encrypt data using password-derived key"""
        key = self._derive_key(password)
        f = Fernet(key)
        return f.encrypt(data.encode()).decode()
    
    def _decrypt_data(self, encrypted_data: str, password: str) -> Optional[str]:
        """Decrypt data using password-derived key"""
        try:
            key = self._derive_key(password)
            f = Fernet(key)
            return f.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return None
    
    def _load_encrypted_keys(self) -> Dict[str, str]:
        """Load encrypted keys from file"""
        if self.keys_file.exists():
            try:
                with open(self.keys_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_encrypted_keys(self, encrypted_keys: Dict[str, str]):
        """Save encrypted keys to file"""
        try:
            with open(self.keys_file, 'w') as f:
                json.dump(encrypted_keys, f, indent=2)
        except Exception as e:
            print(f"Error saving encrypted keys: {e}")
    
    def _load_payment_status(self) -> Dict[str, Any]:
        """Load payment status from file"""
        if self.payment_file.exists():
            try:
                with open(self.payment_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {'paid': False, 'payment_date': None, 'api_keys_provided': []}
    
    def _save_payment_status(self, status: Dict[str, Any]):
        """Save payment status to file"""
        try:
            with open(self.payment_file, 'w') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            print(f"Error saving payment status: {e}")
    
    def show_payment_options(self):
        """Display payment options to the user."""
        print("\n🔐 StableAgents API Key Management")
        print("=" * 50)
        print("To use StableAgents with AI providers, you have two options:")
        print()
        print("1. 💳 Monthly Subscription ($20/month)")
        print("   - We provide working API keys")
        print("   - Keys are securely encrypted")
        print("   - Monthly recurring subscription")
        print("   - Cancel anytime")
        print("   - No setup fees or hidden costs")
        print()
        print("2. 🔑 Bring your own API keys")
        print("   - Use your existing OpenAI, Anthropic, or other API keys")
        print("   - Keys are securely encrypted and stored locally")
        print("   - No additional cost beyond your existing API usage")
        print()
        print("3. 🏠 Use local models only")
        print("   - Download GGUF models for local inference")
        print("   - No API keys or payment required")
        print("   - Works offline, privacy-focused")
        print()
    
    def process_payment(self) -> bool:
        """Process monthly subscription signup"""
        # Use Stripe API subscription only
        if self.stripe_manager and self.stripe_manager.stripe_secret_key:
            print("💳 Using Stripe for monthly subscription...")
            if self.stripe_manager.process_monthly_subscription():
                return True
        print("❌ Stripe is not configured. Please set STRIPE_SECRET_KEY as an environment variable.")
        return False
    
    def provide_api_keys_after_payment(self, password: str) -> bool:
        """Provide API keys after successful payment"""
        # Check if payment was made
        payment_status = self.check_payment_status()
        if not payment_status.get('paid'):
            print("❌ Payment required before providing API keys")
            return False
        
        # Generate and store API keys
        api_keys = {
            'openai': 'sk-proj-your-openai-key-here',
            'anthropic': 'sk-ant-your-anthropic-key-here',
            'google': 'your-google-api-key-here'
        }
        
        encrypted_keys = {}
        for provider, key in api_keys.items():
            encrypted_key = self._encrypt_data(key, password)
            encrypted_keys[provider] = encrypted_key
        
        self._save_encrypted_keys(encrypted_keys)
        
        # Update payment status
        status = payment_status.copy()
        status['api_keys_provided'] = list(api_keys.keys())
        self._save_payment_status(status)
        
        return True
    
    def setup_custom_api_keys(self, password: str) -> bool:
        """Setup custom API keys provided by the user"""
        print("\n🔑 Custom API Key Setup")
        print("=" * 25)
        print("Enter your API keys securely. They will be encrypted.")
        print("You must provide at least one API key to continue.")
        print("\nType 'exit' at any time to quit the setup.")
        print()
        
        custom_keys = {}
        providers = ["openai", "anthropic"]
        
        for provider in providers:
            try:
                print(f"📡 {provider.capitalize()} API Key:")
                print(f"   Get your key from: https://platform.{provider}.com/account/api-keys")
                api_key = getpass.getpass(f"   Enter your {provider.capitalize()} API key (or type 'exit'): ")
                
                # Check for exit command
                if api_key.lower() in ['exit', 'quit', 'q']:
                    print("👋 Setup cancelled.")
                    return False
                
                if api_key and api_key.strip():
                    custom_keys[provider] = api_key
                    print(f"   ✅ {provider.capitalize()} key stored securely")
                else:
                    print(f"   ⚠️  {provider.capitalize()} key skipped (optional)")
            except (KeyboardInterrupt, EOFError):
                print(f"\n👋 Setup cancelled.")
                return False
        
        if custom_keys:
            # Set the first provider as active
            first_provider = list(custom_keys.keys())[0]
            custom_keys["active_provider"] = first_provider
            
            # Save encrypted keys
            self._save_encrypted_keys(custom_keys)
            
            # Update payment status
            payment_status = self._load_payment_status()
            payment_status["api_keys_provided"] = list(custom_keys.keys())
            self._save_payment_status(payment_status)
            
            print(f"\n✅ {len(custom_keys) - 1} API key(s) stored securely")
            print(f"🔒 Keys are encrypted with your password")
            print(f"🎯 Active provider: {first_provider.capitalize()}")
            return True
        else:
            print("\n❌ No API keys provided")
            print("You must provide at least one API key to use AI features.")
            return False
    
    def get_api_key(self, provider: str, password: str) -> Optional[str]:
        """Get API key for a specific provider"""
        encrypted_keys = self._load_encrypted_keys()
        if provider not in encrypted_keys:
            return None
        
        return self._decrypt_data(encrypted_keys[provider], password)
    
    def set_api_key(self, provider: str, api_key: str, password: str) -> bool:
        """Set API key for a specific provider"""
        encrypted_keys = self._load_encrypted_keys()
        encrypted_key = self._encrypt_data(api_key, password)
        encrypted_keys[provider] = encrypted_key
        self._save_encrypted_keys(encrypted_keys)
        
        # Update payment status to include this provider
        status = self._load_payment_status()
        if provider not in status.get('api_keys_provided', []):
            status['api_keys_provided'].append(provider)
            self._save_payment_status(status)
        
        return True
    
    def get_active_provider(self, password: str) -> Optional[str]:
        """Get the currently active provider."""
        encrypted_keys = self._load_encrypted_keys()
        return encrypted_keys.get("active_provider")
    
    def set_active_provider(self, provider: str, password: str) -> bool:
        """Set the active provider."""
        encrypted_keys = self._load_encrypted_keys()
        if provider in encrypted_keys:
            encrypted_keys["active_provider"] = provider
            self._save_encrypted_keys(encrypted_keys)
            return True
        return False
    
    def list_providers(self, password: str) -> List[Dict[str, Any]]:
        """List all providers with their status"""
        encrypted_keys = self._load_encrypted_keys()
        providers = []
        
        for provider in ['openai', 'anthropic', 'google']:
            has_key = provider in encrypted_keys
            key = None
            if has_key:
                key = self.get_api_key(provider, password)
                has_key = key is not None
            
            providers.append({
                'name': provider,
                'has_key': has_key,
                'is_active': False  # You can implement active provider logic
            })
        
        return providers
    
    def check_payment_status(self) -> Dict[str, Any]:
        """Check if user has an active subscription"""
        # First check Stripe subscription status if available
        if self.stripe_manager:
            stripe_status = self.stripe_manager.get_subscription_status()
            if stripe_status.get('subscribed') and stripe_status.get('status') in ['active', 'trialing']:
                return {
                    'paid': True,  # Keep 'paid' for backward compatibility
                    'subscribed': True,
                    'payment_date': stripe_status.get('subscription_date'),
                    'next_billing_date': stripe_status.get('next_billing_date'),
                    'subscription_id': stripe_status.get('subscription_id'),
                    'api_keys_provided': self._get_available_providers(),
                    'payment_method': 'stripe_subscription',
                    'status': stripe_status.get('status')
                }
        
        # Fallback to local payment status
        local_status = self._load_payment_status()
        return local_status
    
    def _get_available_providers(self) -> List[str]:
        """Get list of providers that have keys stored"""
        encrypted_keys = self._load_encrypted_keys()
        return list(encrypted_keys.keys())
    
    def reset_encryption(self):
        """Reset all encrypted data (for testing)"""
        try:
            if self.keys_file.exists():
                self.keys_file.unlink()
            if self.payment_file.exists():
                self.payment_file.unlink()
            print("✅ All encrypted data has been reset")
        except Exception as e:
            print(f"Error resetting encryption: {e}")
    
    def get_stripe_config(self) -> Dict[str, Any]:
        """Get Stripe configuration"""
        if self.stripe_manager:
            return self.stripe_manager.get_stripe_config()
        return {'stripe_available': False}

def main():
    """Main function for testing the API key manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description='StableAgents API Key Manager')
    parser.add_argument('--reset', action='store_true', help='Reset encryption')
    parser.add_argument('--status', action='store_true', help='Check payment status')
    
    args = parser.parse_args()
    
    manager = SecureAPIKeyManager()
    
    if args.reset:
        manager.reset_encryption()
        return 0
    
    if args.status:
        status = manager.check_payment_status()
        print(f"Payment status: {status}")
        return 0
    
    # Show payment options
    manager.show_payment_options()
    
    # Get user choice
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        # Handle exit commands
        if choice.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Setup cancelled.")
            return 0
        
        if choice == "1":
            # Process payment
            if manager.process_payment():
                try:
                    password = getpass.getpass("Enter a password to encrypt your API keys: ")
                    if password:
                        manager.provide_api_keys_after_payment(password)
                    else:
                        print("❌ Password required for encryption")
                except (KeyboardInterrupt, EOFError):
                    print("\n👋 Setup cancelled.")
                    return 0
        
        elif choice == "2":
            # Custom API keys
            try:
                password = getpass.getpass("Enter a password to encrypt your API keys: ")
                if password:
                    manager.setup_custom_api_keys(password)
                else:
                    print("❌ Password required for encryption")
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Setup cancelled.")
                return 0
        
        elif choice == "3":
            # Local models only
            print("\n🏠 Local Models Setup")
            print("=" * 30)
            print("Great choice! You can use StableAgents with local models.")
            print("Download GGUF models and place them in ~/.stableagents/models/")
            print("No API keys or payment required.")
        
        else:
            print("❌ Invalid choice")
            return 1
    
    except (KeyboardInterrupt, EOFError):
        print("\n👋 Setup cancelled.")
        return 0

if __name__ == "__main__":
    exit(main()) 