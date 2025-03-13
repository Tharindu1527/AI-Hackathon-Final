# agents/transcriber.py
from agents.base import BaseAgent
from crewai import Task

class TranscriberAgent(BaseAgent):
    """Agent specialized in podcast transcription refinement"""
    
    def __init__(self, model="gpt-4"):
        """Initialize the Transcriber Agent"""
        super().__init__(
            role="Podcast Transcriber",
            goal="Accurately refine and enhance the raw podcast transcript, identifying speakers and ensuring clarity",
            backstory="I am an expert in speech recognition with exceptional hearing abilities. "
                    "I can distinguish different speakers, correct transcription errors, and ensure "
                    "the transcript accurately represents what was said in the podcast.",
            model=model
        )
        
    def create_task(self, transcript_path):
        """
        Create a task for the Transcriber Agent
        
        Args:
            transcript_path: Path to the transcript file
            
        Returns:
            Task: CrewAI task
        """
        task = Task(
            description=f"""
            Your task is to review and refine the transcript at {transcript_path}.
            
            1. Read the transcript thoroughly
            2. Correct any obvious transcription errors
            3. Format the transcript for better readability
            4. If there are multiple speakers, try to identify and label them
            5. Ensure punctuation and paragraph breaks are appropriate
            6. Remove filler words and correct sentence structures when appropriate
            7. Maintain the original meaning and context of the discussion
            
            The refined transcript should be accurate, well-formatted, and ready for deeper analysis.
            """,
            agent=self.create_agent(),
            expected_output="A complete and refined text transcript of the podcast with proper formatting and speaker identification where possible.",
            async_execution=False
        )
        
        return task
        
    def process_transcript(self, transcript_text):
        """
        Process and refine a transcript directly from text
        
        Args:
            transcript_text: Raw transcript text
            
        Returns:
            str: Refined transcript
        """
        # Create a temporary file with the transcript
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tmp_file:
            tmp_file.write(transcript_text)
            transcript_path = tmp_file.name
        
        # Create and execute the task
        task = self.create_task(transcript_path)
        agent = self.create_agent()
        result = agent.execute_task(task)
        
        # Clean up the temporary file
        import os
        os.unlink(transcript_path)
        
        return result