# StableAgents Desktop App Generator - API + JavaScript Architecture

This document describes the new architecture where the Python code has been moved into a FastAPI backend, and a modern JavaScript frontend provides the user interface.

## 🏗️ Architecture Overview

### Backend (Python API)
- **FastAPI Server**: Handles all AI generation, desktop app creation, and project management
- **Natural Language Desktop Generator**: Core functionality for creating desktop applications
- **RESTful API**: Clean, documented endpoints for all operations

### Frontend (JavaScript)
- **Modern Web Interface**: Beautiful, responsive UI built with HTML, CSS, and JavaScript
- **Tailwind CSS**: Modern styling framework for professional appearance
- **Real-time Updates**: Live preview and status updates during app generation

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install fastapi uvicorn google-genai customtkinter

# Or install from requirements
pip install -r requirements.txt
```

### 2. Start the Application

```bash
# Start both API and frontend servers
python start_desktop_generator.py
```

This will start:
- **API Server**: http://localhost:8000
- **Frontend**: http://localhost:3000

### 3. Open the Application

Open your browser and go to: **http://localhost:3000**

## 📋 API Endpoints

### Desktop App Generation

#### Create Desktop App
```http
POST /desktop/create
Content-Type: application/json

{
  "description": "Create a modern calculator with scientific functions",
  "app_name": "SmartCalculator",
  "ui_framework": "customtkinter"
}
```

#### Generate Code
```http
POST /desktop/generate-code
Content-Type: application/json

{
  "prompt": "Create a login form with validation",
  "framework": "customtkinter"
}
```

#### List Frameworks
```http
GET /desktop/frameworks
```

#### List Projects
```http
GET /desktop/projects
```

#### Run Project
```http
POST /desktop/run/{project_name}
```

### AI Generation

#### Text Generation
```http
POST /generate
Content-Type: application/json

{
  "prompt": "Write a short poem about AI",
  "max_tokens": 100,
  "temperature": 0.7
}
```

#### Chat
```http
POST /chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "max_tokens": 100
}
```

### Memory Operations

#### Add to Memory
```http
POST /memory/add
Content-Type: application/json

{
  "memory_type": "user_preferences",
  "key": "favorite_color",
  "value": "blue"
}
```

#### Get from Memory
```http
POST /memory/get
Content-Type: application/json

{
  "memory_type": "user_preferences",
  "key": "favorite_color"
}
```

### Computer Control

#### Control Computer
```http
POST /control
Content-Type: application/json

{
  "command": "What is the current time?"
}
```

### Provider Management

#### List Providers
```http
GET /providers
```

#### Set Provider
```http
POST /providers/set
Content-Type: application/json

{
  "provider": "gemini",
  "api_key": "your-api-key-here"
}
```

### Health Check

#### API Health
```http
GET /health
```

## 🎨 Frontend Features

### Main Interface
- **App Description Form**: Natural language input for describing your desktop app
- **Framework Selection**: Choose from CustomTkinter, Tkinter, or PyQt
- **Live Preview**: Real-time status updates during generation
- **Project Management**: View and manage all generated projects

### Additional Features
- **Code Generation**: Generate specific UI components from descriptions
- **Project History**: View all previously generated applications
- **Framework Information**: Learn about supported UI frameworks
- **API Key Management**: Set and manage your Gemini API key
- **Health Monitoring**: Check API server status

### User Experience
- **Modern Design**: Clean, professional interface with Tailwind CSS
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Real-time Feedback**: Loading states, success/error messages
- **Modal Dialogs**: Clean, focused interactions
- **Notifications**: Toast notifications for user feedback

## 🔧 Development

### Running Servers Separately

#### API Server Only
```bash
python -m stableagents.api_server
```

#### Frontend Server Only
```bash
cd frontend
python server.py
```

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (Alternative docs)

### File Structure
```
stableagents/
├── api.py                    # FastAPI application with all endpoints
├── api_server.py            # Server startup script
├── natural_language_desktop.py  # Core desktop generation logic
└── ...

