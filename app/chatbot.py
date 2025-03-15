from api.openai import get_openai_client
from database.mongodb import get_podcast_by_title

def generate_answer(podcast_data, user_question):
    """
    Generate an answer to a user question based on podcast data
    
    Args:
        podcast_data: Dictionary containing podcast information
        user_question: User's question
        
    Returns:
        str: Generated answer
    """
    # Initialize OpenAI client
    openai_client = get_openai_client()
    
    # Check if podcast_data is complete or needs more information
    if not podcast_data.get("summary") or podcast_data.get("summary") == "Summary not available":
        return "I'm sorry, but I don't have enough information about this podcast. It may not have been fully analyzed yet."
    
    # Create a context for the AI to use
    context = f"""
    Podcast Title: {podcast_data.get('title', 'Unknown Title')}
    Date Analyzed: {podcast_data.get('date_analyzed', 'Unknown Date')}
    
    Summary:
    {podcast_data.get('summary', 'No summary available')}
    
    Key Topics:
    {', '.join(podcast_data.get('key_topics', ['No topics available']))}
    
    Sentiment Analysis:
    {podcast_data.get('sentiment', 'No sentiment analysis available')}
    
    Action Items:
    {', '.join(podcast_data.get('action_items', ['No action items available']))}
    """
    
    # Create a prompt for the AI
    prompt = f"""
    You are a helpful assistant that answers questions about podcasts.
    Use the following podcast information to answer the user's question.
    Only use information from the provided context. If the answer cannot be found
    in the context, acknowledge that you don't have enough information.
    
    Context:
    {context}
    
    User Question: {user_question}
    """
    
    # Generate an answer
    completion = openai_client.invoke(prompt)
    
    return completion.content

def get_podcast_data_by_id(podcast_id):
    """
    Get podcast data by ID or title
    
    Args:
        podcast_id: Podcast ID or title
        
    Returns:
        dict: Podcast data or None
    """
    from database.mongodb import get_podcast_by_id, get_podcast_by_title
    
    # Try to get by ID first
    podcast_data = get_podcast_by_id(podcast_id)
    
    # If not found, try by title
    if not podcast_data:
        podcast_data = get_podcast_by_title(podcast_id)
    
    return podcast_data

def format_sources(podcast_data):
    """
    Format source information for attribution
    
    Args:
        podcast_data: Dictionary containing podcast information
        
    Returns:
        str: Formatted source information
    """
    return f"Source: {podcast_data.get('title', 'Unknown Podcast')} (analyzed on {podcast_data.get('date_analyzed', 'unknown date')})"