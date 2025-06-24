import json
import os
import time
from typing import Dict, List, Any, Optional
from pathlib import Path

class PromptsShowcase:
    """
    Showcase of sample prompts and examples for users to understand
    what they can build with StableAgents AI functionality.
    """
    
    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or self._get_default_config_dir()
        self.samples = self._load_sample_prompts()
        self.examples = self._load_examples()
        self.templates = self._load_templates()
    
    def _get_default_config_dir(self) -> str:
        """Get the default configuration directory."""
        home_dir = os.path.expanduser("~")
        config_dir = os.path.join(home_dir, ".stableagents", "prompts_showcase")
        os.makedirs(config_dir, exist_ok=True)
        return config_dir
    
    def _load_sample_prompts(self) -> Dict[str, Any]:
        """Load sample prompts for different categories."""
        return {
            "computer_control": {
                "title": "Computer Control & Automation",
                "description": "Control your computer with natural language commands",
                "samples": [
                    {
                        "name": "Open Applications",
                        "prompt": "Open my email application and compose a new message",
                        "category": "basic_control",
                        "difficulty": "beginner"
                    },
                    {
                        "name": "File Management",
                        "prompt": "Create a new folder called 'Projects' and move all PDF files there",
                        "category": "file_operations",
                        "difficulty": "beginner"
                    },
                    {
                        "name": "Web Automation",
                        "prompt": "Search for 'Python tutorials' on Google and open the first 3 results",
                        "category": "web_automation",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "System Monitoring",
                        "prompt": "Check my system resources and close any applications using too much memory",
                        "category": "system_monitoring",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Advanced Automation",
                        "prompt": "Take a screenshot every 5 minutes for the next hour and save them with timestamps",
                        "category": "advanced_automation",
                        "difficulty": "advanced"
                    }
                ]
            },
            "desktop_applications": {
                "title": "Generate Desktop Applications Using AI",
                "description": "Create desktop applications and tools using AI assistance",
                "samples": [
                    {
                        "name": "File Organizer App",
                        "prompt": "Create a desktop application that automatically organizes files by type and date",
                        "category": "file_management",
                        "difficulty": "beginner"
                    },
                    {
                        "name": "Task Manager Tool",
                        "prompt": "Build a desktop app for managing daily tasks with reminders and progress tracking",
                        "category": "task_management",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Data Visualization Dashboard",
                        "prompt": "Create a desktop application that reads CSV files and generates interactive charts and graphs",
                        "category": "data_visualization",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Code Editor Assistant",
                        "prompt": "Build a desktop code editor with AI-powered autocomplete and code suggestions",
                        "category": "code_editor",
                        "difficulty": "advanced"
                    },
                    {
                        "name": "System Monitor Dashboard",
                        "prompt": "Create a desktop application that monitors system performance with real-time graphs and alerts",
                        "category": "system_monitoring",
                        "difficulty": "advanced"
                    }
                ]
            }
        }
    
    def _load_examples(self) -> Dict[str, Any]:
        """Load complete examples with code and explanations."""
        return {
            "beginner_examples": [
                {
                    "name": "Simple File Organizer",
                    "description": "Automatically organize files by type and date",
                    "prompt": "Create a script that organizes files in my Downloads folder by file type and creation date",
                    "expected_output": "A Python script that sorts files into folders like 'Images', 'Documents', 'Videos'",
                    "use_case": "File management automation"
                },
                {
                    "name": "Weather Checker",
                    "description": "Get weather information for any location",
                    "prompt": "Check the weather for New York City and tell me if I should bring an umbrella",
                    "expected_output": "Current weather conditions and recommendation about umbrella",
                    "use_case": "Information retrieval"
                },
                {
                    "name": "Text Summarizer",
                    "description": "Summarize long articles or documents",
                    "prompt": "Summarize this 2000-word article about AI trends in 3 bullet points",
                    "expected_output": "Concise summary with key points",
                    "use_case": "Content processing"
                }
            ],
            "intermediate_examples": [
                {
                    "name": "E-commerce Price Tracker",
                    "description": "Monitor product prices across multiple websites",
                    "prompt": "Track the price of iPhone 15 on Amazon, Best Buy, and Walmart, and alert me when it drops below $800",
                    "expected_output": "Automated price monitoring system with notifications",
                    "use_case": "Price monitoring automation"
                },
                {
                    "name": "Social Media Content Scheduler",
                    "description": "Generate and schedule social media posts",
                    "prompt": "Create a week's worth of social media posts for my coffee shop and schedule them to post at optimal times",
                    "expected_output": "Generated content with scheduling automation",
                    "use_case": "Social media management"
                },
                {
                    "name": "Customer Support Ticket Classifier",
                    "description": "Automatically categorize and route support tickets",
                    "prompt": "Analyze incoming support emails and categorize them as 'Technical', 'Billing', 'General', or 'Urgent'",
                    "expected_output": "Email classification system with routing logic",
                    "use_case": "Customer service automation"
                }
            ],
            "advanced_examples": [
                {
                    "name": "AI-Powered Sales Assistant",
                    "description": "Complete sales pipeline automation",
                    "prompt": "Create a sales assistant that can qualify leads, schedule demos, send follow-up emails, and track conversion rates",
                    "expected_output": "End-to-end sales automation system",
                    "use_case": "Sales process automation"
                },
                {
                    "name": "Intelligent Document Processor",
                    "description": "Process and extract information from various document types",
                    "prompt": "Build a system that can read invoices, contracts, and receipts, extract key data, and organize it into a database",
                    "expected_output": "Document processing pipeline with data extraction",
                    "use_case": "Document automation"
                },
                {
                    "name": "Predictive Maintenance System",
                    "description": "Predict equipment failures using sensor data",
                    "prompt": "Analyze sensor data from manufacturing equipment to predict when maintenance is needed and prevent breakdowns",
                    "expected_output": "ML-based predictive maintenance system",
                    "use_case": "Industrial automation"
                }
            ]
        }
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load prompt templates for different use cases."""
        return {
            "computer_control_templates": {
                "file_operations": [
                    "Create a {file_type} file named '{filename}' in the {location} folder",
                    "Move all {file_extension} files from {source} to {destination}",
                    "Delete files older than {days} days in the {folder} directory",
                    "Rename all files in {folder} to follow the pattern '{pattern}'"
                ],
                "application_control": [
                    "Open {application} and {action}",
                    "Close {application} and save any open documents",
                    "Switch to {application} and {task}",
                    "Minimize all windows except {application}"
                ],
                "web_automation": [
                    "Search for '{query}' on {website} and {action}",
                    "Open {url} and extract {information}",
                    "Fill out the form on {website} with {data}",
                    "Download all {file_type} files from {url}"
                ]
            },
            "ai_application_templates": {
                "chatbot": [
                    "Create a chatbot that can {capability} for {audience}",
                    "Build a customer service bot that handles {types_of_queries}",
                    "Develop a sales assistant that can {sales_tasks}",
                    "Make a support bot that {support_functions}"
                ],
                "data_processor": [
                    "Build an AI that can {process_type} {data_type} and {output_format}",
                    "Create a system that analyzes {data_source} and generates {insights}",
                    "Develop a tool that processes {input_format} and converts to {output_format}",
                    "Make an application that {processing_task} and {result_action}"
                ],
                "automation": [
                    "Create an automation that {task} when {trigger}",
                    "Build a workflow that {process} and then {next_step}",
                    "Develop a system that monitors {monitor_target} and {response_action}",
                    "Make a tool that {primary_function} and {secondary_function}"
                ]
            },
            "code_generation_templates": {
                "function": [
                    "Write a {language} function that {function_purpose}",
                    "Create a {language} class that {class_purpose}",
                    "Generate {language} code to {task_description}",
                    "Build a {language} script that {script_purpose}"
                ],
                "integration": [
                    "Integrate with {api_name} API to {integration_purpose}",
                    "Connect to {database_type} database and {database_task}",
                    "Set up authentication for {service} and {auth_task}",
                    "Create a webhook that {webhook_purpose}"
                ],
                "automation": [
                    "Automate {task} using {technology}",
                    "Create a scheduled job that {job_purpose}",
                    "Build a monitoring script that {monitoring_task}",
                    "Develop a deployment pipeline that {pipeline_purpose}"
                ]
            }
        }
    
    def show_welcome_message(self) -> str:
        """Display a welcome message with overview of capabilities."""
        return """
