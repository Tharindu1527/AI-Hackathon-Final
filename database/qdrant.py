# database/qdrant.py
from qdrant_client import QdrantClient
from qdrant_client.http import models
from utils.config import get_qdrant_uri
from api.openai import generate_embeddings

def get_qdrant_client():
    """
    Get a Qdrant client instance
    
    Returns:
        QdrantClient: Qdrant client
    """
    uri = get_qdrant_uri()
    return QdrantClient(url=uri)

def create_collection_if_not_exists(collection_name="podcast_vectors", vector_size=1536):
    """
    Create a Qdrant collection if it doesn't exist
    
    Args:
        collection_name: Name of the collection
        vector_size: Size of the vectors
    """
    client = get_qdrant_client()
    
    # Check if collection exists
    collections = client.get_collections()
    collection_names = [c.name for c in collections.collections]
    
    if collection_name not in collection_names:
        # Create the collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )
        print(f"Created collection: {collection_name}")
    else:
        print(f"Collection {collection_name} already exists")

def store_vectors(podcast_data, document_id):
    """
    Store podcast vectors in Qdrant for semantic search
    
    Args:
        podcast_data: Dictionary containing podcast data
        document_id: MongoDB document ID as a reference
        
    Returns:
        bool: True if successful
    """
    # Create collection if it doesn't exist
    create_collection_if_not_exists()
    
    # Generate embedding for the summary text
    summary_text = podcast_data["summary"]
    embedding = generate_embeddings(summary_text)
    
    # Store in Qdrant
    client = get_qdrant_client()
    client.upsert(
        collection_name="podcast_vectors",
        points=[
            models.PointStruct(
                id=hash(document_id),
                vector=embedding,
                payload=podcast_data
            )
        ]
    )
    
    return True

def search_similar_content(query_text, limit=3):
    """
    Search for podcast content similar to the query
    
    Args:
        query_text: Query text to search for
        limit: Maximum number of results to return
        
    Returns:
        list: List of search results
    """
    # Generate embedding for the query
    query_embedding = generate_embeddings(query_text)
    
    # Search Qdrant
    client = get_qdrant_client()
    search_results = client.search(
        collection_name="podcast_vectors",
        query_vector=query_embedding,
        limit=limit
    )
    
    return search_results

def delete_vectors(document_id):
    """
    Delete podcast vectors from Qdrant
    
    Args:
        document_id: MongoDB document ID to delete
        
    Returns:
        bool: True if successful
    """
    client = get_qdrant_client()
    result = client.delete(
        collection_name="podcast_vectors",
        points_selector=models.PointIdsList(
            points=[hash(document_id)]
        )
    )
    
    return result