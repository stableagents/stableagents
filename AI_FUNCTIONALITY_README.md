# StableAgents AI Functionality

StableAgents now includes comprehensive AI functionality for computer control and AI application creation. This guide covers the new features, setup process, and usage examples.

## 🎯 New Guided Setup Process

StableAgents now offers a **guided setup process** that helps you pick a prompt and select a provider before setting up API keys. This creates a more purposeful and guided experience.

### Quick Start with Guided Setup

```bash
# Start the guided setup process
stableagents guided-setup

# Or explore prompts first
stableagents showcase

# Then start guided setup
stableagents guided-setup
```

### What the Guided Setup Includes

1. **📋 Prompt Selection**: Choose from 6 categories with 30+ sample prompts
2. **🤖 Provider Selection**: Get AI-powered recommendations for the best provider
3. **📋 Setup Instructions**: Step-by-step instructions for your specific combination
4. **🔧 API Key Setup**: Seamless integration with secure API key management

### Prompt Categories Available

- **🖥️ Computer Control**: Automate your computer with natural language
- **🧠 AI Applications**: Build custom AI applications and chatbots
- **💻 Code Generation**: Generate, debug, and optimize code
- **📝 Content Creation**: Create articles, emails, and marketing content
- **📊 Data Analysis**: Analyze data and extract insights
- **⚡ Productivity**: Automate workflows and boost productivity

### Provider Recommendations

The system provides intelligent recommendations based on your prompt:

- **OpenAI (GPT-4, GPT-3.5)**: Fast, general-purpose, good for prototyping
- **Anthropic (Claude)**: Excellent reasoning, long context, safety-focused
- **Google (PaLM, Gemini)**: Competitive pricing, Google ecosystem integration
- **Local Models (GGUF)**: Privacy-focused, offline, no API costs

## 🚀 Getting Started

### Option 1: Guided Setup (Recommended)

```bash
# Start the complete guided setup
stableagents guided-setup
```

This will walk you through:
1. Selecting a prompt from our curated examples
2. Choosing the best AI provider for your needs
3. Getting specific setup instructions
4. Setting up your API keys securely

### Option 2: Explore First, Setup Later

```bash
# Explore prompts and examples
stableagents showcase

# Browse specific categories
stableagents showcase computer_control
stableagents showcase ai_applications
stableagents showcase code_generation

# When ready, start guided setup
stableagents guided-setup
```

### Option 3: Interactive Mode

```bash
# Start interactive mode with new AI commands
stableagents interactive

# Available commands:
# showcase [category] - Show AI functionality examples
# guided-setup - Start guided setup with prompt selection
# select-prompt - Select a prompt and provider
# ai-capabilities - Check available AI capabilities
```

## 📋 Sample Prompts by Category

### Computer Control Examples

**Beginner:**
- "Open my email application and compose a new message"
- "Create a new folder called Projects and move all PDF files there"

**Intermediate:**
- "Search for Python tutorials on Google and open the first 3 results"
- "Take a screenshot of my current desktop and save it to my Pictures folder"

**Advanced:**
- "Monitor my system resources and alert me when CPU usage exceeds 80%"
- "Automatically organize my Downloads folder by file type and date"

### AI Applications Examples

**Beginner:**
- "Create a simple chatbot that can answer basic questions"
- "Build an app that can convert text to speech"

**Intermediate:**
- "Create a chatbot that can answer customer questions about our product"
- "Build an AI app that can read PDF documents and extract key information"

**Advanced:**
- "Create an application that can identify objects in photos"
- "Build a sentiment analysis tool for social media monitoring"

### Code Generation Examples

**Beginner:**
- "Write a Python function that sorts a list of dictionaries by a specific key"
- "Create a simple web scraper that extracts titles from a website"

**Intermediate:**
- "Create a web scraper that extracts product information from an e-commerce website"
- "Generate code to integrate with a REST API and handle authentication"

**Advanced:**
- "Build a machine learning pipeline for text classification"
- "Create a microservice architecture with Docker and Kubernetes"

## 🔧 AI Capabilities

StableAgents includes the following AI capabilities:

### Core AI Features
- ✅ **Text Generation**: Generate text, code, and content
- ✅ **Chat Interface**: Conversational AI interactions
- ✅ **Computer Control**: Natural language computer automation
- ✅ **Memory Management**: Short-term and long-term memory storage

### Advanced AI Features (Optional Dependencies)
- 🔄 **Computer Vision**: Image analysis and object detection
- 🔄 **Speech Recognition**: Convert speech to text
- 🔄 **Speech Synthesis**: Convert text to speech
- 🔄 **Natural Language Processing**: Advanced text analysis
- 🔄 **Machine Learning**: Model training and inference

### AI Application Creation
- ✅ **Custom AI Apps**: Build specialized AI applications
- ✅ **Workflow Automation**: Automate complex tasks
- ✅ **Integration APIs**: Connect with external services
- ✅ **Code Generation**: Generate and debug code

## 🤖 AI Providers

### Supported Providers

1. **OpenAI (GPT-4, GPT-3.5)**
   - **Best for**: General AI tasks, quick prototyping, content creation
   - **Pros**: Fast response times, wide model selection, good documentation
   - **Cons**: Higher cost for GPT-4, rate limits
   - **Cost**: GPT-3.5: ~$0.002/1K tokens, GPT-4: ~$0.03/1K tokens

