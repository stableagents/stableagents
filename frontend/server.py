#!/usr/bin/env python3
"""
Simple HTTP server for serving the StableAgents Desktop App Generator frontend.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with CORS support."""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests."""
        self.send_response(200)
        self.end_headers()
    
    def translate_path(self, path):
        """Translate URL path to file system path."""
        # Remove leading slash
        path = path.lstrip('/')
        
        # If no path specified, serve index.html
        if not path:
            path = 'index.html'
        
        # Convert to absolute path
        return str(SCRIPT_DIR / path)

def main():
    """Main function to start the server."""
    PORT = 3000
    
    # Change to the frontend directory
    os.chdir(SCRIPT_DIR)
    
    # Create server
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Frontend server started!")
        print(f"📱 Open your browser and go to: http://localhost:{PORT}")
        print(f"🔗 API server should be running at: http://localhost:8000")
        print(f"📁 Serving files from: {SCRIPT_DIR}")
        print(f"⏹️  Press Ctrl+C to stop the server")
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped by user")
            httpd.shutdown()

if __name__ == "__main__":
    main() 