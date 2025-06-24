#!/usr/bin/env python3
"""
Entry point script for StableAgents CLI.
Handles API keys properly by passing them directly to the CLI class.
"""
import sys
import os

# Import the main CLI function from cli.py
from stableagents.cli import main

if __name__ == "__main__":
    sys.exit(main()) 