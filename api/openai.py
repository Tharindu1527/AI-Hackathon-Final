# api/openai.py
import requests
from langchain_openai import ChatOpenAI
from utils.config import get_openai_api_key

def get_openai_client():
    """
    Get a configured OpenAI client from LangChain
    
    Returns:
        ChatOpenAI: Configured OpenAI client
    """
    api_key = get_openai_api_key()
    return ChatOpenAI(api_key=api_key, model="gpt-4o")

def generate_embeddings(text):
    """
    Generate embeddings for text using OpenAI API
    
    Args:
        text: The text to generate embeddings for
        
    Returns:
        list: Vector embedding
    """
    api_key = get_openai_api_key()
    
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "input": text,
            "model": "text-embedding-3-small"
        }
    )
    
    # Check if request was successful
    if response.status_code != 200:
        raise Exception(f"Error generating embeddings: {response.text}")
    
    # Extract and return the embedding
    return response.json()["data"][0]["embedding"]

def chat_completion(prompt, system_message=None, temperature=0.7):
    """
    Generate a completion using OpenAI ChatCompletion API
    
    Args:
        prompt: User prompt
        system_message: Optional system message
        temperature: Temperature for generation (0.0 to 1.0)
        
    Returns:
        str: Generated completion
    """
    client = get_openai_client()
    
    # Create messages array
    messages = []
    
    # Add system message if provided
    if system_message:
        messages.append({"role": "system", "content": system_message})
    
    # Add user message
    messages.append({"role": "user", "content": prompt})
    
    # Generate completion
    completion = client.invoke(prompt)
    
    return completion.content