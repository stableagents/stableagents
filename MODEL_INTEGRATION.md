# StableAgents Model Integration Guide

This guide explains how to integrate different AI models with StableAgents and how all components work together to create a comprehensive AI agent system.

## Overview

StableAgents provides a unified framework for integrating various AI models and capabilities:

- **AI Providers**: OpenAI, Anthropic, Google, and custom providers
- **Local Models**: Llama, Mistral, and other GGUF-compatible models
- **Self-Healing System**: Automatic monitoring, diagnosis, and recovery
- **Memory Management**: Short-term, long-term, and context memory
- **Computer Control**: Safe system interaction capabilities
- **Health Monitoring**: Real-time system health tracking

## Quick Start

### 1. Basic Setup

```python
from stableagents import StableAgents

# Initialize with self-healing enabled
agent = StableAgents(enable_self_healing=True)

# Set up AI provider
agent.set_api_key('openai', 'your-api-key')
agent.set_active_ai_provider('openai')

# Generate text
response = agent.generate_text("Hello, world!")
print(response)
```

### 2. Run Integration Test

```bash
# Test basic integration
python examples/simple_integration_test.py

# Test AI integration
python examples/ai_integration_example.py

# Test computer control
python examples/computer_control_example.py
```

## AI Provider Integration

### OpenAI Integration

```python
# Set up OpenAI
agent.set_api_key('openai', 'your-openai-api-key')
agent.set_active_ai_provider('openai')

# Generate text
response = agent.generate_text(
    "Explain quantum computing",
    max_tokens=200,
    temperature=0.7
)

# Chat conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is machine learning?"}
]
response = agent.generate_chat(messages)
```

### Anthropic Integration

```python
# Set up Anthropic
agent.set_api_key('anthropic', 'your-anthropic-api-key')
agent.set_active_ai_provider('anthropic')

# Generate text
response = agent.generate_text(
    "Write a poem about AI",
    max_tokens=150
)
```

### Google Integration

```python
# Set up Google
agent.set_api_key('google', 'your-google-api-key')
agent.set_active_ai_provider('google')

# Generate text
response = agent.generate_text("Explain neural networks")
```

## Local Model Integration

### Prerequisites

Install local model support:

```bash
# Install with local extras
pip install stableagents-ai[local]

# Or install manually
pip install llama-cpp-python
```

### Using Local Models

```python
# Set up local model
agent.set_local_model("/path/to/your/model.gguf")

# Generate text
response = agent.generate_text("Hello from local model!")

# Chat conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"}
]
response = agent.generate_chat(messages)
```

### Supported Local Models

- **Llama 2**: `llama-2-7b-chat.gguf`
- **Mistral**: `mistral-7b-instruct-v0.1.Q4_K_M.gguf`
- **Code Llama**: `codellama-7b-instruct.gguf`
- **Any GGUF format model**

### Model Management

```python
# Check available models
models_dir = os.path.join(os.path.expanduser("~"), ".stableagents", "models")
print(f"Models directory: {models_dir}")

# List available models
import os
for file in os.listdir(models_dir):
    if file.endswith('.gguf'):
        print(f"Found model: {file}")
```

## Self-Healing System

### Basic Self-Healing

```python
# Initialize with self-healing
agent = StableAgents(enable_self_healing=True)

# Enable automatic recovery
agent.self_healing.set_config({
    "auto_recovery": True,
    "min_severity_for_recovery": "medium",
    "monitoring_interval": 10.0
})

# Get health report
health = agent.get_health_report()
print(health)
```

### Custom Health Checks

```python
def custom_health_check():
    """Custom health check function."""
    return [
        {
            "name": "custom_metric",
            "value": 42,
            "timestamp": time.time(),
            "healthy": True
        }
    ]

# Register custom component
agent.self_healing.register_component(
    "my_component",
    custom_health_check,
    thresholds={
        "custom_metric": {"min": 0, "max": 100, "severity": "low"}
    }
)
```

### Recovery Actions

The self-healing system includes built-in recovery actions:

- **Log Diagnostics**: Log detailed issue information
- **Garbage Collection**: Free memory
- **Retry API Calls**: Retry failed API requests
- **Reset API Provider**: Reset provider connections
- **Reload Model**: Reload local models
- **Switch to Fallback**: Use alternative models/providers
- **Restart Component**: Restart affected components

