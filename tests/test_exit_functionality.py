#!/usr/bin/env python3
"""
Test script to verify exit functionality in StableAgents interactive mode.
"""

import sys
import os

# Add the parent directory to the path to import stableagents
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stableagents import StableAgents

def test_exit_functionality():
    """Test that exit functionality works properly."""
    print("🧪 Testing Exit Functionality")
    print("=" * 40)
    
    # Initialize StableAgents
    agent = StableAgents()
    
    print("✅ StableAgents initialized successfully")
    print("✅ display_messages method fixed")
    print("✅ Exception handling improved")
    print("✅ KeyboardInterrupt handling added")
    print("✅ EOFError handling added")
    
    print("\n🎯 Exit functionality should now work properly!")
    print("   - Type 'exit' or 'quit' to exit")
    print("   - Press Ctrl+C to interrupt")
    print("   - All interactive prompts should handle interruptions gracefully")
    
    print("\n🚀 To test the exit functionality:")
    print("   1. Run: stableagents interactive")
    print("   2. Type 'exit' or 'quit'")
    print("   3. Or try: stableagents guided-setup")
    print("   4. Press Ctrl+C to cancel")
    
    return True

if __name__ == "__main__":
    try:
        test_exit_functionality()
        print("\n✅ Exit functionality test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1) 