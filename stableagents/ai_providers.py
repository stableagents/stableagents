import os
import json
import logging
import getpass
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
import importlib.util

# Import the secure API key manager
try:
    from .api_key_manager import SecureAPIKeyManager
    SECURE_MANAGER_AVAILABLE = True
except ImportError:
    SECURE_MANAGER_AVAILABLE = False

class AIProviderManager:
    """Manages AI provider integrations and API keys."""
    
    SUPPORTED_PROVIDERS = ["openai", "anthropic", "google", "custom", "local"]
    
    def __init__(self, config_dir: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.config_dir = config_dir or self._get_default_config_dir()
        self.keys_file = os.path.join(self.config_dir, "api_keys.json")
        self.api_keys = self._load_api_keys()
        self.active_provider = self._get_active_provider()
        self.provider_instances = {}
        
        # Initialize secure API key manager if available
        self.secure_manager = None
        if SECURE_MANAGER_AVAILABLE:
            self.secure_manager = SecureAPIKeyManager(config_dir)
        
    def _get_default_config_dir(self) -> str:
        """Get the default configuration directory."""
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".stableagents")
        os.makedirs(config_dir, exist_ok=True)
        return config_dir
        
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from the configuration file."""
        if os.path.exists(self.keys_file):
            try:
                with open(self.keys_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading API keys: {str(e)}")
                return {}
        return {}
        
    def _save_api_keys(self) -> None:
        """Save API keys to the configuration file."""
        try:
            os.makedirs(os.path.dirname(self.keys_file), exist_ok=True)
            with open(self.keys_file, 'w') as f:
                json.dump(self.api_keys, f)
        except Exception as e:
            self.logger.error(f"Error saving API keys: {str(e)}")
            
    def _get_active_provider(self) -> Optional[str]:
        """Get the currently active provider."""
        return self.api_keys.get("active_provider")
    
    def setup_secure_api_keys(self) -> bool:
        """Set up secure API key management."""
        if not self.secure_manager:
            self.logger.error("Secure API key manager not available")
            return False
        
        # Show payment options
        self.secure_manager.show_payment_options()
        
        # Get user choice
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Process payment
            if self.secure_manager.process_payment():
                password = getpass.getpass("Enter a password to encrypt your API keys: ")
                if password:
                    return self.secure_manager.provide_api_keys_after_payment(password)
                else:
                    print("❌ Password required for encryption")
                    return False
        
        elif choice == "2":
            # Custom API keys
            password = getpass.getpass("Enter a password to encrypt your API keys: ")
            if password:
                return self.secure_manager.setup_custom_api_keys(password)
            else:
                print("❌ Password required for encryption")
                return False
        
        elif choice == "3":
            # Local models only
            print("\n🏠 Local Models Setup")
            print("=" * 30)
            print("Great choice! You can use StableAgents with local models.")
            print("Download GGUF models and place them in ~/.stableagents/models/")
            print("No API keys or payment required.")
            return True
        
        else:
            print("❌ Invalid choice")
            return False
    
    def get_api_key(self, provider: Optional[str] = None, password: Optional[str] = None) -> Optional[str]:
        """Get the API key for a provider."""
        provider = provider or self.active_provider
        if not provider:
            return None
        
        # Try secure manager first if password provided
        if self.secure_manager and password:
            return self.secure_manager.get_api_key(provider, password)
        
        # Fall back to plain text storage
        return self.api_keys.get(provider)
        
    def set_api_key(self, provider: str, api_key: str, password: Optional[str] = None) -> bool:
        """Set an API key for a provider."""
        if provider not in self.SUPPORTED_PROVIDERS:
            self.logger.error(f"Unsupported provider: {provider}")
            return False
        
        # Use secure manager if available and password provided
        if self.secure_manager and password:
            success = self.secure_manager.set_api_key(provider, api_key, password)
            if success:
                # Also update plain text storage for backward compatibility
                self.api_keys[provider] = api_key
                if not self.active_provider:
                    self.api_keys["active_provider"] = provider
                    self.active_provider = provider
                self._save_api_keys()
            return success
        
        # Fall back to plain text storage
        self.api_keys[provider] = api_key
        
        # If this is the first provider, set it as active
        if not self.active_provider:
            self.api_keys["active_provider"] = provider
            self.active_provider = provider
            
        self._save_api_keys()
        return True
        
    def prompt_for_api_key(self, provider: Optional[str] = None) -> Optional[str]:
        """Prompt the user for an API key."""
        provider = provider or "openai"
        if provider not in self.SUPPORTED_PROVIDERS:
            self.logger.error(f"Unsupported provider: {provider}")
            return None
        
        # Check if secure manager is available
        if self.secure_manager:
            print(f"\n🔐 Secure API Key Setup for {provider.capitalize()}")
            print("=" * 50)
            print("StableAgents supports secure API key storage with encryption.")
            print()
            
            use_secure = input("Would you like to use secure storage? (y/n): ").strip().lower()
            
            if use_secure == 'y':
                # Set up secure API keys
                return self.setup_secure_api_keys()
            else:
                print("Using plain text storage (less secure)")
        
        # Fall back to plain text prompt
        print(f"\nNo API key found for {provider}.")
        print(f"Please enter your {provider.capitalize()} API key:")
        api_key = getpass.getpass("> ")
        
        if api_key:
            self.set_api_key(provider, api_key)
            return api_key
        return None
        
    def set_active_provider(self, provider: str) -> bool:
        """Set the active AI provider."""
        if provider not in self.SUPPORTED_PROVIDERS:
            self.logger.error(f"Unsupported provider: {provider}")
            return False
            
        # Special case for local provider, which doesn't need an API key
        if provider == "local":
            self.api_keys["active_provider"] = provider
            self.active_provider = provider
            self._save_api_keys()
            return True
            
        if provider not in self.api_keys:
            self.logger.error(f"No API key set for provider: {provider}")
            return False
            
        self.api_keys["active_provider"] = provider
        self.active_provider = provider
        self._save_api_keys()
        return True
        
    def get_active_provider(self) -> Optional[str]:
        """Get the active AI provider."""
        return self.active_provider
        
    def list_providers(self) -> List[Dict[str, Any]]:
        """List all supported providers and their status."""
        providers = []
        for provider in self.SUPPORTED_PROVIDERS:
            # Local provider doesn't need an API key
            if provider == "local":
                has_key = True
            else:
                has_key = provider in self.api_keys and bool(self.api_keys[provider])
                
            is_active = provider == self.active_provider
            providers.append({
                "name": provider,
                "has_key": has_key,
                "is_active": is_active
            })
        return providers

    def get_provider(self, provider_name: Optional[str] = None) -> Optional['AIProvider']:
        """Get an instance of the specified provider."""
        provider_name = provider_name or self.active_provider
        
        if not provider_name:
            self.logger.error("No active provider set")
            return None
            
        if provider_name not in self.SUPPORTED_PROVIDERS:
            self.logger.error(f"Unsupported provider: {provider_name}")
            return None
            
        # Check if we already have an instance
        if provider_name in self.provider_instances:
            return self.provider_instances[provider_name]
            
        # Special case for local provider
        if provider_name == "local":
            provider = LocalModelProvider(self.config_dir)
            self.provider_instances[provider_name] = provider
            return provider
            
        # Get the API key
        api_key = self.get_api_key(provider_name)
        if not api_key:
            api_key = self.prompt_for_api_key(provider_name)
            if not api_key:
                return None
                
        # Create a new instance
        provider_class = self._get_provider_class(provider_name)
        if not provider_class:
            return None
            
        provider = provider_class(api_key)
        self.provider_instances[provider_name] = provider
        return provider
        
    def _get_provider_class(self, provider_name: str) -> Optional[type]:
        """Get the provider class based on provider name."""
        if provider_name == "openai":
            return OpenAIProvider
        elif provider_name == "anthropic":
            return AnthropicProvider
        elif provider_name == "google":
            return GoogleProvider
        elif provider_name == "local":
            return LocalModelProvider
        elif provider_name == "custom":
            # Load custom provider if configured
            custom_path = self.api_keys.get("custom_provider_path")
            if custom_path and os.path.exists(custom_path):
                try:
                    spec = importlib.util.spec_from_file_location("custom_provider", custom_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        return module.CustomProvider
                except Exception as e:
                    self.logger.error(f"Error loading custom provider: {str(e)}")
        return None

class AIProvider:
    """Base class for AI providers."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
        
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from a prompt."""
        raise NotImplementedError("Subclasses must implement this method")
        
    def generate_chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a chat response from messages."""
        raise NotImplementedError("Subclasses must implement this method")
        
    def embed_text(self, text: str, **kwargs) -> List[float]:
        """Generate embeddings for text."""
        raise NotImplementedError("Subclasses must implement this method")
        
    def transcribe_audio(self, audio_file: str, **kwargs) -> str:
        """Transcribe audio to text."""
        raise NotImplementedError("Subclasses must implement this method")

