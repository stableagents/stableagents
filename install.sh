#!/bin/bash

# Colors for better user experience
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== StableAgents Installation ===${NC}"
echo "This script will install StableAgents globally on your system."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed. Please install pip3 first.${NC}"
    exit 1
fi

# Get the current directory
CURRENT_DIR=$(pwd)

echo -e "\n${BLUE}Installing StableAgents...${NC}"

# First, uninstall any existing installation
echo "Removing any existing installation..."
pip3 uninstall -y stableagents-ai

# Install the package globally with pip
echo "Installing StableAgents..."
pip3 install --user -e .

# Get the user's bin directory
USER_BIN="$HOME/.local/bin"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
    echo -e "\n${BLUE}Adding $USER_BIN to your PATH...${NC}"
    
    # Add to .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        echo "Added to .bashrc"
    fi
    
    # Add to .zshrc if it exists
    if [ -f "$HOME/.zshrc" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
        echo "Added to .zshrc"
    fi
    
    # Add to current session
    export PATH="$USER_BIN:$PATH"
fi

# Verify installation
if command -v stableagents-ai &> /dev/null; then
    echo -e "\n${GREEN}Installation successful!${NC}"
    echo -e "You can now run StableAgents from anywhere using: ${BLUE}stableagents-ai${NC}"
    echo -e "Try it with: ${BLUE}stableagents-ai start${NC}"
else
    echo -e "\n${RED}Installation completed, but the command is not in your PATH.${NC}"
    echo "Please run this command to add it to your current session:"
    echo -e "${BLUE}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
    echo "Then try running: stableagents-ai start"
fi

# Verify Python can find the module
echo -e "\n${BLUE}Verifying Python module installation...${NC}"
if python3 -c "import stableagents" 2>/dev/null; then
    echo -e "${GREEN}Python module verification successful!${NC}"
else
    echo -e "${RED}Python module verification failed.${NC}"
    echo "Please try running:"
    echo -e "${BLUE}pip3 install --user -e .${NC}"
    echo "Then restart your terminal and try again."
fi

echo -e "\n${GREEN}Installation complete!${NC}" 