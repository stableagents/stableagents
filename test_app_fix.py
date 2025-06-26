#!/usr/bin/env python3
"""
Test script to verify the run_app fix works correctly
"""

import os
import tempfile
from pathlib import Path

# Create a simple test app (console-based, no GUI)
test_app_code = '''#!/usr/bin/env python3
"""
Simple test app to verify run_app functionality
"""

def main():
    print("Hello! This is a test app.")
    print("The run_app fix is working correctly!")
    print("✅ No path duplication detected!")
    return 0

if __name__ == "__main__":
    exit(main())
'''

def test_run_app_fix():
    """Test the run_app method with valid Python code."""
    print("🧪 Testing run_app fix...")
    
    # Create a temporary test app
    with tempfile.TemporaryDirectory() as temp_dir:
        test_project = Path(temp_dir) / "test_app"
        test_project.mkdir()
        
        # Create main.py with valid code
        main_file = test_project / "main.py"
        with open(main_file, 'w') as f:
            f.write(test_app_code)
        
        # Create requirements.txt
        requirements_file = test_project / "requirements.txt"
        with open(requirements_file, 'w') as f:
            f.write("# No external requirements needed for this test\n")
        
        print(f"📁 Created test app at: {test_project}")
        print(f"📄 Main file: {main_file}")
        
        # Test the run_app method
        from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator
        
        generator = NaturalLanguageDesktopGenerator()
        
        print("\n🚀 Testing run_app method...")
        print("=" * 50)
        
        try:
            # This should work without path duplication
            success = generator.run_app(str(test_project))
            
            if success:
                print("✅ run_app test PASSED - No path duplication!")
                return True
            else:
                print("❌ run_app test FAILED")
                return False
                
        except Exception as e:
            print(f"❌ run_app test ERROR: {e}")
            return False

if __name__ == "__main__":
    test_run_app_fix() 