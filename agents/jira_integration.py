import os
from jira import JIRA

class JiraAgent:
    def __init__(self):
        # Get environment variables with new names
        jira_server = os.getenv("JIRA_SERVER")
        self.jira_email = os.getenv("JIRA_USERNAME")  # Using USERNAME instead of EMAIL
        self.jira_api_token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT", "SCRUM")  # Using PROJECT instead of PROJECT_KEY
        
        # Extract domain from server URL
        self.jira_domain = jira_server.replace("https://", "") if jira_server else None
        
        if not all([self.jira_domain, self.jira_email, self.jira_api_token]):
            raise ValueError("Missing required JIRA environment variables: JIRA_SERVER, JIRA_USERNAME, or JIRA_API_TOKEN")
        
        self.jira = JIRA(
            server=f"https://{self.jira_domain}",
            basic_auth=(self.jira_email, self.jira_api_token)
        )

    def create_issue(self, summary, description, issue_type="Task"):
        """
        Create a Jira issue with the given summary and description.
        
        Args:
            summary (str): Title of the Jira issue
            description (str): Detailed description of the issue
            issue_type (str): Type of issue (default: Task)
            
        Returns:
            str: Key of the created issue
        """
        issue_dict = {
            'project': {'key': self.project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        
        issue = self.jira.create_issue(fields=issue_dict)
        return issue.key

    def process_task(self, task):
        """
        Process a task and create a corresponding Jira issue.
        
        Args:
            task (dict): Task dictionary containing summary and description
            
        Returns:
            str: Jira issue key if successful, None otherwise
        """
        try:
            summary = task.get('summary') or task.get('title', 'New Task')
            description = task.get('description', '')
            
            # Create Jira issue
            issue_key = self.create_issue(summary, description)
            return issue_key
        except Exception as e:
            print(f"Error creating Jira issue: {str(e)}")
            return None