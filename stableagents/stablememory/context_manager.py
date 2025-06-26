"""
Context manager for session-based memory organization.
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

from .core import MemoryEntry


class ContextManager:
    """
    Manages context and session-based memory organization.
    
    Provides session tracking, context retrieval, and conversation flow management.
    """
    
    def __init__(self, storage_path: Path):
        """
        Initialize context manager.
        
        Args:
            storage_path: Path to storage directory
        """
        self.storage_path = storage_path
        self.context_file = storage_path / "context.json"
        
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_entries: Dict[str, List[str]] = {}
        
    def load(self):
        """Load context data from storage."""
        try:
            if self.context_file.exists():
                with open(self.context_file, 'r') as f:
                    data = json.load(f)
                    self.sessions = data.get('sessions', {})
                    self.session_entries = data.get('session_entries', {})
        except Exception as e:
            print(f"⚠️  Warning: Could not load context manager: {e}")
    
    def save(self):
        """Save context data to storage."""
        try:
            data = {
                'version': '1.0',
                'last_updated': datetime.now().isoformat(),
                'sessions': self.sessions,
                'session_entries': self.session_entries
            }
            
            with open(self.context_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving context manager: {e}")
    
    def add_context(self, entry: MemoryEntry):
        """
        Add memory entry to context.
        
        Args:
            entry: Memory entry to add
        """
        session_id = entry.session_id
        
        # Initialize session if not exists
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'created_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'entry_count': 0,
                'context_types': set()
            }
        
        # Update session info
        self.sessions[session_id]['last_activity'] = datetime.now().isoformat()
        self.sessions[session_id]['entry_count'] += 1
        self.sessions[session_id]['context_types'].add(entry.context_type)
        
        # Add entry to session
        if session_id not in self.session_entries:
            self.session_entries[session_id] = []
        self.session_entries[session_id].append(entry.id)
        
        # Auto-save
        self.save()
    
    def get_session_context(self, 
                           session_id: str,
                           limit: int = 50) -> List[str]:
        """
        Get context entry IDs for a session.
        
        Args:
            session_id: Session ID
            limit: Maximum number of entries
            
        Returns:
            List of entry IDs in chronological order
        """
        if session_id not in self.session_entries:
            return []
        
        entries = self.session_entries[session_id]
        return entries[-limit:] if limit > 0 else entries
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session information.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session information or None if not found
        """
        if session_id not in self.sessions:
            return None
        
        info = self.sessions[session_id].copy()
        info['context_types'] = list(info['context_types'])
        return info
    
    def get_active_sessions(self, 
                           max_age_hours: int = 24) -> List[str]:
        """
        Get list of active sessions.
        
        Args:
            max_age_hours: Maximum age in hours to consider session active
            
        Returns:
            List of active session IDs
        """
        active_sessions = []
        cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
        
        for session_id, session_info in self.sessions.items():
            try:
                last_activity = datetime.fromisoformat(session_info['last_activity'])
                if last_activity.timestamp() > cutoff_time:
                    active_sessions.append(session_id)
            except:
                # If parsing fails, consider session active
                active_sessions.append(session_id)
        
        return active_sessions
    
    def clear_session(self, session_id: str):
        """
        Clear a session and all its entries.
        
        Args:
            session_id: Session ID to clear
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
        
        if session_id in self.session_entries:
            del self.session_entries[session_id]
        
        self.save()
    
    def merge_sessions(self, 
                      source_session_id: str,
                      target_session_id: str):
        """
        Merge source session into target session.
        
        Args:
            source_session_id: Source session ID
            target_session_id: Target session ID
        """
        if source_session_id not in self.session_entries:
            return
        
        # Move entries
        if target_session_id not in self.session_entries:
            self.session_entries[target_session_id] = []
        
        self.session_entries[target_session_id].extend(
            self.session_entries[source_session_id]
        )
        
        # Merge session info
        if target_session_id not in self.sessions:
            self.sessions[target_session_id] = {
                'created_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'entry_count': 0,
                'context_types': set()
            }
        
        if source_session_id in self.sessions:
            source_info = self.sessions[source_session_id]
            target_info = self.sessions[target_session_id]
            
            # Merge context types
            target_info['context_types'].update(source_info['context_types'])
            
            # Update entry count
            target_info['entry_count'] += source_info['entry_count']
            
            # Use most recent activity
            source_activity = datetime.fromisoformat(source_info['last_activity'])
            target_activity = datetime.fromisoformat(target_info['last_activity'])
            if source_activity > target_activity:
                target_info['last_activity'] = source_info['last_activity']
        
        # Remove source session
        self.clear_session(source_session_id)
    
    def get_conversation_flow(self, 
                             session_id: str,
                             limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get conversation flow for a session.
        
        Args:
            session_id: Session ID
            limit: Maximum number of entries
            
        Returns:
            List of conversation entries with metadata
        """
        entry_ids = self.get_session_context(session_id, limit)
        flow = []
        
        for entry_id in entry_ids:
            # This would need access to the actual memory entries
            # For now, return basic info
            flow.append({
                'entry_id': entry_id,
                'timestamp': None,  # Would be filled from actual entry
                'context_type': None  # Would be filled from actual entry
            })
        
        return flow
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get context manager statistics.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_sessions': len(self.sessions),
            'active_sessions': len(self.get_active_sessions()),
            'total_entries': sum(len(entries) for entries in self.session_entries.values()),
            'context_types': set(),
            'avg_entries_per_session': 0
        }
        
        # Collect context types
        for session_info in self.sessions.values():
            stats['context_types'].update(session_info.get('context_types', set()))
        
        stats['context_types'] = list(stats['context_types'])
        
        # Calculate average entries per session
        if self.sessions:
            stats['avg_entries_per_session'] = stats['total_entries'] / len(self.sessions)
        
        return stats 