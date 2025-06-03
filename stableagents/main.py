import json 
import os
import threading
import datetime
import sys
import logging
import tensorflow as tf
from .computer import ComputerControl
from .ai_providers import AIProviderManager, AIProvider
# from stableagents import * 


class StableAgents:
    """
    
    This is the stable agent libraries
   
    """
    
    def __init__(self, config_dir: str = None):
        self.computer = ComputerControl()
        self.computer_has_imported_computer_api = True
        self.messages = []
        self.last_messages_count = 0
        self.plain_text_display = True
        self.logger = logging.getLogger(__name__)
        # Memory component initialization
        self.memory = {
            "short_term": [],
            "long_term": {},
            "context": {},
            "last_accessed": datetime.datetime.now()
        }
        # Initialize TensorFlow
        self.tf_model = None
        
        # Initialize AI provider manager
        self.ai_manager = AIProviderManager(config_dir)
        self.ai_provider = None
        self.using_local_model = False
        self.local_model = None
    
    def reset(self):
        if hasattr(self, 'computer') and self.computer:
            self.computer.terminate()
        self.computer_has_imported_computer_api = False
        self.messages = []
        self.last_messages_count = 0
        # Reset memory but keep long-term memory
        self.memory["short_term"] = []
        self.memory["context"] = {}
        self.memory["last_accessed"] = datetime.datetime.now()
        # Reset TensorFlow model
        self.tf_model = None
    
    def display_messages(self, markdown):
        if self.plain_text_display:
            print(markdown)
        else: 
            # Assuming display_markdown_message is defined elsewhere
            try:
                display_markdown_message(markdown)
            except NameError:
                self.logger.error("display_markdown_message function not defined")
                print(markdown)
    
    def add_to_memory(self, memory_type, key, value):
        """
        Add information to the agent's memory
        
        Args:
            memory_type (str): Type of memory ('short_term', 'long_term', or 'context')
            key (str): Key to store the memory under
            value (any): Value to store in memory
        """
        if memory_type == "short_term":
            self.memory["short_term"].append({"key": key, "value": value, "timestamp": datetime.datetime.now()})
            # Limit short-term memory size
            if len(self.memory["short_term"]) > 100:
                self.memory["short_term"].pop(0)
        elif memory_type == "long_term":
            self.memory["long_term"][key] = {"value": value, "timestamp": datetime.datetime.now()}
        elif memory_type == "context":
            self.memory["context"][key] = {"value": value, "timestamp": datetime.datetime.now()}
        
        self.memory["last_accessed"] = datetime.datetime.now()
    
    def get_from_memory(self, memory_type, key=None):
        """
        Retrieve information from the agent's memory
        
        Args:
            memory_type (str): Type of memory ('short_term', 'long_term', or 'context')
            key (str, optional): Key to retrieve. If None, returns all memories of that type.
            
        Returns:
            The requested memory value or dictionary of values
        """
        self.memory["last_accessed"] = datetime.datetime.now()
        
        if memory_type == "short_term":
            if key is None:
                return self.memory["short_term"]
            return [item for item in self.memory["short_term"] if item["key"] == key]
        elif memory_type == "long_term":
            if key is None:
                return self.memory["long_term"]
            return self.memory["long_term"].get(key, {}).get("value")
        elif memory_type == "context":
            if key is None:
                return self.memory["context"]
            return self.memory["context"].get(key, {}).get("value")
        
        return None
    
    def get_stableagents_dir(self):
        """
        Get the stable agents directory path from environment or use default
        
        Returns:
            str: Path to the stable agents directory
        """
        stableagents_dir = os.environ.get("STABLEAGENTS_DIR", os.path.join(os.path.expanduser("~"), ".stableagents"))
        return stableagents_dir

    def control_computer(self, command: str) -> str:
        """
        Control the computer using natural language commands.
        
        Args:
            command (str): Natural language command to execute
            
        Returns:
            str: Result of the command execution
        """
        if not self.computer_has_imported_computer_api:
            self.computer = ComputerControl()
            self.computer_has_imported_computer_api = True
            
        result = self.computer.execute(command)
        
        # Add to short-term memory
        self.add_to_memory("short_term", "computer_command", {
            "command": command,
            "result": result,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        return result
        
    def set_api_key(self, provider: str, api_key: str) -> bool:
        """
        Set an API key for an AI provider.
        
        Args:
            provider (str): The name of the AI provider
            api_key (str): The API key
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.ai_manager.set_api_key(provider, api_key)
    
    def get_api_key(self, provider: str = None) -> str:
        """
        Get the API key for an AI provider.
        
        Args:
            provider (str, optional): The name of the AI provider. If None, uses the active provider.
            
        Returns:
            str: The API key or None if not found
        """
        return self.ai_manager.get_api_key(provider)
    
    def list_ai_providers(self) -> list:
        """
        List all supported AI providers and their status.
        
        Returns:
            list: A list of provider information dictionaries
        """
        return self.ai_manager.list_providers()
    
    def set_active_ai_provider(self, provider: str) -> bool:
        """
        Set the active AI provider.
        
        Args:
            provider (str): The name of the AI provider
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.ai_manager.set_active_provider(provider)
    
    def get_active_ai_provider(self) -> str:
        """
        Get the name of the active AI provider.
        
        Returns:
            str: The name of the active provider or None if not set
        """
        return self.ai_manager.get_active_provider()
    
    def get_ai_provider(self, provider_name: str = None) -> AIProvider:
        """
        Get an instance of an AI provider.
        
        Args:
            provider_name (str, optional): The name of the provider. If None, uses the active provider.
            
        Returns:
            AIProvider: An instance of the AI provider or None if not available
        """
        return self.ai_manager.get_provider(provider_name)
    
    def set_local_model(self, model_path: str = None):
        """
        Set up a local model for inference
        
        Args:
            model_path (str, optional): Path to local model. If None, uses default model.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.using_local_model = True
            
            # If model_path is None, use a default model location
            if model_path is None:
                model_path = os.path.join(self.get_stableagents_dir(), "models", "default")
                
            # Check if model exists
            if not os.path.exists(model_path):
                self.logger.warning(f"Local model not found at {model_path}. Will download default model.")
                # Here we would implement model downloading, but for now just log
                
            # Load the model (simplified for now)
            self.logger.info(f"Loading local model from {model_path}")
            # self.local_model = load_model_function(model_path)
            
            return True
        except Exception as e:
            self.logger.error(f"Error setting up local model: {e}")
            self.using_local_model = False
            return False
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt using the active AI provider or local model.
        
        Args:
            prompt (str): The text prompt
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            str: The generated text
        """
        if self.using_local_model:
            # Use local model for inference
            if self.local_model:
                try:
                    # Simplified local model inference
                    return f"[Local model response to: {prompt}]"
                except Exception as e:
                    self.logger.error(f"Error using local model: {e}")
                    return f"Error using local model: {str(e)}"
            else:
                return "Local model not loaded. Please set up a local model first."
        else:
            # Use remote provider
            provider = self.get_ai_provider()
            if not provider:
                return "No AI provider available. Please set an API key first."
            
            return provider.generate_text(prompt, **kwargs)
    
    def generate_chat(self, messages: list, **kwargs) -> str:
        """
        Generate a chat response using the active AI provider or local model.
        
        Args:
            messages (list): A list of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            str: The generated response
        """
        if self.using_local_model:
            # Use local model for chat inference
            if self.local_model:
                try:
                    # Extract just the last user message for simplicity
                    last_message = messages[-1]['content'] if messages else ""
                    # Simplified local model chat inference
                    return f"[Local model chat response to: {last_message}]"
                except Exception as e:
                    self.logger.error(f"Error using local model for chat: {e}")
                    return f"Error using local model for chat: {str(e)}"
            else:
                return "Local model not loaded. Please set up a local model first."
        else:
            # Use remote provider
            provider = self.get_ai_provider()
            if not provider:
                return "No AI provider available. Please set an API key first."
            
            return provider.generate_chat(messages, **kwargs)
    
    def embed_text(self, text: str, **kwargs) -> list:
        """
        Generate embeddings for text using the active AI provider.
        
        Args:
            text (str): The text to embed
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            list: The embedding vector
        """
        provider = self.get_ai_provider()
        if not provider:
            return []
        
        return provider.embed_text(text, **kwargs)
    
    def transcribe_audio(self, audio_file: str, **kwargs) -> str:
        """
        Transcribe audio to text using the active AI provider.
        
        Args:
            audio_file (str): Path to the audio file
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            str: The transcribed text
        """
        provider = self.get_ai_provider()
        if not provider:
            return "No AI provider available. Please set an API key first."
        
        return provider.transcribe_audio(audio_file, **kwargs)


# For testing in terminal
if __name__ == "__main__":
    # Configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create an instance of StableAgents
    agent = StableAgents()
    print("StableAgents initialized successfully!")
    
    # Test memory functions
    agent.add_to_memory("short_term", "test_key", "test_value")
    agent.add_to_memory("long_term", "persistent_key", "persistent_value")
    
    # Display some test messages
    agent.display_messages("# StableAgents Test\nThis is a test of the StableAgents system.")
    
    # Retrieve and display memory contents
    short_term = agent.get_from_memory("short_term")
    long_term = agent.get_from_memory("long_term")
    
    print("\nShort-term memory contents:")
    print(json.dumps(short_term, default=str, indent=2))
    
    print("\nLong-term memory contents:")
    print(json.dumps(long_term, default=str, indent=2))
    
    print(f"\nStableAgents directory: {agent.get_stableagents_dir()}")