import os 
import math 
import asyncio 

import asyncpg
import numpy as np
from openai import AsyncOpenAI
from sentence_transformers import SentenceTransformer

# Default model configuration
DEFAULT_MODEL = 'all-MiniLM-L6-v2'
MEMORY_DEPENDENCIES = {
    'sentence-transformers': 'sentence-transformers',
    'numpy': 'numpy',
    'asyncpg': 'asyncpg',
    'openai': 'openai'
}

def stablememory(model_name: str = DEFAULT_MODEL):
    """
    A function that creates and returns an embedding model for stable memory operations.
    This model can be used to convert text into vector representations.
    
    Args:
        model_name (str): Name of the model to use. Defaults to 'all-MiniLM-L6-v2'
    
    Returns:
        SentenceTransformer: The initialized embedding model
        
    Raises:
        ImportError: If required dependencies are not installed
    """
    try:
        model = SentenceTransformer(model_name)
        return model
    except ImportError as e:
        missing_deps = [dep for dep in MEMORY_DEPENDENCIES if dep not in globals()]
        if missing_deps:
            raise ImportError(
                f"Missing required dependencies: {', '.join(missing_deps)}. "
                f"Please install them using: pip install {' '.join(MEMORY_DEPENDENCIES.values())}"
            ) from e
        raise e








if __name__ == "__main__":
    asyncio.run(())