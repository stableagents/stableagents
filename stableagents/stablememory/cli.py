"""
CLI commands for StableMemory integration.
"""

import argparse
from typing import Optional, List
from pathlib import Path

from .core import StableMemory


def memory_add_command(args):
    """Add memory entry via CLI."""
    try:
        memory = StableMemory()
        
        memory_id = memory.add_memory(
            content=args.content,
            context_type=args.context_type,
            metadata={"source": "cli", "tags": args.tags.split(",") if args.tags else []},
            tags=args.tags.split(",") if args.tags else []
        )
        
        print(f"✅ Memory added with ID: {memory_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error adding memory: {e}")
        return False


def memory_search_command(args):
    """Search memory via CLI."""
    try:
        memory = StableMemory()
        
        results = memory.search_memory(
            query=args.query,
            limit=args.limit,
            context_type=args.context_type,
            tags=args.tags.split(",") if args.tags else None
        )
        
        if not results:
            print("🔍 No memory entries found.")
            return True
        
        print(f"🔍 Found {len(results)} memory entries:")
        print("=" * 60)
        
        for i, entry in enumerate(results, 1):
            print(f"\n{i}. ID: {entry.id}")
            print(f"   Content: {entry.content[:100]}{'...' if len(entry.content) > 100 else ''}")
            print(f"   Type: {entry.context_type}")
            print(f"   Tags: {', '.join(entry.tags)}")
            print(f"   Timestamp: {entry.timestamp}")
            print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Error searching memory: {e}")
        return False


def memory_stats_command(args):
    """Show memory statistics via CLI."""
    try:
        memory = StableMemory()
        stats = memory.get_memory_stats()
        
        print("📊 Memory Statistics")
        print("=" * 30)
        print(f"Total Entries: {stats.get('total_entries', 0)}")
        print(f"Total Sessions: {stats.get('total_sessions', 0)}")
        print(f"Active Sessions: {stats.get('active_sessions', 0)}")
        print(f"Entries with Embeddings: {stats.get('entries_with_embeddings', 0)}")
        print(f"MCP Available: {stats.get('mcp_available', False)}")
        print(f"Embeddings Enabled: {stats.get('embeddings_enabled', False)}")
        
        if stats.get('context_types'):
            print(f"\nContext Types:")
            for context_type, count in stats['context_types'].items():
                print(f"  {context_type}: {count}")
        
        if stats.get('tags'):
            print(f"\nTop Tags:")
            sorted_tags = sorted(stats['tags'].items(), key=lambda x: x[1], reverse=True)[:10]
            for tag, count in sorted_tags:
                print(f"  {tag}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error getting memory stats: {e}")
        return False


def memory_clear_command(args):
    """Clear memory via CLI."""
    try:
        memory = StableMemory()
        
        if args.session_id:
            memory.clear_session_memory(args.session_id)
            print(f"✅ Cleared memory for session: {args.session_id}")
        else:
            # Clear current session
            memory.clear_session_memory()
            print("✅ Cleared memory for current session")
        
        return True
        
    except Exception as e:
        print(f"❌ Error clearing memory: {e}")
        return False


def memory_export_command(args):
    """Export memory via CLI."""
    try:
        memory = StableMemory()
        
        success = memory.export_memory(args.filepath, args.format)
        
        if success:
            print(f"✅ Memory exported to: {args.filepath}")
        else:
            print("❌ Memory export failed")
        
        return success
        
    except Exception as e:
        print(f"❌ Error exporting memory: {e}")
        return False


def main():
    """Main CLI entry point for StableMemory."""
    parser = argparse.ArgumentParser(
        description="StableMemory CLI - Model Context Protocol Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  stablememory add "User asked about Python programming" --type conversation --tags python,programming
  stablememory search "Python programming" --limit 5
  stablememory stats
  stablememory clear --session-id abc123
  stablememory export memory.json --format json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add memory entry')
    add_parser.add_argument('content', help='Memory content')
    add_parser.add_argument('--type', '--context-type', dest='context_type', 
                           default='general', help='Context type')
    add_parser.add_argument('--tags', help='Comma-separated tags')
    add_parser.set_defaults(func=memory_add_command)
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search memory')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=10, help='Maximum results')
    search_parser.add_argument('--type', '--context-type', dest='context_type', 
                              help='Filter by context type')
    search_parser.add_argument('--tags', help='Comma-separated tags to filter by')
    search_parser.set_defaults(func=memory_search_command)
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show memory statistics')
    stats_parser.set_defaults(func=memory_stats_command)
    
    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear memory')
    clear_parser.add_argument('--session-id', help='Session ID to clear (default: current)')
    clear_parser.set_defaults(func=memory_clear_command)
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export memory')
    export_parser.add_argument('filepath', help='Export file path')
    export_parser.add_argument('--format', choices=['json', 'csv'], default='json', 
                              help='Export format')
    export_parser.set_defaults(func=memory_export_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    success = args.func(args)
    exit(0 if success else 1)


if __name__ == "__main__":
    main() 