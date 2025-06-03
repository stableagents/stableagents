# StableAgents AI

A framework for building the Linux kernel of AI agents - providing the core infrastructure and system-level capabilities that enable reliable, secure, and efficient AI agent operations.

## Installation

```bash
pip install stableagents-ai
```

Or with Poetry:

```bash
poetry add stableagents-ai
```

## Quick Start

```python
# Using the Python API
from stableagents import StableAgents

agent = StableAgents()
agent.set_api_key('openai', 'your-api-key')
agent.set_active_ai_provider('openai')

response = agent.generate_text("Tell me about AI agents")
print(response)

# Using with a local model
agent = StableAgents()
agent.set_local_model()  # Uses default model location
response = agent.generate_text("Tell me about AI agents")
print(response)
```

## Command Line Interface

StableAgents comes with a simple CLI that you can run from anywhere:

```bash
# Run the CLI directly with any of these commands
stableagents
stableagents-ai
run-stableagents

# Run with a specific model and API key
stableagents --model openai --key your-api-key

# Run with a local model
stableagents --local
```

Once in the CLI, you can:
- Chat with the AI directly by typing any text
- Use commands like `memory`, `control`, and `provider`
- Type `help` to see all available commands

## Features

- Multiple AI provider support (OpenAI, Anthropic, etc.)
- Local model support for offline usage
- Memory management
- Computer control capabilities
- Simple but powerful CLI
- Logging system

## License

MIT