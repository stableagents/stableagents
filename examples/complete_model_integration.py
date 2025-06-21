#!/usr/bin/env python3
"""
Complete StableAgents Model Integration Example

This example demonstrates a complete setup and usage of StableAgents with:
- Proper API key management
- Local model integration
- Self-healing system
- Memory management
- Computer control
- Health monitoring

This is a production-ready example that shows how all components work together.
"""

import sys
import os
import time
import json
import getpass
from pathlib import Path

# Add parent directory to path to import stableagents
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stableagents import StableAgents

def setup_agent():
    """Set up the StableAgents instance with all features."""
    print("🔧 Setting up StableAgents...")
    
    # Initialize with self-healing enabled
    agent = StableAgents(enable_self_healing=True)
    
    # Configure self-healing
    agent.self_healing.set_config({
        "auto_recovery": True,
        "min_severity_for_recovery": "medium",
        "monitoring_interval": 10.0
    })
    
    print("✅ Agent initialized with self-healing")
    return agent

def setup_api_keys(agent):
    """Set up API keys for different providers."""
    print("\n🔑 Setting up API Keys")
    print("=" * 30)
    
    # Check for existing API keys
    config_dir = os.path.join(os.path.expanduser("~"), ".stableagents")
    keys_file = os.path.join(config_dir, "api_keys.json")
    
    if os.path.exists(keys_file):
        print("📁 Found existing API keys configuration")
        with open(keys_file, 'r') as f:
            keys = json.load(f)
        
        for provider, key in keys.items():
            if provider != "active_provider" and key and key != "test123":
                print(f"   ✅ {provider.capitalize()}: Key configured")
            elif provider != "active_provider":
                print(f"   ⚠️  {provider.capitalize()}: No valid key")
    else:
        print("📁 No existing API keys found")
    
    # Prompt for API keys if needed
    providers = ["openai", "anthropic"]
    
    for provider in providers:
        current_key = agent.get_api_key(provider)
        if not current_key or current_key == "test123":
            print(f"\n🔑 {provider.capitalize()} API Key Setup")
            print(f"Enter your {provider.capitalize()} API key (or press Enter to skip):")
            api_key = getpass.getpass("> ")
            
            if api_key:
                success = agent.set_api_key(provider, api_key)
                if success:
                    print(f"   ✅ {provider.capitalize()} API key set successfully")
                else:
                    print(f"   ❌ Failed to set {provider.capitalize()} API key")
            else:
                print(f"   ⏭️  Skipped {provider.capitalize()} setup")

def test_ai_providers(agent):
    """Test AI providers with proper error handling."""
    print("\n🤖 Testing AI Providers")
    print("=" * 30)
    
    providers = ["openai", "anthropic"]
    results = {}
    
    for provider in providers:
        print(f"\n📡 Testing {provider.capitalize()}...")
        
        api_key = agent.get_api_key(provider)
        if not api_key or api_key == "test123":
            print(f"   ⚠️  No valid API key for {provider}")
            results[provider] = {"status": "no_key"}
            continue
        
        # Set as active provider
        if agent.set_active_ai_provider(provider):
            print(f"   ✅ {provider.capitalize()} activated")
            
            # Test text generation
            try:
                prompt = "Write a one-sentence summary of artificial intelligence."
                response = agent.generate_text(prompt, max_tokens=50)
                print(f"   📝 Text generation successful")
                print(f"   💬 Response: {response[:100]}...")
                
                # Test chat generation
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What is 2+2?"}
                ]
                chat_response = agent.generate_chat(messages)
                print(f"   💬 Chat response: {chat_response[:100]}...")
                
                results[provider] = {
                    "status": "success",
                    "text_response": response[:100],
                    "chat_response": chat_response[:100]
                }
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                results[provider] = {"status": "error", "error": str(e)}
        else:
            print(f"   ❌ Failed to activate {provider}")
            results[provider] = {"status": "activation_failed"}
    
    return results

