# StableAgents

A framework for building stable AI agents.

## Installation

### From PyPI

```bash
pip install stableagents
```

### From Source with Poetry

```bash
# Clone the repository
git clone https://github.com/yourusername/stableagents.git
cd stableagents

# Install with Poetry
poetry install
```

## Usage

### As a Command-Line Tool

```bash
# Interactive mode
stableagents interactive

# Memory operations
stableagents memory add short_term test_key "test value"
stableagents memory get short_term test_key
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