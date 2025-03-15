# agents/transcriber.py (fixed)
from agents.base import BaseAgent
from crewai import Task

class TranscriberAgent(BaseAgent):
    """Agent specialized in podcast transcription refinement"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Transcriber Agent"""
        super().__init__(
            role="Podcast Transcriber",
            goal="Accurately refine and enhance the raw podcast transcript, identifying speakers and ensuring clarity",
            backstory="I am an expert in speech recognition with exceptional hearing abilities. "
                    "I can distinguish different speakers, correct transcription errors, and ensure "
                    "the transcript accurately represents what was said in the podcast.",
            model=model
        )
        
    def create_task(self, transcript_content):
        """
        Create a task for the Transcriber Agent
        
        Args:
            transcript_content: The transcript content as a string
            
        Returns:
            Task: CrewAI task
        """
        task = Task(
            description=f"""
            Your task is to review and refine the following transcript:
            
            {transcript_content[:5000]}  # Limiting to 5000 characters to avoid issues
            
            1. Correct any obvious transcription errors
            2. Format the transcript for better readability
            3. If there are multiple speakers, try to identify and label them
            4. Ensure punctuation and paragraph breaks are appropriate
            5. Remove filler words and correct sentence structures when appropriate
            6. Maintain the original meaning and context of the discussion
            
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
        print(f"Processing transcript with {len(transcript_text)} characters")
        
        # Create and execute the task directly with the content
        task = self.create_task(transcript_text)
        agent = self.create_agent()
        
        try:
            print("Executing transcriber task...")
            result = agent.execute_task(task)
            print(f"Transcriber task completed successfully, result length: {len(str(result))}")
            return result
        except Exception as e:
            print(f"Error in transcriber agent: {str(e)}")
            # Return a simplified transcript as fallback
            return f"PROCESSED TRANSCRIPT: {transcript_text[:1000]}... [Content truncated due to error]"