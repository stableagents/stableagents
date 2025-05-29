# <div align="center">StableAgents</div>

The Linux kernel of AI agents - a foundational framework that provides the core infrastructure, stability, and extensibility needed to build production-grade AI agents. Just as Linux powers everything from smartphones to supercomputers, StableAgents serves as the bedrock for creating reliable, secure, and scalable AI agents that can be deployed across any environment. With its modular architecture, robust memory management, and comprehensive tooling, it enables developers to build agents that are as stable and trustworthy as traditional software systems.
## Installation

### From PyPI

```bash
# Basic installation
pip install stableagents

# With OpenAI support
pip install stableagents[openai]

# With Anthropic support
pip install stableagents[anthropic]

# With all AI providers
pip install stableagents[all]
```

### From Source with Poetry

```bash
# Clone the repository
git clone https://github.com/yourusername/stableagents.git
cd stableagents

# Install with Poetry
poetry install  # Basic installation
poetry install --extras "openai"  # With OpenAI support
poetry install --extras "all"  # With all AI providers
```

## Usage

### As a Command-Line Tool

```bash
# Interactive mode
stableagents interactive

# Memory operations
stableagents memory add short_term test_key "test value"
stableagents memory get short_term test_key

# Computer control with natural language
stableagents control open calculator
stableagents control search for python documentation
stableagents control list .

# AI text generation (requires API key)
stableagents apikey set openai your_api_key
stableagents ai "Write a short poem about AI"

# Chat with AI (requires API key)
stableagents chat "What are the benefits of using Python for AI development?"
```

### As a Python Library

```python
from stableagents import StableAgents

# Create an agent
agent = StableAgents()

# Add to memory
agent.add_to_memory("short_term", "key", "value")

# Get from memory
value = agent.get_from_memory("short_term", "key")

# Control your computer with natural language
result = agent.control_computer("open calculator")
print(result)

# Use AI with your API key
agent.set_api_key("openai", "your_api_key")

# Generate text
response = agent.generate_text("Write a short poem about AI")
print(response)

# Chat with AI
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is machine learning?"}
]
response = agent.generate_chat(messages)
print(response)
```

## Computer Control Features

StableAgents includes functionality to control your computer using natural language commands:

- **File operations**: create, list, find, move, copy, delete files and folders
- **Web browsing**: open websites, search the web
- **Application control**: open applications
- **Command execution**: run shell commands

Example commands:

```
open calculator
browse github.com
search for python documentation
create file example.txt
list .
find *.py in .
move example.txt to backup/example.txt
copy file.txt to file_copy.txt
delete example.txt
execute echo "Hello World"
```

## AI Integration

StableAgents supports multiple AI providers:

- **OpenAI**: For text generation, chat, embeddings, and audio transcription
- **Anthropic**: For text generation and chat
- **Google**: Coming soon
- **Custom providers**: Support for custom provider integration

### Setting up API Keys

API keys can be set in several ways:

1. Via the CLI:
   ```bash
   stableagents apikey set openai your_api_key
   ```

2. Via the Python API:
   ```python
   agent = StableAgents()
   agent.set_api_key("openai", "your_api_key")
   ```

3. When prompted during the first use of an AI feature

API keys are stored securely in the `~/.stableagents/api_keys.json` file.

### AI Commands

```bash
# List available providers and their status
stableagents providers

# Set the active provider
stableagents provider openai

# Generate text
stableagents ai "Write a short story about a robot"

# Chat with AI
stableagents chat "Tell me about the history of AI"
```

## Development

```bash
# Install dev dependencies
poetry install

# Run tests
poetry run pytest
```

## Publishing to PyPI

```bash
# Build the package
poetry build

# Publish to PyPI
poetry publish
```