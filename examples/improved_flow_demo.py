#!/usr/bin/env python3
"""
Improved Flow Demo for StableAgents

This script demonstrates the new improved user flow:
1. Show prompt examples first
2. Let user pick their preferred provider
3. Provide setup instructions
4. Optionally proceed to API key setup

This creates a much better user experience!
"""

import sys
import os

# Add the parent directory to the path to import stableagents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stableagents import StableAgents

def demo_improved_flow():
    """Demonstrate the improved user flow."""
    print("🎯 Improved User Flow Demo")
    print("=" * 60)
    print("This demo shows the new improved flow that:")
    print("1. 📋 Shows prompt examples FIRST")
    print("2. 🤖 Lets users pick their preferred provider")
    print("3. 🔧 Provides clear setup instructions")
    print("4. 🚀 Optionally proceeds to API key setup")
    print()
    
    # Initialize StableAgents
    agent = StableAgents()
    
    # Step 1: Show prompt examples
    print("📋 STEP 1: EXPLORE WHAT YOU CAN BUILD")
    print("=" * 50)
    print("Let's start by showing you some examples of what you can create:")
    print()
    
    # Show quick examples
    examples = {
        "🖥️  Computer Control": [
            "Open my email and compose a new message",
            "Create a new folder and organize my files",
            "Search for Python tutorials and open the first 3 results"
        ],
        "🧠 AI Applications": [
            "Create a chatbot for customer support",
            "Build an app that reads PDFs and extracts key info",
            "Make an AI assistant that can identify objects in photos"
        ],
        "💻 Code Generation": [
            "Write a Python function to sort data",
            "Create a web scraper for e-commerce sites",
            "Generate code to integrate with REST APIs"
        ],
        "📝 Content Creation": [
            "Write a 500-word blog post about AI trends",
            "Create professional email templates",
            "Generate engaging social media posts"
        ],
        "📊 Data Analysis": [
            "Analyze monthly sales data and identify trends",
            "Process customer reviews and extract sentiment",
            "Build a model to predict customer churn"
        ],
        "⚡ Productivity": [
            "Automatically categorize emails and draft responses",
            "Create an AI assistant for meeting scheduling",
            "Build a system to prioritize tasks"
        ]
    }
    
    for category, prompts in examples.items():
        print(f"{category}:")
        for prompt in prompts:
            print(f"   • '{prompt}'")
        print()
    
    print("💡 These are just examples! You can create anything you can imagine.")
    print()
    
    # Step 2: Provider selection
    print("🤖 STEP 2: CHOOSE YOUR AI PROVIDER")
    print("=" * 50)
    print("Now let's help you choose the best AI provider for your needs:")
    print()
    
    providers = {
        'openai': {
            'name': 'OpenAI (GPT-4, GPT-3.5)',
            'pros': ['Fast response times', 'Good for general tasks', 'Wide model selection'],
            'cons': ['Higher cost for GPT-4', 'Rate limits'],
            'best_for': ['General AI tasks', 'Quick prototyping', 'Content creation'],
            'cost': 'GPT-3.5: ~$0.002/1K tokens, GPT-4: ~$0.03/1K tokens'
        },
        'anthropic': {
            'name': 'Anthropic (Claude)',
            'pros': ['Excellent reasoning', 'Long context windows', 'Safety-focused'],
            'cons': ['Slower response times', 'Higher cost'],
            'best_for': ['Complex reasoning', 'Code generation', 'Analysis tasks'],
            'cost': 'Claude: ~$0.008/1K tokens'
        },
        'google': {
            'name': 'Google (PaLM, Gemini)',
            'pros': ['Good performance', 'Competitive pricing', 'Integration with Google services'],
            'cons': ['Limited model selection', 'Newer to market'],
            'best_for': ['Google ecosystem integration', 'Cost-effective solutions'],
            'cost': 'PaLM: ~$0.001/1K tokens, Gemini: ~$0.002/1K tokens'
        },
        'local': {
            'name': 'Local Models (GGUF)',
            'pros': ['Privacy-focused', 'No API costs', 'Works offline'],
            'cons': ['Limited model quality', 'Requires setup', 'Resource intensive'],
            'best_for': ['Privacy-sensitive tasks', 'Offline use', 'Learning/experimentation'],
            'cost': 'Free (one-time model download)'
        }
    }
    
    print("Available AI Providers:")
    print()
    
    for i, (provider_id, provider_info) in enumerate(providers.items(), 1):
        print(f"{i}. {provider_info['name']}")
        print(f"   ✅ Pros: {', '.join(provider_info['pros'])}")
        print(f"   ⚠️  Cons: {', '.join(provider_info['cons'])}")
        print(f"   🎯 Best for: {', '.join(provider_info['best_for'])}")
        print(f"   💰 Cost: {provider_info['cost']}")
        print()
    
    # Simulate provider selection (OpenAI for demo)
    selected_provider = 'openai'
    print(f"✅ Selected Provider: {providers[selected_provider]['name']}")
    
    # Step 3: Setup instructions
    print("\n🔧 STEP 3: SETUP INSTRUCTIONS")
    print("=" * 50)
    
    instructions = f"""
🎯 Setup Instructions for {providers[selected_provider]['name']}
🤖 Provider: {selected_provider.upper()}

📋 NEXT STEPS:

1. 🔑 Get API Key:
   • Visit: https://platform.openai.com/signup
   • Create account and get API key
   • Note: {providers[selected_provider]['cost']}

2. 🔧 Configure API Key:
   • Run: stableagents setup
   • Choose "Bring your own API keys"
   • Enter your {selected_provider.upper()} API key

3. 🚀 Start Building:
   • Run: stableagents interactive
   • Try your first AI prompt!
"""
    
    print(instructions)
    
    # Step 4: Optional setup
    print("\n🎯 STEP 4: OPTIONAL SETUP")
    print("=" * 50)
    print("✅ Perfect! You now know what you can build and which provider to use.")
    print("💡 When you're ready, run 'stableagents setup' to configure your API keys.")
    print("🚀 Or run 'stableagents guided-setup' to go through this process interactively!")
    
    return True

def demo_new_default_flow():
    """Demonstrate the new default flow when no command is specified."""
    print("\n🎯 NEW DEFAULT FLOW DEMO")
    print("=" * 50)
    print("When users run 'stableagents' (no command), they now see:")
    print()
    
    print("🎯 Welcome to StableAgents!")
    print("=" * 40)
    print("Would you like to:")
    print("1. 🎯 Start guided setup (recommended for new users)")
    print("2. 🚀 Go directly to interactive mode")
    print("3. 📋 Explore examples and prompts")
    print()
    
    print("💡 This gives users a clear choice and guides them to the best option!")
    print("🎯 Most new users will choose option 1 (guided setup)")
    print("🚀 Experienced users can jump straight to interactive mode")
    print("📋 Curious users can explore examples first")
    
    return True

if __name__ == "__main__":
    try:
        demo_improved_flow()
        demo_new_default_flow()
        
        print("\n" + "="*60)
        print("🎉 Improved Flow Demo Completed!")
        print("="*60)
        print("The new flow provides a much better user experience:")
        print("✅ Users see what they can build FIRST")
        print("✅ Users choose their preferred provider")
        print("✅ Users get clear setup instructions")
        print("✅ Users can exit at any time")
        print("✅ Users have multiple entry points")
        
        print("\n🚀 To try the new flow:")
        print("   stableagents                    # New default flow")
        print("   stableagents guided-setup       # Guided setup")
        print("   stableagents showcase           # Explore examples")
        print("   stableagents interactive        # Direct to interactive")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying StableAgents!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your installation and try again.") 