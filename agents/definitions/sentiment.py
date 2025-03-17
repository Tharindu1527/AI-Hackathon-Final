# agents/definitions/sentiment.py
from agents.base import BaseAgent
from agents.registry import register_agent

@register_agent("sentiment")
class SentimentAgent(BaseAgent):
    """Agent specialized in analyzing emotional tone and sentiment"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Sentiment Agent"""
        super().__init__(
            role="Sentiment Analyzer",
            goal="Analyze the emotional tone and sentiment throughout the Meeting",
            backstory="With a background in psychology and NLP, I can detect subtle emotional cues in communication. "
                    "I understand how tone, language choice, and speech patterns reveal attitudes and feelings. "
                    "I can map the emotional journey of a conversation.",
            model=model
        )
    
    def analyze_sentiment(self, transcript_data, analysis_data=None):
        """
        Analyze sentiment of Meeting content
        
        Args:
            transcript_data: Transcript data (string or task result)
            analysis_data: Optional analysis data (string or task result)
            
        Returns:
            str: Sentiment analysis result
        """
        from agents.tasks.sentiment import SentimentTask
        
        task = SentimentTask.create_sentiment_task(self, transcript_data, analysis_data)
        return self.execute_task(task)
    
    def analyze_speaker_sentiment(self, transcript_data):
        """
        Analyze sentiment of individual speakers
        
        Args:
            transcript_data: Transcript data with speaker identifications
            
        Returns:
            str: Speaker sentiment analysis result
        """
        from agents.tasks.sentiment import SentimentTask
        
        task = SentimentTask.create_speaker_sentiment_task(self, transcript_data)
        return self.execute_task(task)
    
    def analyze_topic_sentiment(self, transcript_data, topics):
        """
        Analyze sentiment associated with specific topics
        
        Args:
            transcript_data: Transcript data
            topics: List of topics to analyze sentiment for
            
        Returns:
            str: Topic sentiment analysis result
        """
        from agents.tasks.sentiment import SentimentTask
        
        task = SentimentTask.create_topic_sentiment_task(self, transcript_data, topics)
        return self.execute_task(task)