def test_local_models(agent):
    """Set up and test local models."""
    print("\n🏠 Testing Local Models")
    print("=" * 30)
    
    # Check if llama-cpp-python is available
    try:
        import llama_cpp
        print("✅ llama-cpp-python is available")
    except ImportError:
        print("⚠️  llama-cpp-python not installed")
        print("   💡 Install with: pip install llama-cpp-python")
        print("   💡 Or install StableAgents with local extras:")
        print("      pip install stableagents-ai[local]")
        return {"status": "not_available"}
    
    # Set up models directory
    models_dir = os.path.join(os.path.expanduser("~"), ".stableagents", "models")
    os.makedirs(models_dir, exist_ok=True)
    print(f"📁 Models directory: {models_dir}")
    
    # Look for GGUF models
    gguf_files = []
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file.endswith('.gguf'):
                gguf_files.append(os.path.join(root, file))
    
    if not gguf_files:
        print("📁 No GGUF models found")
        print("   💡 To test local models, download a GGUF model file")
        print("   💡 Place it in ~/.stableagents/models/")
        print("   💡 Example models:")
        print("      - llama-2-7b-chat.gguf")
        print("      - mistral-7b-instruct-v0.1.Q4_K_M.gguf")
        print("      - codellama-7b-instruct.gguf")
        return {"status": "no_models"}
    
    print(f"📁 Found {len(gguf_files)} local model(s):")
    for model_path in gguf_files:
        print(f"   - {os.path.basename(model_path)}")
    
    # Test the first available model
    test_model = gguf_files[0]
    print(f"\n🧪 Testing local model: {os.path.basename(test_model)}")
    
    try:
        # Set up local model
        success = agent.set_local_model(test_model)
        if success:
            print("   ✅ Local model loaded successfully")
            
            # Test text generation
            prompt = "Explain quantum computing in one sentence."
            response = agent.generate_text(prompt, max_tokens=100)
            print(f"   📝 Local model response: {response[:150]}...")
            
            # Test chat generation
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is machine learning?"}
            ]
            chat_response = agent.generate_chat(messages)
            print(f"   💬 Local chat response: {chat_response[:150]}...")
            
            result = {
                "status": "success",
                "model_path": test_model,
                "text_response": response[:150],
                "chat_response": chat_response[:150]
            }
            
        else:
            print("   ❌ Failed to load local model")
            result = {"status": "failed", "model_path": test_model}
            
    except Exception as e:
        print(f"   ❌ Error testing local model: {str(e)}")
        result = {"status": "error", "error": str(e), "model_path": test_model}
    
    return result

def test_memory_system(agent):
    """Test the memory management system."""
    print("\n🧠 Testing Memory System")
    print("=" * 30)
    
    try:
        # Test short-term memory
        print("📝 Testing short-term memory...")
        agent.add_to_memory("short_term", "session_data", {
            "user_id": "demo_user",
            "session_start": time.time(),
            "preferences": {"theme": "dark", "language": "en"}
        })
        
        short_term = agent.get_from_memory("short_term", "session_data")
        print(f"   ✅ Short-term memory: {len(short_term)} entries")
        
        # Test long-term memory
        print("📝 Testing long-term memory...")
        agent.add_to_memory("long_term", "user_profile", {
            "user_id": "demo_user",
            "preferred_provider": "openai",
            "created_at": time.time(),
            "usage_stats": {"sessions": 1, "requests": 5}
        })
        
        long_term = agent.get_from_memory("long_term", "user_profile")
        print(f"   ✅ Long-term memory: {len(long_term)} entries")
        
        # Test context memory
        print("📝 Testing context memory...")
        agent.add_to_memory("context", "current_task", {
            "task_id": "demo_task_001",
            "task_type": "integration_test",
            "start_time": time.time(),
            "components_tested": ["ai_providers", "local_models", "memory"]
        })
        
        context = agent.get_from_memory("context", "current_task")
        print(f"   ✅ Context memory: {len(context)} entries")
        
        # Test memory health
        if agent.self_healing_enabled:
            memory_health = agent._check_memory_health()
            print(f"🏥 Memory health metrics: {len(memory_health)} metrics")
            
            for metric in memory_health:
                status = "✅" if metric.healthy else "❌"
                print(f"   {status} {metric.name}: {metric.value}")
        
        result = {
            "status": "success",
            "short_term_count": len(short_term),
            "long_term_count": len(long_term),
            "context_count": len(context)
        }
        
    except Exception as e:
        print(f"   ❌ Error testing memory: {str(e)}")
        result = {"status": "error", "error": str(e)}
    
    return result