## Memory Management

### Memory Types

```python
# Short-term memory (session-based)
agent.add_to_memory("short_term", "user_input", "Hello, how are you?")
short_term = agent.get_from_memory("short_term", "user_input")

# Long-term memory (persistent)
agent.add_to_memory("long_term", "user_preferences", {
    "preferred_provider": "openai",
    "language": "en"
})
preferences = agent.get_from_memory("long_term", "user_preferences")

# Context memory (task-specific)
agent.add_to_memory("context", "current_task", {
    "task": "code_generation",
    "language": "python"
})
context = agent.get_from_memory("context", "current_task")
```

### Memory Health Monitoring

```python
# Check memory health
memory_health = agent._check_memory_health()
for metric in memory_health:
    print(f"{metric.name}: {metric.value} (healthy: {metric.healthy})")
```

## Computer Control

### Safe Operations

```python
# Get system information
result = agent.control_computer("get_system_info")
print(result)

# Get current directory
result = agent.control_computer("get_current_directory")
print(result)

# List files
result = agent.control_computer("list_files .")
print(result)

# Read file
result = agent.control_computer("read_file example.txt")
print(result)

# Write file
result = agent.control_computer("write_file test.txt Hello, world!")
print(result)
```

### Advanced Operations

```python
# Execute command (with safety checks)
result = agent.control_computer("execute ls -la")
print(result)

# Get process information
result = agent.control_computer("get_process_info")
print(result)
```

## Integrated Workflows

### AI + Memory + Computer Control

```python
# Step 1: Generate code with AI
code_prompt = "Write a Python function to calculate fibonacci numbers"
ai_response = agent.generate_text(code_prompt, max_tokens=200)

# Step 2: Store in memory
agent.add_to_memory("short_term", "generated_code", ai_response)

# Step 3: Create file with computer control
file_content = f"# Generated by StableAgents\n\n{ai_response}\n"
result = agent.control_computer(f"write_file fibonacci.py {file_content}")

# Step 4: Track progress in memory
agent.add_to_memory("context", "workflow_progress", {
    "step": "file_created",
    "filename": "fibonacci.py",
    "timestamp": time.time()
})

# Step 5: Health check
if agent.self_healing_enabled:
    health = agent.get_health_report()
    print(f"System health: {len(health.get('components', {}))} components")
```

### Multi-Provider Fallback

```python
# Try primary provider
try:
    agent.set_active_ai_provider('openai')
    response = agent.generate_text("Hello")
except Exception as e:
    print(f"OpenAI failed: {e}")
    
    # Fallback to local model
    try:
        agent.set_local_model()
        response = agent.generate_text("Hello")
        print("Using local model as fallback")
    except Exception as e2:
        print(f"Local model also failed: {e2}")
        
        # Fallback to another provider
        try:
            agent.set_active_ai_provider('anthropic')
            response = agent.generate_text("Hello")
            print("Using Anthropic as fallback")
        except Exception as e3:
            print(f"All providers failed: {e3}")
```

## Configuration Management

### API Key Management

```python
# Set multiple API keys
agent.set_api_key('openai', 'your-openai-key')
agent.set_api_key('anthropic', 'your-anthropic-key')
agent.set_api_key('google', 'your-google-key')

# List available providers
providers = agent.list_ai_providers()
for provider in providers:
    print(f"{provider['name']}: {'✅' if provider['has_key'] else '❌'}")

# Switch between providers
agent.set_active_ai_provider('openai')
# ... use OpenAI
agent.set_active_ai_provider('anthropic')
# ... use Anthropic
```

### Configuration Files

API keys are stored in `~/.stableagents/api_keys.json`:

```json
{
    "openai": "your-openai-api-key",
    "anthropic": "your-anthropic-api-key",
    "google": "your-google-api-key",
    "active_provider": "openai"
}
```

## Error Handling and Recovery

### Automatic Recovery

```python
# Enable automatic recovery
agent = StableAgents(enable_self_healing=True)
agent.self_healing.set_config({
    "auto_recovery": True,
    "min_severity_for_recovery": "medium"
})

# The system will automatically:
# 1. Monitor for issues
# 2. Diagnose problems
# 3. Apply recovery actions
# 4. Verify recovery success
```

### Manual Recovery

