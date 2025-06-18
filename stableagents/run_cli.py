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
    
    # If no arguments or 'start' command or --start flag, run in interactive mode
    if not args or args[0] == 'start' or args[0] == '--start':
        cli = UnifiedCLI()
        cli.start()
        return
    
    model = None
    api_key = None
    use_local = False
    model_path = None
    enable_self_healing = False
    auto_recovery = False
    show_banner = True
    
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
        elif args[i] == "--model-path" and i + 1 < len(args):
            model_path = args[i + 1]
            i += 2
        elif args[i] == "--self-healing":
            enable_self_healing = True
            i += 1
        elif args[i] == "--auto-recovery":
            enable_self_healing = True
            auto_recovery = True
            i += 1
        elif args[i] == "--no-banner":
            show_banner = False
            i += 1
        else:
            # Skip unknown argument
            i += 1
    
    # Start the CLI with specified options
    cli = UnifiedCLI()
    cli.start(model, api_key, use_local, model_path, enable_self_healing, auto_recovery, show_banner)

if __name__ == "__main__":
    main() 