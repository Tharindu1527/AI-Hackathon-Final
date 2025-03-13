# agents/sentiment.py
from agents.base import BaseAgent

class SentimentAgent(BaseAgent):
    """Agent specialized in analyzing emotional tone and sentiment"""
    
    def __init__(self, model="gpt-4"):
        """Initialize the Sentiment Agent"""
        super().__init__(
            role="Sentiment Analyzer",
            goal="Analyze the emotional tone and sentiment throughout the podcast",
            backstory="With a background in psychology and NLP, I can detect subtle emotional cues in communication. "
                    "I understand how tone, language choice, and speech patterns reveal attitudes and feelings. "
                    "I can map the emotional journey of a conversation.",
            model=model
        )
        
    def create_task(self, transcript_task, analyzer_task):
        """
        Create a task for the Sentiment Agent
        
        Args:
            transcript_task: The completed transcription task
            analyzer_task: The completed analyzer task
            
        Returns:
            Task: CrewAI task
        """
        from crewai import Task
        
        task = Task(
            description="""
            Your task is to analyze the emotional tone and sentiment throughout the podcast.
            
            Perform the following analysis:
            
            1. Identify the overall emotional tone of the podcast
            2. Track sentiment shifts throughout the discussion
            3. Note emotional reactions to specific topics
            4. Detect underlying attitudes or biases
            5. Analyze the speakers' level of passion, confidence, or uncertainty
            6. Identify potential areas of consensus and disagreement
            
            Provide a nuanced analysis that goes beyond simple positive/negative classifications
            to reveal the authentic emotional undertones of the conversation.
            """,
            agent=self.create_agent(),
            expected_output="A detailed sentiment analysis of the podcast discussion.",
            context=[transcript_task, analyzer_task]
        )
        
        return task