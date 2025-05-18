import os 
import math 
import asyncio 

import numpy as np


def stablememory():
    """
    A function that creates and returns an embedding model for stable memory operations.
    This model can be used to convert text into vector representations.
    """
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return model
    except ImportError:
        raise ImportError("Please install sentence-transformers: pip install sentence-transformers")


if isinstance(stablememory, MemoryError):
    error_message = "---------------"

