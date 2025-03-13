# utils/config.py
import os
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    
    # Check for required environment variables
    required_vars = [
        "OPENAI_API_KEY",
        "ASSEMBLYAI_API_KEY",
        "COMPOSIO_API_KEY",
        "MONGODB_URI",
        "QDRANT_URI"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            f"Please check your .env file."
        )
    
    return {var: os.getenv(var) for var in required_vars}

def get_openai_api_key():
    """Get OpenAI API key from environment"""
    return os.getenv("OPENAI_API_KEY")

def get_assemblyai_api_key():
    """Get AssemblyAI API key from environment"""
    return os.getenv("ASSEMBLYAI_API_KEY")

def get_composio_api_key():
    """Get Composio API key from environment"""
    return os.getenv("COMPOSIO_API_KEY")

def get_mongodb_uri():
    """Get MongoDB URI from environment"""
    return os.getenv("MONGODB_URI")

def get_qdrant_uri():
    """Get Qdrant URI from environment"""
    return os.getenv("QDRANT_URI")

def get_qdrant_api_key():
    """Get Qdrant API key from environment"""
    return os.getenv("QDRANT_API_KEY")