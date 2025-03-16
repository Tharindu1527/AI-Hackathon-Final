# agents/tasks/analysis.py
from agents.tasks.task_base import BaseTask

class AnalysisTask(BaseTask):
    """Tasks related to content analysis of podcast transcripts"""
    
    @staticmethod
    def create_content_analysis_task(agent, transcript_data):
        """
        Create a content analysis task
        
        Args:
            agent: Analyzer agent (ID or instance)
            transcript_data: Transcript data (string or task result)
            
        Returns:
            Task: Content analysis task
        """
        return BaseTask.create_task(
            agent=agent,
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
            expected_output="A detailed analysis of the podcast content structure and main points.",
            input_data=transcript_data
        )
    
    @staticmethod
    def create_topic_extraction_task(agent, transcript_data):
        """
        Create a topic extraction task
        
        Args:
            agent: Analyzer agent (ID or instance)
            transcript_data: Transcript data (string or task result)
            
        Returns:
            Task: Topic extraction task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to extract and categorize the main topics discussed in the podcast:
            
            1. List all significant topics mentioned in the podcast
            2. For each topic, provide a brief description and context
            3. Identify which topics were covered in most depth
            4. Note connections between different topics
            5. Categorize topics by domain (e.g., technology, business, science)
            
            The goal is to provide a comprehensive map of the podcast's content areas.
            """,
            expected_output="A structured list of topics with descriptions, categories, and significance levels.",
            input_data=transcript_data
        )
    
    @staticmethod
    def create_argument_analysis_task(agent, transcript_data):
        """
        Create an argument analysis task
        
        Args:
            agent: Analyzer agent (ID or instance)
            transcript_data: Transcript data (string or task result)
            
        Returns:
            Task: Argument analysis task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to analyze the arguments and claims made in the podcast:
            
            1. Identify major claims or arguments presented
            2. Note the evidence provided to support each claim
            3. Evaluate the logic and reasoning used
            4. Highlight any counterarguments or alternative perspectives mentioned
            5. Assess the overall strength of key arguments
            
            Focus on the substance of the discussion rather than stylistic elements.
            """,
            expected_output="An analysis of the key arguments and claims with their supporting evidence and logical structure.",
            input_data=transcript_data
        )
    
    @staticmethod
    def execute_content_analysis(transcript_data, agent_id="analyzer", agent_instance=None):
        """
        Execute content analysis directly
        
        Args:
            transcript_data: Transcript data (string or task result)
            agent_id: ID of analyzer agent (if not providing instance)
            agent_instance: Analyzer agent instance (if not providing ID)
            
        Returns:
            str: Content analysis result
        """
        task = AnalysisTask.create_content_analysis_task(
            agent=agent_instance or agent_id,
            transcript_data=transcript_data
        )
        
        return BaseTask.execute_with_agent(
            task=task,
            agent_id=agent_id,
            agent_instance=agent_instance
        )