def test_computer_control(agent):
    """Test computer control capabilities."""
    print("\n💻 Testing Computer Control")
    print("=" * 30)
    
    try:
        # Test basic operations
        print("🔍 Testing basic operations...")
        
        # Get current directory
        result = agent.control_computer("get_current_directory")
        print(f"   📁 Current directory: {result}")
        
        # Get system info
        result = agent.control_computer("get_system_info")
        print(f"   💻 System info: {result[:100]}...")
        
        # List files in current directory
        result = agent.control_computer("list_files .")
        files = result.split() if result else []
        print(f"   📋 Files in directory: {len(files)} items")
        
        # Test file operations
        print("📝 Testing file operations...")
        
        # Create a test file
        test_content = "# Generated by StableAgents\n# Integration test file\nprint('Hello, StableAgents!')"
        result = agent.control_computer(f"write_file test_integration.py {test_content}")
        print(f"   ✅ File created: test_integration.py")
        
        # Read the file back
        result = agent.control_computer("read_file test_integration.py")
        print(f"   📖 File content: {result[:50]}...")
        
        # Clean up
        result = agent.control_computer("delete_file test_integration.py")
        print(f"   🗑️  File cleaned up")
        
        result_data = {
            "status": "success",
            "current_directory": result,
            "files_count": len(files),
            "file_operations": "successful"
        }
        
    except Exception as e:
        print(f"   ❌ Error testing computer control: {str(e)}")
        result_data = {"status": "error", "error": str(e)}
    
    return result_data

def test_self_healing(agent):
    """Test the self-healing system."""
    print("\n🔄 Testing Self-Healing System")
    print("=" * 30)
    
    if not agent.self_healing_enabled:
        print("⚠️  Self-healing is not enabled")
        return {"status": "not_enabled"}
    
    try:
        # Get current health report
        health_report = agent.get_health_report()
        print("📊 Current Health Report:")
        print(f"   Status: {health_report.get('status', 'unknown')}")
        print(f"   Components: {len(health_report.get('components', {}))}")
        print(f"   Issues: {len(health_report.get('issues', []))}")
        
        # Test component registration
        print("\n🔧 Testing component registration...")
        
        def demo_health_check():
            """Demo health check function."""
            return [
                {
                    "name": "demo_metric",
                    "value": 42,
                    "timestamp": time.time(),
                    "healthy": True
                },
                {
                    "name": "demo_counter",
                    "value": 1,
                    "timestamp": time.time(),
                    "healthy": True
                }
            ]
        
        # Register demo component
        agent.self_healing.register_component(
            "demo_component",
            demo_health_check,
            thresholds={
                "demo_metric": {"min": 0, "max": 100, "severity": "low"},
                "demo_counter": {"min": 0, "max": 10, "severity": "medium"}
            }
        )
        print("   ✅ Demo component registered")
        
        # Get updated health report
        updated_health = agent.get_health_report()
        print(f"   📊 Updated components: {len(updated_health.get('components', {}))}")
        
        # Test self-healing status
        status = agent.self_healing.get_status()
        print(f"   🔄 Self-healing status: {status.get('is_active', False)}")
        
        result = {
            "status": "success",
            "health_status": health_report.get('status'),
            "components_count": len(updated_health.get('components', {})),
            "self_healing_active": status.get('is_active', False)
        }
        
    except Exception as e:
        print(f"   ❌ Error testing self-healing: {str(e)}")
        result = {"status": "error", "error": str(e)}
    
    return result

