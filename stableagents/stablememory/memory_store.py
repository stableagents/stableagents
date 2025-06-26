"""
Memory store for local storage with embedding support.
"""

import json
import pickle
import numpy as np
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

from .core import MemoryEntry


class MemoryStore:
    """
    Local memory store with embedding-based search capabilities.
    
    Provides persistent storage and semantic search for memory entries.
    """
    
    def __init__(self, storage_path: Path):
        """
        Initialize memory store.
        
        Args:
            storage_path: Path to storage directory
        """
        self.storage_path = storage_path
        self.memory_file = storage_path / "memories.json"
        self.embeddings_file = storage_path / "embeddings.pkl"
        
        self.entries: Dict[str, MemoryEntry] = {}
        self.embeddings: Dict[str, np.ndarray] = {}
        
    def load(self):
        """Load memory entries from storage."""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    for entry_data in data.get('entries', []):
                        entry = MemoryEntry(**entry_data)
                        self.entries[entry.id] = entry
                
                # Load embeddings if available
                if self.embeddings_file.exists():
                    with open(self.embeddings_file, 'rb') as f:
                        self.embeddings = pickle.load(f)
                        
        except Exception as e:
            print(f"⚠️  Warning: Could not load memory store: {e}")
    
    def save(self):
        """Save memory entries to storage."""
        try:
            # Save entries
            data = {
                'version': '1.0',
                'last_updated': datetime.now().isoformat(),
                'entries': [entry.__dict__ for entry in self.entries.values()]
            }
            
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Save embeddings
            if self.embeddings:
                with open(self.embeddings_file, 'wb') as f:
                    pickle.dump(self.embeddings, f)
                    
        except Exception as e:
            print(f"❌ Error saving memory store: {e}")
    
    def add_entry(self, entry: MemoryEntry):
        """
        Add a memory entry.
        
        Args:
            entry: Memory entry to add
        """
        self.entries[entry.id] = entry
        
        # Store embedding if available
        if entry.embedding:
            self.embeddings[entry.id] = np.array(entry.embedding)
        
        # Auto-save
        self.save()
    
    def get_entry(self, entry_id: str) -> Optional[MemoryEntry]:
        """
        Get a memory entry by ID.
        
        Args:
            entry_id: Entry ID
            
        Returns:
            MemoryEntry or None if not found
        """
        return self.entries.get(entry_id)
    
    def get_all_entries(self) -> List[MemoryEntry]:
        """
        Get all memory entries.
        
        Returns:
            List of all memory entries
        """
        return list(self.entries.values())
    
    def semantic_search(self, 
                       query_embedding: List[float],
                       limit: int = 10,
                       context_type: Optional[str] = None,
                       tags: Optional[List[str]] = None) -> List[MemoryEntry]:
        """
        Search memory using semantic similarity.
        
        Args:
            query_embedding: Query embedding vector
            limit: Maximum number of results
            context_type: Filter by context type
            tags: Filter by tags
            
        Returns:
            List of relevant memory entries
        """
        if not self.embeddings:
            return []
        
        query_vector = np.array(query_embedding)
        similarities = []
        
        for entry_id, embedding in self.embeddings.items():
            entry = self.entries.get(entry_id)
            if not entry:
                continue
            
            # Apply filters
            if context_type and entry.context_type != context_type:
                continue
            if tags and not any(tag in entry.tags for tag in tags):
                continue
            
            # Calculate cosine similarity
            similarity = np.dot(query_vector, embedding) / (
                np.linalg.norm(query_vector) * np.linalg.norm(embedding)
            )
            similarities.append((similarity, entry))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in similarities[:limit]]
    
    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[MemoryEntry]:
        """
        Search memory by tags.
        
        Args:
            tags: Tags to search for
            limit: Maximum number of results
            
        Returns:
            List of matching memory entries
        """
        results = []
        
        for entry in self.entries.values():
            if any(tag in entry.tags for tag in tags):
                results.append(entry)
                if len(results) >= limit:
                    break
        
        return results
    
    def search_by_context_type(self, context_type: str, limit: int = 10) -> List[MemoryEntry]:
        """
        Search memory by context type.
        
        Args:
            context_type: Context type to search for
            limit: Maximum number of results
            
        Returns:
            List of matching memory entries
        """
        results = []
        
        for entry in self.entries.values():
            if entry.context_type == context_type:
                results.append(entry)
                if len(results) >= limit:
                    break
        
        return results
    
    def clear_session(self, session_id: str):
        """
        Clear all entries for a specific session.
        
        Args:
            session_id: Session ID to clear
        """
        entries_to_remove = []
        
        for entry_id, entry in self.entries.items():
            if entry.session_id == session_id:
                entries_to_remove.append(entry_id)
        
        for entry_id in entries_to_remove:
            del self.entries[entry_id]
            if entry_id in self.embeddings:
                del self.embeddings[entry_id]
        
        self.save()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get memory store statistics.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_entries': len(self.entries),
            'entries_with_embeddings': len(self.embeddings),
            'context_types': {},
            'tags': {},
            'sessions': set()
        }
        
        for entry in self.entries.values():
            # Count context types
            stats['context_types'][entry.context_type] = stats['context_types'].get(entry.context_type, 0) + 1
            
            # Count tags
            for tag in entry.tags:
                stats['tags'][tag] = stats['tags'].get(tag, 0) + 1
            
            # Collect sessions
            stats['sessions'].add(entry.session_id)
        
        stats['sessions'] = len(stats['sessions'])
        return stats 