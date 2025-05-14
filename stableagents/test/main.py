import json 
import os
import threading
import datetime
import sys
import logging
# from stableagents import * 


class StableAgents:
    """
    This is the stable agent libraries
    """
    
    def __init__(self):
        self.computer = None
        self.computer_has_imported_computer_api = False
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