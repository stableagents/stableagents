# stableagents-ai AI Functionality

stableagents-ai now includes comprehensive AI functionality for computer control and AI application creation. This guide covers the new features, setup process, and usage examples.

## 🎯 New Guided Setup Process

stableagents-ai now offers a **guided setup process** that helps you pick a prompt and select a provider before setting up API keys. This creates a more purposeful and guided experience.

### Quick Start Commands

```bash
# Guided setup with prompt selection and provider choice
stableagents-ai guided-setup

# Explore available prompts and examples
stableagents-ai showcase

# Start guided setup after exploring examples
stableagents-ai guided-setup
```

## 🚀 Getting Started

### 1. Explore Examples First (Recommended)

```bash
stableagents-ai showcase
```

This shows you:
- Available prompt categories
- Example outputs for each category
- Provider comparisons
- Setup instructions

### 2. Guided Setup

```bash
stableagents-ai guided-setup
```

This walks you through:
- Prompt category selection
- Provider comparison and selection
- API key setup
- Security configuration

### 3. Direct Setup (Advanced Users)

```bash
stableagents-ai setup
```

Direct API key setup without the guided flow.

## 📋 Available Commands

### Showcase Commands
```bash
stableagents-ai showcase                    # Show all categories
stableagents-ai showcase computer_control   # Computer control examples
stableagents-ai showcase ai_applications    # AI application examples
stableagents-ai showcase code_generation    # Code generation examples
```

### Setup Commands
```bash
stableagents-ai guided-setup               # Guided setup with examples
stableagents-ai setup                      # Direct API key setup
```

### Usage Commands
```bash
stableagents-ai interactive                # Start interactive mode
```

## 🔧 AI Capabilities

stableagents-ai includes the following AI capabilities:

### 1. Computer Control
- **File Operations**: Create, read, write, and manage files
- **Application Control**: Open, close, and interact with applications
- **Web Automation**: Navigate websites, fill forms, extract data
- **System Monitoring**: Monitor system resources and performance
- **Screenshot & Recording**: Capture screenshots and record screen activity

### 2. AI Application Creation
- **Chatbots**: Create conversational AI assistants
- **Document Processing**: Extract information from PDFs, images, and text
- **Data Analysis**: Analyze datasets and generate insights
- **Content Generation**: Create blog posts, emails, and social media content
- **Code Generation**: Generate and debug code in multiple languages

### 3. Integration Capabilities
- **API Integration**: Connect with external services and APIs
- **Database Operations**: Query and manage databases
- **Cloud Services**: Integrate with AWS, Google Cloud, and Azure
- **Web Scraping**: Extract data from websites automatically

## 🛠️ Setup Process

### Step 1: Explore Capabilities
```bash
stableagents-ai showcase
```

### Step 2: Choose Your Provider
The guided setup helps you choose between:
- **OpenAI**: Fast, reliable, good for general tasks
- **Anthropic**: Excellent reasoning, long context windows
- **Google**: Cost-effective, good integration
- **Local Models**: Privacy-focused, works offline

### Step 3: Configure API Keys
```bash
stableagents-ai setup
```

Choose from:
1. **Monthly Subscription** ($20/month) - We provide working API keys
2. **Bring Your Own Keys** - Use your existing API keys
3. **Local Models** - Download GGUF models for offline use

### Step 4: Start Building
```bash
stableagents-ai interactive
```

## 📝 Example Prompts

### Computer Control
```bash
# Open applications and manage files
"Open my email and compose a new message"
"Create a new folder called 'Projects' and organize my files"
"Search for Python tutorials and open the first 3 results"
```

### AI Applications
```bash
# Create custom AI applications
"Create a chatbot for customer support"
"Build an app that reads PDFs and extracts key information"
"Make an AI assistant that can identify objects in photos"
```

### Code Generation
```bash
# Generate and debug code
"Write a Python function to sort data"
"Create a web scraper for e-commerce sites"
"Generate code to integrate with REST APIs"
```

## 🔐 Security Features

- **Encrypted API Keys**: All API keys are encrypted with your password
- **Secure Storage**: Keys stored locally in encrypted format
- **No Data Collection**: We don't collect or store your data
- **Privacy-First**: Local models available for complete privacy

