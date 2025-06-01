# StableAgents AI

A framework for creating stable and reliable AI agents.

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
```

## Command Line Interface

StableAgents comes with a simple CLI:

```bash
# Run the CLI with a specific model and API key
stableagents --model openai --key your-api-key
```

Once in the CLI, you can:
- Chat with the AI directly by typing any text
- Use commands like `memory`, `control`, and `provider`
- Type `help` to see all available commands

## Features

- Multiple AI provider support (OpenAI, Anthropic, etc.)
- Memory management
- Computer control capabilities
- Simple but powerful CLI
- Logging system

## License

MIT