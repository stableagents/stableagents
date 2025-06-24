#!/usr/bin/env python3
"""
Guided Setup Demo for StableAgents

This script demonstrates the new guided setup process that includes:
1. Prompt selection from various categories
2. Provider selection with recommendations
3. Setup instructions for the chosen combination
4. Integration with API key setup

Run this script to see the complete guided setup experience!
"""

import sys
import os

# Add the parent directory to the path to import stableagents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stableagents import StableAgents

def main():
    print("🎯 StableAgents Guided Setup Demo")
    print("=" * 60)
    print("This demo shows the new guided setup process that helps users")
    print("pick a prompt and select a provider before setting up API keys.")
    print()
    
    # Initialize StableAgents
    print("Initializing StableAgents...")
    agent = StableAgents()
    
    # Show the guided setup process
    print("\n" + "="*60)
    print("🎯 GUIDED SETUP PROCESS")
    print("="*60)
    
    setup_result = agent.show_guided_setup()
    print(f"\nSetup Result: {setup_result}")
    
    # Check if user made a selection
    user_selection = agent.get_user_selection()
    if user_selection:
        print("\n" + "="*60)
        print("📋 USER SELECTION SUMMARY")
        print("="*60)
        print(f"Selected Prompt: {user_selection['prompt']['name']}")
        print(f"Prompt Text: {user_selection['prompt']['prompt']}")
        print(f"Category: {user_selection['prompt']['category']}")
        print(f"Difficulty: {user_selection['prompt']['difficulty']}")
        print(f"Selected Provider: {user_selection['provider'].upper()}")
        print(f"Setup Completed: {user_selection.get('setup_completed', False)}")
        
        if not user_selection.get('setup_completed', False):
            print("\n" + "="*60)
            print("🚀 NEXT STEPS")
            print("="*60)
            print("1. Follow the setup instructions above")
            print("2. Get your API key from the selected provider")
            print("3. Run 'stableagents setup' to configure your keys")
            print("4. Start building with your selected prompt!")
        else:
            print("\n✅ Setup is already completed!")
            print("You can start using your selected prompt and provider.")
    else:
        print("\n❌ No selection was made.")
        print("You can run the guided setup again later.")
    
    print("\n" + "="*60)
    print("🎉 Demo completed!")
    print("="*60)
    print("To try the full guided setup:")
    print("  stableagents guided-setup")
    print()
    print("To explore prompts showcase:")
    print("  stableagents showcase")
    print()
    print("To start interactive mode:")
    print("  stableagents interactive")

def demo_prompt_selection():
    """Demonstrate just the prompt selection process."""
    print("\n🎯 PROMPT SELECTION DEMO")
    print("=" * 40)
    
    agent = StableAgents()
    
    # Show available categories
    print("Available prompt categories:")
    categories = list(agent.prompts_showcase.samples.keys())
    for i, category in enumerate(categories, 1):
        category_data = agent.prompts_showcase.samples[category]
        print(f"  {i}. {category_data['title']}")
    
    # Simulate category selection (computer_control)
    print(f"\nSimulating selection of category: {categories[0]}")
    selected_category = categories[0]
    
    # Show prompts in that category
    category_data = agent.prompts_showcase.samples[selected_category]
    print(f"\n📁 {category_data['title']}")
    print(f"📖 {category_data['description']}")
    
    samples = category_data['samples']
    for i, sample in enumerate(samples, 1):
        difficulty_emoji = {
            "beginner": "🟢",
            "intermediate": "🟡", 
            "advanced": "🔴"
        }.get(sample['difficulty'], "⚪")
        
        print(f"{i}. {difficulty_emoji} {sample['name']}")
        print(f"   💡 {sample['prompt']}")
        print(f"   🎯 Difficulty: {sample['difficulty'].title()}")
        print()
    
    # Simulate prompt selection (first one)
    selected_prompt = samples[0]
    selected_prompt['category'] = selected_category
    print(f"Simulating selection of prompt: {selected_prompt['name']}")

def demo_provider_recommendations():
    """Demonstrate provider recommendations."""
    print("\n🤖 PROVIDER RECOMMENDATIONS DEMO")
    print("=" * 40)
    
    agent = StableAgents()
    
    # Create a sample prompt
    sample_prompt = {
        'name': 'Customer Service Chatbot',
        'category': 'ai_applications',
        'difficulty': 'intermediate'
    }
    
    # Show provider recommendations
    recommended = agent.prompts_showcase.get_recommended_provider(sample_prompt)
    print(f"Prompt: {sample_prompt['name']}")
    print(f"Category: {sample_prompt['category']}")
    print(f"Difficulty: {sample_prompt['difficulty']}")
    print(f"Recommended Provider: {recommended}")
    
    # Show detailed recommendations
    agent.prompts_showcase.show_provider_recommendations(sample_prompt)

def demo_setup_instructions():
    """Demonstrate setup instructions generation."""
    print("\n📋 SETUP INSTRUCTIONS DEMO")
    print("=" * 40)
    
    agent = StableAgents()
    
    # Create sample selections
    sample_prompt = {
        'name': 'Code Generation Tool',
        'prompt': 'Write a Python function that sorts a list of dictionaries by a specific key'
    }
    
    # Show instructions for different providers
    providers = ['openai', 'anthropic', 'local']
    
    for provider in providers:
        print(f"\n--- Instructions for {provider.upper()} ---")
        instructions = agent.prompts_showcase.get_setup_instructions(sample_prompt, provider)
        print(instructions)

if __name__ == "__main__":
    try:
        main()
        
        # Uncomment to see individual demos
        # demo_prompt_selection()
        # demo_provider_recommendations()
        # demo_setup_instructions()
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying StableAgents!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your installation and try again.") 