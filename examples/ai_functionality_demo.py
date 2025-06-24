#!/usr/bin/env python3
"""
AI Functionality Demo for StableAgents

This script demonstrates the new AI functionality including:
- Prompts showcase and examples
- Computer vision and image analysis
- Natural language processing
- Speech recognition and synthesis
- AI application creation
- Intelligent computer control
- Code generation and debugging
- Workflow automation

Run this script to see what you can build with StableAgents!
"""

import sys
import os
import time

# Add the parent directory to the path to import stableagents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stableagents import StableAgents

def main():
    print("🤖 StableAgents AI Functionality Demo")
    print("=" * 60)
    
    # Initialize StableAgents
    print("Initializing StableAgents...")
    agent = StableAgents()
    
    # Show the AI functionality setup
    print("\n" + "="*60)
    print("🎯 AI FUNCTIONALITY SHOWCASE")
    print("="*60)
    
    setup_result = agent.setup_ai_functionality()
    print(f"\nSetup Result: {setup_result}")
    
    # Interactive demo menu
    while True:
        print("\n" + "="*60)
        print("🎮 INTERACTIVE DEMO MENU")
        print("="*60)
        print("1. 📋 Show Prompts Showcase")
        print("2. 🔍 Search Prompts")
        print("3. 📁 Show Computer Control Examples")
        print("4. 🧠 Show AI Application Examples")
        print("5. 💻 Show Code Generation Examples")
        print("6. 📝 Show Content Creation Examples")
        print("7. 📊 Show Data Analysis Examples")
        print("8. ⚡ Show Productivity Examples")
        print("9. 🎯 Quick Start Guide")
        print("10. ❓ Help & Tips")
        print("11. 🔧 Check AI Capabilities")
        print("12. 📚 Show Examples by Difficulty")
        print("13. 🚀 Try Sample Prompts")
        print("14. 💾 Save Custom Prompt")
        print("15. 📖 View Custom Prompts")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-15): ").strip()
        
        if choice == "0":
            print("👋 Thanks for trying StableAgents AI Functionality!")
            break
        elif choice == "1":
            print(agent.show_prompts_showcase())
        elif choice == "2":
            query = input("Enter search query: ").strip()
            print(agent.search_prompts(query))
        elif choice == "3":
            print(agent.show_prompts_showcase("computer_control"))
        elif choice == "4":
            print(agent.show_prompts_showcase("desktop_applications"))
        elif choice == "5":
            print(agent.show_prompts_showcase("quick_start"))
        elif choice == "6":
            print(agent.show_prompts_showcase("help"))
        elif choice == "7":
            capabilities = agent.get_ai_capabilities()
            print("\n🔧 AI Capabilities:")
            for capability, available in capabilities.items():
                status = "✅ Available" if available else "❌ Not Available"
                print(f"   {capability}: {status}")
        elif choice == "8":
            difficulty = input("Enter difficulty (beginner/intermediate/advanced): ").strip()
            print(agent.show_prompts_showcase(difficulty))
        elif choice == "9":
            try_sample_prompts(agent)
        elif choice == "10":
            save_custom_prompt(agent)
        elif choice == "11":
            view_custom_prompts(agent)
        else:
            print("❌ Invalid choice. Please try again.")

def try_sample_prompts(agent):
    """Try some sample prompts with the AI functionality."""
    print("\n🚀 Trying Sample Prompts")
    print("=" * 40)
    
    # Check if AI provider is available
    if not agent.get_ai_provider():
        print("⚠️  No AI provider configured. Some features may not work.")
        print("   You can still explore the prompts showcase and examples.")
        return
    
    # Sample prompts to try
    sample_prompts = [
        {
            "name": "Text Analysis",
            "prompt": "Analyze the sentiment of this text: 'I love this new AI tool, it's amazing!'",
            "function": "analyze_text"
        },
        {
            "name": "Code Generation",
            "prompt": "Write a Python function to calculate the factorial of a number",
            "function": "generate_code"
        },
        {
            "name": "Computer Control",
            "prompt": "Open my web browser and search for 'Python tutorials'",
            "function": "intelligent_computer_control"
        }
    ]
    
    for i, sample in enumerate(sample_prompts, 1):
        print(f"\n{i}. {sample['name']}")
        print(f"   Prompt: {sample['prompt']}")
        
        try:
            if sample['function'] == 'analyze_text':
                result = agent.analyze_text(sample['prompt'].split(": ")[1])
                print(f"   Result: {result}")
            elif sample['function'] == 'generate_code':
                result = agent.generate_code(sample['prompt'])
                print(f"   Result:\n{result}")
            elif sample['function'] == 'intelligent_computer_control':
                result = agent.intelligent_computer_control(sample['prompt'])
                print(f"   Result: {result}")
        except Exception as e:
            print(f"   Error: {str(e)}")
        
        if i < len(sample_prompts):
            input("\n   Press Enter to continue...")

