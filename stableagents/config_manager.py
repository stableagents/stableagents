#!/usr/bin/env python3
"""
Configuration Manager for StableAgents

Handles API keys, settings, and configuration management.
"""

import os
import json
import getpass
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration and API keys for StableAgents."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the configuration manager."""
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".stableagents"
        
        self.config_file = self.config_dir / "config.json"
        self.api_keys_file = self.config_dir / "api_keys.json"
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing configuration
        self.config = self._load_config()
        self.api_keys = self._load_api_keys()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from file."""
        if self.api_keys_file.exists():
            try:
                with open(self.api_keys_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_api_keys(self) -> None:
        """Save API keys to file."""
        try:
            with open(self.api_keys_file, 'w') as f:
                json.dump(self.api_keys, f, indent=2)
        except Exception as e:
            print(f"Error saving API keys: {e}")
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for a provider."""
        # Try environment variable first
        env_key = f"{provider.upper()}_API_KEY"
        if env_key in os.environ:
            return os.environ[env_key]
        
        # Try config file
        return self.api_keys.get(provider)
    
    def set_api_key(self, provider: str, api_key: str, save_to_file: bool = True) -> bool:
        """Set API key for a provider."""
        try:
            # Set in memory
            self.api_keys[provider] = api_key
            
            # Set environment variable
            os.environ[f"{provider.upper()}_API_KEY"] = api_key
            
            # Save to file if requested
            if save_to_file:
                self._save_api_keys()
            
            return True
        except Exception as e:
            print(f"Error setting API key: {e}")
            return False
    
    def prompt_for_api_key(self, provider: str) -> Optional[str]:
        """Prompt user for API key."""
        print(f"🔑 {provider.upper()} API Key Required")
        print("=" * 40)
        
        if provider.lower() == "gemini":
            print("Get your API key from: https://makersuite.google.com/app/apikey")
        elif provider.lower() == "openai":
            print("Get your API key from: https://platform.openai.com/api-keys")
        elif provider.lower() == "anthropic":
            print("Get your API key from: https://console.anthropic.com/")
        else:
            print(f"Get your {provider.upper()} API key from their website")
        
        print()
        
        try:
            api_key = getpass.getpass(f"Enter your {provider.upper()} API key: ")
            if api_key.strip():
                return api_key.strip()
            else:
                print("❌ No API key provided")
                return None
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Setup cancelled.")
            return None
    
    def setup_gemini_api_key(self) -> bool:
        """Setup Gemini API key interactively."""
        print("🔑 Setting up Google Gemini API Key")
        print("=" * 40)
        
        # Check if already set
        existing_key = self.get_api_key("gemini")
        if existing_key:
            print("✅ Gemini API key already configured")
            return True
        
        # Prompt for new key
        api_key = self.prompt_for_api_key("gemini")
        if not api_key:
            return False
        
        # Save the key
        if self.set_api_key("gemini", api_key):
            print("✅ Gemini API key saved successfully")
            return True
        else:
            print("❌ Failed to save API key")
            return False
    
    def list_api_keys(self) -> Dict[str, bool]:
        """List configured API keys (without showing the actual keys)."""
        providers = ["gemini", "openai", "anthropic"]
        status = {}
        
        for provider in providers:
            key = self.get_api_key(provider)
            status[provider] = key is not None
        
        return status
    
    def remove_api_key(self, provider: str) -> bool:
        """Remove API key for a provider."""
        try:
            # Remove from memory
            if provider in self.api_keys:
                del self.api_keys[provider]
            
            # Remove from environment
            env_key = f"{provider.upper()}_API_KEY"
            if env_key in os.environ:
                del os.environ[env_key]
            
            # Save to file
            self._save_api_keys()
            
            print(f"✅ {provider.upper()} API key removed")
            return True
        except Exception as e:
            print(f"Error removing API key: {e}")
            return False
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any) -> bool:
        """Set configuration value."""
        try:
            self.config[key] = value
            self._save_config()
            return True
        except Exception as e:
            print(f"Error setting config: {e}")
            return False


def setup_gemini_api_key() -> bool:
    """Convenience function to setup Gemini API key."""
    config_manager = ConfigManager()
    return config_manager.setup_gemini_api_key()


def get_gemini_api_key() -> Optional[str]:
    """Convenience function to get Gemini API key."""
    config_manager = ConfigManager()
    return config_manager.get_api_key("gemini")


if __name__ == "__main__":
    # Test the configuration manager
    config = ConfigManager()
    
    print("🔧 Configuration Manager Test")
    print("=" * 40)
    
    # Check current API keys
    api_keys = config.list_api_keys()
    for provider, has_key in api_keys.items():
        status = "✅" if has_key else "❌"
        print(f"{status} {provider.upper()}: {'Configured' if has_key else 'Not configured'}")
    
    # Setup Gemini if not configured
    if not api_keys.get("gemini"):
        print("\n🔑 Setting up Gemini API key...")
        if config.setup_gemini_api_key():
            print("✅ Gemini API key setup complete!")
        else:
            print("❌ Gemini API key setup failed")
    
    print("\n💡 Usage:")
    print("   from stableagents.config_manager import get_gemini_api_key")
    print("   api_key = get_gemini_api_key()") 