🤖 Welcome to StableAgents AI Functionality!

Discover what you can build with AI-powered computer control and automation:

📁 COMPUTER CONTROL & AUTOMATION
• Open applications and automate tasks
• Manage files and folders intelligently
• Control web browsers and extract data
• Monitor system resources
• Take screenshots and automate workflows

🖥️ GENERATE DESKTOP APPLICATIONS USING AI
• Create file organizer and management tools
• Build task manager and productivity apps
• Develop data visualization dashboards
• Design code editors with AI assistance
• Build system monitoring applications

Ready to get started? Choose a category to see sample prompts and examples!
        """
    
    def show_category_prompts(self, category: str) -> str:
        """Show prompts for a specific category."""
        if category not in self.samples:
            return f"Category '{category}' not found. Available categories: {', '.join(self.samples.keys())}"
        
        category_data = self.samples[category]
        output = f"\n🎯 {category_data['title']}\n"
        output += f"📖 {category_data['description']}\n"
        output += "=" * 60 + "\n\n"
        
        for i, sample in enumerate(category_data['samples'], 1):
            difficulty_emoji = {
                "beginner": "🟢",
                "intermediate": "🟡", 
                "advanced": "🔴"
            }.get(sample['difficulty'], "⚪")
            
            output += f"{i}. {difficulty_emoji} {sample['name']}\n"
            output += f"   💡 {sample['prompt']}\n"
            output += f"   📂 Category: {sample['category']}\n"
            output += f"   🎯 Difficulty: {sample['difficulty'].title()}\n\n"
        
        return output
    
    def show_examples_by_difficulty(self, difficulty: str = "beginner") -> str:
        """Show examples by difficulty level."""
        if difficulty not in self.examples:
            return f"Difficulty '{difficulty}' not found. Available: {', '.join(self.examples.keys())}"
        
        examples_data = self.examples[difficulty]
        output = f"\n📚 {difficulty.title()} Examples\n"
        output += "=" * 50 + "\n\n"
        
        for i, example in enumerate(examples_data, 1):
            output += f"{i}. 🎯 {example['name']}\n"
            output += f"   📝 {example['description']}\n"
            output += f"   💬 Prompt: {example['prompt']}\n"
            output += f"   ✅ Expected: {example['expected_output']}\n"
            output += f"   🏷️  Use Case: {example['use_case']}\n\n"
        
        return output
    
    def show_templates(self, template_type: str) -> str:
        """Show prompt templates for a specific type."""
        if template_type not in self.templates:
            return f"Template type '{template_type}' not found. Available: {', '.join(self.templates.keys())}"
        
        templates_data = self.templates[template_type]
        output = f"\n📋 {template_type.replace('_', ' ').title()} Templates\n"
        output += "=" * 50 + "\n\n"
        
        for category, templates in templates_data.items():
            output += f"📂 {category.replace('_', ' ').title()}:\n"
            for i, template in enumerate(templates, 1):
                output += f"   {i}. {template}\n"
            output += "\n"
        
        return output
    
    def get_interactive_menu(self) -> str:
        """Get an interactive menu for exploring prompts."""
        return """