```python
# Get current issues
health_report = agent.get_health_report()
issues = health_report.get('issues', [])

for issue in issues:
    print(f"Issue: {issue.component} - {issue.description}")
    
    # Manual recovery
    recovery_plan = agent.self_healing.handle_issue(issue, auto_recover=False)
    if recovery_plan:
        print(f"Recovery plan: {recovery_plan.actions}")
```

## Performance Optimization

### Model Loading

```python
# Load local model once and reuse
agent.set_local_model("/path/to/model.gguf")

# The model stays loaded in memory
response1 = agent.generate_text("First request")
response2 = agent.generate_text("Second request")
```

### Memory Management

```python
# Monitor memory usage
memory_health = agent._check_memory_health()
for metric in memory_health:
    if metric.name == "memory_usage_mb":
        print(f"Memory usage: {metric.value} MB")

# Clear short-term memory if needed
agent.memory["short_term"] = []
```

### Health Monitoring

```python
# Regular health checks
import time

while True:
    health = agent.get_health_report()
    print(f"Health status: {health['status']}")
    
    if health['status'] != 'healthy':
        print("Issues detected, attempting recovery...")
        # Recovery happens automatically if enabled
    
    time.sleep(60)  # Check every minute
```

## Best Practices

### 1. Provider Selection

```python
# Use the most appropriate provider for each task
def get_best_provider(task_type):
    if task_type == "coding":
        return "openai"  # Good for code generation
    elif task_type == "creative":
        return "anthropic"  # Good for creative writing
    elif task_type == "local":
        return "local"  # Privacy-sensitive tasks
    else:
        return "openai"  # Default

# Switch providers based on task
agent.set_active_ai_provider(get_best_provider("coding"))
```

### 2. Error Handling

```python
def safe_generate_text(agent, prompt, max_retries=3):
    """Safely generate text with retry logic."""
    for attempt in range(max_retries):
        try:
            return agent.generate_text(prompt)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e
```

### 3. Memory Efficiency

```python
# Use appropriate memory types
def store_user_data(agent, user_id, data):
    # Short-term: session data
    agent.add_to_memory("short_term", f"session_{user_id}", data)
    
    # Long-term: persistent preferences
    if "preferences" in data:
        agent.add_to_memory("long_term", f"preferences_{user_id}", data["preferences"])
    
    # Context: current task
    agent.add_to_memory("context", f"task_{user_id}", {"current_task": data.get("task")})
```

### 4. Health Monitoring

```python
# Set up comprehensive monitoring
def setup_monitoring(agent):
    # Register custom health checks
    agent.self_healing.register_component(
        "api_latency",
        lambda: [{"name": "latency", "value": measure_latency(), "healthy": True}],
        thresholds={"latency": {"max": 5.0, "severity": "high"}}
    )
    
    # Enable automatic recovery
    agent.self_healing.set_config({
        "auto_recovery": True,
        "monitoring_interval": 30.0
    })
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   ```python
   # Check if API key is set
   api_key = agent.get_api_key('openai')
   if not api_key:
       print("API key not found")
   ```

2. **Local Model Issues**
   ```python
   # Check if llama-cpp-python is installed
   try:
       import llama_cpp
       print("llama-cpp-python is available")
   except ImportError:
       print("Install with: pip install llama-cpp-python")
   ```

3. **Memory Issues**
   ```python
   # Check memory usage
   memory_health = agent._check_memory_health()
   for metric in memory_health:
       if not metric.healthy:
           print(f"Memory issue: {metric.name}")
   ```

4. **Self-Healing Issues**
   ```python
   # Check self-healing status
   if not agent.self_healing_enabled:
       print("Self-healing not enabled")
   else:
       status = agent.self_healing.get_status()
       print(f"Self-healing status: {status}")
   ```

### Getting Help

- Check the examples directory for working code
- Run integration tests to verify setup
- Check health reports for system status
- Review logs for detailed error information

## Next Steps

1. **Run the integration test**: `python examples/simple_integration_test.py`
2. **Explore AI integration**: `python examples/ai_integration_example.py`
3. **Test computer control**: `python examples/computer_control_example.py`
4. **Set up local models**: Download GGUF models and test local inference
5. **Configure self-healing**: Enable automatic monitoring and recovery
6. **Build custom workflows**: Combine all components for your specific use case

For more advanced usage, check the API documentation and explore the source code in the `stableagents/` directory. 