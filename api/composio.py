# api/composio.py
import composio as cp
from utils.config import get_composio_api_key

def initialize_composio():
    """Initialize Composio with API key"""
    api_key = get_composio_api_key()
    cp.api_key = api_key
    return api_key

def create_email_template():
    """
    Create a Composio email template for podcast summaries
    
    Returns:
        Template: Composio email template object
    """
    # Initialize Composio
    initialize_composio()
    
    # Create a template
    template = cp.Template(
        name="Podcast Summary",
        content="""
        <h1>Podcast Summary: {{podcast_title}}</h1>
        <p><strong>Date Analyzed:</strong> {{date_analyzed}}</p>
        <h2>Executive Summary</h2>
        <p>{{summary}}</p>
        <h2>Key Topics</h2>
        <ul>
        {% for topic in key_topics %}
            <li>{{topic}}</li>
        {% endfor %}
        </ul>
        <h2>Sentiment Analysis</h2>
        <p>{{sentiment}}</p>
        <h2>Action Items</h2>
        <ul>
        {% for item in action_items %}
            <li>{{item}}</li>
        {% endfor %}
        </ul>
        """
    )
    
    return template

def send_email_summary(podcast_data, recipients):
    """
    Send podcast summary email to recipients using Composio
    
    Args:
        podcast_data: Dictionary containing podcast analysis data
        recipients: List of email addresses to send to
    """
    # Initialize Composio
    initialize_composio()
    
    # Create email template
    template = create_email_template()
    
    # Prepare email data
    email_data = {
        "podcast_title": podcast_data["title"],
        "date_analyzed": podcast_data["date_analyzed"],
        "summary": podcast_data["summary"],
        "key_topics": podcast_data["key_topics"],
        "sentiment": podcast_data["sentiment"],
        "action_items": podcast_data["action_items"]
    }
    
    # Send email to each recipient
    results = []
    for recipient in recipients:
        result = cp.Email.send(
            to=recipient,
            from_email="podcast-analyzer@company.com",
            subject=f"Podcast Summary: {podcast_data['title']}",
            template=template,
            data=email_data
        )
        results.append(result)
    
    return results