🎮 Interactive Prompts Explorer

Choose an option:

1. 📁 Computer Control & Automation
2. 🖥️ Generate Desktop Applications Using AI
3. 📚 Examples by Difficulty
4. 📋 Prompt Templates
5. 🎯 Quick Start Guide
6. ❓ Help & Tips

Enter a number (1-6) or type 'all' to see everything:
        """
    
    def show_quick_start_guide(self) -> str:
        """Show a quick start guide for new users."""
        return """
🚀 Quick Start Guide

Step 1: Choose Your First Project
   • Start with "Computer Control" for basic automation
   • Try "Content Creation" for writing tasks
   • Explore "Code Generation" for programming help

Step 2: Pick a Sample Prompt
   • Choose a beginner-level prompt to start
   • Read the description and expected output
   • Understand the use case and difficulty

Step 3: Customize the Prompt
   • Replace placeholder text with your specific needs
   • Adjust the complexity based on your requirements
   • Add specific details about your use case

Step 4: Execute and Iterate
   • Run your prompt and see the results
   • Refine the prompt based on the output
   • Save successful prompts for future use

💡 Pro Tips:
• Start simple and gradually increase complexity
• Be specific about your requirements
• Include context and examples in your prompts
• Test with small datasets before scaling up

🎯 Recommended First Prompts:
1. "Create a script that organizes my Downloads folder"
2. "Write a professional email template for customer follow-up"
3. "Generate a Python function to sort a list of dictionaries"
4. "Summarize this article in 3 bullet points"

Ready to try? Pick a category and start exploring!
        """
    
    def show_help_and_tips(self) -> str:
        """Show help and tips for using prompts effectively."""
        return """
❓ Help & Tips for Effective Prompts

🎯 PROMPT STRUCTURE
• Be specific about what you want to achieve
• Include relevant context and constraints
• Specify the desired output format
• Mention any technical requirements

