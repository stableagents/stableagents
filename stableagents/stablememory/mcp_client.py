"""
MCP Client for external memory services integration.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
import aiohttp
import numpy as np


class MCPClient:
    """
    Model Context Protocol (MCP) client for external memory services.
    
    Provides integration with MCP-compatible memory servers for
    distributed memory storage and retrieval.
    """
    
    def __init__(self, server_url: str, timeout: int = 30):
        """
        Initialize MCP client.
        
        Args:
            server_url: URL of the MCP server
            timeout: Request timeout in seconds
        """
        self.server_url = server_url.rstrip('/')
        self.timeout = timeout
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def store_memory(self, 
                          content: str,
                          metadata: Dict[str, Any],
                          embedding: Optional[List[float]] = None) -> str:
        """
        Store memory in MCP server.
        
        Args:
            content: Memory content
            metadata: Memory metadata
            embedding: Optional embedding vector
            
        Returns:
            Memory ID from server
        """
        if not self.session:
            raise RuntimeError("MCP client not initialized. Use async context manager.")
        
        payload = {
            "content": content,
            "metadata": metadata,
            "embedding": embedding
        }
        
        async with self.session.post(f"{self.server_url}/memory/store", json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("memory_id")
            else:
                raise Exception(f"MCP server error: {response.status}")
    
    async def retrieve_memory(self, 
                             query: str,
                             limit: int = 10,
                             filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve memory from MCP server.
        
        Args:
            query: Search query
            limit: Maximum number of results
            filters: Optional filters
            
        Returns:
            List of memory entries
        """
        if not self.session:
            raise RuntimeError("MCP client not initialized. Use async context manager.")
        
        payload = {
            "query": query,
            "limit": limit,
            "filters": filters or {}
        }
        
        async with self.session.post(f"{self.server_url}/memory/retrieve", json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("memories", [])
            else:
                raise Exception(f"MCP server error: {response.status}")
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding using MCP server.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if not self.session:
            raise RuntimeError("MCP client not initialized. Use async context manager.")
        
        payload = {"text": text}
        
        async with self.session.post(f"{self.server_url}/embedding/generate", json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("embedding", [])
            else:
                raise Exception(f"MCP server error: {response.status}")
    
    def generate_embedding_sync(self, text: str) -> List[float]:
        """
        Synchronous wrapper for embedding generation.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self.generate_embedding(text))
        except RuntimeError:
            # No event loop, create new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(self.generate_embedding(text))
            finally:
                loop.close()
    
    async def get_server_info(self) -> Dict[str, Any]:
        """
        Get MCP server information.
        
        Returns:
            Server information
        """
        if not self.session:
            raise RuntimeError("MCP client not initialized. Use async context manager.")
        
        async with self.session.get(f"{self.server_url}/info") as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"MCP server error: {response.status}")
    
    def is_available(self) -> bool:
        """
        Check if MCP server is available.
        
        Returns:
            True if server is reachable
        """
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(self._check_availability())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(self._check_availability())
            finally:
                loop.close()
    
    async def _check_availability(self) -> bool:
        """Check server availability."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.server_url}/health", timeout=5) as response:
                    return response.status == 200
        except:
            return False 