#!/bin/bash
# Installation script for StableAgents

echo "Installing StableAgents..."

# Install the package with pip
pip install -e .

# Make the command executable and available
chmod +x run-stableagents

# Check if command is working
if command -v run-stableagents &> /dev/null; then
    echo "Installation successful! You can now run 'run-stableagents' from anywhere."
else
    echo "Command not found in PATH. Adding a symbolic link to /usr/local/bin/"
    
    # Create symbolic link in a directory that's likely in PATH
    if [ -d "/usr/local/bin" ]; then
        sudo ln -sf "$(pwd)/run-stableagents" /usr/local/bin/run-stableagents
        echo "Symbolic link created. You can now run 'run-stableagents' from anywhere."
    else
        echo "Could not find /usr/local/bin. Please ensure the installation directory is in your PATH."
    fi
fi

echo "Installation complete!" 