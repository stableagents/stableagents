# Multi-Process Architecture - StableAgents Desktop App Generator

This document describes the multi-process architecture implementation, similar to Electron's main and renderer process model, for the StableAgents Desktop App Generator.

## 🏗️ Architecture Overview

### Process Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Process                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   API Server    │  │   Frontend      │                  │
│  │   Process       │  │   Server        │                  │
│  │                 │  │   Process       │                  │
│  │ • FastAPI       │  │ • HTTP Server   │                  │
│  │ • AI Generation │  │ • Static Files  │                  │
│  │ • App Creation  │  │ • CORS Support  │                  │
│  └─────────────────┘  └─────────────────┘                  │
│         │                       │                          │
│         └──────────────┬────────┘                          │
│                        │                                   │
│         ┌──────────────▼──────────────┐                    │
│         │      Renderer Process       │                    │
│         │                             │                    │
│         │ • User Interface            │                    │
│         │ • Web-based or Native       │                    │
│         │ • IPC Communication         │                    │
│         │ • Process Management        │                    │
│         └─────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

### Communication Flow

1. **Main ↔ Renderer**: IPC (Inter-Process Communication)
2. **Renderer ↔ Frontend**: HTTP (Web interface)
3. **Frontend ↔ API**: HTTP (REST API)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Required dependencies
pip install fastapi uvicorn google-genai requests

# Optional: For native window support
pip install pywebview
```

### 2. Start Multi-Process Architecture

```bash
python start_multi_process.py
```

This will start:
- **Main Process**: Manages all sub-processes
- **API Server**: http://localhost:8000
- **Frontend Server**: http://localhost:3000
- **Renderer Process**: Opens UI window

## 📋 Process Details

### Main Process (`main_process.py`)

**Responsibilities:**
- Process lifecycle management
- IPC (Inter-Process Communication) handling
- System-level operations
- Graceful shutdown coordination

**Key Features:**
- Starts and monitors all sub-processes
- Handles IPC messages from renderer
- Manages process health and restart
- Coordinates system shutdown

**Code Structure:**
```python
class MainProcess:
    def __init__(self):
        self.api_process = None
        self.renderer_process = None
        self.frontend_process = None
        self.ipc_queue = mp.Queue()
    
    def start(self):
        # Start all sub-processes
        self._start_api_server()
        self._start_frontend_server()
        self._start_renderer_process()
        self._start_ipc_handler()
```

### Renderer Process (`renderer_process.py`)

**Responsibilities:**
- User interface management
- Communication with main process
- Web interface hosting
- User interaction handling

**Key Features:**
- Native window (webview) or browser fallback
- IPC communication with main process
- Frontend server integration
- Process monitoring and health checks

**Code Structure:**
```python
class RendererProcess:
    def __init__(self):
        self.main_process_queue = None
        self.response_queue = None
        self.window = None
    
    def start(self):
        # Set up IPC communication
        self._setup_ipc()
        # Start UI (native or browser)
        self._start_ui()
        # Handle IPC messages
        self._start_ipc_handler()
```

### API Server Process

**Responsibilities:**
- REST API endpoints
- AI generation and app creation
- Project management
- Health monitoring

**Key Features:**
- FastAPI-based REST server
- Desktop app generation
- Code generation
- Project listing and management

### Frontend Server Process

**Responsibilities:**
- Static file serving
- CORS support
- Web interface hosting

**Key Features:**
- HTTP server for frontend files
- CORS headers for API communication
- Development-friendly configuration

## 🔗 IPC Communication

### Message Types

```python
# Process Management
'start_api'      # Start API server
'stop_api'       # Stop API server
'restart_api'    # Restart API server
'start_renderer' # Start renderer process
'stop_renderer'  # Stop renderer process
'restart_renderer' # Restart renderer process

# Status and Monitoring
'get_status'     # Get process status

# Application Operations
'create_app'     # Create desktop application
'list_projects'  # List generated projects
'run_project'    # Run specific project
```

### Message Format

```python
{
    'type': 'message_type',
    'data': {
        # Message-specific data
    },
    'response_queue': queue  # For responses
}
```

### Example Usage

```python
# Send message from renderer to main
response = renderer.send_to_main('create_app', {
    'description': 'Create a calculator app',
    'app_name': 'MyCalculator',
    'framework': 'customtkinter'
})

# Handle response
if response and response.get('success'):
    print("App created successfully!")
