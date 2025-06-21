#!/usr/bin/env python3
"""
Example API client for StableAgents.
Demonstrates how to use the REST API endpoints.
"""
import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_providers():
    """Test the providers endpoint"""
    print("Testing providers endpoint...")
    response = requests.get(f"{BASE_URL}/providers")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_text_generation():
    """Test text generation"""
    print("Testing text generation...")
    data = {
        "prompt": "Write a short poem about artificial intelligence",
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = requests.post(f"{BASE_URL}/generate", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_chat():
    """Test chat functionality"""
    print("Testing chat functionality...")
    data = {
        "messages": [
            {"role": "user", "content": "Hello! How are you today?"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = requests.post(f"{BASE_URL}/chat", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_memory():
    """Test memory operations"""
    print("Testing memory operations...")
    
    # Add to memory
    add_data = {
        "memory_type": "user_preferences",
        "key": "favorite_color",
        "value": "blue"
    }
    response = requests.post(f"{BASE_URL}/memory/add", json=add_data)
    print(f"Add memory status: {response.status_code}")
    print(f"Add memory response: {json.dumps(response.json(), indent=2)}")
    
    # Get from memory
    get_data = {
        "memory_type": "user_preferences",
        "key": "favorite_color"
    }
    response = requests.post(f"{BASE_URL}/memory/get", json=get_data)
    print(f"Get memory status: {response.status_code}")
    print(f"Get memory response: {json.dumps(response.json(), indent=2)}")
    print()

def test_computer_control():
    """Test computer control (if available)"""
    print("Testing computer control...")
    data = {
        "command": "What is the current time?"
    }
    response = requests.post(f"{BASE_URL}/control", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def main():
    """Run all API tests"""
    print("StableAgents API Client Example")
    print("=" * 40)
    
    try:
        # Test basic endpoints
        test_health()
        test_providers()
        
        # Test AI functionality (requires API key to be set)
        test_text_generation()
        test_chat()
        
        # Test memory
        test_memory()
        
        # Test computer control
        test_computer_control()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python -m stableagents.api_server")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 