#!/bin/bash
# Script to properly build and publish the package to PyPI

# Ensure we have the latest build tools
pip install --upgrade pip build twine

# Clean up any old builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build

# Check the distribution
twine check dist/*

# Upload to PyPI (will prompt for username and password)
echo "Uploading to PyPI..."
twine upload dist/*

echo "Package published successfully!" 