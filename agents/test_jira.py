from agents.jira_integration import JiraIntegrationAgent
from dotenv import load_dotenv
load_dotenv()

# Test with simple summary
test_summary = "Action Items: 1. Update documentation 2. Fix bug in login"

agent = JiraIntegrationAgent()
result = agent.process_meeting(test_summary)
print(f"Extracted {len(result['extracted_issues'])} issues")
print(result)