def test_integrated_workflow(agent):
    """Test how all components work together."""
    print("\n🔄 Testing Integrated Workflow")
    print("=" * 30)
    
    try:
        print("🎯 Running integrated workflow...")
        
        # Step 1: Use AI to generate content
        print("1️⃣  AI Generation...")
        if agent.get_active_ai_provider():
            try:
                # Generate a Python function
                prompt = "Write a Python function that calculates the factorial of a number with proper error handling."
                ai_response = agent.generate_text(prompt, max_tokens=200)
                print(f"   ✅ AI generated: {ai_response[:100]}...")
                
                # Step 2: Store in memory
                print("2️⃣  Memory Storage...")
                agent.add_to_memory("short_term", "generated_code", {
                    "prompt": prompt,
                    "response": ai_response,
                    "timestamp": time.time()
                })
                print("   ✅ Stored in memory")
                
                # Step 3: Create file with computer control
                print("3️⃣  Computer Control...")
                file_content = f"# Generated by StableAgents\n# Integration test - {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n{ai_response}\n"
                result = agent.control_computer(f"write_file integration_demo.py {file_content}")
                print(f"   ✅ File created: integration_demo.py")
                
                # Step 4: Update context
                print("4️⃣  Context Update...")
                agent.add_to_memory("context", "workflow_progress", {
                    "step": "file_created",
                    "filename": "integration_demo.py",
                    "timestamp": time.time(),
                    "components_used": ["ai_generation", "memory", "computer_control"]
                })
                print("   ✅ Context updated")
                
                # Step 5: Health check
                print("5️⃣  Health Check...")
                if agent.self_healing_enabled:
                    health = agent.get_health_report()
                    print(f"   ✅ Health status: {health.get('status', 'unknown')}")
                    print(f"   ✅ Components monitored: {len(health.get('components', {}))}")
                
                # Step 6: Clean up
                print("6️⃣  Cleanup...")
                result = agent.control_computer("delete_file integration_demo.py")
                print("   ✅ File cleaned up")
                
                print("\n✅ Integrated workflow completed successfully!")
                
                result_data = {
                    "status": "success",
                    "ai_generation": "successful",
                    "memory_storage": "successful",
                    "file_operations": "successful",
                    "health_check": "successful",
                    "cleanup": "successful"
                }
                
            except Exception as e:
                print(f"   ❌ Workflow error: {str(e)}")
                result_data = {"status": "error", "error": str(e)}
        else:
            print("   ⚠️  No AI provider available")
            result_data = {"status": "no_ai_provider"}
            
    except Exception as e:
        print(f"   ❌ Error in integrated workflow: {str(e)}")
        result_data = {"status": "error", "error": str(e)}
    
    return result_data

def main():
    """Main function to run the complete demo."""
    print("🚀 Complete StableAgents Model Integration Demo")
    print("=" * 60)
    print("This demo shows how all StableAgents components work together")
    print("in a production-ready environment.")
    print()
    
    # Setup agent
    agent = setup_agent()
    
    # Setup API keys
    setup_api_keys(agent)
    
    # Run all tests
    results = {}
    
    tests = [
        ("AI Providers", test_ai_providers),
        ("Local Models", test_local_models),
        ("Memory System", test_memory_system),
        ("Computer Control", test_computer_control),
        ("Self-Healing", test_self_healing),
        ("Integrated Workflow", test_integrated_workflow)
    ]
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func(agent)
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"❌ Error in {test_name} test: {str(e)}")
            results[test_name] = {"status": "error", "error": str(e)}
    
    # Print summary
    print("\n📊 Complete Demo Summary")
    print("=" * 40)
    
    total_tests = len(results)
    successful_tests = sum(1 for result in results.values() 
                         if result.get("status") == "success")
    
    print(f"Total tests run: {total_tests}")
    print(f"Successful tests: {successful_tests}")
    print(f"Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        status = result.get("status", "unknown")
        status_icon = "✅" if status == "success" else "⚠️" if status in ["not_available", "no_models", "no_ai_provider"] else "❌"
        print(f"  {status_icon} {test_name}: {status}")
        
        # Print additional details for successful tests
        if status == "success" and test_name == "AI Providers":
            providers = [p for p, r in result.items() if r.get("status") == "success"]
            if providers:
                print(f"     Working providers: {', '.join(providers)}")
        
        elif status == "success" and test_name == "Local Models":
            model_path = result.get("model_path", "")
            if model_path:
                print(f"     Model: {os.path.basename(model_path)}")
    
    print("\n🎉 Complete demo finished!")
    print("\n💡 Next Steps:")
    print("   1. Set up your API keys for full functionality")
    print("   2. Download GGUF models for local inference")
    print("   3. Explore the examples directory")
    print("   4. Check the documentation at https://docs.stableagents.dev")
    print("   5. Build your own AI agent applications!")
    
    return 0

if __name__ == "__main__":
    exit(main()) 