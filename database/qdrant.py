# database/qdrant.py
from qdrant_client import QdrantClient
from qdrant_client.http import models
from utils.config import get_qdrant_api_key, get_qdrant_uri
from api.openai import generate_embeddings

def get_qdrant_client():
    """
    Get a Qdrant client instance
    
    Returns:
        QdrantClient: Qdrant client
    """
    uri = get_qdrant_uri()
    api_key = get_qdrant_api_key()
    
    return QdrantClient(url=uri, api_key=api_key)

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
    try:
        # Create collection if it doesn't exist
        create_collection_if_not_exists()
        
        # Generate embedding for the summary text
        summary_text = podcast_data["summary"]
        embedding = generate_embeddings(summary_text)
        
        # Convert MongoDB document to JSON-serializable dict
        # This is the key fix - convert any MongoDB ObjectId to string
        cleaned_data = json_serialize_podcast_data(podcast_data)
        
        # Generate a numeric hash ID from the string document_id
        point_id = hash(str(document_id)) % (2**63)
        
        # Store in Qdrant
        client = get_qdrant_client()
        client.upsert(
            collection_name="podcast_vectors",
            points=[
                models.PointStruct(
                    id=point_id,  # Use a numeric ID
                    vector=embedding,
                    payload=cleaned_data  # Use cleaned data
                )
            ]
        )
        
        return True
    except Exception as e:
        print(f"Error storing vectors in Qdrant: {e}")
        # Continue without vector storage for testing
        return False

def json_serialize_podcast_data(podcast_data):
    """
    Convert MongoDB document with ObjectId to JSON-serializable dict
    
    Args:
        podcast_data: Dictionary that may contain ObjectId
        
    Returns:
        dict: JSON-serializable dictionary
    """
    from bson.objectid import ObjectId
    import json
    
    # Define a custom JSON encoder to handle ObjectId
    class MongoJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            return super().default(obj)
    
    # Convert to JSON and back to dict to ensure all values are serializable
    json_str = json.dumps(podcast_data, cls=MongoJSONEncoder)
    return json.loads(json_str)

def generate_consistent_id(document_id):
    """
    Generate a consistent numeric ID from a string ID
    
    Args:
        document_id: String ID
        
    Returns:
        int: Consistent numeric ID
    """
    import hashlib
    
    # Convert document_id to string if it's not already
    doc_id_str = str(document_id)
    
    # Use MD5 to get a consistent hash
    hash_object = hashlib.md5(doc_id_str.encode())
    # Convert first 8 bytes of hash to integer
    numeric_id = int.from_bytes(hash_object.digest()[:8], byteorder='big')
    
    return numeric_id

def search_similar_content(query_text, limit=3):
    """
    Search for podcast content similar to the query
    
    Args:
        query_text: Query text to search for
        limit: Maximum number of results to return
        
    Returns:
        list: List of search results
    """
    try:
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
    except Exception as e:
        print(f"Error searching vectors: {e}")
        return []