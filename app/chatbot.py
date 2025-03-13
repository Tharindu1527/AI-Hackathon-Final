# app/chatbot.py
from api.openai import get_openai_client

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
    
    # Create a context for the AI to use
    context = f"""
    Podcast Title: {podcast_data['title']}
    Date Analyzed: {podcast_data['date_analyzed']}
    
    Summary:
    {podcast_data['summary']}
    
    Key Topics:
    {', '.join(podcast_data['key_topics'])}
    
    Sentiment Analysis:
    {podcast_data['sentiment']}
    
    Action Items:
    {', '.join(podcast_data['action_items'])}
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

def format_sources(podcast_data):
    """
    Format source information for attribution
    
    Args:
        podcast_data: Dictionary containing podcast information
        
    Returns:
        str: Formatted source information
    """
    return f"Source: {podcast_data['title']} (analyzed on {podcast_data['date_analyzed']})"