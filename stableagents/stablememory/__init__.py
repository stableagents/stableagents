"""
StableMemory - Model Context Protocol (MCP) Integration for StableAgents

This module provides persistent, structured memory capabilities using MCP standards
for AI agents to maintain context across sessions and interactions.
"""

from .core import StableMemory
from .mcp_client import MCPClient
from .memory_store import MemoryStore
from .context_manager import ContextManager

__version__ = "1.0.0"
__all__ = [
    "StableMemory",
    "MCPClient", 
    "MemoryStore",
    "ContextManager"
] 