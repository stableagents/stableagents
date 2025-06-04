#!/bin/bash
# Script to build and publish StableAgents to PyPI

echo "Building and publishing StableAgents v0.1.2"

# Ensure build tools are installed
pip install --upgrade pip build twine

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build the package
echo "Building package..."
python -m build

# Check the distribution
echo "Checking distribution..."
twine check dist/*

# Upload to PyPI
echo "Uploading to PyPI..."
twine upload dist/*

echo "Process completed!" 