## 💡 Tips for Success

1. **Start with Examples**: Use `stableagents-ai showcase` to see what's possible
2. **Choose the Right Provider**: Consider your use case and budget
3. **Use Specific Prompts**: Be detailed about what you want to achieve
4. **Iterate and Improve**: Refine your prompts based on results
5. **Combine Capabilities**: Mix computer control with AI generation

## 🆘 Troubleshooting

### Common Issues

**API Key Errors**
- Verify your API key is correct
- Check your account has sufficient credits
- Ensure the provider is supported

**Setup Problems**
- Run `stableagents-ai setup` to reconfigure
- Check the provider's documentation
- Verify your internet connection

**Performance Issues**
- Try a different AI provider
- Use local models for offline work
- Check system resources

### Getting Help

- Run `stableagents-ai showcase` for examples
- Use `stableagents-ai guided-setup` for step-by-step help
- Check the main README.md for more information

## 🚀 Advanced Usage

### Custom Prompts
Save your own prompts for reuse:
```bash
stableagents-ai showcase
# Navigate to custom prompts section
```

### Provider Switching
Switch between providers as needed:
```bash
# In interactive mode
switch-provider openai
switch-provider anthropic
switch-provider local
```

### Memory Management
Use memory to maintain context:
```bash
# Add to memory
memory.add short_term "user_preference" "prefers concise responses"

# Retrieve from memory
memory.get short_term "user_preference"
```

## 📊 Cost Optimization

### Provider Costs (approximate)
- **OpenAI GPT-3.5**: ~$0.002/1K tokens
- **OpenAI GPT-4**: ~$0.03/1K tokens
- **Anthropic Claude**: ~$0.008/1K tokens
- **Google PaLM**: ~$0.001/1K tokens
- **Local Models**: Free (one-time download)

### Tips for Cost Savings
1. Use GPT-3.5 for simple tasks
2. Use local models for development/testing
3. Be specific in prompts to reduce token usage
4. Monitor usage with provider dashboards

## 🔄 Updates and Maintenance

### Keeping Updated
```bash
pip install --upgrade stableagents-ai
```

### Configuration Files
- API keys: `~/.stableagents/`
- Local models: `~/.stableagents/models/`
- Custom prompts: `~/.stableagents/prompts_showcase/`

## 📞 Support

For issues and questions:
- Run `stableagents-ai showcase` for examples
- Use `stableagents-ai guided-setup` for setup help
- Check the main project documentation
- Review the troubleshooting section above

---

**Ready to get started?** Run `stableagents-ai guided-setup` to begin your AI journey!

## 🛠️ Installation

### Option 1: Install from GitHub (Recommended)
```bash
pip install git+https://github.com/jordanplows/stableagents.git
```

### Option 2: Install with Local Models Support
```bash
pip install git+https://github.com/jordanplows/stableagents.git[local]
```

### Option 3: Development Installation
```bash
git clone https://github.com/your-repo/stableagents.git
cd stableagents
pip install -e .
```

## 🚀 Quick Start Guide

### 1. Install stableagents-ai
```bash
pip install git+https://github.com/jordanplows/stableagents.git
```

### 2. Explore Examples
```bash
stableagents-ai showcase
```

### 3. Run Guided Setup
```bash
stableagents-ai guided-setup
```

### 4. Start Building
```bash
stableagents-ai interactive
```

## 📚 Documentation

- **Main Documentation**: [stableagents.dev](https://stableagents.dev)
- **API Reference**: [docs.stableagents.dev](https://docs.stableagents.dev)
- **Examples**: Run `stableagents-ai showcase` to see examples
- **Guides**: Run `stableagents-ai guided-setup` for step-by-step setup

## 🔧 Configuration

### Environment Variables
```bash
export STABLEAGENTS_API_KEY="your-api-key"
export STABLEAGENTS_PROVIDER="openai"
export STABLEAGENTS_MODEL="gpt-4"
```

### Configuration File
```bash
# Create config directory
mkdir -p ~/.stableagents

# Edit configuration
nano ~/.stableagents/config.json
``` 