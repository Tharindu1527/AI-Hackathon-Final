# database/mongodb.py
from pymongo import MongoClient
from utils.config import get_mongodb_uri

def get_mongodb_client():
    """
    Get a MongoDB client instance
    
    Returns:
        MongoClient: MongoDB client
    """
    uri = get_mongodb_uri()
    return MongoClient(uri)

def get_podcast_collection():
    """
    Get the MongoDB collection for podcast summaries
    
    Returns:
        Collection: MongoDB collection
    """
    client = get_mongodb_client()
    db = client["podcast_analytics"]
    return db["summaries"]

def store_podcast_data(podcast_data):
    """
    Store podcast data in MongoDB
    
    Args:
        podcast_data: Dictionary containing podcast data and analysis
        
    Returns:
        str: ID of the inserted document
    """
    collection = get_podcast_collection()
    result = collection.insert_one(podcast_data)
    return str(result.inserted_id)

def get_podcast_by_id(podcast_id):
    """
    Retrieve podcast data by ID
    
    Args:
        podcast_id: ID of the podcast document
        
    Returns:
        dict: Podcast data or None if not found
    """
    from bson.objectid import ObjectId
    
    collection = get_podcast_collection()
    return collection.find_one({"_id": ObjectId(podcast_id)})

def get_podcast_by_title(title):
    """
    Retrieve podcast data by title
    
    Args:
        title: Title of the podcast
        
    Returns:
        dict: Podcast data or None if not found
    """
    collection = get_podcast_collection()
    return collection.find_one({"title": title})

def get_all_podcasts():
    """
    Retrieve all podcast data
    
    Returns:
        list: List of all podcast documents
    """
    collection = get_podcast_collection()
    return list(collection.find())

def get_all_podcast_titles():
    """
    Retrieve all podcast titles
    
    Returns:
        list: List of all podcast titles
    """
    collection = get_podcast_collection()
    return [doc["title"] for doc in collection.find({}, {"title": 1})]

def update_podcast_data(podcast_id, update_data):
    """
    Update podcast data
    
    Args:
        podcast_id: ID of the podcast document
        update_data: Dictionary containing fields to update
        
    Returns:
        bool: True if update was successful
    """
    from bson.objectid import ObjectId
    
    collection = get_podcast_collection()
    result = collection.update_one(
        {"_id": ObjectId(podcast_id)},
        {"$set": update_data}
    )
    
    return result.modified_count > 0

def delete_podcast(podcast_id):
    """
    Delete a podcast document
    
    Args:
        podcast_id: ID of the podcast document
        
    Returns:
        bool: True if deletion was successful
    """
    from bson.objectid import ObjectId
    
    collection = get_podcast_collection()
    result = collection.delete_one({"_id": ObjectId(podcast_id)})
    
    return result.deleted_count > 0