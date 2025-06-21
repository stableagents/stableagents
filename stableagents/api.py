#!/usr/bin/env python3
"""
FastAPI-based API for StableAgents.
Provides REST endpoints for AI generation, memory operations, and computer control.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import logging

from stableagents import StableAgents

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

def get_agent():
    """Get or create the global agent instance"""
    global agent
    if agent is None:
        agent = StableAgents()
    return agent

# Pydantic models for request/response
class TextGenerationRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class MemoryRequest(BaseModel):
    memory_type: str
    key: str
    value: str

class MemoryGetRequest(BaseModel):
    memory_type: str
    key: Optional[str] = None

class ComputerControlRequest(BaseModel):
    command: str

class ProviderRequest(BaseModel):
    provider: str
    api_key: str

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

@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup"""
    logger.info("Starting StableAgents API...")
    get_agent()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down StableAgents API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 