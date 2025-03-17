# api/composio.py
from utils.config import get_composio_api_key
import requests
import json

def initialize_composio():
    """Initialize Composio with API key"""
    api_key = get_composio_api_key()
    return api_key

def send_email_summary(podcast_data, recipients):
    """
    Send Meeting summary email to recipients using Composio API directly
    
    Args:
        Meeting_data: Dictionary containing Meeting analysis data
        recipients: List of email addresses to send to
    """
    api_key = initialize_composio()
    
    # Format the key topics and action items as HTML lists
    key_topics_html = "".join([f"<li>{topic}</li>" for topic in podcast_data["key_topics"]])
    action_items_html = "".join([f"<li>{item}</li>" for item in podcast_data["action_items"]])
    
    # Create email HTML content
    email_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Meeting Summary: {podcast_data['title']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            h2 {{ color: #3498db; margin-top: 20px; }}
            ul {{ padding-left: 20px; }}
            li {{ margin-bottom: 5px; }}
            .date {{ color: #7f8c8d; font-style: italic; }}
            .action-items {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 5px solid #3498db; }}
        </style>
    </head>
    <body>
        <h1>Meeting Summary: {podcast_data['title']}</h1>
        <p class="date"><strong>Date Analyzed:</strong> {podcast_data['date_analyzed']}</p>
        
        <h2>Executive Summary</h2>
        <p>{podcast_data['summary']}</p>
        
        <h2>Key Topics</h2>
        <ul>
            {key_topics_html}
        </ul>
        
        <h2>Sentiment Analysis</h2>
        <p>{podcast_data['sentiment']}</p>
        
        <h2>Action Items</h2>
        <div class="action-items">
            <ul>
                {action_items_html}
            </ul>
        </div>
    </body>
    </html>
    """
    
    # For each recipient, send an email
    results = []
    for recipient in recipients:
        try:
            # Make a direct API call to Composio
            response = requests.post(
                "https://api.composio.dev/v1/send",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "to": recipient,
                    "from": "Meeting-analyzer@company.com",
                    "subject": f"Meeting Summary: {podcast_data['title']}",
                    "html": email_html
                }
            )
            
            if response.status_code == 200:
                print(f"Email sent successfully to {recipient}")
                results.append({"recipient": recipient, "status": "success"})
            else:
                print(f"Failed to send email to {recipient}: {response.text}")
                results.append({"recipient": recipient, "status": "error", "message": response.text})
        except Exception as e:
            print(f"Exception sending email to {recipient}: {str(e)}")
            results.append({"recipient": recipient, "status": "error", "message": str(e)})
    
    return results