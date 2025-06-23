# StableAgents AI Installation Guide

## Quick Install

### Option 1: Install from PyPI (Recommended)
```bash
pip install stableagents-ai
```

### Option 2: Install from GitHub
```bash
pip install git+https://github.com/jordanplows/stableagents.git
```

### Option 3: Install with Local Models Support
```bash
pip install stableagents-ai[local]
```

## System Requirements

- Python 3.8 or higher
- macOS, Linux, or Windows
- Internet connection (for AI providers)
- 4GB+ RAM (8GB+ recommended for local models)

## Installation Methods

### Method 1: Global Installation (Recommended)

Install StableAgents AI globally on your system:

```bash
# Install globally
pip install stableagents-ai

# Verify installation
stableagents-ai --version
```

### Method 2: Virtual Environment Installation

For isolated development or to avoid dependency conflicts:

```bash
# Create virtual environment
python3 -m venv stableagents-env

# Activate virtual environment
# On macOS/Linux:
source stableagents-env/bin/activate
# On Windows:
stableagents-env\Scripts\activate

# Install StableAgents AI
pip install stableagents-ai

# Verify installation
stableagents-ai --version
```

### Method 3: Development Installation

For developers who want to modify the source code:

```bash
# Clone the repository
git clone https://github.com/jordanplows/stableagents.git
cd stableagents

# Install in development mode
pip install -e .

# Verify installation
stableagents-ai --version
```

## Post-Installation Setup

After installation, you'll need to set up API keys or configure local models:

### 1. Start StableAgents AI
```bash
stableagents-ai --start
```

### 2. Choose Your Setup Option
- **Option 1**: Pay $20 for managed API keys (recommended for beginners)
- **Option 2**: Bring your own API keys (OpenAI, Anthropic, Google)
- **Option 3**: Use local models only (no API keys required)

### 3. Follow the Setup Wizard
The CLI will guide you through the secure setup process.

## Troubleshooting

### Common Issues

**1. "Module not found" error**
```bash
# Solution: Reinstall the package
pip uninstall stableagents-ai
pip install stableagents-ai
```

**2. Dependency conflicts**
```bash
# Solution: Use a virtual environment
python3 -m venv stableagents-env
source stableagents-env/bin/activate
pip install stableagents-ai
```

**3. Permission errors on macOS/Linux**
```bash
# Solution: Use user installation
pip install --user stableagents-ai
```

**4. Python version issues**
```bash
# Check your Python version
python3 --version

# Should be 3.8 or higher
```

### Getting Help

- Check the [README.md](README.md) for basic usage
- Review [MODEL_INTEGRATION.md](MODEL_INTEGRATION.md) for AI provider setup
- Open an issue on GitHub for bugs or feature requests

## Uninstalling

To remove StableAgents AI:

```bash
pip uninstall stableagents-ai
```

This will remove the package but keep your configuration files in `~/.stableagents/`.

To completely remove everything:

```bash
pip uninstall stableagents-ai
rm -rf ~/.stableagents/
```

## Next Steps

After installation, check out:
- [Quick Start Guide](README.md#quick-start)
- [Model Integration Guide](MODEL_INTEGRATION.md)
- [Examples](examples/)
- [API Documentation](DOCS.md) 