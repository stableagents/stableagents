#!/usr/bin/env python3
"""
Entry point script for StableAgents CLI.
Handles API keys properly by passing them directly to the UnifiedCLI class.
"""
import sys
import os
from stableagents.unified_cli import UnifiedCLI

def main():
    # Check for arguments
    args = sys.argv[1:]
    
    model = None
    api_key = None
    use_local = False
    
    # Parse arguments manually to handle special characters in API keys
    i = 0
    while i < len(args):
        if args[i] == "--model" and i + 1 < len(args):
            model = args[i + 1]
            i += 2
        elif args[i] == "--key" and i + 1 < len(args):
            api_key = args[i + 1]
            i += 2
        elif args[i] == "--local":
            use_local = True
            i += 1
        else:
            # Skip unknown argument
            i += 1
    
    # Start the CLI
    cli = UnifiedCLI()
    cli.start(model, api_key, use_local)

if __name__ == "__main__":
    main() 