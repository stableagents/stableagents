#!/usr/bin/env python3
"""
Gemini to Desktop Example

This example shows how your gemini_example.py connects to the enhanced
natural desktop integration for creating desktop applications.
"""

import os
import sys
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def demonstrate_connection():
    """Demonstrate the connection between gemini_example.py and desktop integration."""
    print("🔗 Gemini to Desktop Integration Demo")
    print("=" * 50)
    print("This demo shows how your gemini_example.py connects to desktop app creation")
    print()
    
    # Step 1: Show the original gemini_example.py approach
    print("📝 Step 1: Your Original Gemini Example")
    print("-" * 40)
    print("Your gemini_example.py uses:")
    print("  from google import genai")
    print("  client = genai.Client()")
    print("  response = client.models.generate_content(")
    print("      model='gemini-2.5-flash',")
    print("      contents='Explain how AI works in a few words'")
    print("  )")
    print()
    
    # Step 2: Show how the enhanced integration uses the same approach
    print("📝 Step 2: Enhanced Natural Desktop Integration")
    print("-" * 50)
    print("The enhanced integration uses the SAME approach:")
    print("  from google import genai")
    print("  client = genai.Client()")
    print("  response = client.models.generate_content(")
    print("      model='gemini-2.5-flash',")
    print("      contents='Create a modern calculator app...'")
    print("  )")
    print()
    
    # Step 3: Show the connection
    print("🔗 The Connection")
    print("-" * 20)
    print("✅ Both use the same google.genai client")
    print("✅ Both use the same gemini-2.5-flash model")
    print("✅ Both use the same API key (GEMINI_API_KEY)")
    print("✅ Both use the same generate_content method")
    print()
    
    # Step 4: Show the difference in usage
    print("🎯 The Difference")
    print("-" * 20)
    print("Your gemini_example.py:")
    print("  • Simple text generation")
    print("  • Direct API calls")
    print("  • Manual prompt writing")
    print()
    print("Enhanced Natural Desktop Integration:")
    print("  • Desktop application generation")
    print("  • Structured prompts for UI code")
    print("  • Automatic project creation")
    print("  • Multiple UI framework support")
    print()
    
    # Step 5: Show how to use both together
    print("🚀 How to Use Both Together")
    print("-" * 30)
    print("1. Set your Gemini API key:")
    print("   export GEMINI_API_KEY='your-key'")
    print()
    print("2. Test your basic Gemini setup:")
    print("   python gemini_example.py")
    print()
    print("3. Create desktop applications:")
    print("   stableagents-ai natural-desktop create")
    print()
    print("4. Or use the Python API:")
    print("   from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator")
    print("   generator = NaturalLanguageDesktopGenerator()")
    print("   result = generator.create_app_from_description('Create a calculator')")
    print()


def show_usage_examples():
    """Show practical usage examples."""
    print("\n💡 Practical Usage Examples")
    print("=" * 40)
    
    examples = [
        {
            "title": "Basic Gemini Usage (Your Example)",
            "code": '''
from google import genai
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="Explain how AI works in a few words"
)
print(response.text)
'''
        },
        {
            "title": "Desktop App Creation (Enhanced Integration)",
            "code": '''
from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator

generator = NaturalLanguageDesktopGenerator()
result = generator.create_app_from_description(
    description="Create a modern calculator with scientific functions",
    app_name="SmartCalculator",
    ui_framework="customtkinter"
)
'''
        },
        {
            "title": "Code Generation (Enhanced Integration)",
            "code": '''
from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator

generator = NaturalLanguageDesktopGenerator()
code = generator.generate_code_from_prompt(
    prompt="Create a login form with validation",
    framework="customtkinter"
)
print(code)
'''
        }
    ]
    
    for example in examples:
        print(f"\n📖 {example['title']}")
        print("-" * 40)
        print(example['code'])


def main():
    """Main function."""
    demonstrate_connection()
    show_usage_examples()
    
    print("\n🎉 Summary")
    print("=" * 20)
    print("Your gemini_example.py and the enhanced natural desktop integration")
    print("are now properly connected and use the same underlying Gemini API!")
    print()
    print("🚀 Ready to create desktop applications with natural language!")


if __name__ == "__main__":
    main() 