📝 WRITING GOOD PROMPTS
• Use clear, descriptive language
• Break complex tasks into smaller parts
• Include examples when possible
• Specify the target audience or use case

🔧 TECHNICAL TIPS
• Mention programming languages when relevant
• Specify file formats and data structures
• Include API endpoints or service names
• Define performance requirements

🎨 CREATIVITY TIPS
• Think beyond basic functionality
• Consider user experience and interface
• Include error handling and edge cases
• Plan for scalability and maintenance

⚠️ COMMON MISTAKES
• Being too vague about requirements
• Not specifying the output format
• Ignoring error handling scenarios
• Forgetting to mention constraints

💡 ADVANCED TECHNIQUES
• Use conditional logic in your prompts
• Include multiple scenarios or use cases
• Specify integration requirements
• Mention security and privacy considerations

🔍 PROMPT OPTIMIZATION
• Test different phrasings for better results
• Iterate based on output quality
• Save and reuse successful prompt patterns
• Combine multiple prompts for complex tasks

📚 RESOURCES
• Check the examples for inspiration
• Use templates as starting points
• Explore different difficulty levels
• Learn from the sample applications

Need more specific help? Try the interactive menu or explore the examples!
        """
    
    def get_all_prompts_summary(self) -> str:
        """Get a summary of all available prompts."""
        output = "📋 All Available Prompts Summary\n"
        output += "=" * 50 + "\n\n"
        
        for category, data in self.samples.items():
            output += f"📁 {data['title']}\n"
            output += f"   {data['description']}\n"
            output += f"   📊 {len(data['samples'])} sample prompts\n"
            
            # Count by difficulty
            difficulties = {}
            for sample in data['samples']:
                diff = sample['difficulty']
                difficulties[diff] = difficulties.get(diff, 0) + 1
            
            for diff, count in difficulties.items():
                output += f"   • {diff.title()}: {count}\n"
            output += "\n"
        
        return output
    
    def search_prompts(self, query: str) -> str:
        """Search prompts by keyword or category."""
        query_lower = query.lower()
        results = []
        
        for category, data in self.samples.items():
            for sample in data['samples']:
                if (query_lower in sample['name'].lower() or 
                    query_lower in sample['prompt'].lower() or
                    query_lower in sample['category'].lower()):
                    results.append({
                        'category': category,
                        'sample': sample
                    })
        
        if not results:
            return f"No prompts found matching '{query}'"
        
        output = f"🔍 Search Results for '{query}'\n"
        output += f"Found {len(results)} matching prompts:\n"
        output += "=" * 50 + "\n\n"
        
        for i, result in enumerate(results, 1):
            sample = result['sample']
            output += f"{i}. 📁 {result['category'].replace('_', ' ').title()}\n"
            output += f"   🎯 {sample['name']}\n"
            output += f"   💬 {sample['prompt']}\n"
            output += f"   🎯 Difficulty: {sample['difficulty'].title()}\n\n"
        
        return output
    
    def get_prompt_by_id(self, category: str, prompt_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific prompt by category and ID."""
        if category not in self.samples:
            return None
        
        samples = self.samples[category]['samples']
        if 1 <= prompt_id <= len(samples):
            return samples[prompt_id - 1]
        
        return None
    
    def save_custom_prompt(self, category: str, name: str, prompt: str, 
                          description: str = "", difficulty: str = "intermediate") -> bool:
        """Save a custom prompt created by the user."""
        custom_prompts_file = os.path.join(self.config_dir, "custom_prompts.json")
        
        try:
            # Load existing custom prompts
            custom_prompts = {}
            if os.path.exists(custom_prompts_file):
                with open(custom_prompts_file, 'r') as f:
                    custom_prompts = json.load(f)
            
            # Add new prompt
            if category not in custom_prompts:
                custom_prompts[category] = []
            
            custom_prompts[category].append({
                "name": name,
                "prompt": prompt,
                "description": description,
                "difficulty": difficulty,
                "created_at": time.time(),
                "custom": True
            })
            
            # Save back to file
            with open(custom_prompts_file, 'w') as f:
                json.dump(custom_prompts, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving custom prompt: {str(e)}")
            return False
    
    def get_custom_prompts(self, category: str = None) -> Dict[str, Any]:
        """Get custom prompts created by the user."""
        custom_prompts_file = os.path.join(self.config_dir, "custom_prompts.json")
        
        if not os.path.exists(custom_prompts_file):
            return {}
        
        try:
            with open(custom_prompts_file, 'r') as f:
                custom_prompts = json.load(f)
            
            if category:
                return custom_prompts.get(category, [])
            else:
                return custom_prompts
                
        except Exception as e:
            print(f"Error loading custom prompts: {str(e)}")
            return {}
    
    def select_prompt_interactive(self) -> Optional[Dict[str, Any]]:
        """Interactive prompt selection for users."""
        print("\n🎯 Let's pick a prompt to get started!")
        print("=" * 50)
        
        # Show categories
        categories = list(self.samples.keys())
        print("Available categories:")
        for i, category in enumerate(categories, 1):
            category_data = self.samples[category]
            print(f"  {i}. {category_data['title']}")
            print(f"     {category_data['description']}")
        
        # Get category choice
        while True:
            try:
                choice = input(f"\nSelect a category (1-{len(categories)}): ").strip()
                cat_index = int(choice) - 1
                if 0 <= cat_index < len(categories):
                    selected_category = categories[cat_index]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(categories)}")
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                return None
        
        # Show prompts in selected category
        category_data = self.samples[selected_category]
        print(f"\n📁 {category_data['title']}")
        print(f"📖 {category_data['description']}")
        print("=" * 60)
        
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
        
        # Get prompt choice
        while True:
            try:
                choice = input(f"Select a prompt (1-{len(samples)}): ").strip()
                prompt_index = int(choice) - 1
                if 0 <= prompt_index < len(samples):
                    selected_prompt = samples[prompt_index]
                    selected_prompt['category'] = selected_category
                    break
                else:
                    print(f"Please enter a number between 1 and {len(samples)}")
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                return None
        
        return selected_prompt
    
    def get_recommended_provider(self, prompt: Dict[str, Any]) -> str:
        """Get recommended AI provider based on prompt type."""
        category = prompt.get('category', '')
        difficulty = prompt.get('difficulty', 'intermediate')
        
        # Provider recommendations based on category and difficulty
        recommendations = {
            'computer_control': {
                'beginner': 'openai',
                'intermediate': 'openai',
                'advanced': 'anthropic'
            },
            'desktop_applications': {
                'beginner': 'openai',
                'intermediate': 'anthropic',
                'advanced': 'anthropic'
            }
        }
        
        return recommendations.get(category, {}).get(difficulty, 'openai')
    
    def show_provider_recommendations(self, prompt: Dict[str, Any]) -> str:
        """Show provider recommendations for a selected prompt."""
        recommended = self.get_recommended_provider(prompt)
        
        print(f"\n🤖 Provider Recommendations for: {prompt['name']}")
        print("=" * 60)
        
        providers = {
            'openai': {
                'name': 'OpenAI (GPT-4, GPT-3.5)',
                'pros': ['Fast response times', 'Good for general tasks', 'Wide model selection'],
                'cons': ['Higher cost for GPT-4', 'Rate limits'],
                'best_for': ['General AI tasks', 'Quick prototyping', 'Content creation']
            },
            'anthropic': {
                'name': 'Anthropic (Claude)',
                'pros': ['Excellent reasoning', 'Long context windows', 'Safety-focused'],
                'cons': ['Slower response times', 'Higher cost'],
                'best_for': ['Complex reasoning', 'Code generation', 'Analysis tasks']
            },
            'google': {
                'name': 'Google (PaLM, Gemini)',
                'pros': ['Good performance', 'Competitive pricing', 'Integration with Google services'],
                'cons': ['Limited model selection', 'Newer to market'],
                'best_for': ['Google ecosystem integration', 'Cost-effective solutions']
            },
            'local': {
                'name': 'Local Models (GGUF)',
                'pros': ['Privacy-focused', 'No API costs', 'Works offline'],
                'cons': ['Limited model quality', 'Requires setup', 'Resource intensive'],
                'best_for': ['Privacy-sensitive tasks', 'Offline use', 'Learning/experimentation']
            }
        }
        
        print(f"🎯 Recommended: {providers[recommended]['name']}")
        print()
        
        for provider_id, provider_info in providers.items():
            status = "⭐ RECOMMENDED" if provider_id == recommended else ""
            print(f"📋 {provider_info['name']} {status}")
            print(f"   ✅ Pros: {', '.join(provider_info['pros'])}")
            print(f"   ⚠️  Cons: {', '.join(provider_info['cons'])}")
            print(f"   🎯 Best for: {', '.join(provider_info['best_for'])}")
            print()
        
        return recommended
    
    def select_provider_interactive(self, prompt: Dict[str, Any]) -> Optional[str]:
        """Interactive provider selection for users."""
        recommended = self.show_provider_recommendations(prompt)
        
        providers = ['openai', 'anthropic', 'google', 'local']
        provider_names = {
            'openai': 'OpenAI (GPT-4, GPT-3.5)',
            'anthropic': 'Anthropic (Claude)',
            'google': 'Google (PaLM, Gemini)',
            'local': 'Local Models (GGUF)'
        }
        
        print("Select your preferred provider:")
        for i, provider in enumerate(providers, 1):
            status = "⭐ RECOMMENDED" if provider == recommended else ""
            print(f"  {i}. {provider_names[provider]} {status}")
        
        while True:
            try:
                choice = input(f"\nSelect provider (1-{len(providers)}): ").strip()
                provider_index = int(choice) - 1
                if 0 <= provider_index < len(providers):
                    selected_provider = providers[provider_index]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(providers)}")
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                return None
        
        return selected_provider
    
    def get_setup_instructions(self, prompt: Dict[str, Any], provider: str) -> str:
        """Get setup instructions for the selected prompt and provider."""
        instructions = f"""
🎯 Setup Instructions for: {prompt['name']}
🤖 Provider: {provider.upper()}
📋 Prompt: {prompt['prompt']}

📋 NEXT STEPS:
"""
        
        if provider == 'local':
            instructions += """
1. 📥 Download GGUF Models:
   • Visit https://huggingface.co/TheBloke
   • Download a model like: llama-2-7b-chat.Q4_K_M.gguf
   • Place it in: ~/.stableagents/models/

2. 🔧 Configure Local Model:
   • Run: stableagents-ai setup
   • Choose "Local models only"
   • Point to your downloaded model

3. 🚀 Start Building:
   • Run: stableagents-ai interactive
   • Try your selected prompt
"""
        else:
            instructions += f"""
1. 🔑 Get API Key:
   • Visit: {self._get_provider_url(provider)}
   • Create account and get API key
   • Note: {self._get_provider_cost_info(provider)}

2. 🔧 Configure API Key:
   • Run: stableagents-ai setup
   • Choose "Bring your own API keys"
   • Enter your {provider.upper()} API key

3. 🚀 Start Building:
   • Run: stableagents-ai interactive
   • Try your selected prompt
"""
        
        return instructions
    
    def _get_provider_url(self, provider: str) -> str:
        """Get signup URL for provider."""
        urls = {
            'openai': 'https://platform.openai.com/signup',
            'anthropic': 'https://console.anthropic.com/',
            'google': 'https://makersuite.google.com/app/apikey'
        }
        return urls.get(provider, 'https://example.com')
    
    def _get_provider_cost_info(self, provider: str) -> str:
        """Get cost information for provider."""
        costs = {
            'openai': 'GPT-3.5: ~$0.002/1K tokens, GPT-4: ~$0.03/1K tokens',
            'anthropic': 'Claude: ~$0.008/1K tokens',
            'google': 'PaLM: ~$0.001/1K tokens, Gemini: ~$0.002/1K tokens'
        }
        return costs.get(provider, 'Check provider website for current pricing')
    
    def save_user_selection(self, prompt: Dict[str, Any], provider: str) -> bool:
        """Save user's prompt and provider selection."""
        selection_file = os.path.join(self.config_dir, "user_selection.json")
        
        try:
            selection = {
                "prompt": prompt,
                "provider": provider,
                "selected_at": time.time(),
                "setup_completed": False
            }
            
            with open(selection_file, 'w') as f:
                json.dump(selection, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving selection: {str(e)}")
            return False
    
    def get_user_selection(self) -> Optional[Dict[str, Any]]:
        """Get user's saved prompt and provider selection."""
        selection_file = os.path.join(self.config_dir, "user_selection.json")
        
        if not os.path.exists(selection_file):
            return None
        
        try:
            with open(selection_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading selection: {str(e)}")
            return None
    
    def mark_setup_completed(self) -> bool:
        """Mark the setup as completed."""
        selection_file = os.path.join(self.config_dir, "user_selection.json")
        
        try:
            if os.path.exists(selection_file):
                with open(selection_file, 'r') as f:
                    selection = json.load(f)
                
                selection["setup_completed"] = True
                selection["completed_at"] = time.time()
                
                with open(selection_file, 'w') as f:
                    json.dump(selection, f, indent=2)
                
                return True
        except Exception as e:
            print(f"Error marking setup completed: {str(e)}")
        
        return False 