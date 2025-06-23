# StableAgents Framework

A production-ready framework for building enterprise-grade AI agents - providing robust infrastructure and system-level capabilities that enable reliable, secure, and efficient AI agent operations at scale.

Official site: [stableagents.dev](https://stableagents.dev)

## Overview

StableAgents is designed to be the foundation for large-scale AI agent deployments with a focus on:

- **Reliability**: Built-in self-healing mechanisms ensure consistent operation even under adverse conditions
- **Scalability**: Architecture supports everything from single-agent deployments to complex multi-agent systems
- **Security**: Enterprise-grade authentication, access controls, and data protection mechanisms
- **Extensibility**: Modular design allows for customization and extension of core capabilities

## Key Features

- **Multi-Provider Support**: Seamlessly integrate with OpenAI, Anthropic, and other AI providers
- **Local Model Integration**: Run models offline with local inference capabilities
- **Self-Healing System**: Automatic issue detection, diagnosis, and recovery
- **Memory Management**: Efficient handling of context and persistent storage
- **Computer Control**: Safe system interaction capabilities
- **Comprehensive Logging**: Detailed activity tracking and monitoring

## Quick Installation

### Option 1: Install from GitHub (Recommended)
```bash
pip install git+https://github.com/jordanplows/stableagents.git
```

### Option 2: Install with Local Models Support
```bash
pip install git+https://github.com/jordanplows/stableagents.git[local]
```

### Option 3: Development Installation
```bash
git clone https://github.com/jordanplows/stableagents.git
cd stableagents
pip install -e .
```

## Quick Start

After installation, start StableAgents:

```bash
stableagents-ai --start
```

The CLI will guide you through:
1. **API Key Setup**: Choose between managed keys ($20) or bring your own
2. **Provider Selection**: Configure OpenAI, Anthropic, Google, or local models
3. **Security Setup**: Set up encrypted storage for your credentials

## Basic Usage

### Python API

```python
from stableagents import StableAgents

# Initialize the agent
agent = StableAgents()

# Generate text
response = agent.generate_text("Hello, how can you help me today?")
print(response)
```

### Command Line Interface

```bash
# Start interactive mode
stableagents-ai

# Run with specific model
stableagents-ai --model openai --api-key your-key

# Use local models
stableagents-ai --local --model-path ~/models/llama-2-7b.gguf
```

## Access

StableAgents is a private framework available to authorized partners and enterprise customers. For access inquiries:

- Visit: [stableagents.dev](https://stableagents.dev)
- Contact: support@stableagents.dev

## Documentation

Comprehensive documentation is available to authorized users at [docs.stableagents.dev](https://docs.stableagents.dev)

## Implementation Examples

### Basic Agent Setup

```python
from stableagents import StableAgents

# Initialize with enterprise configuration
agent = StableAgents(
    enable_self_healing=True,
    enable_logging=True
)

# Configure AI provider
agent.set_api_key('openai', 'your-api-key')
agent.set_active_ai_provider('openai')

# Generate text with the agent
response = agent.generate_text("Analyze the performance of our product in Q1")
```

### Custom Health Check Integration

```python
# Register custom component for monitoring
agent.self_healing.register_component(
    "database",
    check_database_health,
    thresholds={
        "connection_status": {"min": True, "severity": "high"}
    }
)
```

## Use Cases

- **Customer Service**: Deploy conversational agents that can understand, respond, and solve customer issues
- **Enterprise Assistants**: Create specialized assistants for internal business processes
- **Data Analysis**: Build agents that can process, analyze, and report on complex business data
- **Content Generation**: Develop agents for content creation, curation, and management
- **Research Automation**: Automate literature reviews, data collection, and preliminary analysis

## License

Proprietary software licensed exclusively to authorized partners and customers.

© 2023-2025 StableAgents. All rights reserved.