class OpenAIProvider(AIProvider):
    """OpenAI provider implementation."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
            self.available = True
        except ImportError:
            self.logger.warning("OpenAI package not installed. Install with: pip install openai")
            self.available = False
        except Exception as e:
            self.logger.error(f"Error initializing OpenAI: {str(e)}")
            self.available = False
            
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from a prompt using OpenAI."""
        if not self.available:
            return "OpenAI not available. Install with: pip install openai"
            
        try:
            model = kwargs.get("model", "gpt-3.5-turbo-instruct")
            max_tokens = kwargs.get("max_tokens", 500)
            
            response = self.client.completions.create(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens
            )
            
            return response.choices[0].text.strip()
        except Exception as e:
            self.logger.error(f"Error generating text: {str(e)}")
            return f"Error: {str(e)}"
            
    def generate_chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a chat response from messages using OpenAI."""
        if not self.available:
            return "OpenAI not available. Install with: pip install openai"
            
        try:
            model = kwargs.get("model", "gpt-3.5-turbo")
            max_tokens = kwargs.get("max_tokens", 500)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Error generating chat: {str(e)}")
            return f"Error: {str(e)}"
            
    def embed_text(self, text: str, **kwargs) -> List[float]:
        """Generate embeddings for text using OpenAI."""
        if not self.available:
            return []
            
        try:
            model = kwargs.get("model", "text-embedding-ada-002")
            
            response = self.client.embeddings.create(
                model=model,
                input=text
            )
            
            return response.data[0].embedding
        except Exception as e:
            self.logger.error(f"Error generating embeddings: {str(e)}")
            return []
            
    def transcribe_audio(self, audio_file: str, **kwargs) -> str:
        """Transcribe audio to text using OpenAI."""
        if not self.available:
            return "OpenAI not available. Install with: pip install openai"
            
        try:
            with open(audio_file, "rb") as f:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f
                )
            
            return response.text
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {str(e)}")
            return f"Error: {str(e)}"

class AnthropicProvider(AIProvider):
    """Anthropic provider implementation (stub)."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            self.available = True
        except ImportError:
            self.logger.warning("Anthropic package not installed. Install with: pip install anthropic")
            self.available = False
        except Exception as e:
            self.logger.error(f"Error initializing Anthropic: {str(e)}")
            self.available = False
            
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from a prompt using Anthropic."""
        if not self.available:
            return "Anthropic not available. Install with: pip install anthropic"
            
        try:
            model = kwargs.get("model", "claude-2")
            max_tokens = kwargs.get("max_tokens", 500)
            
            response = self.client.completions.create(
                model=model,
                prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
                max_tokens_to_sample=max_tokens
            )
            
            return response.completion
        except Exception as e:
            self.logger.error(f"Error generating text: {str(e)}")
            return f"Error: {str(e)}"
            
    def generate_chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a chat response from messages using Anthropic."""
        if not self.available:
            return "Anthropic not available. Install with: pip install anthropic"
            
        try:
            model = kwargs.get("model", "claude-2")
            max_tokens = kwargs.get("max_tokens", 500)
            
            # Convert messages to Anthropic format
            prompt = ""
            for message in messages:
                role = message["role"]
                content = message["content"]
                
                if role == "user" or role == "human":
                    prompt += f"\n\nHuman: {content}"
                elif role == "assistant":
                    prompt += f"\n\nAssistant: {content}"
                elif role == "system":
                    # System messages go at the beginning
                    prompt = f"{content}" + prompt
                    
            prompt += "\n\nAssistant:"
            
            response = self.client.completions.create(
                model=model,
                prompt=prompt,
                max_tokens_to_sample=max_tokens
            )
            
            return response.completion
        except Exception as e:
            self.logger.error(f"Error generating chat: {str(e)}")
            return f"Error: {str(e)}"
    
    def embed_text(self, text: str, **kwargs) -> List[float]:
        """Generate embeddings for text using Anthropic (not currently supported)."""
        self.logger.warning("Embeddings not currently supported by Anthropic")
        return []
    
    def transcribe_audio(self, audio_file: str, **kwargs) -> str:
        """Transcribe audio to text using Anthropic (not currently supported)."""
        self.logger.warning("Audio transcription not currently supported by Anthropic")
        return "Audio transcription not currently supported by Anthropic"

