# agents/sentiment.py (fixed)
from agents.base import BaseAgent

class SentimentAgent(BaseAgent):
    """Agent specialized in analyzing emotional tone and sentiment"""
    
    def __init__(self, model="gpt-4o"):
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
            transcript_task: The completed transcription task (string or Task object)
            analyzer_task: The completed analyzer task (string or Task object)
            
        Returns:
            Task: CrewAI task
        """
        from crewai import Task
        
        # Handle both string and Task object inputs for transcript
        transcript_content = transcript_task
        if hasattr(transcript_task, 'get'):
            # It's a Task object or dictionary, get the content
            transcript_content = transcript_task.get("output", transcript_task)
        elif hasattr(transcript_task, 'output'):
            # It's a Task object with direct output attribute
            transcript_content = transcript_task.output
        
        # Handle both string and Task object inputs for analyzer
        analysis_content = analyzer_task
        if hasattr(analyzer_task, 'get'):
            # It's a Task object or dictionary, get the content
            analysis_content = analyzer_task.get("output", analyzer_task)
        elif hasattr(analyzer_task, 'output'):
            # It's a Task object with direct output attribute
            analysis_content = analyzer_task.output
        
        # Convert to strings if not already
        if not isinstance(transcript_content, str):
            transcript_content = str(transcript_content)
        if not isinstance(analysis_content, str):
            analysis_content = str(analysis_content)
        
        task = Task(
            description=f"""
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
            
            Transcript excerpt:
            {transcript_content[:3000]}
            
            Analysis of content:
            {analysis_content[:2000]}
            """,
            agent=self.create_agent(),
            expected_output="A detailed sentiment analysis of the podcast discussion.",
            context=None
        )
        
        return task