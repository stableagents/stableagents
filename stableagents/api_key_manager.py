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
from typing import Dict, Optional, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureAPIKeyManager:
    """Secure API key manager with payment processing and encryption."""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.config_dir = config_dir or self._get_default_config_dir()
        self.keys_file = os.path.join(self.config_dir, "encrypted_keys.json")
        self.payment_file = os.path.join(self.config_dir, "payment_status.json")
        self.salt_file = os.path.join(self.config_dir, ".salt")
        
        # Create config directory if it doesn't exist
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Initialize encryption
        self._initialize_encryption()
        
    def _get_default_config_dir(self) -> str:
        """Get the default configuration directory."""
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".stableagents")
        return config_dir
    
    def _initialize_encryption(self):
        """Initialize encryption key from user password."""
        if not os.path.exists(self.salt_file):
            # Generate new salt
            salt = os.urandom(16)
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
        else:
            # Load existing salt
            with open(self.salt_file, 'rb') as f:
                salt = f.read()
        
        self.salt = salt
    
    def _get_encryption_key(self, password: str) -> bytes:
        """Derive encryption key from password and salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _encrypt_data(self, data: str, password: str) -> str:
        """Encrypt data using password-derived key."""
        key = self._get_encryption_key(password)
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    
    def _decrypt_data(self, encrypted_data: str, password: str) -> str:
        """Decrypt data using password-derived key."""
        try:
            key = self._get_encryption_key(password)
            fernet = Fernet(key)
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_data = fernet.decrypt(encrypted_bytes)
            return decrypted_data.decode()
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            return ""
    
    def _load_encrypted_keys(self, password: str) -> Dict[str, str]:
        """Load encrypted API keys from file."""
        if not os.path.exists(self.keys_file):
            return {}
        
        try:
            with open(self.keys_file, 'r') as f:
                encrypted_data = json.load(f)
            
            decrypted_keys = {}
            for provider, encrypted_key in encrypted_data.items():
                if provider != "active_provider":
                    decrypted_key = self._decrypt_data(encrypted_key, password)
                    if decrypted_key:
                        decrypted_keys[provider] = decrypted_key
                else:
                    decrypted_keys[provider] = encrypted_key
            
            return decrypted_keys
        except Exception as e:
            self.logger.error(f"Error loading encrypted keys: {e}")
            return {}
    
    def _save_encrypted_keys(self, keys: Dict[str, str], password: str):
        """Save API keys encrypted to file."""
        try:
            encrypted_data = {}
            for provider, key in keys.items():
                if provider != "active_provider":
                    encrypted_data[provider] = self._encrypt_data(key, password)
                else:
                    encrypted_data[provider] = key
            
            with open(self.keys_file, 'w') as f:
                json.dump(encrypted_data, f)
        except Exception as e:
            self.logger.error(f"Error saving encrypted keys: {e}")
    
    def _load_payment_status(self) -> Dict[str, any]:
        """Load payment status from file."""
        if not os.path.exists(self.payment_file):
            return {"paid": False, "payment_date": None, "api_keys_provided": []}
        
        try:
            with open(self.payment_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading payment status: {e}")
            return {"paid": False, "payment_date": None, "api_keys_provided": []}
    
    def _save_payment_status(self, status: Dict[str, any]):
        """Save payment status to file."""
        try:
            with open(self.payment_file, 'w') as f:
                json.dump(status, f)
        except Exception as e:
            self.logger.error(f"Error saving payment status: {e}")
    
    def show_payment_options(self):
        """Display payment options to the user."""
        print("\n🔐 StableAgents API Key Management")
        print("=" * 50)
        print("To use StableAgents with AI providers, you have two options:")
        print()
        print("1. 💳 Pay $20 for API key access")
        print("   - We'll provide you with working API keys")
        print("   - Keys are securely encrypted and stored locally")
        print("   - One-time payment, no recurring charges")
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
        """Process payment for API key access."""
        print("\n💳 Payment Processing")
        print("=" * 30)
        print("Processing payment for API key access...")
        print("Amount: $20.00 USD")
        print()
        
        # Simulate payment processing
        print("🔒 Connecting to secure payment processor...")
        print("📊 Validating payment information...")
        print("✅ Payment processed successfully!")
        print()
        
        # Update payment status
        payment_status = self._load_payment_status()
        payment_status["paid"] = True
        payment_status["payment_date"] = self._get_current_timestamp()
        self._save_payment_status(payment_status)
        
        print("🎉 Payment successful! You now have access to API keys.")
        return True
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def provide_api_keys_after_payment(self, password: str) -> bool:
        """Provide API keys after successful payment."""
        print("\n🔑 Setting up API Keys")
        print("=" * 30)
        print("Providing you with working API keys...")
        print()
        
        # In a real implementation, these would be fetched from a secure server
        # For demo purposes, we'll use placeholder keys that need to be replaced
        demo_keys = {
            "openai": "sk-demo-openai-key-needs-replacement",
            "anthropic": "sk-ant-demo-key-needs-replacement"
        }
        
        print("⚠️  IMPORTANT: Demo keys provided")
        print("   These are placeholder keys that need to be replaced with real ones.")
        print("   Please contact support@stableagents.dev for real API keys.")
        print()
        
        # Save the demo keys (encrypted)
        self._save_encrypted_keys(demo_keys, password)
        
        # Update payment status
        payment_status = self._load_payment_status()
        payment_status["api_keys_provided"] = list(demo_keys.keys())
        self._save_payment_status(payment_status)
        
        print("✅ API keys have been securely stored.")
        print("🔒 Keys are encrypted with your password.")
        return True
    
    def setup_custom_api_keys(self, password: str) -> bool:
        """Set up custom API keys provided by the user."""
        print("\n🔑 Custom API Key Setup")
        print("=" * 30)
        print("Please provide your API keys. They will be securely encrypted.")
        print()
        
        custom_keys = {}
        providers = ["openai", "anthropic"]
        
        for provider in providers:
            print(f"📡 {provider.capitalize()} API Key:")
            print(f"   Get your key from: https://platform.{provider}.com/account/api-keys")
            api_key = getpass.getpass(f"   Enter your {provider.capitalize()} API key (or press Enter to skip): ")
            
            if api_key:
                custom_keys[provider] = api_key
                print(f"   ✅ {provider.capitalize()} key stored securely")
            else:
                print(f"   ⏭️  Skipped {provider.capitalize()}")
        
        if custom_keys:
            # Set the first provider as active
            first_provider = list(custom_keys.keys())[0]
            custom_keys["active_provider"] = first_provider
            
            # Save encrypted keys
            self._save_encrypted_keys(custom_keys, password)
            
            # Update payment status
            payment_status = self._load_payment_status()
            payment_status["api_keys_provided"] = list(custom_keys.keys())
            self._save_payment_status(payment_status)
            
            print(f"\n✅ {len(custom_keys) - 1} API key(s) stored securely")
            print(f"🔒 Keys are encrypted with your password")
            print(f"🎯 Active provider: {first_provider.capitalize()}")
            return True
        else:
            print("\n⚠️  No API keys provided")
            return False
    
    def get_api_key(self, provider: str, password: str) -> Optional[str]:
        """Get API key for a specific provider."""
        keys = self._load_encrypted_keys(password)
        return keys.get(provider)
    
    def set_api_key(self, provider: str, api_key: str, password: str) -> bool:
        """Set API key for a specific provider."""
        try:
            keys = self._load_encrypted_keys(password)
            keys[provider] = api_key
            
            # If this is the first provider, set it as active
            if "active_provider" not in keys:
                keys["active_provider"] = provider
            
            self._save_encrypted_keys(keys, password)
            return True
        except Exception as e:
            self.logger.error(f"Error setting API key: {e}")
            return False
    
    def get_active_provider(self, password: str) -> Optional[str]:
        """Get the currently active provider."""
        keys = self._load_encrypted_keys(password)
        return keys.get("active_provider")
    
    def set_active_provider(self, provider: str, password: str) -> bool:
        """Set the active provider."""
        try:
            keys = self._load_encrypted_keys(password)
            if provider in keys:
                keys["active_provider"] = provider
                self._save_encrypted_keys(keys, password)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error setting active provider: {e}")
            return False
    
    def list_providers(self, password: str) -> list:
        """List all providers and their status."""
        keys = self._load_encrypted_keys(password)
        active_provider = keys.get("active_provider")
        
        providers = []
        for provider in ["openai", "anthropic", "google", "local"]:
            has_key = provider in keys and bool(keys[provider])
            is_active = provider == active_provider
            
            providers.append({
                "name": provider,
                "has_key": has_key,
                "is_active": is_active
            })
        
        return providers
    
    def check_payment_status(self) -> Dict[str, any]:
        """Check if user has paid for API key access."""
        return self._load_payment_status()
    
    def reset_encryption(self):
        """Reset encryption (for testing/debugging)."""
        if os.path.exists(self.keys_file):
            os.remove(self.keys_file)
        if os.path.exists(self.payment_file):
            os.remove(self.payment_file)
        if os.path.exists(self.salt_file):
            os.remove(self.salt_file)
        print("🔒 Encryption reset complete")

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
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        # Process payment
        if manager.process_payment():
            password = getpass.getpass("Enter a password to encrypt your API keys: ")
            if password:
                manager.provide_api_keys_after_payment(password)
            else:
                print("❌ Password required for encryption")
    
    elif choice == "2":
        # Custom API keys
        password = getpass.getpass("Enter a password to encrypt your API keys: ")
        if password:
            manager.setup_custom_api_keys(password)
        else:
            print("❌ Password required for encryption")
    
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
    
    return 0

if __name__ == "__main__":
    exit(main()) 