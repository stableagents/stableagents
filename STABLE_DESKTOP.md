# Stable Desktop - AI-Powered Desktop Software Creation

Stable Desktop is a powerful tool that uses GPT to automatically generate desktop applications. Create professional desktop software with natural language descriptions and AI-powered code generation.

## 🚀 Features

- **AI-Powered Code Generation**: Use GPT to automatically generate desktop application code
- **Multiple UI Frameworks**: Support for Tkinter, CustomTkinter, PyQt, Kivy, and more
- **Project Management**: Create, build, run, and manage desktop applications
- **Cross-Platform**: Generate applications that work on Windows, macOS, and Linux
- **Professional Templates**: Pre-built templates for common application types
- **Easy Deployment**: Build executables and distribute your applications

## 📦 Installation

Stable Desktop is included with stableagents-ai. Install it with:

```bash
pip install stableagents-ai
```

Or install from source:

```bash
git clone https://github.com/your-repo/stableagents
cd stableagents
pip install -e .
```

## 🎯 Quick Start

### 1. Setup AI Provider

First, configure your AI provider for code generation:

```bash
stableagents-ai setup
```

### 2. Create Your First App

Create a simple calculator application:

```bash
stableagents-ai stable-desktop create "My Calculator" "A basic calculator with arithmetic operations" --framework tkinter --features "Addition" "Subtraction" "Multiplication" "Division"
```

### 3. Run Your App

```bash
cd stable_desktop_projects/my_calculator
python main.py
```

### 4. Build for Distribution

```bash
stableagents-ai stable-desktop build stable_desktop_projects/my_calculator
```

## 🛠️ Command Reference

### Create Application

```bash
stableagents-ai stable-desktop create <app_name> <description> [options]
```

**Options:**
- `--framework`: UI framework (tkinter, customtkinter, pyqt, kivy)
- `--features`: List of features to include
- `--output-dir`: Custom output directory

**Examples:**

```bash
# Simple calculator
stableagents-ai stable-desktop create "Calculator" "Basic arithmetic calculator" --framework tkinter

# Modern task manager
stableagents-ai stable-desktop create "Task Manager" "Modern task management app" --framework customtkinter --features "Add tasks" "Mark complete" "Dark mode"

# Professional data viewer
stableagents-ai stable-desktop create "Data Viewer" "Professional data visualization tool" --framework pyqt --features "CSV import" "Charts" "Export"
```

### List Projects

```bash
stableagents-ai stable-desktop list
```

### Build Application

```bash
stableagents-ai stable-desktop build <project_path>
```

### Run Application

```bash
stableagents-ai stable-desktop run <project_path>
```

### List Frameworks

```bash
stableagents-ai stable-desktop frameworks
```

## 🎨 Supported UI Frameworks

### Tkinter (Built-in)
- **Pros**: Built-in, simple, cross-platform, no installation needed
- **Cons**: Basic styling, limited widgets, outdated look
- **Best for**: Simple applications, quick prototypes, learning

### CustomTkinter
- **Pros**: Modern look, easy to use, built on tkinter, beautiful widgets
- **Cons**: Newer library, limited widget set, external dependency
- **Best for**: Modern applications, professional look, easy development

### PyQt
- **Pros**: Professional, rich widgets, modern look, extensive features
- **Cons**: Complex, large size, license considerations, steep learning curve
- **Best for**: Complex applications, professional software, rich interfaces

### Kivy
- **Pros**: Modern, touch-friendly, cross-platform, mobile support
- **Cons**: Learning curve, different from traditional GUIs, complex setup
- **Best for**: Touch applications, mobile-like interfaces, modern apps

## 📱 Application Examples

### Calculator App
```bash
stableagents-ai stable-desktop create "Calculator" "A basic calculator with arithmetic operations" --framework tkinter --features "Addition" "Subtraction" "Multiplication" "Division" "Clear function"
```

### Task Manager
```bash
stableagents-ai stable-desktop create "Task Manager" "A modern task management application" --framework customtkinter --features "Add tasks" "Mark complete" "Delete tasks" "Modern UI" "Dark mode support"
```

### File Organizer
```bash
stableagents-ai stable-desktop create "File Organizer" "Organize files by type and date" --framework pyqt --features "File browsing" "Auto organization" "Batch operations" "Progress tracking"
```

### Note Taking App
```bash
stableagents-ai stable-desktop create "Note Taker" "Simple note taking application" --framework customtkinter --features "Create notes" "Save to file" "Search notes" "Rich text"
```

## 🔧 Advanced Usage

### Custom Project Structure

You can specify a custom output directory:

```bash
stableagents-ai stable-desktop create "My App" "Description" --output-dir /path/to/custom/directory
```

### Multiple Features

Add multiple features to your application:

```bash
stableagents-ai stable-desktop create "Advanced App" "Description" --features "Feature 1" "Feature 2" "Feature 3" "Feature 4"
```

### Building Executables

Build your application into an executable:

```bash
stableagents-ai stable-desktop build stable_desktop_projects/my_app
```

This creates a distributable executable in the `build` directory.

## 🎯 Best Practices

### 1. Choose the Right Framework
- **Beginners**: Start with Tkinter (built-in)
- **Modern Apps**: Use CustomTkinter
- **Professional Apps**: Use PyQt
- **Touch Apps**: Use Kivy

### 2. Write Clear Descriptions
Be specific about what your app should do:

```bash
# Good
stableagents-ai stable-desktop create "Budget Tracker" "Track income and expenses with categories, monthly reports, and data visualization"

# Less specific
stableagents-ai stable-desktop create "Budget App" "Track money"
```

### 3. Specify Features
List the key features you want:

```bash
stableagents-ai stable-desktop create "App Name" "Description" --features "User authentication" "Data persistence" "Export to CSV" "Charts and graphs"
```

### 4. Test and Iterate
1. Create your app
2. Run it to test functionality
3. Modify the generated code if needed
4. Rebuild and test again

## 🐛 Troubleshooting

### AI Provider Not Configured
```
❌ AI setup failed. Stable Desktop requires an AI provider for code generation.
```
**Solution**: Run `stableagents-ai setup` to configure your AI provider.

### Framework Not Available
```
❌ Framework 'customtkinter' not available - Missing dependencies: customtkinter
```
**Solution**: Install the required framework:
```bash
pip install customtkinter
```

### Build Errors
```
❌ Build failed: PyInstaller not available
```
**Solution**: Install PyInstaller:
```bash
pip install pyinstaller
```

### Import Errors
```
❌ Error importing stable desktop modules
```
**Solution**: Ensure stableagents-ai is properly installed:
```bash
pip install --upgrade stableagents-ai
```

## 📚 Examples and Demos

Run the interactive demo:

```bash
python examples/stable_desktop_demo.py
```

This demo showcases:
- Creating simple applications
- Listing available frameworks
- Creating modern applications
- Managing projects

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check this README and the main stableagents documentation
- **Issues**: Report bugs and request features on GitHub
- **Community**: Join our community discussions

## 🎉 Success Stories

Share your success stories! We'd love to hear about the applications you've created with Stable Desktop.

---

**Happy coding! 🚀**

Create amazing desktop applications with the power of AI and Stable Desktop. 