```

## 🎯 Benefits

### 1. Process Isolation
- **UI crashes don't affect backend**: If the renderer process crashes, the API server continues running
- **Independent process management**: Each process can be restarted independently
- **Resource isolation**: Memory and CPU usage are separated

### 2. Security
- **Sandboxed renderer**: UI process runs in a restricted environment
- **Limited system access**: Renderer process has minimal system permissions
- **Controlled communication**: All inter-process communication is explicit

### 3. Scalability
- **Easy to add processes**: New processes can be added without affecting existing ones
- **Load distribution**: Different processes can run on different cores
- **Modular architecture**: Each process has a specific responsibility

### 4. Reliability
- **Automatic monitoring**: Main process monitors all sub-processes
- **Graceful degradation**: If one process fails, others continue
- **Restart capability**: Failed processes can be automatically restarted

### 5. Development
- **Independent debugging**: Each process can be debugged separately
- **Hot reloading**: Individual processes can be restarted during development
- **Clear separation**: Easy to understand which code runs where

## 🔧 Development Workflow

### Starting Individual Processes

```bash
# Start main process only
python main_process.py

# Start renderer process only (for testing)
python renderer_process.py

# Start API server only
python -m stableagents.api_server

# Start frontend server only
cd frontend && python server.py
```

### Debugging

```bash
# Debug main process
python -m pdb main_process.py

# Debug renderer process
python -m pdb renderer_process.py

# Check process status
curl http://localhost:8000/health
```

### Logging

Each process has its own logging configuration:

```python
# Main process logging
logging.getLogger('MainProcess')

# Renderer process logging
logging.getLogger('RendererProcess')

# API server logging
logging.getLogger('uvicorn')
```

## 🛠️ Configuration

### Environment Variables

```bash
# IPC communication
STABLEAGENTS_IPC_QUEUE=queue_reference

# API configuration
STABLEAGENTS_API_HOST=localhost
STABLEAGENTS_API_PORT=8000

# Frontend configuration
STABLEAGENTS_FRONTEND_PORT=3000

# Development mode
STABLEAGENTS_DEBUG=true
```

### Process Configuration

```python
# Main process settings
MAIN_PROCESS_CONFIG = {
    'api_server_timeout': 30,
    'frontend_server_timeout': 20,
    'renderer_timeout': 10,
    'ipc_timeout': 5,
    'restart_attempts': 3
}

# Renderer process settings
RENDERER_PROCESS_CONFIG = {
    'window_width': 1200,
    'window_height': 800,
    'native_window': True,
    'browser_fallback': True
}
```

## 🐛 Troubleshooting

### Common Issues

#### Process Won't Start
```bash
# Check dependencies
pip install fastapi uvicorn google-genai requests

# Check file permissions
chmod +x main_process.py renderer_process.py

# Check port availability
lsof -i :8000
lsof -i :3000
```

#### IPC Communication Issues
```bash
# Check if processes are running
ps aux | grep python

# Check logs for IPC errors
tail -f main_process.log
tail -f renderer_process.log
```

#### UI Not Opening
```bash
# Check if webview is available
pip install pywebview

# Check browser fallback
python -c "import webbrowser; webbrowser.open('http://localhost:3000')"
```

### Debug Mode

```bash
# Enable debug logging
export STABLEAGENTS_DEBUG=true

# Start with verbose output
python start_multi_process.py --verbose
```

## 📈 Performance

### Process Monitoring

```python
# Get process status
status = main_process.get_status()

# Monitor resource usage
for process_name, process_info in status.items():
    print(f"{process_name}: {process_info['running']}")
    if process_info.get('pid'):
        print(f"PID: {process_info['pid']}")
```

### Resource Optimization

- **Memory usage**: Each process has isolated memory
- **CPU usage**: Processes can utilize multiple cores
- **Network**: Efficient HTTP communication between processes
- **Disk I/O**: Shared file system access with proper locking

## 🔄 Migration from Single Process

### Before (Single Process)
```python
# Everything in one process
generator = NaturalLanguageDesktopGenerator()
result = generator.create_app_from_description(...)
```

### After (Multi-Process)
```python
# API call from renderer process
response = requests.post('http://localhost:8000/desktop/create', json={
    'description': 'Create a calculator app',
    'app_name': 'MyCalculator',
    'ui_framework': 'customtkinter'
})
```

### Benefits of Migration
- **Better reliability**: Process isolation prevents crashes
- **Improved performance**: Parallel processing capabilities
- **Enhanced security**: Sandboxed UI process
- **Easier maintenance**: Clear separation of concerns

## 🎉 Success!

The multi-process architecture provides:

- ✅ **Process Isolation**: UI crashes don't affect backend
- ✅ **Security**: Sandboxed renderer process
- ✅ **Scalability**: Easy to add new processes
- ✅ **Reliability**: Automatic process monitoring and restart
- ✅ **Development**: Independent process debugging
- ✅ **Performance**: Multi-core utilization
- ✅ **Maintainability**: Clear separation of concerns

**Start building robust desktop applications with the multi-process architecture! 🚀** 