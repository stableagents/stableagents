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

# Computer control with natural language
stableagents control open calculator
stableagents control search for python documentation
stableagents control list .
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