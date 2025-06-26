# Natural Language Desktop App Generator

Create beautiful, modern desktop applications using natural language descriptions and Google Gemini AI. No Electron required - generate native Python desktop apps with modern UI frameworks.

## 🚀 Features

- **Natural Language to Desktop App**: Describe your app in plain English and let AI generate the code
- **Modern UI Frameworks**: Support for CustomTkinter, Tkinter, and PyQt
- **Google Gemini Integration**: Powered by Google's latest AI model
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **No Electron**: Lightweight, native Python applications
- **Code Generation**: Generate specific UI components from descriptions
- **Interactive CLI**: User-friendly command-line interface

## 🎯 Quick Start

### 1. Install Dependencies

```bash
# Install the required packages
pip install google-generativeai customtkinter stableagents-ai

# Or install from requirements
pip install -r requirements.txt
```

### 2. Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key for use in the application

### 3. Create Your First App

```bash
# Interactive mode
stableagents-ai natural-desktop

# Or use specific commands
stableagents-ai natural-desktop create
stableagents-ai natural-desktop demo
```

## 📝 Usage Examples

### Interactive App Creation

```bash
stableagents-ai natural-desktop create
```

This will guide you through:
1. Entering your Gemini API key
2. Describing your application
3. Choosing a UI framework
4. Generating the complete application

### Create a Calculator App

```python
from stableagents.natural_language_desktop import NaturalLanguageDesktopGenerator

# Initialize with your Gemini API key
generator = NaturalLanguageDesktopGenerator("your-gemini-api-key")

# Create a calculator app
result = generator.create_app_from_description(
    description="""
    Create a modern calculator application with:
    - Beautiful modern UI with dark/light mode toggle
    - Basic arithmetic operations (add, subtract, multiply, divide)
    - Scientific functions (sin, cos, tan, log, sqrt, power)
    - Memory functions (store, recall, clear)
    - History of calculations
    - Keyboard shortcuts for all operations
    """,
    app_name="SmartCalculator",
    ui_framework="customtkinter"
)

if result.get("success"):
    print(f"App created at: {result['project_path']}")
    print(f"To run: cd {result['project_path']} && python main.py")
```

### Generate Code Components

```python
# Generate a login form
code = generator.generate_code_from_prompt(
    prompt="Create a login form with username and password fields, validation, and a submit button",
    framework="customtkinter"
)
print(code)
```

## 🎨 Supported UI Frameworks

### 1. CustomTkinter (Recommended)
- **Description**: Modern and beautiful custom tkinter widgets
- **Pros**: Modern look, Easy to use, Built on tkinter, Beautiful widgets
- **Cons**: Newer library, Limited widget set
- **Best for**: Modern applications, Professional look, Quick development

### 2. Tkinter
- **Description**: Python's standard GUI toolkit
- **Pros**: Built-in, Simple, Cross-platform, No installation needed
- **Cons**: Basic styling, Limited widgets, Outdated look
- **Best for**: Simple applications, Quick prototypes, Learning

### 3. PyQt
- **Description**: Qt framework for Python
- **Pros**: Professional, Rich widgets, Modern look, Extensive features
- **Cons**: Complex, Large size, License considerations
- **Best for**: Professional applications, Complex UIs, Commercial software

## 🔧 CLI Commands

### Create Application
```bash
# Interactive app creation
stableagents-ai natural-desktop create

# Create demo application
stableagents-ai natural-desktop demo
```

### List Frameworks
```bash
# Show supported UI frameworks
stableagents-ai natural-desktop frameworks
```

### Setup Instructions
```bash
# Show setup instructions
stableagents-ai natural-desktop setup
```

### Code Generation
```bash
# Generate code from description
stableagents-ai natural-desktop code
```

## 📋 Example Applications

### Task Manager
```python
description = """
Build a comprehensive task management application with:
- Modern, intuitive user interface with dark/light theme
- Add, edit, and delete tasks with descriptions
- Task categories and priority levels (High, Medium, Low)
- Due dates and reminders
- Mark tasks as complete/incomplete with visual indicators
- Search and filter tasks by category, priority, or status
- Data persistence - save tasks to local file
- Export tasks to different formats (CSV, JSON)
- Statistics and progress tracking
- Responsive design for different window sizes
"""
```

