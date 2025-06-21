#!/usr/bin/env python3
"""
Simple StableAgents Integration Test

This script demonstrates how the core StableAgents components work together:
- AI Providers (OpenAI, Anthropic)
- Local Models
- Self-Healing System
- Memory Management
- Computer Control

Run this to see the basic integration in action.
"""

import sys
import os
import time

# Add parent directory to path to import stableagents
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stableagents import StableAgents

def test_basic_integration():
    """Test basic integration of StableAgents components."""
    print("🚀 Testing StableAgents Integration")
    print("=" * 40)
    
    # Initialize agent with self-healing
    print("1. Initializing agent...")
    agent = StableAgents(enable_self_healing=True)
    print("✅ Agent initialized")
    
    # Test AI providers
    print("\n2. Testing AI providers...")
    providers = ["openai", "anthropic"]
    
    for provider in providers:
        api_key = agent.get_api_key(provider)
        if api_key:
            print(f"   📡 {provider.capitalize()}: API key found")
            if agent.set_active_ai_provider(provider):
                print(f"   ✅ {provider.capitalize()}: Activated")
                
                # Test text generation
                try:
                    response = agent.generate_text("Hello, world!", max_tokens=10)
                    print(f"   📝 {provider.capitalize()}: Generated text")
                except Exception as e:
                    print(f"   ❌ {provider.capitalize()}: Error - {str(e)}")
        else:
            print(f"   ⚠️  {provider.capitalize()}: No API key")
    
    # Test local models
    print("\n3. Testing local models...")
    try:
        import llama_cpp
        print("   ✅ llama-cpp-python available")
        
        # Check for models
        models_dir = os.path.join(os.path.expanduser("~"), ".stableagents", "models")
        if os.path.exists(models_dir):
            gguf_files = [f for f in os.listdir(models_dir) if f.endswith('.gguf')]
            if gguf_files:
                print(f"   📁 Found {len(gguf_files)} local model(s)")
                # Test loading first model
                model_path = os.path.join(models_dir, gguf_files[0])
                if agent.set_local_model(model_path):
                    print(f"   ✅ Local model loaded: {gguf_files[0]}")
                else:
                    print(f"   ❌ Failed to load local model")
            else:
                print("   📁 No GGUF models found")
        else:
            print("   📁 Models directory not found")
    except ImportError:
        print("   ⚠️  llama-cpp-python not installed")
    
    # Test memory
    print("\n4. Testing memory system...")
    agent.add_to_memory("short_term", "test", {"value": 42})
    memory_data = agent.get_from_memory("short_term", "test")
    print(f"   ✅ Memory test: {memory_data}")
    
    # Test computer control
    print("\n5. Testing computer control...")
    try:
        result = agent.control_computer("get_current_directory")
        print(f"   ✅ Computer control: {result}")
    except Exception as e:
        print(f"   ❌ Computer control error: {str(e)}")
    
    # Test self-healing
    print("\n6. Testing self-healing...")
    if agent.self_healing_enabled:
        health_report = agent.get_health_report()
        print(f"   ✅ Self-healing active: {len(health_report.get('components', {}))} components")
    else:
        print("   ⚠️  Self-healing not enabled")
    
    print("\n🎉 Integration test completed!")
    return True

def test_workflow_integration():
    """Test how components work together in a workflow."""
    print("\n🔄 Testing Workflow Integration")
    print("=" * 40)
    
    agent = StableAgents(enable_self_healing=True)
    
    # Step 1: Use AI to generate content
    print("1. AI Generation...")
    if agent.get_active_ai_provider():
        try:
            response = agent.generate_text("Write a simple Python function", max_tokens=100)
            print(f"   ✅ AI generated: {response[:50]}...")
            
            # Step 2: Store in memory
            print("2. Memory Storage...")
            agent.add_to_memory("short_term", "generated_code", response)
            print("   ✅ Stored in memory")
            
            # Step 3: Computer control
            print("3. Computer Control...")
            result = agent.control_computer("get_current_directory")
            print(f"   ✅ Current directory: {result}")
            
            # Step 4: Health check
            print("4. Health Check...")
            health = agent.get_health_report()
            print(f"   ✅ Health status: {len(health.get('components', {}))} components")
            
            print("\n✅ Workflow integration successful!")
            return True
            
        except Exception as e:
            print(f"   ❌ Workflow error: {str(e)}")
            return False
    else:
        print("   ⚠️  No AI provider available")
        return False

if __name__ == "__main__":
    print("StableAgents Integration Test")
    print("=" * 50)
    
    # Run basic integration test
    test_basic_integration()
    
    # Run workflow test
    test_workflow_integration()
    
    print("\n📊 Test Summary")
    print("=" * 20)
    print("✅ Basic integration test completed")
    print("✅ Workflow integration test completed")
    print("\n💡 To explore more features:")
    print("   - Check the examples directory")
    print("   - Run: python examples/ai_integration_example.py")
    print("   - Run: python examples/computer_control_example.py") 