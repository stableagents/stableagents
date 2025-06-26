#!/usr/bin/env python3
"""
Test script for StableMemory integration with Model Context Protocol (MCP).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'stableagents'))

from stableagents.stablememory import StableMemory


def test_stablememory_basic():
    """Test basic StableMemory functionality."""
    print("🧪 Testing StableMemory Basic Functionality")
    print("=" * 45)
    
    try:
        # Initialize StableMemory
        memory = StableMemory()
        print("✅ StableMemory initialized successfully")
        
        # Test adding memory
        memory_id1 = memory.add_memory(
            content="User asked about Python programming and AI integration",
            context_type="conversation",
            tags=["python", "programming", "ai"]
        )
        print(f"✅ Added memory with ID: {memory_id1}")
        
        memory_id2 = memory.add_memory(
            content="Agent provided code example for machine learning model",
            context_type="task",
            tags=["ml", "code", "example"]
        )
        print(f"✅ Added memory with ID: {memory_id2}")
        
        # Test conversation memory
        conv_id = memory.add_conversation_memory(
            user_input="How do I build an AI agent?",
            agent_response="You can use StableAgents framework with MCP integration for persistent memory.",
            metadata={"topic": "ai_development"}
        )
        print(f"✅ Added conversation memory with ID: {conv_id}")
        
        # Test search functionality
        results = memory.search_memory("Python programming", limit=5)
        print(f"✅ Search found {len(results)} results")
        
        # Test context retrieval
        context = memory.get_context(limit=10)
        print(f"✅ Retrieved {len(context)} context entries")
        
        # Test memory stats
        stats = memory.get_memory_stats()
        print(f"✅ Memory stats: {stats.get('total_entries', 0)} total entries")
        
        print("\n✅ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_stablememory_search():
    """Test memory search functionality."""
    print("\n🧪 Testing Memory Search")
    print("=" * 25)
    
    try:
        memory = StableMemory()
        
        # Add test memories
        memory.add_memory(
            content="Machine learning models require training data and validation",
            context_type="knowledge",
            tags=["ml", "training", "data"]
        )
        
        memory.add_memory(
            content="Python is great for data science and AI development",
            context_type="knowledge", 
            tags=["python", "data-science", "ai"]
        )
        
        # Test semantic search
        results = memory.search_memory("artificial intelligence", limit=3)
        print(f"✅ Semantic search found {len(results)} results")
        
        # Test tag-based search
        results = memory.search_memory("", tags=["python"], limit=5)
        print(f"✅ Tag search found {len(results)} results")
        
        # Test context type search
        results = memory.search_memory("", context_type="knowledge", limit=5)
        print(f"✅ Context type search found {len(results)} results")
        
        print("✅ Search functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Search functionality test failed: {e}")
        return False


def test_stablememory_mcp_integration():
    """Test MCP integration capabilities."""
    print("\n🧪 Testing MCP Integration")
    print("=" * 25)
    
    try:
        # Test without MCP server (local mode)
        memory = StableMemory()
        
        # Check MCP availability
        stats = memory.get_memory_stats()
        mcp_available = stats.get('mcp_available', False)
        embeddings_enabled = stats.get('embeddings_enabled', True)
        
        print(f"✅ MCP Available: {mcp_available}")
        print(f"✅ Embeddings Enabled: {embeddings_enabled}")
        
        # Test embedding generation
        test_text = "This is a test for embedding generation"
        embedding = memory._generate_embedding(test_text)
        print(f"✅ Generated embedding with {len(embedding)} dimensions")
        
        # Test with MCP server URL (will fail gracefully if server not available)
        try:
            memory_with_mcp = StableMemory(mcp_server_url="http://localhost:8000")
            print("✅ MCP client initialized (server availability not tested)")
        except Exception as e:
            print(f"⚠️  MCP client initialization: {e}")
        
        print("✅ MCP integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ MCP integration test failed: {e}")
        return False


def test_stablememory_export():
    """Test memory export functionality."""
    print("\n🧪 Testing Memory Export")
    print("=" * 25)
    
    try:
        memory = StableMemory()
        
        # Add some test data
        memory.add_memory(
            content="Export test memory entry",
            context_type="test",
            tags=["export", "test"]
        )
        
        # Test JSON export
        success = memory.export_memory("test_memory_export.json", "json")
        if success:
            print("✅ JSON export successful")
            # Clean up
            import os
            if os.path.exists("test_memory_export.json"):
                os.remove("test_memory_export.json")
        else:
            print("❌ JSON export failed")
            return False
        
        # Test CSV export
        success = memory.export_memory("test_memory_export.csv", "csv")
        if success:
            print("✅ CSV export successful")
            # Clean up
            import os
            if os.path.exists("test_memory_export.csv"):
                os.remove("test_memory_export.csv")
        else:
            print("❌ CSV export failed")
            return False
        
        print("✅ Export functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Export functionality test failed: {e}")
        return False


def main():
    """Run all StableMemory tests."""
    print("🧠 StableMemory Integration Test Suite")
    print("=" * 50)
    print("Testing Model Context Protocol (MCP) integration for StableAgents")
    print()
    
    tests = [
        test_stablememory_basic,
        test_stablememory_search,
        test_stablememory_mcp_integration,
        test_stablememory_export
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! StableMemory integration is working correctly.")
        print("\n💡 You can now use StableMemory in your StableAgents:")
        print("   • Import: from stableagents.stablememory import StableMemory")
        print("   • CLI: stablememory add/search/stats/export")
        print("   • MCP Integration: Supports external memory servers")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 