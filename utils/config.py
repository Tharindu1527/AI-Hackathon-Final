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
    """Get MongoDB URI from environment with proper formatting for cloud connections"""
    uri = os.getenv("MONGODB_URI")
    
    # Clean up the URI to ensure proper formatting
    if uri:
        # Remove quotes that might be included
        uri = uri.replace('"', '').replace("'", '')
        
        # Ensure the database name is specified
        if '/?' in uri:
            # URI has options but might be missing db name
            host_part, options_part = uri.split('/?', 1)
            if not any(part.startswith('podcast_analytics') for part in host_part.split('/')):
                # Add database name before options
                uri = f"{host_part}/podcast_analytics?{options_part}"
        elif '?' in uri and '/' not in uri.split('?')[0].split('@')[-1]:
            # Missing slash before question mark
            base_part, options_part = uri.split('?', 1)
            uri = f"{base_part}/podcast_analytics?{options_part}"
    
    return uri

def get_qdrant_uri():
    """Get Qdrant URI from environment"""
    return os.getenv("QDRANT_URI")

def get_qdrant_api_key():
    """Get Qdrant API key from environment"""
    return os.getenv("QDRANT_API_KEY")