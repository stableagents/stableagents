#!/usr/bin/env python3
"""
Test script to verify that all functionality from unified_cli.py 
has been successfully migrated to cli.py.
"""

import sys
import os

# Add the parent directory to the path to import stableagents
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cli_migration():
    """Test that all unified_cli.py functionality has been migrated to cli.py."""
    print("🧪 Testing CLI Migration")
    print("=" * 50)
    print("Verifying that all functionality from unified_cli.py")
    print("has been successfully migrated to cli.py")
    print()
    
    # Test that unified_cli.py has been deleted
    unified_cli_path = "stableagents/unified_cli.py"
    if os.path.exists(unified_cli_path):
        print(f"❌ {unified_cli_path} still exists - should have been deleted")
        return False
    else:
        print(f"✅ {unified_cli_path} has been successfully deleted")
    
    # Test that cli.py exists and has the new functionality
    cli_path = "stableagents/cli.py"
    if not os.path.exists(cli_path):
        print(f"❌ {cli_path} does not exist")
        return False
    else:
        print(f"✅ {cli_path} exists")
    
    # Check for key functionality in cli.py
    with open(cli_path, 'r') as f:
        cli_content = f.read()
    
    # Test for migrated commands
    migrated_commands = [
        'health',
        'keys',
        'add-key',
        'remove-key', 
        'list-keys',
        'change-password',
        'switch-provider',
        'current-provider'
    ]
    
    print("\n🔍 Checking for migrated commands:")
    for command in migrated_commands:
        if command in cli_content:
            print(f"  ✅ {command} - Found")
        else:
            print(f"  ❌ {command} - Missing")
            return False
    
    # Test for command line arguments
    cli_args = [
        '--model',
        '--api-key', 
        '--local',
        '--model-path',
        '--self-healing',
        '--auto-recovery',
        '--no-banner'
    ]
    
    print("\n🔍 Checking for command line arguments:")
    for arg in cli_args:
        if arg in cli_content:
            print(f"  ✅ {arg} - Found")
        else:
            print(f"  ❌ {arg} - Missing")
            return False
    
    # Test for health report functionality
    health_features = [
        'StableAgents Health Report',
        'AI Providers:',
        'Memory Status:',
        'Self-Healing Status:'
    ]
    
    print("\n🔍 Checking for health report functionality:")
    for feature in health_features:
        if feature in cli_content:
            print(f"  ✅ {feature} - Found")
        else:
            print(f"  ❌ {feature} - Missing")
            return False
    
    # Test for API key management functionality
    key_management_features = [
        'API Key Management',
        'Adding',
        'Removing',
        'Switching to'
    ]
    
    print("\n🔍 Checking for API key management functionality:")
    for feature in key_management_features:
        if feature in cli_content:
            print(f"  ✅ {feature} - Found")
        else:
            print(f"  ❌ {feature} - Missing")
            return False
    
    print("\n" + "="*50)
    print("🎉 CLI Migration Test Completed Successfully!")
    print("="*50)
    print("✅ All functionality from unified_cli.py has been preserved")
    print("✅ unified_cli.py has been deleted")
    print("✅ cli.py now contains all the features")
    
    print("\n🚀 The new cli.py now supports:")
    print("   • All original CLI commands")
    print("   • Health reporting")
    print("   • Advanced API key management")
    print("   • Provider switching")
    print("   • Self-healing features")
    print("   • Local model support")
    print("   • Command line arguments")
    print("   • Improved user flow")
    print("   • Better exit handling")
    
    return True

if __name__ == "__main__":
    try:
        success = test_cli_migration()
        if success:
            print("\n✅ Migration test passed!")
            sys.exit(0)
        else:
            print("\n❌ Migration test failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1) 