# agents/definitions/analyzer.py
from agents.base import BaseAgent
from agents.registry import register_agent

@register_agent("analyzer")
class AnalyzerAgent(BaseAgent):
    """Agent specialized in analyzing Meeting content structure and topics"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Analyzer Agent"""
        super().__init__(
            role="Content Analyzer",
            goal="Analyze the transcript to identify key topics, themes, and structure of the Meeting",
            backstory="I have a PhD in linguistics and content analysis with years of experience "
                    "breaking down complex discussions. I can identify the main topics, "
                    "track conversation flow, and understand the underlying structure of any Meeting.",
            model=model
        )
    
    def analyze_content(self, transcript_data):
        """
        Analyze Meeting content 
        
        Args:
            transcript_data: Transcript data (string or task result)
            
        Returns:
            str: Analysis result
        """
        from agents.tasks.analysis import AnalysisTask
        
        task = AnalysisTask.create_content_analysis_task(self, transcript_data)
        return self.execute_task(task)
    
    def extract_topics(self, transcript_data):
        """
        Extract topics from a transcript
        
        Args:
            transcript_data: Transcript data (string or task result)
            
        Returns:
            str: Topics extraction result
        """
        from agents.tasks.analysis import AnalysisTask
        
        task = AnalysisTask.create_topic_extraction_task(self, transcript_data)
        return self.execute_task(task)
    
    def analyze_arguments(self, transcript_data):
        """
        Analyze arguments and claims in a transcript
        
        Args:
            transcript_data: Transcript data (string or task result)
            
        Returns:
            str: Argument analysis result
        """
        from agents.tasks.analysis import AnalysisTask
        
        task = AnalysisTask.create_argument_analysis_task(self, transcript_data)
        return self.execute_task(task)