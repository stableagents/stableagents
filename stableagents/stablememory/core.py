"""
Core StableMemory implementation with Model Context Protocol (MCP) integration.
"""

import json
import time
import uuid
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

from .mcp_client import MCPClient
from .memory_store import MemoryStore
from .context_manager import ContextManager


@dataclass
class MemoryEntry:
    """A single memory entry with MCP-compatible structure."""
    id: str
    content: str
    metadata: Dict[str, Any]
    timestamp: float
    session_id: str
    context_type: str
    embedding: Optional[List[float]] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.embedding is None:
            self.embedding = []


class StableMemory:
    """
    StableMemory - Persistent memory system with MCP integration.
    
    Provides structured memory storage, retrieval, and context management
    for AI agents using Model Context Protocol standards.
    """
    
    def __init__(self, 
                 storage_path: Optional[str] = None,
                 mcp_server_url: Optional[str] = None,
                 enable_embeddings: bool = True):
        """
        Initialize StableMemory with MCP integration.
        
        Args:
            storage_path: Path to store memory data (default: ~/.stableagents/memory)
            mcp_server_url: MCP server URL for external memory services
            enable_embeddings: Whether to enable semantic search via embeddings
        """
        self.storage_path = Path(storage_path or "~/.stableagents/memory").expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.memory_store = MemoryStore(self.storage_path)
        self.context_manager = ContextManager(self.storage_path)
        self.mcp_client = MCPClient(mcp_server_url) if mcp_server_url else None
        
        self.enable_embeddings = enable_embeddings
        self.current_session_id = str(uuid.uuid4())
        
        # Load existing memory
        self._load_memory()
    
    def _load_memory(self):
        """Load existing memory from storage."""
        try:
            self.memory_store.load()
            self.context_manager.load()
        except Exception as e:
            print(f"⚠️  Warning: Could not load existing memory: {e}")
    
    def add_memory(self, 
                   content: str,
                   context_type: str = "general",
                   metadata: Optional[Dict[str, Any]] = None,
                   tags: Optional[List[str]] = None) -> str:
        """
        Add a new memory entry.
        
        Args:
            content: The memory content
            context_type: Type of context (e.g., "conversation", "task", "knowledge")
            metadata: Additional metadata
            tags: Tags for categorization
            
        Returns:
            Memory entry ID
        """
        memory_id = str(uuid.uuid4())
        
        entry = MemoryEntry(
            id=memory_id,
            content=content,
            metadata=metadata or {},
            timestamp=time.time(),
            session_id=self.current_session_id,
            context_type=context_type,
            tags=tags or []
        )
        
        # Generate embedding if enabled
        if self.enable_embeddings:
            try:
                entry.embedding = self._generate_embedding(content)
            except Exception as e:
                print(f"⚠️  Warning: Could not generate embedding: {e}")
        
        # Store memory
        self.memory_store.add_entry(entry)
        
        # Update context
        self.context_manager.add_context(entry)
        
        return memory_id
    
    def get_memory(self, 
                   memory_id: str) -> Optional[MemoryEntry]:
        """
        Retrieve a specific memory entry.
        
        Args:
            memory_id: ID of the memory entry
            
        Returns:
            MemoryEntry or None if not found
        """
        return self.memory_store.get_entry(memory_id)
    
    def search_memory(self, 
                      query: str,
                      limit: int = 10,
                      context_type: Optional[str] = None,
                      tags: Optional[List[str]] = None) -> List[MemoryEntry]:
        """
        Search memory using semantic similarity.
        
        Args:
            query: Search query
            limit: Maximum number of results
            context_type: Filter by context type
            tags: Filter by tags
            
        Returns:
            List of relevant memory entries
        """
        if not self.enable_embeddings:
            # Fallback to text-based search
            return self._text_search(query, limit, context_type, tags)
        
        try:
            query_embedding = self._generate_embedding(query)
            return self.memory_store.semantic_search(
                query_embedding, limit, context_type, tags
            )
        except Exception as e:
            print(f"⚠️  Warning: Semantic search failed, falling back to text search: {e}")
            return self._text_search(query, limit, context_type, tags)
    
    def _text_search(self, 
                     query: str,
                     limit: int,
                     context_type: Optional[str],
                     tags: Optional[List[str]]) -> List[MemoryEntry]:
        """Fallback text-based search."""
        results = []
        query_lower = query.lower()
        
        for entry in self.memory_store.get_all_entries():
            # Apply filters
            if context_type and entry.context_type != context_type:
                continue
            if tags and not any(tag in entry.tags for tag in tags):
                continue
            
            # Check if query matches content or tags
            if (query_lower in entry.content.lower() or
                any(query_lower in tag.lower() for tag in entry.tags)):
                results.append(entry)
            
            if len(results) >= limit:
                break
        
        return results
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using MCP or local model."""
        if self.mcp_client:
            return self.mcp_client.generate_embedding_sync(text)
        else:
            # Fallback to local embedding model
            return self._local_embedding(text)
    
    def _local_embedding(self, text: str) -> List[float]:
        """Generate embedding using local model."""
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embedding = model.encode(text).tolist()
            return embedding
        except ImportError:
            # Simple fallback: hash-based embedding
            import hashlib
            hash_obj = hashlib.md5(text.encode())
            return [float(int(hash_obj.hexdigest()[:8], 16)) / 1e8]
    
    def get_context(self, 
                    session_id: Optional[str] = None,
                    limit: int = 50) -> List[MemoryEntry]:
        """
        Get context for current or specified session.
        
        Args:
            session_id: Session ID (default: current session)
            limit: Maximum number of context entries
            
        Returns:
            List of context memory entries
        """
        session = session_id or self.current_session_id
        entry_ids = self.context_manager.get_session_context(session, limit)
        return [self.memory_store.get_entry(entry_id) for entry_id in entry_ids if self.memory_store.get_entry(entry_id)]
    
    def add_conversation_memory(self, 
                               user_input: str,
                               agent_response: str,
                               metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add conversation memory with user input and agent response.
        
        Args:
            user_input: User's input
            agent_response: Agent's response
            metadata: Additional metadata
            
        Returns:
            Memory entry ID
        """
        content = f"User: {user_input}\nAgent: {agent_response}"
        return self.add_memory(
            content=content,
            context_type="conversation",
            metadata=metadata or {},
            tags=["conversation", "interaction"]
        )
    
    def add_task_memory(self, 
                        task_description: str,
                        task_result: str,
                        metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add task execution memory.
        
        Args:
            task_description: Description of the task
            task_result: Result or outcome of the task
            metadata: Additional metadata
            
        Returns:
            Memory entry ID
        """
        content = f"Task: {task_description}\nResult: {task_result}"
        return self.add_memory(
            content=content,
            context_type="task",
            metadata=metadata or {},
            tags=["task", "execution"]
        )
    
    def add_knowledge_memory(self, 
                            knowledge_content: str,
                            source: Optional[str] = None,
                            tags: Optional[List[str]] = None) -> str:
        """
        Add knowledge or information memory.
        
        Args:
            knowledge_content: The knowledge content
            source: Source of the knowledge
            tags: Tags for categorization
            
        Returns:
            Memory entry ID
        """
        metadata = {"source": source} if source else {}
        return self.add_memory(
            content=knowledge_content,
            context_type="knowledge",
            metadata=metadata,
            tags=tags or ["knowledge"]
        )
    
    def get_relevant_context(self, 
                            query: str,
                            limit: int = 5) -> List[MemoryEntry]:
        """
        Get relevant context for a query.
        
        Args:
            query: The query to find relevant context for
            limit: Maximum number of context entries
            
        Returns:
            List of relevant memory entries
        """
        return self.search_memory(query, limit, context_type="conversation")
    
    def clear_session_memory(self, session_id: Optional[str] = None):
        """Clear memory for a specific session."""
        session = session_id or self.current_session_id
        self.memory_store.clear_session(session)
        self.context_manager.clear_session(session)
    
    def export_memory(self, 
                      filepath: str,
                      format: str = "json") -> bool:
        """
        Export memory to file.
        
        Args:
            filepath: Path to export file
            format: Export format ("json" or "csv")
            
        Returns:
            True if successful
        """
        try:
            if format == "json":
                return self._export_json(filepath)
            elif format == "csv":
                return self._export_csv(filepath)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def _export_json(self, filepath: str) -> bool:
        """Export memory as JSON."""
        data = {
            "version": "1.0",
            "export_date": datetime.now().isoformat(),
            "entries": [asdict(entry) for entry in self.memory_store.get_all_entries()]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    
    def _export_csv(self, filepath: str) -> bool:
        """Export memory as CSV."""
        import csv
        
        entries = self.memory_store.get_all_entries()
        if not entries:
            return True
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(entries[0]).keys())
            writer.writeheader()
            for entry in entries:
                writer.writerow(asdict(entry))
        return True
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        memory_stats = self.memory_store.get_stats()
        context_stats = self.context_manager.get_stats()
        
        return {
            **memory_stats,
            **context_stats,
            "mcp_available": self.mcp_client is not None,
            "embeddings_enabled": self.enable_embeddings
        } 