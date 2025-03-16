# agents/tasks/sentiment.py
from agents.tasks.task_base import BaseTask

class SentimentTask(BaseTask):
    """Tasks related to sentiment analysis of podcast content"""
    
    @staticmethod
    def create_sentiment_task(agent, transcript_data, analysis_data=None):
        """
        Create a sentiment analysis task
        
        Args:
            agent: Sentiment agent (ID or instance)
            transcript_data: Transcript data (string or task result)
            analysis_data: Optional analysis data (string or task result)
            
        Returns:
            Task: Sentiment analysis task
        """
        input_dict = {"transcript": transcript_data}
        if analysis_data:
            input_dict["analysis"] = analysis_data
            
        return BaseTask.create_task(
            agent=agent,
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
            expected_output="A detailed sentiment analysis of the podcast discussion.",
            input_data=input_dict
        )
    
    @staticmethod
    def create_speaker_sentiment_task(agent, transcript_data):
        """
        Create a speaker-specific sentiment analysis task
        
        Args:
            agent: Sentiment agent (ID or instance)
            transcript_data: Transcript data with speaker identifications
            
        Returns:
            Task: Speaker sentiment task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to analyze the sentiment of each speaker individually:
            
            1. Identify the distinct speakers in the transcript
            2. For each speaker, analyze their emotional tone and sentiment
            3. Note how each speaker's sentiment shifts during the conversation
            4. Detect differences in attitudes or perspectives between speakers
            5. Identify emotional reactions to specific topics by each speaker
            6. Analyze the interpersonal dynamics between speakers
            
            Create a speaker-by-speaker sentiment analysis that captures the unique
            voice and perspective of each participant.
            """,
            expected_output="A sentiment analysis broken down by individual speakers.",
            input_data=transcript_data
        )
    
    @staticmethod
    def create_topic_sentiment_task(agent, transcript_data, topics):
        """
        Create a topic-based sentiment analysis task
        
        Args:
            agent: Sentiment agent (ID or instance)
            transcript_data: Transcript data
            topics: List of topics to analyze sentiment for
            
        Returns:
            Task: Topic sentiment task
        """
        input_dict = {
            "transcript": transcript_data,
            "topics": ", ".join(topics) if isinstance(topics, list) else topics
        }
        
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to analyze the sentiment associated with each specified topic:
            
            1. For each topic listed, identify all mentions in the transcript
            2. Analyze the emotional tone and sentiment when each topic is discussed
            3. Note how sentiment toward each topic may shift throughout the conversation
            4. Compare sentiment across different topics
            5. Identify which topics evoke the strongest emotional responses
            6. Note any topics with mixed or contentious sentiment
            
            Create a topic-by-topic sentiment analysis that reveals how each subject
            is perceived and discussed emotionally.
            """,
            expected_output="A sentiment analysis organized by topic, showing how each topic is discussed emotionally.",
            input_data=input_dict
        )
    
    @staticmethod
    def execute_sentiment_analysis(transcript_data, analysis_data=None, agent_id="sentiment", agent_instance=None):
        """
        Execute sentiment analysis directly
        
        Args:
            transcript_data: Transcript data
            analysis_data: Optional analysis data
            agent_id: ID of sentiment agent (if not providing instance)
            agent_instance: Sentiment agent instance (if not providing ID)
            
        Returns:
            str: Sentiment analysis result
        """
        task = SentimentTask.create_sentiment_task(
            agent=agent_instance or agent_id,
            transcript_data=transcript_data,
            analysis_data=analysis_data
        )
        
        return BaseTask.execute_with_agent(
            task=task,
            agent_id=agent_id,
            agent_instance=agent_instance
        )