### File Manager
```python
description = """
Create a modern file manager application with:
- Dual-pane interface for easy file navigation
- File and folder operations (copy, move, delete, rename)
- File preview for common formats (text, images)
- Search functionality with filters
- File size and modification date display
- Drag and drop support
- Context menus for right-click operations
- Keyboard shortcuts for common actions
- Bookmark favorite locations
- Modern UI with icons and visual feedback
"""
```

### Calculator
```python
description = """
Create a modern calculator application with:
- Beautiful modern UI with dark/light mode toggle
- Basic arithmetic operations (add, subtract, multiply, divide)
- Scientific functions (sin, cos, tan, log, sqrt, power)
- Memory functions (store, recall, clear)
- History of calculations
- Keyboard shortcuts for all operations
- Responsive design that works on different screen sizes
- Professional animations and transitions
"""
```

## 🏗️ Project Structure

Generated applications follow this structure:
```
YourApp/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── project.json        # Project metadata
└── ui/                 # UI components (if any)
    └── components.py
```

## 🔍 Generated Features

The AI analyzes your description and extracts features like:
- User interface elements (buttons, forms, lists, etc.)
- Core functionality (data storage, calculations, file operations, etc.)
- User interactions (clicking, typing, dragging, etc.)
- Visual elements (charts, images, animations, etc.)

## 🚀 Running Generated Apps

```bash
# Navigate to the project directory
cd /path/to/generated/app

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🔧 Advanced Usage

### Custom API Key Management

```python
import os

# Set environment variable
os.environ["GEMINI_API_KEY"] = "your-api-key"

# Or pass directly to constructor
generator = NaturalLanguageDesktopGenerator("your-api-key")
```

### Custom Output Directory

```python
from pathlib import Path

result = generator.create_app_from_description(
    description="Your app description",
    output_dir=Path("/custom/output/path")
)
```

### Framework-Specific Code Generation

```python
# Generate PyQt code
pyqt_code = generator.generate_code_from_prompt(
    prompt="Create a data visualization widget",
    framework="pyqt"
)

# Generate Tkinter code
tkinter_code = generator.generate_code_from_prompt(
    prompt="Create a settings dialog",
    framework="tkinter"
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Gemini API Key Error**
   ```
   Error: Google Gemini not available. Install with: pip install google-generativeai
   ```
   **Solution**: Install the required package: `pip install google-generativeai`

2. **CustomTkinter Not Found**
   ```
   ModuleNotFoundError: No module named 'customtkinter'
   ```
   **Solution**: Install CustomTkinter: `pip install customtkinter`

3. **API Key Invalid**
   ```
   Error: Invalid API key
   ```
   **Solution**: Get a valid API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

generator = NaturalLanguageDesktopGenerator("your-api-key")
```

## 📚 API Reference

### NaturalLanguageDesktopGenerator

#### `__init__(gemini_api_key=None)`
Initialize the generator with a Gemini API key.

#### `create_app_from_description(description, app_name=None, ui_framework="customtkinter", output_dir=None)`
Create a desktop application from a natural language description.

**Parameters:**
- `description` (str): Natural language description of the app
- `app_name` (str, optional): Name for the application
- `ui_framework` (str): UI framework to use
- `output_dir` (Path, optional): Output directory

**Returns:**
- `Dict[str, Any]`: Result with success status and project information

#### `generate_code_from_prompt(prompt, code_type="python", framework="customtkinter")`
Generate code from a natural language prompt.

**Parameters:**
- `prompt` (str): Natural language description of the code needed
- `code_type` (str): Type of code to generate
- `framework` (str): Framework to use

**Returns:**
- `str`: Generated code

#### `list_supported_frameworks()`
List supported UI frameworks with descriptions.

**Returns:**
- `List[Dict[str, Any]]`: List of framework information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for providing the AI capabilities
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI framework
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the base GUI toolkit

## 📞 Support

- **Documentation**: [https://docs.stableagents.dev](https://docs.stableagents.dev)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

**Happy coding! 🎉**

Create amazing desktop applications with the power of natural language and AI. 