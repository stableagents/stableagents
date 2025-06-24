import json 
import os
import threading
import datetime
import sys
import time
import logging
from typing import Optional, Dict, Any

# Make TensorFlow optional
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

from .computer import ComputerControl
from .ai_providers import AIProviderManager, AIProvider
from .ai_functionality import AIFunctionality
from .prompts_showcase import PromptsShowcase
from .core.self_healing import SelfHealingController
# from stableagents import * 


class StableAgents:
    """
    
    This is the stableagents-ai libraries
   
    """
    
    def __init__(self, config_dir: str = None, enable_self_healing: bool = False):
        self.computer = ComputerControl()
        self.computer_has_imported_computer_api = True
        self.messages = []
        self.last_messages_count = 0
        self.plain_text_display = True
        self.logger = logging.getLogger(__name__)
        # Memory component initialization
        self.memory = {
            "short_term": [],
            "long_term": {},
            "context": {},
            "last_accessed": datetime.datetime.now()
        }
        # Initialize TensorFlow if available
        self.tf_model = None if not TENSORFLOW_AVAILABLE else None
        
        # Initialize AI provider manager
        self.ai_manager = AIProviderManager(config_dir)
        self.ai_provider = None
        self.using_local_model = False
        self.local_model = None
        
        # Initialize AI functionality
        self.ai_functionality = AIFunctionality(ai_provider=None, config_dir=config_dir)
        
        # Initialize prompts showcase
        self.prompts_showcase = PromptsShowcase(config_dir)
        
        # Initialize self-healing system
        self.self_healing = SelfHealingController(agent=self)
        self.self_healing_enabled = False
        
        # Enable self-healing if requested
        if enable_self_healing:
            self.enable_self_healing()
            
        # Register standard components for health monitoring
        self._register_health_components()
    
    def _register_health_components(self):
        """Register standard components for health monitoring."""
        # Register AI provider health check
        self.self_healing.register_component(
            "ai_provider",
            self._check_ai_provider_health,
            thresholds={
                "provider_available": {"min": True, "severity": "high"},
                "response_time": {"max": 10.0, "severity": "medium"}
            }
        )
        
        # Register memory health check
        self.self_healing.register_component(
            "memory",
            self._check_memory_health,
            thresholds={
                "short_term_count": {"max": 1000, "severity": "medium"},
                "memory_usage_mb": {"max": 1000, "severity": "high"}
            }
        )
        
        # Register local model health check if using local model
        if self.using_local_model:
            self.self_healing.register_component(
                "local_model",
                self._check_local_model_health,
                thresholds={
                    "model_loaded": {"min": True, "severity": "high"}
                }
            )
    
    def _check_ai_provider_health(self):
        """Check the health of the AI provider."""
        from .core.self_healing.monitor import HealthMetric
        
        metrics = []
        timestamp = time.time()
        
        # Check if a provider is active
        active_provider = self.get_active_ai_provider()
        provider_available = active_provider is not None
        
        metrics.append(HealthMetric(
            name="provider_available",
            value=provider_available,
            timestamp=timestamp,
            healthy=provider_available
        ))
        
        if provider_available:
            metrics.append(HealthMetric(
                name="active_provider",
                value=active_provider,
                timestamp=timestamp,
                healthy=True
            ))
            
            # Test API response time
            try:
                start_time = time.time()
                self.generate_text("test", max_tokens=5)
                response_time = time.time() - start_time
                
                metrics.append(HealthMetric(
                    name="response_time",
                    value=response_time,
                    timestamp=timestamp,
                    healthy=response_time < 10.0
                ))
            except Exception as e:
                metrics.append(HealthMetric(
                    name="api_error",
                    value=str(e),
                    timestamp=timestamp,
                    healthy=False
                ))
        
        return metrics
    
    def _check_memory_health(self):
        """Check the health of the memory system."""
        from .core.self_healing.monitor import HealthMetric
        
        metrics = []
        timestamp = time.time()
        
        # Check short-term memory size
        short_term_count = len(self.memory["short_term"])
        metrics.append(HealthMetric(
            name="short_term_count",
            value=short_term_count,
            timestamp=timestamp,
            healthy=short_term_count < 1000
        ))
        
        # Check memory usage
        import psutil
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            memory_usage_mb = memory_info.rss / (1024 * 1024)
            
            metrics.append(HealthMetric(
                name="memory_usage_mb",
                value=memory_usage_mb,
                timestamp=timestamp,
                healthy=memory_usage_mb < 1000
            ))
        except:
            # psutil might not be available
            pass
            
        return metrics
    
    def _check_local_model_health(self):
        """Check the health of the local model."""
        from .core.self_healing.monitor import HealthMetric
        
        metrics = []
        timestamp = time.time()
        
        # Check if local model is being used
        metrics.append(HealthMetric(
            name="using_local_model",
            value=self.using_local_model,
            timestamp=timestamp,
            healthy=True
        ))
        
        if self.using_local_model:
            # Get the local provider
            local_provider = self.ai_manager.get_provider("local")
            model_loaded = local_provider is not None and local_provider.model is not None
            
            metrics.append(HealthMetric(
                name="model_loaded",
                value=model_loaded,
                timestamp=timestamp,
                healthy=model_loaded
            ))
            
            if model_loaded and hasattr(local_provider, "model_path"):
                metrics.append(HealthMetric(
                    name="model_path",
                    value=local_provider.model_path,
                    timestamp=timestamp,
                    healthy=True
                ))
        
        return metrics
    
    def enable_self_healing(self, auto_recovery: bool = False):
        """
        Enable the self-healing system.
        
        Args:
            auto_recovery: Whether to automatically recover from issues
        """
        if self.self_healing_enabled:
            return
            
        self.self_healing_enabled = True
        self.self_healing.start(auto_recovery=auto_recovery)
        self.logger.info("Self-healing system enabled")
        
    def disable_self_healing(self):
        """Disable the self-healing system."""
        if not self.self_healing_enabled:
            return
            
        self.self_healing_enabled = False
        self.self_healing.stop()
        self.logger.info("Self-healing system disabled")
        
    def get_health_report(self):
        """Get a health report for the agent."""
        if not self.self_healing_enabled:
            return {"status": "self_healing_disabled"}
            
        return self.self_healing.get_health_report()
    
    def reset(self):
        if hasattr(self, 'computer') and self.computer:
            self.computer.terminate()
        self.computer_has_imported_computer_api = False
        self.messages = []
        self.last_messages_count = 0
        # Reset memory but keep long-term memory
        self.memory["short_term"] = []
        self.memory["context"] = {}
        self.memory["last_accessed"] = datetime.datetime.now()
        # Reset TensorFlow model
        self.tf_model = None
    
    def display_messages(self, markdown):
        """Display messages to the user. Falls back to plain text if markdown display is not available."""
        if self.plain_text_display:
            print(markdown)
        else: 
            # Try to use markdown display if available
            try:
                # Check if display_markdown_message is available
                if 'display_markdown_message' in globals():
                    display_markdown_message(markdown)
                else:
                    # Fall back to plain text
                    print(markdown)
            except Exception as e:
                # Log the error but don't crash
                self.logger.debug(f"Markdown display failed, falling back to plain text: {e}")
                print(markdown)
    
    def add_to_memory(self, memory_type, key, value):
        """
        Add information to the agent's memory
        
        Args:
            memory_type (str): Type of memory ('short_term', 'long_term', or 'context')
            key (str): Key to store the memory under
            value (any): Value to store in memory
        """
        if memory_type == "short_term":
            self.memory["short_term"].append({"key": key, "value": value, "timestamp": datetime.datetime.now()})
            # Limit short-term memory size
            if len(self.memory["short_term"]) > 100:
                self.memory["short_term"].pop(0)
        elif memory_type == "long_term":
            self.memory["long_term"][key] = {"value": value, "timestamp": datetime.datetime.now()}
        elif memory_type == "context":
            self.memory["context"][key] = {"value": value, "timestamp": datetime.datetime.now()}
        
        self.memory["last_accessed"] = datetime.datetime.now()
    
    def get_from_memory(self, memory_type, key=None):
        """
        Retrieve information from the agent's memory
        
        Args:
            memory_type (str): Type of memory ('short_term', 'long_term', or 'context')
            key (str, optional): Key to retrieve. If None, returns all memories of that type.
            
        Returns:
            The requested memory value or dictionary of values
        """
        self.memory["last_accessed"] = datetime.datetime.now()
        
        if memory_type == "short_term":
            if key is None:
                return self.memory["short_term"]
            return [item for item in self.memory["short_term"] if item["key"] == key]
        elif memory_type == "long_term":
            if key is None:
                return self.memory["long_term"]
            return self.memory["long_term"].get(key, {}).get("value")
        elif memory_type == "context":
            if key is None:
                return self.memory["context"]
            return self.memory["context"].get(key, {}).get("value")
        
        return None
    
    def get_stableagents_directory(self):
        """
        Get the stableagents-ai directory path from environment or use default
        
        Returns:
            str: Path to the stableagents-ai directory
        """
        stableagents_dir = os.environ.get("STABLEAGENTS_DIR", os.path.join(os.path.expanduser("~"), ".stableagents"))
        return stableagents_dir

    def control_computer(self, command: str) -> str:
        """
        Control the computer using natural language commands.
        
        Args:
            command (str): Natural language command to execute
            
        Returns:
            str: Result of the command execution
        """
        return self.computer.execute(command)
    
    def ai_control_computer(self, natural_command: str) -> str:
        """
        Use AI to intelligently interpret and execute natural language computer commands.
        
        Args:
            natural_command (str): Natural language command like "open youtube and play the latest bruno mars song"
            
        Returns:
            str: Result of the AI interpretation and command execution
        """
        # Check if AI provider is properly configured
        if not self.check_ai_provider_ready():
            print("❌ AI provider not properly configured.")
            print("💡 You need to configure an AI provider to use AI-powered features.")
            print()
            
            try:
                reconfigure = input("Would you like to configure an AI provider now? (y/n): ").strip().lower()
                if reconfigure in ['y', 'yes']:
                    if self.reconfigure_ai_provider():
                        print("✅ AI provider configured successfully!")
                        print("🔄 Retrying your command...")
                        # Recursive call to try again
                        return self.ai_control_computer(natural_command)
                    else:
                        return "❌ AI provider configuration failed. Please run 'stableagents-ai setup' to configure manually."
                else:
                    return "❌ AI provider required for AI-powered computer control. Please configure an AI provider first."
            except (KeyboardInterrupt, EOFError):
                return "❌ Configuration cancelled. Please configure an AI provider first."
        
        try:
            # Step 1: Use AI to interpret the natural language command
            interpretation_prompt = f"""
            You are an AI assistant that converts natural language commands into specific computer actions.
            
            User command: "{natural_command}"
            
            Available computer actions:
            - open [application]: Open an application (e.g., "open youtube", "open spotify")
            - browse [url]: Open a website (e.g., "browse youtube.com")
            - search [query]: Search the web (e.g., "search bruno mars latest song")
            - open_media_service [service] [action]: Open media services (e.g., "open_media_service youtube search bruno mars")
            - search_and_play_media [query] [service]: Search and play media (e.g., "search_and_play_media bruno mars latest song youtube")
            - execute [command]: Run a terminal command
            - click [coordinates]: Click at specific coordinates
            - type [text]: Type text
            - screenshot: Take a screenshot
            - monitor [type]: Get system information
            - process [action]: Control processes
            - create [type] [path]: Create files/folders (e.g., "create folder ai_demo")
            
            Convert the user's natural language command into a JSON object with:
            {{
                "actions": [
                    {{
                        "action": "action_name",
                        "parameters": "action_parameters",
                        "description": "what this action does"
                    }}
                ],
                "reasoning": "explanation of how you interpreted the command",
                "confidence": 0.95
            }}
            
            For complex commands, break them down into multiple sequential actions.
            Be specific and actionable. Return only valid JSON.
            
            Examples:
            - "open youtube and play the latest bruno mars song" → open_media_service youtube search bruno mars latest song
            - "search for python tutorials and open the first result" → search python tutorials
            - "take a screenshot and save it to desktop" → screenshot
            - "check system performance and show memory usage" → monitor memory
            """
            
            # Get AI interpretation
            ai_provider = self.get_ai_provider()
            if not ai_provider:
                return "❌ AI provider not available. Please configure an AI provider first."
            
            interpretation_response = ai_provider.generate_text(interpretation_prompt)
            
            # Parse the JSON response
            try:
                import json
                interpretation = json.loads(interpretation_response)
            except json.JSONDecodeError:
                # Fallback to simple parsing
                return f"❌ Failed to parse AI interpretation. Raw response: {interpretation_response}"
            
            # Step 2: Execute the interpreted actions
            results = []
            actions = interpretation.get("actions", [])
            reasoning = interpretation.get("reasoning", "No reasoning provided")
            
            if not actions:
                return f"❌ AI couldn't interpret the command: {natural_command}"
            
            results.append(f"🤖 AI Interpretation: {reasoning}")
            results.append(f"📋 Planned Actions: {len(actions)}")
            
            # Execute each action
            for i, action_info in enumerate(actions, 1):
                action = action_info.get("action", "")
                parameters = action_info.get("parameters", "")
                description = action_info.get("description", "")
                
                results.append(f"\n🔧 Action {i}: {description}")
                
                # Execute the action using the computer control module
                try:
                    if action == "open":
                        result = self.computer.open_application(parameters)
                    elif action == "browse":
                        result = self.computer.browse_web(parameters)
                    elif action == "search":
                        result = self.computer.search_web(parameters)
                    elif action == "open_media_service":
                        # Parse service and action from parameters
                        parts = parameters.split(' ', 1)
                        service = parts[0] if parts else ""
                        action_param = parts[1] if len(parts) > 1 else ""
                        result = self.computer.open_media_service(service, action_param)
                    elif action == "search_and_play_media":
                        # Parse query and service from parameters
                        parts = parameters.split(' ', 1)
                        query = parts[0] if parts else ""
                        service = parts[1] if len(parts) > 1 else "youtube"
                        result = self.computer.search_and_play_media(query, service)
                    elif action == "execute":
                        result = self.computer.execute_command(parameters)
                    elif action == "click":
                        result = self.computer.mouse_click(parameters)
                    elif action == "type":
                        result = self.computer.type_text(parameters)
                    elif action == "screenshot":
                        result = self.computer.take_screenshot(parameters)
                    elif action == "monitor":
                        result = self.computer.system_monitor(parameters)
                    elif action == "process":
                        result = self.computer.process_control(parameters)
                    elif action == "create":
                        result = self.computer.create_file_or_folder(parameters)
                    else:
                        result = f"❌ Unknown action: {action}"
                    
                    results.append(f"   ✅ Result: {result}")
                    
                except Exception as e:
                    results.append(f"   ❌ Error: {str(e)}")
            
            # Step 3: Provide a summary
            results.append(f"\n🎯 Summary: Successfully executed {len(actions)} actions for '{natural_command}'")
            
            return "\n".join(results)
            
        except Exception as e:
            return f"❌ Error in AI computer control: {str(e)}"
    
    # AI Functionality Methods
    def show_prompts_showcase(self, category: str = None) -> str:
        """
        Show the prompts showcase to help users understand what they can build.
        
        Args:
            category (str, optional): Specific category to show. If None, shows welcome message.
            
        Returns:
            str: Formatted showcase content
        """
        if category is None:
            return self.prompts_showcase.show_welcome_message()
        elif category == "menu":
            return self.prompts_showcase.get_interactive_menu()
        elif category == "quick_start":
            return self.prompts_showcase.show_quick_start_guide()
        elif category == "help":
            return self.prompts_showcase.show_help_and_tips()
        elif category == "all":
            return self.prompts_showcase.get_all_prompts_summary()
        elif category in ["beginner", "intermediate", "advanced"]:
            return self.prompts_showcase.show_examples_by_difficulty(category)
        elif category.endswith("_templates"):
            return self.prompts_showcase.show_templates(category)
        else:
            return self.prompts_showcase.show_category_prompts(category)
    
    def search_prompts(self, query: str) -> str:
        """
        Search for prompts by keyword or category.
        
        Args:
            query (str): Search query
            
        Returns:
            str: Search results
        """
        return self.prompts_showcase.search_prompts(query)
    
    def get_sample_prompt(self, category: str, prompt_id: int) -> dict:
        """
        Get a specific sample prompt by category and ID.
        
        Args:
            category (str): Prompt category
            prompt_id (int): Prompt ID (1-based)
            
        Returns:
            dict: Prompt information or None if not found
        """
        return self.prompts_showcase.get_prompt_by_id(category, prompt_id)
    
    def save_custom_prompt(self, category: str, name: str, prompt: str, 
                          description: str = "", difficulty: str = "intermediate") -> bool:
        """
        Save a custom prompt created by the user.
        
        Args:
            category (str): Prompt category
            name (str): Prompt name
            prompt (str): The actual prompt text
            description (str): Optional description
            difficulty (str): Difficulty level (beginner/intermediate/advanced)
            
        Returns:
            bool: True if saved successfully
        """
        return self.prompts_showcase.save_custom_prompt(category, name, prompt, description, difficulty)
    
    def get_custom_prompts(self, category: str = None) -> dict:
        """
        Get custom prompts created by the user.
        
        Args:
            category (str, optional): Specific category to get. If None, returns all.
            
        Returns:
            dict: Custom prompts
        """
        return self.prompts_showcase.get_custom_prompts(category)
    
    # AI Functionality Methods
    def analyze_image(self, image_path: str, task: str = "general") -> dict:
        """
        Analyze an image using computer vision.
        
        Args:
            image_path (str): Path to the image file
            task (str): Analysis task (general, objects, faces, text, colors)
            
        Returns:
            dict: Analysis results
        """
        return self.ai_functionality.analyze_image(image_path, task)
    
    def analyze_text(self, text: str, task: str = "general") -> dict:
        """
        Analyze text using natural language processing.
        
        Args:
            text (str): Text to analyze
            task (str): Analysis task (general, sentiment, entities, keywords, summary)
            
        Returns:
            dict: Analysis results
        """
        return self.ai_functionality.analyze_text(text, task)
    
    def listen_for_speech(self, timeout: int = 5) -> dict:
        """
        Listen for speech input.
        
        Args:
            timeout (int): Timeout in seconds
            
        Returns:
            dict: Speech recognition results
        """
        return self.ai_functionality.listen_for_speech(timeout)
    
    def speak_text(self, text: str, voice: str = None) -> bool:
        """
        Convert text to speech.
        
        Args:
            text (str): Text to speak
            voice (str, optional): Voice to use
            
        Returns:
            bool: True if successful
        """
        return self.ai_functionality.speak_text(text, voice)
    
    def create_ai_application(self, app_type: str, config: dict) -> dict:
        """
        Create an AI application.
        
        Args:
            app_type (str): Type of application (chatbot, image_analyzer, text_processor, voice_assistant, automation)
            config (dict): Application configuration
            
        Returns:
            dict: Application creation results
        """
        return self.ai_functionality.create_ai_application(app_type, config)
    
    def list_ai_applications(self) -> list:
        """
        List all created AI applications.
        
        Returns:
            list: List of applications
        """
        return self.ai_functionality.list_applications()
    
    def run_ai_application(self, app_id: str, function: str, *args, **kwargs) -> any:
        """
        Run a function in an AI application.
        
        Args:
            app_id (str): Application ID
            function (str): Function name to run
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            any: Function result
        """
        return self.ai_functionality.run_application(app_id, function, *args, **kwargs)
    
    def intelligent_computer_control(self, natural_command: str) -> dict:
        """
        Use AI to interpret and execute computer control commands.
        
        Args:
            natural_command (str): Natural language command
            
        Returns:
            dict: Command interpretation and execution results
        """
        return self.ai_functionality.intelligent_computer_control(natural_command)
    
    def generate_code(self, description: str, language: str = "python") -> str:
        """
        Generate code based on description.
        
        Args:
            description (str): Code description
            language (str): Programming language
            
        Returns:
            str: Generated code
        """
        return self.ai_functionality.generate_code(description, language)
    
    def debug_code(self, code: str, error_message: str = None) -> str:
        """
        Debug code using AI.
        
        Args:
            code (str): Code to debug
            error_message (str, optional): Error message
            
        Returns:
            str: Corrected code
        """
        return self.ai_functionality.debug_code(code, error_message)
    
    def create_ai_workflow(self, workflow_description: str) -> dict:
        """
        Create an AI workflow.
        
        Args:
            workflow_description (str): Workflow description
            
        Returns:
            dict: Workflow definition
        """
        return self.ai_functionality.create_ai_workflow(workflow_description)
    
    def execute_ai_workflow(self, workflow: dict, inputs: dict) -> dict:
        """
        Execute an AI workflow.
        
        Args:
            workflow (dict): Workflow definition
            inputs (dict): Input data
            
        Returns:
            dict: Workflow execution results
        """
        return self.ai_functionality.execute_ai_workflow(workflow, inputs)
    
    def get_ai_capabilities(self) -> dict:
        """
        Get available AI capabilities.
        
        Returns:
            dict: Available capabilities
        """
        return self.ai_functionality.get_capabilities()
    
    def check_ai_dependencies(self) -> dict:
        """
        Check if required AI dependencies are available.
        
        Returns:
            dict: Dependency availability status
        """
        return self.ai_functionality.check_dependencies()
    
    def install_ai_dependencies(self, dependencies: list) -> bool:
        """
        Install required AI dependencies.
        
        Args:
            dependencies (list): List of dependencies to install
            
        Returns:
            bool: True if successful
        """
        return self.ai_functionality.install_dependencies(dependencies)
    
    def setup_ai_functionality(self) -> str:
        """
        Interactive setup for AI functionality.
        
        Returns:
            str: Setup results
        """
        # Show prompts showcase first
        print(self.prompts_showcase.show_welcome_message())
        print("\n" + "="*60)
        print("🎯 SAMPLE PROMPTS & EXAMPLES")
        print("="*60)
        
        # Show some sample prompts
        print("\n📁 Computer Control Examples:")
        print("• 'Open my email application and compose a new message'")
        print("• 'Create a new folder called Projects and move all PDF files there'")
        print("• 'Search for Python tutorials on Google and open the first 3 results'")
        
        print("\n🧠 AI Application Examples:")
        print("• 'Create a chatbot that can answer customer questions about our product'")
        print("• 'Build an AI app that can read PDF documents and extract key information'")
        print("• 'Create an application that can identify objects in photos'")
        
        print("\n💻 Code Generation Examples:")
        print("• 'Write a Python function that sorts a list of dictionaries by a specific key'")
        print("• 'Create a web scraper that extracts product information from an e-commerce website'")
        print("• 'Generate code to integrate with a REST API and handle authentication'")
        
        print("\n📝 Content Creation Examples:")
        print("• 'Write a 500-word blog post about the benefits of AI in business'")
        print("• 'Create professional email templates for customer outreach'")
        print("• 'Generate engaging social media posts for a tech company product launch'")
        
        print("\n📊 Data Analysis Examples:")
        print("• 'Analyze monthly sales data and identify trends and recommendations'")
        print("• 'Process customer reviews and extract sentiment and improvement suggestions'")
        print("• 'Build a model to predict customer churn based on usage patterns'")
        
        print("\n⚡ Productivity Examples:")
        print("• 'Automatically categorize emails and draft responses for common inquiries'")
        print("• 'Create an AI assistant that can schedule meetings and manage calendar conflicts'")
        print("• 'Build a system that can prioritize tasks based on deadlines and importance'")
        
        print("\n" + "="*60)
        print("🚀 READY TO GET STARTED?")
        print("="*60)
        print("Now you can proceed to set up your AI provider and start building!")
        
        return "AI functionality showcase completed. Ready for provider setup."
    
    def select_prompt_and_provider(self) -> Optional[Dict[str, Any]]:
        """
        Interactive prompt and provider selection.
        
        Returns:
            dict: Selected prompt and provider information, or None if cancelled
        """
        print("\n🎯 Let's get you started with a specific prompt!")
        print("=" * 60)
        
        try:
            # Select a prompt
            selected_prompt = self.prompts_showcase.select_prompt_interactive()
            if not selected_prompt:
                print("❌ Prompt selection cancelled.")
                return None
            
            print(f"\n✅ Selected: {selected_prompt['name']}")
            print(f"📋 Prompt: {selected_prompt['prompt']}")
            
            # Select a provider
            selected_provider = self.prompts_showcase.select_provider_interactive(selected_prompt)
            if not selected_provider:
                print("❌ Provider selection cancelled.")
                return None
            
            print(f"\n✅ Selected Provider: {selected_provider.upper()}")
            
            # Save the selection
            self.prompts_showcase.save_user_selection(selected_prompt, selected_provider)
            
            # Show setup instructions
            instructions = self.prompts_showcase.get_setup_instructions(selected_prompt, selected_provider)
            print(instructions)
            
            return {
                "prompt": selected_prompt,
                "provider": selected_provider,
                "instructions": instructions
            }
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Selection cancelled.")
            return None
        except Exception as e:
            print(f"\n❌ Error during selection: {e}")
            return None
    
    def get_user_selection(self) -> Optional[Dict[str, Any]]:
        """
        Get the user's saved prompt and provider selection.
        
        Returns:
            dict: User selection or None if not found
        """
        return self.prompts_showcase.get_user_selection()
    
    def mark_setup_completed(self) -> bool:
        """
        Mark the setup as completed.
        
        Returns:
            bool: True if successful
        """
        return self.prompts_showcase.mark_setup_completed()
    
    def show_guided_setup(self) -> str:
        """
        Show a guided setup process that includes prompt and provider selection.
        
        Returns:
            str: Setup status
        """
        print("\n🎯 GUIDED SETUP PROCESS")
        print("=" * 50)
        print("This will help you:")
        print("1. 📋 Pick a specific prompt to work with")
        print("2. 🤖 Choose the best AI provider for your needs")
        print("3. 🔧 Get step-by-step setup instructions")
        print("4. 🚀 Start building immediately")
        
        # Check if user already has a selection
        existing_selection = self.get_user_selection()
        if existing_selection and not existing_selection.get("setup_completed", False):
            print(f"\n📋 You have a previous selection:")
            print(f"   Prompt: {existing_selection['prompt']['name']}")
            print(f"   Provider: {existing_selection['provider'].upper()}")
            
            try:
                use_existing = input("\nUse this selection? (y/n): ").strip().lower()
                if use_existing == 'y':
                    instructions = self.prompts_showcase.get_setup_instructions(
                        existing_selection['prompt'], 
                        existing_selection['provider']
                    )
                    print(instructions)
                    return "Using existing selection"
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Setup cancelled.")
                return "Setup was cancelled"
            except Exception as e:
                print(f"\n❌ Error: {e}")
                return "Setup encountered an error"
        
        # Start new selection process
        try:
            result = self.select_prompt_and_provider()
            if result:
                return "Selection completed successfully"
            else:
                return "Selection was cancelled"
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Setup cancelled.")
            return "Setup was cancelled"
        except Exception as e:
            print(f"\n❌ Error during setup: {e}")
            return "Setup encountered an error"
    
    def set_api_key(self, provider: str, api_key: str) -> bool:
        """
        Set an API key for an AI provider.
        
        Args:
            provider (str): The name of the AI provider
            api_key (str): The API key
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.ai_manager.set_api_key(provider, api_key)
    
    def get_api_key(self, provider: str = None) -> str:
        """
        Get the API key for an AI provider.
        
        Args:
            provider (str, optional): The name of the AI provider. If None, uses the active provider.
            
        Returns:
            str: The API key or None if not found
        """
        return self.ai_manager.get_api_key(provider)
    
    def list_ai_providers(self) -> list:
        """
        List all supported AI providers and their status.
        
        Returns:
            list: A list of provider information dictionaries
        """
        return self.ai_manager.list_providers()
    
    def set_active_ai_provider(self, provider: str) -> bool:
        """
        Set the active AI provider.
        
        Args:
            provider (str): The name of the AI provider
            
        Returns:
            bool: True if successful, False otherwise
        """
        success = self.ai_manager.set_active_provider(provider)
        if success:
            # Update the AI provider in the AI functionality module
            ai_provider = self.ai_manager.get_provider(provider)
            if ai_provider:
                self.ai_functionality.set_ai_provider(ai_provider)
        return success
    
    def get_active_ai_provider(self) -> str:
        """
        Get the name of the active AI provider.
        
        Returns:
            str: The name of the active provider or None if not set
        """
        return self.ai_manager.get_active_provider()
    
    def get_ai_provider(self, provider_name: str = None) -> AIProvider:
        """
        Get an instance of an AI provider.
        
        Args:
            provider_name (str, optional): The name of the provider. If None, uses the active provider.
            
        Returns:
            AIProvider: An instance of the AI provider or None if not available
        """
        provider = self.ai_manager.get_provider(provider_name)
        if provider:
            # Update the AI provider in the AI functionality module
            self.ai_functionality.set_ai_provider(provider)
        return provider
    
    def set_local_model(self, model_path: str = None):
        """
        Set up a local model for inference
        
        Args:
            model_path (str, optional): Path to local model. If None, uses default model.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.using_local_model = True
            
            # Set the provider to local
            self.ai_manager.set_active_provider("local")
            
            # Get the local provider
            local_provider = self.ai_manager.get_provider("local")
            if not local_provider:
                self.logger.error("Failed to initialize local model provider")
                self.using_local_model = False
                return False
                
            # Load the model
            success = local_provider.load_model(model_path)
            if not success:
                self.logger.error("Failed to load local model")
                self.using_local_model = False
                return False
                
            self.logger.info(f"Local model loaded successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error setting up local model: {e}")
            self.using_local_model = False
            return False
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text from a prompt using the active AI provider or local model.
        """
        if self.using_local_model:
            local_provider = self.ai_manager.get_provider("local")
            if not local_provider:
                return "Local model provider not initialized. Please set up a local model first."
            return local_provider.generate_text(prompt, **kwargs)
        else:
            provider = self.get_ai_provider()
            if not provider:
                return "No AI provider available. Please set an API key first."
            try:
                return provider.generate_text(prompt, **kwargs)
            except Exception as e:
                # Detect 401 Unauthorized error
                msg = str(e)
                if ("401" in msg or "unauthorized" in msg.lower() or "invalid_api_key" in msg.lower()) and ("api key" in msg.lower() or "Unauthorized" in msg):
                    print("\n❌ Your API key appears to be invalid or unauthorized.")
                    print("Would you like to update your API key now? (y/n)")
                    try:
                        choice = input("> ").strip().lower()
                        if choice in ["y", "yes"]:
                            if self.reconfigure_ai_provider():
                                print("✅ API key updated. Retrying your request...")
                                return self.generate_text(prompt, **kwargs)
                            else:
                                return "❌ API key update cancelled. Please run 'reconfigure' to update your key."
                        else:
                            return "❌ API key is invalid. Please update it with 'reconfigure' or 'apikey set ...' command."
                    except (KeyboardInterrupt, EOFError):
                        return "❌ API key update cancelled."
                raise

    def generate_chat(self, messages: list, **kwargs) -> str:
        """
        Generate a chat response using the active AI provider or local model.
        """
        if self.using_local_model:
            local_provider = self.ai_manager.get_provider("local")
            if not local_provider:
                return "Local model provider not initialized. Please set up a local model first."
            return local_provider.generate_chat(messages, **kwargs)
        else:
            provider = self.get_ai_provider()
            if not provider:
                return "No AI provider available. Please set an API key first."
            try:
                return provider.generate_chat(messages, **kwargs)
            except Exception as e:
                msg = str(e)
                if ("401" in msg or "unauthorized" in msg.lower() or "invalid_api_key" in msg.lower()) and ("api key" in msg.lower() or "Unauthorized" in msg):
                    print("\n❌ Your API key appears to be invalid or unauthorized.")
                    print("Would you like to update your API key now? (y/n)")
                    try:
                        choice = input("> ").strip().lower()
                        if choice in ["y", "yes"]:
                            if self.reconfigure_ai_provider():
                                print("✅ API key updated. Retrying your request...")
                                return self.generate_chat(messages, **kwargs)
                            else:
                                return "❌ API key update cancelled. Please run 'reconfigure' to update your key."
                        else:
                            return "❌ API key is invalid. Please update it with 'reconfigure' or 'apikey set ...' command."
                    except (KeyboardInterrupt, EOFError):
                        return "❌ API key update cancelled."
                raise
    
    def embed_text(self, text: str, **kwargs) -> list:
        """
        Generate embeddings for text using the active AI provider.
        
        Args:
            text (str): The text to embed
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            list: The embedding vector
        """
        provider = self.get_ai_provider()
        if not provider:
            return []
        
        return provider.embed_text(text, **kwargs)
    
    def transcribe_audio(self, audio_file: str, **kwargs) -> str:
        """
        Transcribe audio to text using the active AI provider.
        
        Args:
            audio_file (str): Path to the audio file
            **kwargs: Additional arguments to pass to the provider
            
        Returns:
            str: The transcribed text
        """
        provider = self.get_ai_provider()
        if not provider:
            return "No AI provider available. Please set an API key first."
        
        return provider.transcribe_audio(audio_file, **kwargs)
    
    def reconfigure_ai_provider(self) -> bool:
        """
        Reconfigure the AI provider by prompting the user to set up API keys.
        
        Returns:
            bool: True if configuration was successful, False otherwise
        """
        try:
            print("\n🔧 AI Provider Reconfiguration")
            print("=" * 40)
            print("Let's set up your AI provider to use AI-powered features.")
            print()
            
            # List available providers
            providers = self.list_ai_providers()
            print("Available AI providers:")
            for i, provider in enumerate(providers, 1):
                status = "✅" if provider["has_key"] else "❌"
                print(f"  {i}. {status} {provider['name']}")
            
            print()
            print("Choose a provider to configure:")
            
            while True:
                try:
                    choice = input("Enter provider number or 'exit' to cancel: ").strip()
                    
                    if choice.lower() in ['exit', 'quit', 'q']:
                        print("Configuration cancelled.")
                        return False
                    
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(providers):
                        selected_provider = providers[choice_num - 1]["name"]
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(providers)}")
                except ValueError:
                    print("Please enter a valid number")
                except (KeyboardInterrupt, EOFError):
                    print("\nConfiguration cancelled.")
                    return False
            
            # Get API key
            print(f"\n🔑 {selected_provider.capitalize()} API Key Setup")
            print("=" * 40)
            print("Get your API key from:")
            
            if selected_provider == "openai":
                print("   https://platform.openai.com/api-keys")
            elif selected_provider == "anthropic":
                print("   https://console.anthropic.com/")
            elif selected_provider == "google":
                print("   https://makersuite.google.com/app/apikey")
            else:
                print(f"   {selected_provider} provider website")
            
            print("\nEnter your API key (or 'exit' to cancel):")
            
            import getpass
            api_key = getpass.getpass("> ")
            
            if api_key.lower() in ['exit', 'quit', 'q']:
                print("Configuration cancelled.")
                return False
            
            if not api_key.strip():
                print("❌ API key cannot be empty.")
                return False
            
            # Set the API key
            if self.set_api_key(selected_provider, api_key):
                # Set as active provider
                if self.set_active_ai_provider(selected_provider):
                    print(f"✅ {selected_provider.capitalize()} configured successfully!")
                    print(f"✅ {selected_provider.capitalize()} is now the active AI provider.")
                    return True
                else:
                    print(f"❌ Failed to set {selected_provider.capitalize()} as active provider.")
                    return False
            else:
                print(f"❌ Failed to configure {selected_provider.capitalize()} API key.")
                return False
                
        except Exception as e:
            print(f"❌ Error during configuration: {e}")
            return False
    
    def check_ai_provider_ready(self) -> bool:
        """
        Check if the AI provider is properly configured and ready to use.
        
        Returns:
            bool: True if AI provider is ready, False otherwise
        """
        active_provider = self.get_active_ai_provider()
        if not active_provider:
            return False
        
        # Check if the provider has a valid API key
        providers = self.list_ai_providers()
        for provider in providers:
            if provider["name"] == active_provider and provider["has_key"]:
                return True
        
        return False


# For testing in terminal
if __name__ == "__main__":
    # Configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create an instance of StableAgents
    agent = StableAgents()
    print("StableAgents initialized successfully!")
    
    # Test memory functions
    agent.add_to_memory("short_term", "test_key", "test_value")
    agent.add_to_memory("long_term", "persistent_key", "persistent_value")
    
    # Display some test messages
    agent.display_messages("# StableAgents Test\nThis is a test of the StableAgents system.")
    
    # Retrieve and display memory contents
    short_term = agent.get_from_memory("short_term")
    long_term = agent.get_from_memory("long_term")
    
    print("\nShort-term memory contents:")
    print(json.dumps(short_term, default=str, indent=2))
    
    print("\nLong-term memory contents:")
    print(json.dumps(long_term, default=str, indent=2))
    
    print(f"\nStableAgents directory: {agent.get_stableagents_directory()}")