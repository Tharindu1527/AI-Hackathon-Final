# app/email.py
from api.composio import initialize_composio, create_email_template, send_email_summary
import os

def create_email_template_dir():
    """Create directory for email templates if it doesn't exist"""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    return template_dir

def save_email_template(template_content, template_name='Meeting_summary.html'):
    """
    Save email template to file
    
    Args:
        template_content: HTML content of the template
        template_name: Filename for the template
        
    Returns:
        str: Path to the saved template
    """
    template_dir = create_email_template_dir()
    template_path = os.path.join(template_dir, template_name)
    
    with open(template_path, 'w') as f:
        f.write(template_content)
    
    return template_path

def get_default_template_content():
    """
    Get default email template content
    
    Returns:
        str: HTML template content
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Meeting Summary: {{podcast_title}}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }
            h2 {
                color: #3498db;
                margin-top: 20px;
            }
            ul {
                padding-left: 20px;
            }
            li {
                margin-bottom: 5px;
            }
            .date {
                color: #7f8c8d;
                font-style: italic;
            }
            .action-items {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                border-left: 5px solid #3498db;
            }
        </style>
    </head>
    <body>
        <h1>Meeting Summary: {{podcast_title}}</h1>
        <p class="date"><strong>Date Analyzed:</strong> {{date_analyzed}}</p>
        
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
        <div class="action-items">
            <ul>
            {% for item in action_items %}
                <li>{{item}}</li>
            {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    """

def prepare_email_template():
    """
    Prepare email template for Composio
    
    Returns:
        template: Composio email template
    """
    # Initialize Composio
    initialize_composio()
    
    # Create template
    template = create_email_template()
    
    return template

def send_podcast_summary_email(podcast_data, recipients):
    """
    Send Meeting summary to board members
    
    Args:
        Meeting_data: Dictionary containing Meeting analysis data
        recipients: List of email addresses
        
    Returns:
        list: Results of email sending operations
    """
    return send_email_summary(podcast_data, recipients)