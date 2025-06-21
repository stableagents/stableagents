#!/usr/bin/env python3
"""
Simple API server for StableAgents.
Run this script to start the API server.
"""
import uvicorn
from stableagents.api import app

if __name__ == "__main__":
    print("Starting StableAgents API Server...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    ) 