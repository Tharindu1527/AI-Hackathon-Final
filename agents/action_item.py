# agents/action_item.py
from agents.base import BaseAgent

class ActionItemAgent(BaseAgent):
    """Agent specialized in extracting actionable insights and recommendations"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Action Item Agent"""
        super().__init__(
            role="Action Item Extractor",
            goal="Identify and extract actionable insights and recommendations from the podcast",
            backstory="I excel at identifying practical next steps and business implications from discussions. "
                    "With a background in strategic consulting, I can translate insights into concrete "
                    "action items that organizations can implement for meaningful results.",
            model=model
        )
        
    def create_task(self, summarizer_task, sentiment_task):
        """
        Create a task for the Action Item Agent
        
        Args:
            summarizer_task: The completed summarizer task
            sentiment_task: The completed sentiment analysis task
            
        Returns:
            Task: CrewAI task
        """
        from crewai import Task
        
        task = Task(
            description="""
            Your task is to extract actionable insights and recommendations from the podcast summary and sentiment analysis.
            
            Focus on:
            
            1. Concrete action items mentioned or implied in the podcast
            2. Strategic recommendations based on the insights discussed
            3. Potential business opportunities highlighted
            4. Areas requiring further research or investigation
            5. Explicit next steps suggested by podcast participants
            6. Prioritization of actions based on impact and feasibility
            
            Format the output as a clear list of action items, each with a brief context and potential benefit.
            The goal is to provide board members with a practical roadmap based on the podcast content.
            """,
            agent=self.create_agent(),
            expected_output="A prioritized list of actionable insights and recommendations with clear next steps.",
            context=[summarizer_task, sentiment_task]
        )
        
        return task