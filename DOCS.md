# Introducing stableagents-ai

stableagents-ai is a Text2Agent SDK that allows you to create agents that can perform complex tasks using natural language.

## stableagents-ai vs other Agent Frameworks

stableagents-ai is different than other agent frameworks in that it is the only framework that is able to learn from past agentic experiences to improve future agentic experiences.

Here is a code snippet of a stableagents-ai in action:

```python
from stableagents import StableAgents

# Initialize the agent
agent = StableAgents()

# Create a simple agent
agent.create_agent(
    name="stableagents-ai",
    description="A helpful AI assistant",
    instructions="You are a helpful AI assistant that can help with various tasks."
)

# Use the agent
response = agent.generate_text("Hello, how can you help me today?")
print(response)
```

## Features

- **Text Generation**: Generate human-like text responses
- **Agent Creation**: Create and manage multiple agents
- **Memory Management**: Persistent memory for context retention
- **API Integration**: Easy integration with various AI providers
- **Extensible**: Plugin system for custom functionality

## Installation

```bash
pip install stableagents-ai
```

## Quick Start

```python
from stableagents import StableAgents

# Initialize
agent = StableAgents()

# Set up API key
agent.set_api_key('openai', 'your-api-key-here')

# Generate text
response = agent.generate_text("What is the capital of France?")
print(response)
```

## Documentation

For more detailed documentation, visit [stableagents.dev](https://stableagents.dev)

```python
from stableagents.agent import Agent
from stableagents.task import Task
from stableagents.tools import *
from stableagents.tools.web_search import WebSearch

# Define a web search tool
web_search = WebSearch()


# Define an agent
agent = Agent(
    name="Stable Agent",
    tools=[web_search],
    task=task
)
```




