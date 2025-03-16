# agents/tasks/transcription.py
from agents.tasks.task_base import BaseTask

class TranscriptionTask(BaseTask):
    """Tasks related to podcast transcription and processing"""
    
    @staticmethod
    def create_refinement_task(agent, transcript_content):
        """
        Create a transcript refinement task
        
        Args:
            agent: Transcriber agent (ID or instance)
            transcript_content: Raw transcript content
            
        Returns:
            Task: Transcript refinement task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to review and refine the following transcript:
            
            1. Correct any obvious transcription errors
            2. Format the transcript for better readability
            3. If there are multiple speakers, try to identify and label them
            4. Ensure punctuation and paragraph breaks are appropriate
            5. Remove filler words and correct sentence structures when appropriate
            6. Maintain the original meaning and context of the discussion
            
            The refined transcript should be accurate, well-formatted, and ready for deeper analysis.
            """,
            expected_output="A complete and refined text transcript with proper formatting and speaker identification where possible.",
            input_data=transcript_content
        )
    
    @staticmethod
    def create_segmentation_task(agent, transcript_content):
        """
        Create a transcript segmentation task
        
        Args:
            agent: Transcriber agent (ID or instance)
            transcript_content: Processed transcript content
            
        Returns:
            Task: Transcript segmentation task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to segment the podcast transcript into logical sections:
            
            1. Identify natural break points in the conversation
            2. Create labeled sections for different topics or segments
            3. For each section, provide a brief title or description
            4. Note approximate timestamps if available
            5. Preserve the original content within each segment
            
            The segmented transcript should provide a clear structure of the podcast's content flow.
            """,
            expected_output="A segmented transcript with labeled sections and brief descriptive titles.",
            input_data=transcript_content
        )
    
    @staticmethod
    def execute_refinement(transcript_content, agent_id="transcriber", agent_instance=None):
        """
        Execute transcript refinement directly
        
        Args:
            transcript_content: Raw transcript content
            agent_id: ID of transcriber agent (if not providing instance)
            agent_instance: Transcriber agent instance (if not providing ID)
            
        Returns:
            str: Refined transcript
        """
        task = TranscriptionTask.create_refinement_task(
            agent=agent_instance or agent_id,
            transcript_content=transcript_content
        )
        
        return BaseTask.execute_with_agent(
            task=task,
            agent_id=agent_id,
            agent_instance=agent_instance,
            max_attempts=2
        )