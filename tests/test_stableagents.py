import pytest
from stableagents import StableAgents

def test_stableagents_initialization():
    """Test that StableAgents can be initialized"""
    agent = StableAgents()
    assert agent is not None
    assert agent.memory is not None
    assert "short_term" in agent.memory

def test_memory_operations():
    """Test basic memory operations"""
    agent = StableAgents()
    
    # Add to memory
    test_value = "test_value"
    agent.add_to_memory("short_term", "test_key", test_value)
    
    # Get from memory
    result = agent.get_from_memory("short_term")
    assert len(result) > 0
    
    # Get specific key
    items = [item for item in result if item["key"] == "test_key"]
    assert len(items) == 1
    assert items[0]["value"] == test_value

def test_reset():
    """Test reset functionality"""
    agent = StableAgents()
    
    # Add to memory
    agent.add_to_memory("short_term", "test_key", "test_value")
    agent.add_to_memory("long_term", "persistent_key", "persistent_value")
    
    # Reset
    agent.reset()
    
    # Short-term memory should be empty
    assert len(agent.get_from_memory("short_term")) == 0
    
    # Long-term memory should still have data
    assert agent.get_from_memory("long_term", "persistent_key") == "persistent_value" 