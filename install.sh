#!/bin/bash
# Installation script for StableAgents

echo "Installing StableAgents..."

# Install the package globally with pip
pip install --user -e .

# Make sure the user's bin directory is in PATH
USER_BIN="$HOME/.local/bin"
if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
    echo "Adding $USER_BIN to your PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    export PATH="$HOME/.local/bin:$PATH"
fi

# Check if command is working
if command -v stableagents-ai &> /dev/null; then
    echo "Installation successful! You can now run 'stableagents-ai' from anywhere."
else
    echo "Command not found in PATH. Please make sure $USER_BIN is in your PATH."
    echo "You can add it by running: export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo "Installation complete!" 