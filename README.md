# StableAgents Framework

A production-ready framework for building enterprise-grade AI agents - providing robust infrastructure and system-level capabilities that enable reliable, secure, and efficient AI agent operations at scale.

## Overview

StableAgents is designed to be the foundation for large-scale AI agent deployments with a focus on:

- **Reliability**: Built-in self-healing mechanisms ensure consistent operation even under adverse conditions
- **Scalability**: Architecture supports everything from single-agent deployments to complex multi-agent systems
- **Security**: Implement proper authentication, access controls, and data protection mechanisms
- **Extensibility**: Modular design allows for customization and extension of core capabilities

## Key Features

- **Multi-Provider Support**: Seamlessly integrate with OpenAI, Anthropic, and other AI providers
- **Local Model Integration**: Run models offline with local inference capabilities
- **Self-Healing System**: Automatic issue detection, diagnosis, and recovery
- **Memory Management**: Efficient handling of context and persistent storage
- **Computer Control**: Safe system interaction capabilities
- **Comprehensive Logging**: Detailed activity tracking and monitoring

## Installation

For development:

```bash
git clone https://github.com/yourusername/stableagents.git
cd stableagents
pip install -e .
```

With additional features:

```bash
# For local model support
pip install -e ".[local]"

# For all features
pip install -e ".[all]"
```

## Quick Start

```python
from stableagents import StableAgents

# Initialize with your preferred configuration
agent = StableAgents(
    enable_self_healing=True,
    enable_logging=True
)

# Configure AI provider
agent.set_api_key('openai', 'your-api-key')
agent.set_active_ai_provider('openai')

# Generate text with the agent
response = agent.generate_text("Analyze the performance of our product in Q1")
print(response)
```

## Development

### Project Structure

```
stableagents/
├── core/           # Core system components
├── logic/          # Business logic implementation
├── memory/         # Memory and state management
├── utils/          # Utility functions and helpers
├── __init__.py     # Package initialization
├── ai_providers.py # AI provider integrations
├── cli.py          # Command-line interface
├── computer.py     # System interaction capabilities
└── main.py         # Main application entry point
```

### Testing

Run the test suite:

```bash
pytest
```

## Extending the Framework

StableAgents is designed to be extended for specific use cases:

### Custom AI Providers

```python
from stableagents.ai_providers import BaseAIProvider

class CustomProvider(BaseAIProvider):
    def __init__(self, api_key):
        super().__init__(api_key)
        # Custom initialization
        
    def generate_text(self, prompt, **kwargs):
        # Custom implementation
        pass
```

### Custom Health Checks

```python
def check_database_health():
    from stableagents.core.self_healing.monitor import HealthMetric
    metrics = []
    metrics.append(HealthMetric(
        name="connection_status",
        value=is_connected(),
        timestamp=time.time(),
        healthy=is_connected()
    ))
    return metrics

agent.self_healing.register_component(
    "database",
    check_database_health,
    thresholds={
        "connection_status": {"min": True, "severity": "high"}
    }
)
```

## License

MIT