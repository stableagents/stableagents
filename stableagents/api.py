#!/usr/bin/env python3
"""
FastAPI-based API for StableAgents.
Provides REST endpoints for AI generation, memory operations, computer control, and desktop app generation.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import logging

from stableagents import StableAgents
from .natural_language_desktop import NaturalLanguageDesktopGenerator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="StableAgents API",
    description="A framework for self healing agents that can run locally and minimize hallucinations",
    version="0.2.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None
desktop_generator = None

def get_agent():
    """Get or create the global agent instance"""
    global agent
    if agent is None:
        agent = StableAgents()
    return agent

def get_desktop_generator():
    """Get or create the global desktop generator instance"""
    global desktop_generator
    if desktop_generator is None:
        desktop_generator = NaturalLanguageDesktopGenerator()
    return desktop_generator

# Request/Response Models
class TextGenerationRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class MemoryRequest(BaseModel):
    memory_type: str
    key: str
    value: Any

class MemoryGetRequest(BaseModel):
    memory_type: str
    key: str

class ComputerControlRequest(BaseModel):
    command: str

class ProviderRequest(BaseModel):
    provider: str
    api_key: str

class DesktopAppRequest(BaseModel):
    description: str
    app_name: Optional[str] = None
    ui_framework: str = "customtkinter"

class CodeGenerationRequest(BaseModel):
    prompt: str
    framework: str = "customtkinter"

class HealthResponse(BaseModel):
    status: str
    version: str
    active_provider: Optional[str] = None
    memory_stats: Dict[str, Any]

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "StableAgents API",
        "version": "0.2.1",
        "docs": "/docs",
        "endpoints": {
            "text_generation": "/generate",
            "chat": "/chat",
            "memory": "/memory",
            "computer_control": "/control",
            "providers": "/providers",
            "desktop_apps": "/desktop",
            "health": "/health"
        }
    }

@app.post("/generate")
async def generate_text(request: TextGenerationRequest):
    """Generate text using AI"""
    try:
        agent = get_agent()
        
        # Set model if provided
        if request.model:
            agent.set_active_ai_provider(request.model)
        
        result = agent.generate_text(
            request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return {
            "success": True,
            "text": result,
            "prompt": request.prompt,
            "model": request.model or agent.get_active_ai_provider()
        }
    except Exception as e:
        logger.error(f"Error in text generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    """Generate chat response"""
    try:
        agent = get_agent()
        
        # Set model if provided
        if request.model:
            agent.set_active_ai_provider(request.model)
        
        # Convert to the format expected by the agent
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        result = agent.generate_chat(
            messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return {
            "success": True,
            "response": result,
            "messages": request.messages,
            "model": request.model or agent.get_active_ai_provider()
        }
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/add")
async def add_memory(request: MemoryRequest):
    """Add data to memory"""
    try:
        agent = get_agent()
        agent.add_to_memory(request.memory_type, request.key, request.value)
        
        return {
            "success": True,
            "message": f"Added to {request.memory_type} memory",
            "key": request.key,
            "value": request.value
        }
    except Exception as e:
        logger.error(f"Error adding to memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memory/get")
async def get_memory(request: MemoryGetRequest):
    """Get data from memory"""
    try:
        agent = get_agent()
        result = agent.get_from_memory(request.memory_type, request.key)
        
        return {
            "success": True,
            "memory_type": request.memory_type,
            "key": request.key,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error getting from memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/control")
async def control_computer(request: ComputerControlRequest):
    """Control computer with natural language"""
    try:
        agent = get_agent()
        result = agent.control_computer(request.command)
        
        return {
            "success": True,
            "command": request.command,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error in computer control: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/providers")
async def list_providers():
    """List available AI providers"""
    try:
        agent = get_agent()
        providers = agent.list_ai_providers()
        
        return {
            "success": True,
            "providers": providers
        }
    except Exception as e:
        logger.error(f"Error listing providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/providers/set")
async def set_provider(request: ProviderRequest):
    """Set AI provider and API key"""
    try:
        agent = get_agent()
        success = agent.set_api_key(request.provider, request.api_key)
        
        if success:
            agent.set_active_ai_provider(request.provider)
            return {
                "success": True,
                "message": f"Set {request.provider} as active provider"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Failed to set API key for {request.provider}")
    except Exception as e:
        logger.error(f"Error setting provider: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# New Desktop App Generation Endpoints

@app.post("/desktop/create")
async def create_desktop_app(request: DesktopAppRequest):
    """Create a desktop application from natural language description"""
    try:
        generator = get_desktop_generator()
        
        result = generator.create_app_from_description(
            description=request.description,
            app_name=request.app_name,
            ui_framework=request.ui_framework
        )
        
        return {
            "success": True,
            "app": result
        }
    except Exception as e:
        logger.error(f"Error creating desktop app: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/desktop/generate-code")
async def generate_code(request: CodeGenerationRequest):
    """Generate specific UI code from a prompt"""
    try:
        generator = get_desktop_generator()
        
        code = generator.generate_code_from_prompt(
            prompt=request.prompt,
            framework=request.framework
        )
        
        return {
            "success": True,
            "code": code,
            "framework": request.framework,
            "prompt": request.prompt
        }
    except Exception as e:
        logger.error(f"Error generating code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/desktop/frameworks")
async def list_desktop_frameworks():
    """List available desktop UI frameworks"""
    try:
        generator = get_desktop_generator()
        
        frameworks = generator.list_frameworks()
        descriptions = generator.get_framework_descriptions()
        
        framework_info = []
        for i, framework in enumerate(frameworks):
            framework_info.append({
                "name": framework,
                "description": descriptions[i] if i < len(descriptions) else ""
            })
        
        return {
            "success": True,
            "frameworks": framework_info
        }
    except Exception as e:
        logger.error(f"Error listing frameworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/desktop/projects")
async def list_desktop_projects():
    """List all generated desktop projects"""
    try:
        generator = get_desktop_generator()
        projects_dir = generator.projects_dir
        
        if not projects_dir.exists():
            return {
                "success": True,
                "projects": []
            }
        
        projects = []
        for project_dir in projects_dir.iterdir():
            if project_dir.is_dir():
                project_info = generator.get_project_info(str(project_dir))
                projects.append(project_info)
        
        return {
            "success": True,
            "projects": projects
        }
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/desktop/run/{project_name}")
async def run_desktop_app(project_name: str):
    """Run a generated desktop application"""
    try:
        generator = get_desktop_generator()
        project_path = generator.projects_dir / project_name
        
        if not project_path.exists():
            raise HTTPException(status_code=404, detail=f"Project {project_name} not found")
        
        success = generator.run_app(str(project_path))
        
        return {
            "success": success,
            "project_name": project_name,
            "message": "Application started successfully" if success else "Failed to start application"
        }
    except Exception as e:
        logger.error(f"Error running desktop app: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        agent = get_agent()
        
        # Get memory stats
        memory_stats = {}
        try:
            # This would need to be implemented in the agent
            memory_stats = {"total_entries": 0, "types": []}
        except:
            pass
        
        return HealthResponse(
            status="healthy",
            version="0.2.1",
            active_provider=agent.get_active_ai_provider(),
            memory_stats=memory_stats
        )
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Get status of all processes and services"""
    try:
        import psutil
        import os
        
        # Get current process info
        current_pid = os.getpid()
        current_process = psutil.Process(current_pid)
        
        # Check if ports are in use
        api_port_in_use = False
        frontend_port_in_use = False
        
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 8000))
            api_port_in_use = result == 0
            sock.close()
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', 3000))
            frontend_port_in_use = result == 0
            sock.close()
        except:
            pass
        
        status = {
            "api_server": {
                "running": api_port_in_use,
                "pid": current_pid if api_port_in_use else None,
                "port": 8000
            },
            "frontend_server": {
                "running": frontend_port_in_use,
                "pid": None,  # Frontend runs in separate process
                "port": 3000
            },
            "renderer": {
                "running": False,  # Would need IPC to check
                "pid": None,
                "port": None
            },
            "system": {
                "uptime": current_process.create_time(),
                "memory_usage": current_process.memory_info().rss,
                "cpu_percent": current_process.cpu_percent()
            }
        }
        
        return {
            "success": True,
            "status": status
        }
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup"""
    logger.info("Starting StableAgents API...")
    get_agent()
    get_desktop_generator()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down StableAgents API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 