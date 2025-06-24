# AI-Powered Computer Control

## Overview

The AI-Powered Computer Control feature allows you to control your computer using natural language commands that are interpreted by an AI model. Instead of learning specific commands, you can simply describe what you want to do in plain English.

## How It Works

1. **Natural Language Input**: You provide a natural language command like "open youtube and play the latest bruno mars song"
2. **AI Interpretation**: The AI model analyzes your command and breaks it down into specific computer actions
3. **Action Execution**: The system executes the interpreted actions using the computer control module
4. **Result Feedback**: You get detailed feedback about what actions were performed

## Usage

### Command Line Interface

```bash
# Basic usage
stableagents-ai ai-control "your natural language command"

# Examples
stableagents-ai ai-control "open youtube and search for the latest bruno mars song"
stableagents-ai ai-control "take a screenshot and save it to desktop"
stableagents-ai ai-control "search for python tutorials and open the first result"
stableagents-ai ai-control "check system performance and show memory usage"
```

### Interactive Mode

```bash
# Start interactive mode
stableagents-ai interactive

# Then use the ai-control command
> ai-control open youtube and play the latest bruno mars song
> ai-control search for python tutorials
> ai-control take a screenshot
```

## Supported Actions

The AI can interpret and execute the following types of actions:

### Web and Media
- **Open websites**: "open youtube", "browse google.com"
- **Search the web**: "search for python tutorials"
- **Media services**: "open spotify and play relaxing music"
- **Media search**: "search for bruno mars latest song on youtube"

### System Operations
- **Screenshots**: "take a screenshot"
- **System monitoring**: "check system performance", "show memory usage"
- **Process control**: "list running processes", "kill process chrome"

### File Operations
- **Create files/folders**: "create a new folder called ai_demo"
- **File management**: "list files in current directory"
- **File operations**: "copy file.txt to desktop"

### Applications
- **Open applications**: "open calculator", "open notepad"
- **Application control**: "close chrome", "minimize all windows"

### Automation
- **Mouse control**: "click at coordinates 100,200"
- **Keyboard input**: "type hello world"
- **Terminal commands**: "execute ls -la"

## Example Commands

### Media and Entertainment
```bash
ai-control "open youtube and search for the latest bruno mars song"
ai-control "open spotify and play some relaxing music"
ai-control "search for cooking tutorials on youtube"
ai-control "open netflix and browse new releases"
```

### Productivity
```bash
ai-control "search for python tutorials and open the first result"
ai-control "create a new folder called project_docs on desktop"
ai-control "take a screenshot and save it to desktop"
ai-control "check system performance and show memory usage"
```

### System Management
```bash
ai-control "list all running processes"
ai-control "check disk space usage"
ai-control "monitor CPU and memory usage"
ai-control "close all chrome windows"
```

### File Operations
```bash
ai-control "create a new text file called notes.txt"
ai-control "list files in the current directory"
ai-control "search for files containing 'python'"
ai-control "copy important.txt to backup folder"
```

## Technical Details

### AI Interpretation Process

1. **Command Analysis**: The AI receives your natural language command
2. **Action Mapping**: The AI maps your command to available computer actions
3. **Parameter Extraction**: The AI extracts relevant parameters from your command
4. **Action Planning**: The AI creates a plan of specific actions to execute
5. **Execution**: Each action is executed using the computer control module

### Available Actions

The system supports these core actions:

- `open [application]` - Open applications
- `browse [url]` - Open websites
- `search [query]` - Search the web
- `open_media_service [service] [action]` - Open media services
- `search_and_play_media [query] [service]` - Search and play media
- `execute [command]` - Run terminal commands
- `click [coordinates]` - Mouse clicks
- `type [text]` - Keyboard input
- `screenshot` - Take screenshots
- `monitor [type]` - System monitoring
- `process [action]` - Process control
- `create [type] [path]` - Create files/folders

### Error Handling

The system includes comprehensive error handling:

- **AI Provider Issues**: Graceful fallback if AI provider is unavailable
- **Action Failures**: Individual action failures don't stop the entire sequence
- **Invalid Commands**: Clear error messages for unsupported commands
- **System Errors**: Detailed error reporting for debugging

## Requirements

### AI Provider
You need a configured AI provider (OpenAI, Anthropic, Google, or local models) to use this feature.

### Dependencies
- `pyautogui` for mouse and keyboard control
- `Pillow` for screenshot functionality
- `psutil` for system monitoring
- `webbrowser` for web operations

## Safety Features

- **Confirmation for Destructive Actions**: Some actions may require confirmation
- **Error Boundaries**: Actions are isolated to prevent system-wide failures
- **Logging**: All actions are logged for debugging and audit purposes
- **Rate Limiting**: Built-in delays prevent overwhelming the system

## Troubleshooting

### Common Issues

1. **"AI provider not available"**
   - Configure an AI provider using `stableagents-ai setup`

2. **"Unknown action"**
   - The AI couldn't interpret your command
   - Try rephrasing or using simpler language

3. **"Failed to execute action"**
   - Check if the required application or service is available
   - Verify permissions for the requested operation

4. **"JSON parsing error"**
   - The AI response wasn't properly formatted
   - Try the command again or rephrase it

### Debug Mode

Enable verbose logging to see detailed information:

```bash
stableagents-ai -v ai-control "your command"
```

## Future Enhancements

Planned improvements include:

- **Voice Control**: Speech-to-text input for commands
- **Context Awareness**: Remember previous actions and context
- **Learning**: Improve interpretation based on usage patterns
- **Advanced Automation**: Complex multi-step workflows
- **Integration**: Connect with more applications and services

## Examples in Action

Here's what happens when you run a complex command:

```bash
$ stableagents-ai ai-control "open youtube and search for the latest bruno mars song"

🤖 Using AI to interpret: 'open youtube and search for the latest bruno mars song'
⏳ Processing...

🤖 AI Interpretation: The user wants to open YouTube and search for Bruno Mars' latest song
📋 Planned Actions: 1

🔧 Action 1: Open YouTube and search for Bruno Mars latest song
   ✅ Result: Opened youtube - search bruno mars latest song

🎯 Summary: Successfully executed 1 actions for 'open youtube and search for the latest bruno mars song'
```

This demonstrates how the AI:
1. Understands the natural language command
2. Maps it to specific actions (opening YouTube with search)
3. Executes the action
4. Provides clear feedback about what was done

The AI-powered computer control makes complex computer operations accessible through simple, natural language commands! 