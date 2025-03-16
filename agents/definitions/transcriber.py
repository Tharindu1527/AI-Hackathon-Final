# agents/definitions/transcriber.py
from agents.base import BaseAgent
from agents.registry import register_agent

@register_agent("transcriber")
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
    
    def process_transcript(self, transcript_text):
        """
        Process and refine a transcript directly from text
        
        Args:
            transcript_text: Raw transcript text
            
        Returns:
            str: Refined transcript
        """
        print(f"Processing transcript with {len(transcript_text)} characters")
        
        # Create and execute a transcription task
        from agents.tasks.transcription import TranscriptionTask
        
        task = TranscriptionTask.create_refinement_task(self, transcript_text)
        
        try:
            print("Executing transcriber task...")
            result = self.execute_task(task)
            print(f"Transcriber task completed successfully, result length: {len(str(result))}")
            return result
        except Exception as e:
            print(f"Error in transcriber agent: {str(e)}")
            # Return a simplified transcript as fallback
            return f"PROCESSED TRANSCRIPT: {transcript_text[:1000]}... [Content truncated due to error]"
    
    def segment_transcript(self, transcript_content):
        """
        Segment a transcript into logical sections
        
        Args:
            transcript_content: Processed transcript content
            
        Returns:
            str: Segmented transcript
        """
        from agents.tasks.transcription import TranscriptionTask
        
        task = TranscriptionTask.create_segmentation_task(self, transcript_content)
        return self.execute_task(task)