def save_custom_prompt(agent):
    """Save a custom prompt created by the user."""
    print("\n💾 Save Custom Prompt")
    print("=" * 30)
    
    category = input("Enter category (computer_control/desktop_applications): ").strip()
    name = input("Enter prompt name: ").strip()
    prompt = input("Enter the prompt: ").strip()
    description = input("Enter description (optional): ").strip()
    difficulty = input("Enter difficulty (beginner/intermediate/advanced): ").strip()
    
    if not difficulty:
        difficulty = "intermediate"
    
    success = agent.save_custom_prompt(category, name, prompt, description, difficulty)
    
    if success:
        print("✅ Custom prompt saved successfully!")
    else:
        print("❌ Failed to save custom prompt.")

def view_custom_prompts(agent):
    """View custom prompts created by the user."""
    print("\n📖 Custom Prompts")
    print("=" * 20)
    
    custom_prompts = agent.get_custom_prompts()
    
    if not custom_prompts:
        print("No custom prompts found.")
        return
    
    for category, prompts in custom_prompts.items():
        print(f"\n📁 {category.replace('_', ' ').title()}:")
        for i, prompt in enumerate(prompts, 1):
            print(f"   {i}. {prompt['name']}")
            print(f"      💬 {prompt['prompt']}")
            print(f"      📝 {prompt['description']}")
            print(f"      🎯 Difficulty: {prompt['difficulty']}")
            print()

def demo_ai_applications(agent):
    """Demonstrate AI application creation."""
    print("\n🧠 AI Application Creation Demo")
    print("=" * 40)
    
    # Example chatbot application
    chatbot_config = {
        "name": "Demo Customer Service Bot",
        "description": "A simple chatbot for customer service",
        "capabilities": ["answer_questions", "route_requests"],
        "audience": "customers"
    }
    
    print("Creating a chatbot application...")
    result = agent.create_ai_application("chatbot", chatbot_config)
    print(f"Result: {result}")
    
    if result.get("success"):
        app_id = result["app_id"]
        print(f"Application created with ID: {app_id}")
        
        # List all applications
        apps = agent.list_ai_applications()
        print(f"\nTotal applications: {len(apps)}")
        for app in apps:
            print(f"  - {app['name']} ({app['type']})")

def demo_computer_vision(agent):
    """Demonstrate computer vision capabilities."""
    print("\n👁️ Computer Vision Demo")
    print("=" * 30)
    
    # Check if OpenCV is available
    capabilities = agent.get_ai_capabilities()
    if not capabilities.get("computer_vision", False):
        print("❌ Computer vision not available. Install OpenCV to enable this feature.")
        return
    
    # Example image analysis (would need an actual image file)
    print("Computer vision capabilities available:")
    print("  - Object detection")
    print("  - Face detection")
    print("  - Color analysis")
    print("  - Text extraction (with OCR)")
    
    # You would typically analyze an actual image here
    # result = agent.analyze_image("path/to/image.jpg", "general")

def demo_speech_recognition(agent):
    """Demonstrate speech recognition capabilities."""
    print("\n🎤 Speech Recognition Demo")
    print("=" * 35)
    
    capabilities = agent.get_ai_capabilities()
    if not capabilities.get("speech_recognition", False):
        print("❌ Speech recognition not available. Install SpeechRecognition to enable this feature.")
        return
    
    print("Speech recognition capabilities available:")
    print("  - Voice input processing")
    print("  - Text-to-speech output")
    print("  - Voice command interpretation")
    
    # Example speech recognition (would need microphone access)
    # result = agent.listen_for_speech(timeout=5)
    # print(f"Recognized: {result}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying StableAgents!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your installation and try again.") 