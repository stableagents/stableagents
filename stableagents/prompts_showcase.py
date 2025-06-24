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
            "ai_applications": {
                "title": "AI Application Creation",
                "description": "Build custom AI applications for specific tasks",
                "samples": [
                    {
                        "name": "Customer Service Chatbot",
                        "prompt": "Create a chatbot that can answer customer questions about our product pricing and features",
                        "category": "chatbot",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Document Analyzer",
                        "prompt": "Build an AI app that can read PDF documents and extract key information like dates, names, and amounts",
                        "category": "document_processing",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Image Classification Tool",
                        "prompt": "Create an application that can identify objects in photos and categorize them",
                        "category": "computer_vision",
                        "difficulty": "advanced"
                    },
                    {
                        "name": "Voice Assistant",
                        "prompt": "Build a voice-controlled assistant that can set reminders, play music, and control smart home devices",
                        "category": "voice_assistant",
                        "difficulty": "advanced"
                    },
                    {
                        "name": "Data Analysis Bot",
                        "prompt": "Create an AI that can analyze CSV files and generate insights and visualizations",
                        "category": "data_analysis",
                        "difficulty": "advanced"
                    }
                ]
            },
            "code_generation": {
                "title": "Code Generation & Programming",
                "description": "Generate and debug code with AI assistance",
                "samples": [
                    {
                        "name": "Python Function Generator",
                        "prompt": "Write a Python function that sorts a list of dictionaries by a specific key",
                        "category": "function_generation",
                        "difficulty": "beginner"
                    },
                    {
                        "name": "Web Scraper",
                        "prompt": "Create a web scraper that extracts product information from an e-commerce website",
                        "category": "web_scraping",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "API Integration",
                        "prompt": "Generate code to integrate with a REST API and handle authentication",
                        "category": "api_integration",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Database Operations",
                        "prompt": "Write SQL queries and Python code to manage a database with user authentication",
                        "category": "database",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Machine Learning Pipeline",
                        "prompt": "Create a complete ML pipeline for sentiment analysis including data preprocessing and model training",
                        "category": "machine_learning",
                        "difficulty": "advanced"
                    }
                ]
            },
            "content_creation": {
                "title": "Content Creation & Writing",
                "description": "Generate various types of content with AI",
                "samples": [
                    {
                        "name": "Blog Post Writer",
                        "prompt": "Write a 500-word blog post about the benefits of AI in business",
                        "category": "blog_writing",
                        "difficulty": "beginner"
                    },
                    {
                        "name": "Email Templates",
                        "prompt": "Create professional email templates for customer outreach and follow-ups",
                        "category": "email_templates",
                        "difficulty": "beginner"
                    },
                    {
                        "name": "Social Media Content",
                        "prompt": "Generate engaging social media posts for a tech company's product launch",
                        "category": "social_media",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Technical Documentation",
                        "prompt": "Write comprehensive documentation for a software API with examples",
                        "category": "documentation",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Creative Story Writing",
                        "prompt": "Write a short story with a sci-fi theme and character development",
                        "category": "creative_writing",
                        "difficulty": "advanced"
                    }
                ]
            },
            "data_analysis": {
                "title": "Data Analysis & Insights",
                "description": "Analyze data and generate insights with AI",
                "samples": [
                    {
                        "name": "Sales Data Analysis",
                        "prompt": "Analyze monthly sales data and identify trends, patterns, and recommendations",
                        "category": "business_analytics",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Customer Feedback Analysis",
                        "prompt": "Process customer reviews and extract sentiment, common issues, and improvement suggestions",
                        "category": "sentiment_analysis",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Market Research",
                        "prompt": "Research competitors and generate a market analysis report with key insights",
                        "category": "market_research",
                        "difficulty": "advanced"
                    },
                    {
                        "name": "Financial Data Processing",
                        "prompt": "Analyze financial statements and generate investment insights and risk assessments",
                        "category": "financial_analysis",
                        "difficulty": "advanced"
                    },
                    {
                        "name": "Predictive Analytics",
                        "prompt": "Build a model to predict customer churn based on usage patterns and demographics",
                        "category": "predictive_analytics",
                        "difficulty": "advanced"
                    }
                ]
            },
            "productivity": {
                "title": "Productivity & Workflow Automation",
                "description": "Automate tasks and improve productivity",
                "samples": [
                    {
                        "name": "Email Management",
                        "prompt": "Automatically categorize emails, set up filters, and draft responses for common inquiries",
                        "category": "email_automation",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Meeting Scheduler",
                        "prompt": "Create an AI assistant that can schedule meetings, send invites, and manage calendar conflicts",
                        "category": "calendar_management",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Task Prioritization",
                        "prompt": "Build a system that can prioritize tasks based on deadlines, importance, and available time",
                        "category": "task_management",
                        "difficulty": "intermediate"
                    },
                    {
                        "name": "Report Generation",
                        "prompt": "Automatically generate weekly/monthly reports by collecting data from multiple sources",
                        "category": "reporting",
                        "difficulty": "advanced"
                    },
                    {
                        "name": "Workflow Orchestration",
                        "prompt": "Create a complete workflow that handles customer onboarding from initial contact to account setup",
                        "category": "workflow_automation",
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

📁 COMPUTER CONTROL
• Open applications and automate tasks
• Manage files and folders intelligently
• Control web browsers and extract data
• Monitor system resources

🧠 AI APPLICATIONS
• Create custom chatbots and assistants
• Build document processors and analyzers
• Develop voice-controlled applications
• Automate complex workflows

💻 CODE GENERATION
• Generate Python, JavaScript, and other code
• Debug and optimize existing code
• Create API integrations and web scrapers
• Build machine learning pipelines

📝 CONTENT CREATION
• Write blog posts, emails, and documentation
• Generate social media content
• Create technical documentation
• Write creative stories and scripts

📊 DATA ANALYSIS
• Analyze business data and generate insights
• Process customer feedback and reviews
• Conduct market research and competitor analysis
• Build predictive models and forecasts

⚡ PRODUCTIVITY
• Automate email management and scheduling
• Create task prioritization systems
• Generate automated reports
• Orchestrate complex workflows

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
2. 🧠 AI Application Creation  
3. 💻 Code Generation & Programming
4. 📝 Content Creation & Writing
5. 📊 Data Analysis & Insights
6. ⚡ Productivity & Workflow Automation
7. 📚 Examples by Difficulty
8. 📋 Prompt Templates
9. 🎯 Quick Start Guide
10. ❓ Help & Tips

Enter a number (1-10) or type 'all' to see everything:
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