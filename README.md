# StableAgents

A framework for building stable AI agents.

## Installation

### Option 1: Install as a package

```bash
# Install in development mode
pip install -e .
```

After installation, you can use the CLI from anywhere:

```bash
stableagents interactive
```

### Option 2: Run directly

```bash
# Make sure script is executable
chmod +x cli.py

# Run the script
./cli.py interactive
```

## CLI Usage

The CLI provides several ways to interact with StableAgents:

### Interactive Mode

```bash
stableagents interactive
```

This starts an interactive session where you can type commands:

- `memory.add TYPE KEY VALUE` - Add to memory (TYPE: short_term, long_term, context)
- `memory.get TYPE [KEY]` - Get from memory
- `reset` - Reset the agent
- `help` - Show available commands
- `exit` or `quit` - Exit the program

### Memory Operations

```bash
# Add to memory
stableagents memory add short_term test_key "test value"

# Get from memory
stableagents memory get short_term test_key

# Get all items from a memory type
stableagents memory get short_term
```

### Verbose Mode

Add `-v` or `--verbose` to enable verbose logging:

```bash
stableagents -v interactive
``` 