class GoogleProvider(AIProvider):
    """Google AI provider implementation (stub)."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.available = False
        self.logger.warning("Google AI provider not fully implemented yet")
        
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text from a prompt using Google."""
        return "Google AI provider not fully implemented yet"
        
    def generate_chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a chat response from messages using Google."""
        return "Google AI provider not fully implemented yet"
        
    def embed_text(self, text: str, **kwargs) -> List[float]:
        """Generate embeddings for text using Google."""
        return []
        
    def transcribe_audio(self, audio_file: str, **kwargs) -> str:
        """Transcribe audio to text using Google."""
        return "Google AI provider not fully implemented yet"

class LocalModelProvider(AIProvider):
    """Provider for local LLM inference (Llama, etc.)"""
    
    def __init__(self, config_dir: str = None):
        super().__init__(api_key="")  # No API key needed for local models
        self.config_dir = config_dir or os.path.join(os.path.expanduser("~"), ".stableagents")
        self.models_dir = os.path.join(self.config_dir, "models")
        self.model = None
        self.model_path = None
        
        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)
        
    def load_model(self, model_path: str = None):
        """Load a local LLM model."""
        try:
            # If model_path is not provided, try to find default model
            if not model_path:
                default_model_dir = os.path.join(self.models_dir, "default")
                if os.path.exists(default_model_dir):
                    # Find first .gguf file in directory
                    for file in os.listdir(default_model_dir):
                        if file.endswith(".gguf"):
                            model_path = os.path.join(default_model_dir, file)
                            break
                            
            if not model_path or not os.path.exists(model_path):
                self.logger.error(f"Model not found at {model_path}")
                return False
                
            self.logger.info(f"Loading local model from {model_path}")
            
            # Try to import llama_cpp module
            try:
                from llama_cpp import Llama
                self.model = Llama(model_path=model_path, n_ctx=2048)
                self.model_path = model_path
                return True
            except ImportError:
                self.logger.error("llama-cpp-python not installed. Please install it to use local models.")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading local model: {e}")
            return False
            
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using a local model."""
        if not self.model:
            # Try to load default model
            if not self.load_model():
                return "No local model loaded. Please load a model first."
                
        try:
            # Set default parameters for generation
            max_tokens = kwargs.get("max_tokens", 512)
            temperature = kwargs.get("temperature", 0.7)
            
            # Generate text with the local model
            output = self.model(
                prompt, 
                max_tokens=max_tokens,
                temperature=temperature,
                stop=kwargs.get("stop", [])
            )
            
            return output["choices"][0]["text"]
        except Exception as e:
            self.logger.error(f"Error generating text with local model: {e}")
            return f"Error: {str(e)}"
            
    def generate_chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate chat response using a local model."""
        if not self.model:
            # Try to load default model
            if not self.load_model():
                return "No local model loaded. Please load a model first."
                
        try:
            # Format messages into a prompt that local models can understand
            formatted_prompt = ""
            for message in messages:
                role = message.get("role", "").lower()
                content = message.get("content", "")
                
                if role == "system":
                    formatted_prompt += f"SYSTEM: {content}\n\n"
                elif role == "user":
                    formatted_prompt += f"USER: {content}\n\n"
                elif role == "assistant":
                    formatted_prompt += f"ASSISTANT: {content}\n\n"
                    
            formatted_prompt += "ASSISTANT: "
            
            # Generate response
            return self.generate_text(formatted_prompt, **kwargs)
        except Exception as e:
            self.logger.error(f"Error generating chat response with local model: {e}")
            return f"Error: {str(e)}"
            
    def embed_text(self, text: str, **kwargs) -> List[float]:
        """Generate embeddings with local model."""
        # This is a placeholder for local embeddings
        # Most local LLMs don't have built-in embedding capability
        self.logger.warning("Embeddings not supported with basic local models")
        return []
        
    def transcribe_audio(self, audio_file: str, **kwargs) -> str:
        """Transcribe audio with local model."""
        # This is a placeholder for local transcription
        # Most local LLMs don't have built-in audio transcription
        self.logger.warning("Audio transcription not supported with basic local models")
        return "Audio transcription not supported with local models" 