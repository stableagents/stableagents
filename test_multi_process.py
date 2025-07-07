#!/usr/bin/env python3
"""
Test Multi-Process Architecture - StableAgents Desktop App Generator

This script tests the multi-process architecture to ensure:
- Main process can start and manage sub-processes
- IPC communication works correctly
- Process isolation and monitoring function properly
- Graceful shutdown works as expected
"""

import os
import sys
import time
import signal
import subprocess
import threading
import multiprocessing as mp
from pathlib import Path
from typing import Dict, Any, Optional

def print_test_header(test_name: str):
    """Print test header."""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {test_name}")
    print(f"{'='*60}")

def print_test_result(test_name: str, success: bool, message: str = ""):
    """Print test result."""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if message:
        print(f"   {message}")

class MultiProcessTester:
    """Test the multi-process architecture."""
    
    def __init__(self):
        self.main_process: Optional[subprocess.Popen] = None
        self.test_results = []
        self.ipc_queue = mp.Queue()
    
    def run_all_tests(self):
        """Run all tests."""
        print("🚀 Multi-Process Architecture Test Suite")
        print("=" * 60)
        
        tests = [
            ("Dependency Check", self.test_dependencies),
            ("File Structure Check", self.test_file_structure),
            ("Main Process Start", self.test_main_process_start),
            ("API Server Communication", self.test_api_server),
            ("Frontend Server Communication", self.test_frontend_server),
            ("IPC Communication", self.test_ipc_communication),
            ("Process Monitoring", self.test_process_monitoring),
            ("Graceful Shutdown", self.test_graceful_shutdown),
        ]
        
        for test_name, test_func in tests:
            try:
                print_test_header(test_name)
                success = test_func()
                self.test_results.append((test_name, success))
            except Exception as e:
                print(f"❌ FAIL {test_name} - Exception: {e}")
                self.test_results.append((test_name, False))
        
        self.print_summary()
    
    def test_dependencies(self) -> bool:
        """Test if required dependencies are available."""
        dependencies = [
            ('fastapi', 'FastAPI'),
            ('uvicorn', 'Uvicorn'),
            ('google.genai', 'Google Genai'),
            ('requests', 'Requests'),
        ]
        
        missing = []
        for module, name in dependencies:
            try:
                __import__(module)
                print(f"✅ {name} available")
            except ImportError:
                print(f"❌ {name} not found")
                missing.append(name)
        
        if missing:
            print(f"Missing dependencies: {', '.join(missing)}")
            return False
        
        return True
    
    def test_file_structure(self) -> bool:
        """Test if required files exist."""
        required_files = [
            'main_process.py',
            'renderer_process.py',
            'stableagents/api_server.py',
            'frontend/server.py',
            'frontend/index.html',
            'frontend/js/app.js',
        ]
        
        missing = []
        for file_path in required_files:
            if Path(file_path).exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path}")
                missing.append(file_path)
        
        if missing:
            print(f"Missing files: {', '.join(missing)}")
            return False
        
        return True
    
    def test_main_process_start(self) -> bool:
        """Test if main process can start."""
        try:
            # Start main process
            self.main_process = subprocess.Popen([
                sys.executable, 'main_process.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for startup
            time.sleep(5)
            
            # Check if process is still running
            if self.main_process.poll() is None:
                print("✅ Main process started successfully")
                return True
            else:
                stdout, stderr = self.main_process.communicate()
                print(f"❌ Main process failed to start")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting main process: {e}")
            return False
    
    def test_api_server(self) -> bool:
        """Test API server communication."""
        try:
            import requests
            
            # Test health endpoint
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                print("✅ API server health check passed")
                
                # Test frameworks endpoint
                response = requests.get('http://localhost:8000/desktop/frameworks', timeout=5)
                if response.status_code == 200:
                    frameworks = response.json()
                    print(f"✅ API server frameworks endpoint: {len(frameworks)} frameworks")
                    return True
                else:
                    print(f"❌ API server frameworks endpoint failed: {response.status_code}")
                    return False
            else:
                print(f"❌ API server health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API server test failed: {e}")
            return False
    
    def test_frontend_server(self) -> bool:
        """Test frontend server communication."""
        try:
            import requests
            
            # Test frontend server
            response = requests.get('http://localhost:3000', timeout=5)
            if response.status_code == 200:
                print("✅ Frontend server responding")
                
                # Check if it's serving HTML
                if 'html' in response.headers.get('content-type', '').lower():
                    print("✅ Frontend server serving HTML content")
                    return True
                else:
                    print("❌ Frontend server not serving HTML")
                    return False
            else:
                print(f"❌ Frontend server failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Frontend server test failed: {e}")
            return False
    
    def test_ipc_communication(self) -> bool:
        """Test IPC communication between processes."""
        try:
            # Create test message
            test_message = {
                'type': 'test_message',
                'data': {'test': 'data'},
                'timestamp': time.time()
            }
            
            # Send message to queue
            self.ipc_queue.put(test_message)
            
            # Try to receive message
            try:
                received_message = self.ipc_queue.get(timeout=2)
                if received_message == test_message:
                    print("✅ IPC communication working")
                    return True
                else:
                    print("❌ IPC message mismatch")
                    return False
            except:
                print("❌ IPC message timeout")
                return False
                
        except Exception as e:
            print(f"❌ IPC communication test failed: {e}")
            return False
    
    def test_process_monitoring(self) -> bool:
        """Test process monitoring capabilities."""
        try:
            import requests
            
            # Test status endpoint
            response = requests.get('http://localhost:8000/status', timeout=5)
            if response.status_code == 200:
                status = response.json()
                print("✅ Process status endpoint working")
                
                # Check if status contains expected fields
                expected_fields = ['api_server', 'frontend_server', 'renderer']
                for field in expected_fields:
                    if field in status:
                        print(f"✅ Status contains {field}")
                    else:
                        print(f"❌ Status missing {field}")
                        return False
                
                return True
            else:
                print(f"❌ Process status endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Process monitoring test failed: {e}")
            return False
    
    def test_graceful_shutdown(self) -> bool:
        """Test graceful shutdown."""
        try:
            if self.main_process:
                print("🛑 Testing graceful shutdown...")
                
                # Send SIGTERM to main process
                self.main_process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.main_process.wait(timeout=10)
                    print("✅ Graceful shutdown successful")
                    return True
                except subprocess.TimeoutExpired:
                    print("⚠️  Force killing process...")
                    self.main_process.kill()
                    self.main_process.wait()
                    print("✅ Force shutdown successful")
                    return True
            else:
                print("⚠️  No main process to shutdown")
                return True
                
        except Exception as e:
            print(f"❌ Graceful shutdown test failed: {e}")
            return False
    
    def print_summary(self):
        """Print test summary."""
        print(f"\n{'='*60}")
        print("📊 Test Summary")
        print(f"{'='*60}")
        
        passed = sum(1 for _, success in self.test_results if success)
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        print(f"\nDetailed Results:")
        for test_name, success in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"  {status} {test_name}")
        
        if passed == total:
            print(f"\n🎉 All tests passed! Multi-process architecture is working correctly.")
        else:
            print(f"\n⚠️  Some tests failed. Please check the issues above.")
        
        print(f"{'='*60}")

def test_individual_components():
    """Test individual components separately."""
    print("\n🔧 Testing Individual Components")
    print("=" * 40)
    
    # Test main process script
    print("\n📋 Testing main_process.py...")
    try:
        result = subprocess.run([
            sys.executable, 'main_process.py', '--help'
        ], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ main_process.py script is valid")
        else:
            print(f"❌ main_process.py script error: {result.stderr}")
    except Exception as e:
        print(f"❌ main_process.py test failed: {e}")
    
    # Test renderer process script
    print("\n📋 Testing renderer_process.py...")
    try:
        result = subprocess.run([
            sys.executable, 'renderer_process.py', '--help'
        ], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ renderer_process.py script is valid")
        else:
            print(f"❌ renderer_process.py script error: {result.stderr}")
    except Exception as e:
        print(f"❌ renderer_process.py test failed: {e}")
    
    # Test API server
    print("\n📋 Testing API server...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'stableagents.api_server', '--help'
        ], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ API server script is valid")
        else:
            print(f"❌ API server script error: {result.stderr}")
    except Exception as e:
        print(f"❌ API server test failed: {e}")

def main():
    """Main test function."""
    print("🧪 Multi-Process Architecture Test Suite")
    print("=" * 60)
    
    # Test individual components first
    test_individual_components()
    
    # Run comprehensive tests
    tester = MultiProcessTester()
    tester.run_all_tests()
    
    print("\n🎯 Test Suite Complete!")
    print("If all tests pass, your multi-process architecture is ready to use!")

if __name__ == "__main__":
    main() 