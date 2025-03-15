# agents/action_item.py (fixed)
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
            summarizer_task: The completed summarizer task (string or Task object)
            sentiment_task: The completed sentiment analysis task (string or Task object)
            
        Returns:
            Task: CrewAI task
        """
        from crewai import Task
        
        # Handle both string and Task object inputs for summarizer
        summary_content = summarizer_task
        if hasattr(summarizer_task, 'get'):
            # It's a Task object or dictionary, get the content
            summary_content = summarizer_task.get("output", summarizer_task)
        elif hasattr(summarizer_task, 'output'):
            # It's a Task object with direct output attribute
            summary_content = summarizer_task.output
        
        # Handle both string and Task object inputs for sentiment
        sentiment_content = sentiment_task
        if hasattr(sentiment_task, 'get'):
            # It's a Task object or dictionary, get the content
            sentiment_content = sentiment_task.get("output", sentiment_task)
        elif hasattr(sentiment_task, 'output'):
            # It's a Task object with direct output attribute
            sentiment_content = sentiment_task.output
        
        # Convert to strings if not already
        if not isinstance(summary_content, str):
            summary_content = str(summary_content)
        if not isinstance(sentiment_content, str):
            sentiment_content = str(sentiment_content)
        
        task = Task(
            description=f"""
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
            
            Summary:
            {summary_content[:2500]}
            
            Sentiment Analysis:
            {sentiment_content[:2500]}
            """,
            agent=self.create_agent(),
            expected_output="A prioritized list of actionable insights and recommendations with clear next steps.",
            context=None
        )
        
        return task