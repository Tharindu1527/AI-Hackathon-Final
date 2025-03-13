# agents/summarizer.py
from agents.base import BaseAgent

class SummarizerAgent(BaseAgent):
    """Agent specialized in creating executive summaries"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Summarizer Agent"""
        super().__init__(
            role="Executive Summarizer",
            goal="Create concise, informative summaries of the podcast content for business leaders",
            backstory="I specialize in distilling complex information into clear, actionable summaries "
                    "for executives. I understand what busy professionals need to know and can "
                    "highlight the most valuable insights from any content.",
            model=model
        )
        
    def create_task(self, analyzer_task):
        """
        Create a task for the Summarizer Agent
        
        Args:
            analyzer_task: The completed analyzer task
            
        Returns:
            Task: CrewAI task
        """
        from crewai import Task
        
        task = Task(
            description="""
            Your task is to create an executive summary of the podcast based on the detailed analysis.
            
            The summary should:
            
            1. Be concise yet comprehensive (300-500 words)
            2. Highlight the most important insights and takeaways
            3. Be structured for easy consumption by busy executives
            4. Focus on actionable information and business value
            5. Use clear, direct language without technical jargon
            6. Include a brief overview of the podcast context
            
            The summary must be valuable to board members who need to understand the key points
            without listening to the entire podcast.
            """,
            agent=self.create_agent(),
            expected_output="A concise executive summary highlighting the most important information.",
            context=[analyzer_task]
        )
        
        return task