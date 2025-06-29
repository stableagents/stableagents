#!/usr/bin/env python3
"""
Simple Gemini example with environment variable loading
"""

import os

# Load environment variables from .env.local
def load_env_file(filepath=".env.local"):
    """Load environment variables from a .env file"""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value

# Load the environment variables
load_env_file()

# Now import and use the client
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-pro", contents="make a basic calculator in the terminal"
)
print(response.text) 