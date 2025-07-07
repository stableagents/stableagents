#!/usr/bin/env python3
"""
Example: Using Multi-Process Architecture - StableAgents Desktop App Generator

This example demonstrates how to:
- Start the multi-process architecture
- Communicate between processes
- Create desktop applications
- Monitor process status
- Handle graceful shutdown
"""

import os
import sys
import time
import signal
import subprocess
import requests
import json
from pathlib import Path
from typing import Dict, Any, Optional

class MultiProcessExample:
    """Example usage of the multi-process architecture."""
    
    def __init__(self):
        self.main_process: Optional[subprocess.Popen] = None
        self.api_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
    
    def start_architecture(self):
        """Start the multi-process architecture or connect to existing one."""
        print("🚀 Connecting to Multi-Process Architecture...")
        
        # Check if services are already running
        try:
            import requests
            response = requests.get('http://localhost:8000/health', timeout=2)
            if response.status_code == 200:
                print("✅ Found existing API server, connecting...")
                return True
        except:
            pass
        
        # If not running, start new instance
        try:
            print("🔄 No existing instance found, starting new one...")
            self.main_process = subprocess.Popen([
                sys.executable, 'main_process.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for startup
            print("⏳ Waiting for processes to start...")
            time.sleep(10)
            
            # Check if main process is still running
            if self.main_process.poll() is not None:
                stdout, stderr = self.main_process.communicate()
                print(f"❌ Main process failed to start")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
            
            print("✅ Multi-process architecture started successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error starting architecture: {e}")
            return False
    
    def wait_for_services(self):
        """Wait for all services to be ready."""
        print("⏳ Waiting for services to be ready...")
        
        services = [
            ('API Server', f'{self.api_url}/health'),
            ('Frontend Server', self.frontend_url),
        ]
        
        for service_name, url in services:
            max_attempts = 30
            attempt = 0
            
            while attempt < max_attempts:
                try:
                    response = requests.get(url, timeout=2)
                    if response.status_code == 200:
                        print(f"✅ {service_name} is ready")
                        break
                except requests.exceptions.RequestException:
                    pass
                
                attempt += 1
                time.sleep(1)
            
            if attempt >= max_attempts:
                print(f"❌ {service_name} failed to start")
                return False
        
        return True
    
    def test_api_endpoints(self):
        """Test various API endpoints."""
        print("\n🔧 Testing API Endpoints...")
        
        endpoints = [
            ('Health Check', 'GET', '/health'),
            ('Frameworks', 'GET', '/desktop/frameworks'),
            ('Projects', 'GET', '/desktop/projects'),
            ('Providers', 'GET', '/ai/providers'),
        ]
        
        for name, method, path in endpoints:
            try:
                url = f"{self.api_url}{path}"
                if method == 'GET':
                    response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ {name}: {len(data) if isinstance(data, list) else 'OK'}")
                else:
                    print(f"❌ {name}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {name}: {e}")
    
    def create_sample_app(self):
        """Create a sample desktop application."""
        print("\n🎨 Creating Sample Desktop Application...")
        
        app_data = {
            "description": "Create a simple calculator app with basic arithmetic operations",
            "app_name": "SampleCalculator",
            "ui_framework": "customtkinter"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/desktop/create",
                json=app_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Sample app created successfully!")
                print(f"📁 Project: {result.get('project_name', 'Unknown')}")
                print(f"📂 Location: {result.get('project_path', 'Unknown')}")
                return result
            else:
                print(f"❌ Failed to create app: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating app: {e}")
            return None
    
    def list_projects(self):
        """List all generated projects."""
        print("\n📁 Listing Generated Projects...")
        
        try:
            response = requests.get(f"{self.api_url}/desktop/projects", timeout=5)
            
            if response.status_code == 200:
                projects = response.json()
                if projects:
                    print(f"Found {len(projects)} projects:")
                    for project in projects:
                        print(f"  📂 {project}")
                else:
                    print("No projects found")
                return projects
            else:
                print(f"❌ Failed to list projects: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error listing projects: {e}")
            return []
    
    def run_project(self, project_name: str):
        """Run a specific project."""
        print(f"\n▶️ Running Project: {project_name}")
        
        try:
            response = requests.post(
                f"{self.api_url}/desktop/run",
                json={"project_name": project_name},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Project {project_name} started successfully!")
                return result
            else:
                print(f"❌ Failed to run project: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error running project: {e}")
            return None
    
    def get_process_status(self):
        """Get status of all processes."""
        print("\n📊 Process Status...")
        
        try:
            response = requests.get(f"{self.api_url}/status", timeout=5)
            
            if response.status_code == 200:
                status = response.json()
                for process_name, process_info in status.items():
                    running = "🟢 Running" if process_info.get('running') else "🔴 Stopped"
                    pid = process_info.get('pid', 'N/A')
                    print(f"  {process_name}: {running} (PID: {pid})")
                return status
            else:
                print(f"❌ Failed to get status: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting status: {e}")
            return None
    
    def test_text_generation(self):
        """Test AI text generation."""
        print("\n🤖 Testing AI Text Generation...")
        
        test_prompt = "Write a simple Python function to calculate the factorial of a number"
        
        try:
            response = requests.post(
                f"{self.api_url}/ai/generate",
                json={
                    "prompt": test_prompt,
                    "provider": "gemini"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Text generation successful!")
                print(f"📝 Generated {len(result.get('text', ''))} characters")
                return result
            else:
                print(f"❌ Text generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error in text generation: {e}")
            return None
    
    def shutdown(self):
        """Shutdown the multi-process architecture."""
        print("\n🛑 Shutting down multi-process architecture...")
        
        if self.main_process:
            try:
                # Send SIGTERM for graceful shutdown
                self.main_process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.main_process.wait(timeout=10)
                    print("✅ Graceful shutdown successful")
                except subprocess.TimeoutExpired:
                    print("⚠️  Force killing processes...")
                    self.main_process.kill()
                    self.main_process.wait()
                    print("✅ Force shutdown successful")
                    
            except Exception as e:
                print(f"❌ Error during shutdown: {e}")

def main():
    """Main example function."""
    print("🎯 Multi-Process Architecture Usage Example")
    print("=" * 60)
    
    # Create example instance
    example = MultiProcessExample()
    
    try:
        # Start the architecture
        if not example.start_architecture():
            print("❌ Failed to start architecture")
            return
        
        # Wait for services
        if not example.wait_for_services():
            print("❌ Services failed to start")
            return
        
        print("\n🎉 Multi-process architecture is ready!")
        
        # Test API endpoints
        example.test_api_endpoints()
        
        # Get process status
        example.get_process_status()
        
        # Test text generation
        example.test_text_generation()
        
        # List existing projects
        projects = example.list_projects()
        
        # Create a sample app
        app_result = example.create_sample_app()
        
        if app_result:
            # List projects again to see the new one
            example.list_projects()
            
            # Optionally run the project
            project_name = app_result.get('project_name')
            if project_name:
                print(f"\n💡 To run the project '{project_name}', uncomment the next line:")
                print(f"# example.run_project('{project_name}')")
        
        print("\n✅ Example completed successfully!")
        print("🌐 You can access the web interface at: http://localhost:3000")
        print("📚 API documentation at: http://localhost:8000/docs")
        
        # Keep running for a while to demonstrate
        print("\n⏳ Keeping architecture running for 30 seconds...")
        print("Press Ctrl+C to stop early")
        
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n🛑 Stopping by user request...")
    
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
    finally:
        # Always shutdown
        example.shutdown()
        print("\n👋 Example completed!")

if __name__ == "__main__":
    main() 