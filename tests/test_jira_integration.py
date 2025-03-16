import os
import unittest
from agents.jira_integration import JiraAgent
from utils.config import load_environment

class TestJiraIntegration(unittest.TestCase):
    def setUp(self):
        # Load environment variables using project's config
        load_environment()
        
        # Print environment variables for debugging (excluding API tokens)
        print("\nEnvironment variables:")
        print(f"JIRA_SERVER: {os.getenv('JIRA_SERVER')}")
        print(f"JIRA_USERNAME: {os.getenv('JIRA_USERNAME')}")
        print(f"JIRA_PROJECT: {os.getenv('JIRA_PROJECT', 'SCRUM')} (default: SCRUM)")
        print(f"JIRA_API_TOKEN: {'[SET]' if os.getenv('JIRA_API_TOKEN') else '[NOT SET]'}")
        
        # Ensure required environment variables are set
        required_vars = ["JIRA_SERVER", "JIRA_USERNAME", "JIRA_API_TOKEN"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            self.skipTest(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        self.jira_agent = JiraAgent()
    
    def test_create_issue(self):
        """Test creating a Jira issue"""
        # Test data
        test_task = {
            'summary': '[TEST] Jira Integration Test Issue',
            'description': 'This is a test issue created by the automated test suite.'
        }
        
        # Create issue
        try:
            issue_key = self.jira_agent.process_task(test_task)
            self.assertIsNotNone(issue_key, "Issue key should not be None")
            print(f"\nSuccessfully created test issue: {issue_key}")
        except Exception as e:
            self.fail(f"Failed to create Jira issue: {str(e)}")

if __name__ == '__main__':
    unittest.main()
