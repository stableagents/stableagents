#!/bin/bash

# StableAgents AI Installation Script
# This script installs StableAgents AI globally on your system

set -e

echo "🚀 Installing StableAgents AI..."
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION is installed, but Python $REQUIRED_VERSION or higher is required."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 detected"

# Install StableAgents AI
echo "📦 Installing StableAgents AI from GitHub..."
pip3 install git+https://github.com/jordanplows/stableagents.git

# Verify installation
if command -v stableagents-ai &> /dev/null; then
    echo "✅ StableAgents AI installed successfully!"
    echo ""
    echo "🎉 Installation complete!"
    echo ""
    echo "To get started:"
    echo "  stableagents-ai --start"
    echo ""
    echo "For help:"
    echo "  stableagents-ai --help"
    echo ""
    echo "Documentation: https://github.com/jordanplows/stableagents"
else
    echo "❌ Installation failed. Please try installing manually:"
    echo "  pip3 install git+https://github.com/jordanplows/stableagents.git"
    exit 1
fi 