frontend/
├── index.html               # Main HTML file
├── js/
│   └── app.js              # Main JavaScript application
└── server.py               # Frontend HTTP server

start_desktop_generator.py  # Combined startup script
```

## 🎯 Usage Examples

### 1. Create a Calculator App

1. Open http://localhost:3000
2. Enter description: "Create a modern calculator with scientific functions, dark mode, and history"
3. Choose framework: CustomTkinter
4. Click "Generate Desktop App"
5. Wait for generation to complete
6. Click "Run App" to start the application

### 2. Generate Code Components

1. Click "Code Generation" button
2. Enter description: "Create a login form with username and password fields"
3. Choose framework: CustomTkinter
4. Click "Generate Code"
5. Copy the generated code to clipboard

### 3. Manage Projects

1. Click "Project Management" button
2. View all generated projects
3. Click "Run" to start any project
4. Click "View" to see project details

## 🔒 Security

### API Key Management
- API keys are stored securely in the backend
- Frontend never stores API keys locally
- Keys are encrypted and managed by the Python backend

### CORS Configuration
- Frontend server includes CORS headers
- API server allows cross-origin requests
- Secure communication between frontend and backend

## 🐛 Troubleshooting

### Common Issues

#### API Server Won't Start
```bash
# Check if port 8000 is available
lsof -i :8000

# Check dependencies
pip install fastapi uvicorn google-genai
```

#### Frontend Won't Load
```bash
# Check if port 3000 is available
lsof -i :3000

# Check if frontend files exist
ls -la frontend/
```

#### API Key Issues
1. Get a Gemini API key from: https://makersuite.google.com/app/apikey
2. Click "API Key" button in the frontend
3. Enter your API key
4. Test with the "Health" button

#### App Generation Fails
1. Check API key is set correctly
2. Ensure internet connection for Gemini API
3. Try a simpler description
4. Check API usage limits

### Debug Mode

#### API Server Debug
```bash
# Run with debug logging
python -m stableagents.api_server --log-level debug
```

#### Frontend Debug
- Open browser developer tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API request issues

## 📈 Performance

### Optimization Features
- **Async API Calls**: Non-blocking requests for better UX
- **Caching**: Project list caching for faster loading
- **Error Handling**: Graceful error recovery
- **Loading States**: Visual feedback during operations

### Scalability
- **Stateless API**: Easy to scale horizontally
- **Modular Frontend**: Component-based architecture
- **RESTful Design**: Standard HTTP patterns

## 🔄 Migration from CLI

### Old CLI Commands → New API Endpoints

| CLI Command | API Endpoint | Frontend Action |
|-------------|--------------|-----------------|
| `stableagents-ai natural-desktop create` | `POST /desktop/create` | Fill form and submit |
| `stableagents-ai natural-desktop demo` | `POST /desktop/create` | Use demo description |
| `stableagents-ai natural-desktop frameworks` | `GET /desktop/frameworks` | Click "Framework Info" |
| `stableagents-ai natural-desktop code` | `POST /desktop/generate-code` | Click "Code Generation" |

### Benefits of New Architecture
- **Better UX**: Modern web interface vs command line
- **Real-time Feedback**: Live updates during generation
- **Project Management**: Visual project browser
- **Cross-platform**: Works on any device with a browser
- **Extensible**: Easy to add new features

## 🎉 Success!

The new API + JavaScript architecture provides:

- ✅ **Modern User Interface**: Beautiful, responsive web frontend
- ✅ **Scalable Backend**: FastAPI-based REST API
- ✅ **Real-time Updates**: Live status and progress feedback
- ✅ **Project Management**: Visual project browser and management
- ✅ **Cross-platform**: Works on Windows, macOS, and Linux
- ✅ **Extensible**: Easy to add new features and frameworks
- ✅ **Professional**: Production-ready architecture

**Start creating amazing desktop applications with the new web interface! 🚀** 