2. **Anthropic (Claude)**
   - **Best for**: Complex reasoning, code generation, analysis tasks
   - **Pros**: Excellent reasoning, long context windows, safety-focused
   - **Cons**: Slower response times, higher cost
   - **Cost**: Claude: ~$0.008/1K tokens

3. **Google (PaLM, Gemini)**
   - **Best for**: Google ecosystem integration, cost-effective solutions
   - **Pros**: Good performance, competitive pricing, Google services integration
   - **Cons**: Limited model selection, newer to market
   - **Cost**: PaLM: ~$0.001/1K tokens, Gemini: ~$0.002/1K tokens

4. **Local Models (GGUF)**
   - **Best for**: Privacy-sensitive tasks, offline use, learning/experimentation
   - **Pros**: Privacy-focused, no API costs, works offline
   - **Cons**: Limited model quality, requires setup, resource intensive
   - **Cost**: Free (one-time model download)

### Provider Selection Recommendations

The system automatically recommends the best provider based on your prompt:

- **Computer Control**: OpenAI (beginner/intermediate), Anthropic (advanced)
- **AI Applications**: OpenAI (beginner), Anthropic (intermediate/advanced)
- **Code Generation**: OpenAI (beginner), Anthropic (intermediate/advanced)
- **Content Creation**: OpenAI (beginner/intermediate), Anthropic (advanced)
- **Data Analysis**: OpenAI (beginner), Anthropic (intermediate/advanced)
- **Productivity**: OpenAI (beginner), Anthropic (intermediate/advanced)

## 🔐 Secure API Key Management

StableAgents provides secure API key management with three options:

### Option 1: Subscription ($20/month)
- We provide working API keys
- Keys are securely encrypted
- Monthly recurring billing
- Cancel anytime

### Option 2: Bring Your Own Keys
- Use your existing API keys
- Keys are securely encrypted
- No additional cost beyond your API usage

### Option 3: Local Models Only
- Download GGUF models for local inference
- No API keys or payment required
- Works offline, privacy-focused

## 📚 Usage Examples

### Basic AI Interaction

```python
from stableagents import StableAgents

# Initialize agent
agent = StableAgents()

# Generate text
response = agent.generate_text("Write a Python function to sort a list")
print(response)

# Chat with AI
messages = [
    {"role": "user", "content": "Hello, can you help me with Python?"}
]
response = agent.generate_chat(messages)
print(response)
```

### Computer Control

```python
# Control computer with natural language
result = agent.control_computer("Open my email application")
print(result)

result = agent.control_computer("Create a new folder called Projects")
print(result)
```

### AI Application Creation

```python
# Create a custom AI application
app_config = {
    "name": "Customer Service Bot",
    "description": "AI chatbot for customer support",
    "prompts": ["How can I help you today?"],
    "responses": ["I'm here to assist you with any questions."]
}

result = agent.create_ai_application(app_config)
print(result)
```

## 🛠️ Installation and Setup

### Prerequisites

```bash
# Install StableAgents
pip install stableagents

# Or install from source
git clone https://github.com/your-repo/stableagents.git
cd stableagents
pip install -e .
```

### Optional Dependencies

For advanced AI features, install optional dependencies:

```bash
# Computer vision and image processing
pip install opencv-python pillow

# Speech recognition and synthesis
pip install SpeechRecognition pyttsx3

# Machine learning and data analysis
pip install numpy pandas scikit-learn

# Deep learning (optional)
pip install torch tensorflow
```

### Quick Setup

```bash
# Start guided setup
stableagents guided-setup

# Or explore first
stableagents showcase
stableagents guided-setup
```

## 🎯 Demo Scripts

### Guided Setup Demo

```bash
# Run the guided setup demo
python examples/guided_setup_demo.py
```

This demo shows:
- Complete guided setup process
- Prompt selection from categories
- Provider recommendations
- Setup instructions generation

### AI Functionality Demo

```bash
# Run the AI functionality demo
python examples/ai_functionality_demo.py
```

This demo shows:
- All AI capabilities
- Sample prompts and responses
- Computer control examples
- AI application creation

## 🔍 Troubleshooting

### Common Issues

1. **No AI Provider Configured**
   ```bash
   # Set up AI provider
   stableagents guided-setup
   ```

2. **API Key Issues**
   ```bash
   # Check API key status
   stableagents setup
   ```

3. **Missing Dependencies**
   ```bash
   # Install optional dependencies
   pip install -r requirements.txt
   ```

### Getting Help

- Run `stableagents showcase` to explore examples
- Use `stableagents guided-setup` for step-by-step setup
- Check the interactive mode with `stableagents interactive`
- Review the demo scripts in the `examples/` directory

## 🚀 Next Steps

1. **Start with Guided Setup**: `stableagents guided-setup`
2. **Explore Examples**: `stableagents showcase`
3. **Try Interactive Mode**: `stableagents interactive`
4. **Build Your First AI App**: Follow the prompts and examples
5. **Customize and Extend**: Create your own prompts and applications

The guided setup process makes it easy to get started with a specific goal in mind, ensuring you have the right prompt and provider for your needs before setting up API keys. 