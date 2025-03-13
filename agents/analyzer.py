# agents/analyzer.py
from agents.base import BaseAgent

class AnalyzerAgent(BaseAgent):
    """Agent specialized in analyzing podcast content structure and topics"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Analyzer Agent"""
        super().__init__(
            role="Content Analyzer",
            goal="Analyze the transcript to identify key topics, themes, and structure of the podcast",
            backstory="I have a PhD in linguistics and content analysis with years of experience "
                    "breaking down complex discussions. I can identify the main topics, "
                    "track conversation flow, and understand the underlying structure of any podcast.",
            model=model
        )
        
    def create_task(self, transcript_task):
        """
        Create a task for the Analyzer Agent
        
        Args:
            transcript_task: The completed transcription task
            
        Returns:
            Task: CrewAI task
        """
        from crewai import Task
        
        task = Task(
            description="""
            Your task is to analyze the refined podcast transcript to identify:
            
            1. Main topics and key themes discussed
            2. The structure and flow of the conversation
            3. Important segments of the podcast
            4. Key points and arguments made
            5. Relationships between different topics
            6. The context and background of the discussion
            
            Create a detailed analysis that breaks down the podcast content by topic, 
            including timestamps (if available) or markers to reference specific sections.
            
            Your analysis should be thorough and provide a clear map of what the podcast covered.
            """,
            agent=self.create_agent(),
            expected_output="A detailed analysis of the podcast content structure and main points.",
            context=[transcript_task]
        )
        
        return task