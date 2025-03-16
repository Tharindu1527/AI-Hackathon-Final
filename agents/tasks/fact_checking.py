# agents/tasks/fact_checking.py
from agents.tasks.task_base import BaseTask

class FactCheckingTask(BaseTask):
    """Tasks related to fact checking podcast content"""
    
    @staticmethod
    def create_claim_extraction_task(agent, transcript_content):
        """
        Create a task to extract factual claims from a transcript
        
        Args:
            agent: Fact checker agent (ID or instance)
            transcript_content: Transcript content
            
        Returns:
            Task: Claim extraction task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to extract factual claims from the podcast transcript:
            
            1. Identify specific factual statements (not opinions or predictions)
            2. Focus on claims about events, statistics, historical facts, or scientific information
            3. Include claims that are verifiable through research
            4. Extract the exact wording of each claim when possible
            5. Include the speaker attribution if available
            6. Prioritize the most significant or potentially controversial claims
            
            Format each claim as a clear, concise statement that can be verified.
            """,
            expected_output="A list of factual claims extracted from the podcast, formatted as bullet points.",
            input_data=transcript_content
        )
    
    @staticmethod
    def create_verification_task(agent, input_data):
        """
        Create a task to verify a factual claim
        
        Args:
            agent: Fact checker agent (ID or instance)
            input_data: Dict containing the claim and context
            
        Returns:
            Task: Verification task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to verify the factual accuracy of the provided claim:
            
            1. Assess whether the claim appears to be true, false, partially true, or unverifiable
            2. Use your knowledge to evaluate the claim's accuracy
            3. If context information is provided, consider it in your assessment
            4. Explain your reasoning
            5. Note any important qualifications or nuances
            6. If you determine the claim is false or partially true, explain why
            
            Your verification should be objective and based on factual information only.
            """,
            expected_output="A verification result indicating whether the claim is TRUE, FALSE, PARTIALLY TRUE, or UNVERIFIABLE, followed by an explanation.",
            input_data=input_data
        )
    
    @staticmethod
    def create_comprehensive_fact_check_task(agent, analysis_data):
        """
        Create a task for comprehensive fact checking of the entire podcast
        
        Args:
            agent: Fact checker agent (ID or instance)
            analysis_data: Podcast analysis data
            
        Returns:
            Task: Comprehensive fact check task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to perform a comprehensive fact check of the podcast:
            
            1. Review the podcast analysis for factual claims
            2. Identify the 5-10 most significant claims that warrant verification
            3. Assess the accuracy of each identified claim
            4. Provide verification status (Verified, Refuted, Partially Verified, or Unverifiable)
            5. For each claim, provide brief reasoning for your assessment
            6. Highlight any patterns of misinformation or areas requiring further verification
            
            Create a structured fact checking report that would be valuable to someone evaluating the accuracy of the podcast.
            """,
            expected_output="A comprehensive fact checking report with verification of key claims and overall assessment.",
            input_data=analysis_data
        )
    
    @staticmethod
    def execute_claim_extraction(transcript_content, agent_id="fact_checker", agent_instance=None):
        """
        Execute claim extraction directly
        
        Args:
            transcript_content: Transcript content
            agent_id: ID of fact checker agent (if not providing instance)
            agent_instance: Fact checker agent instance (if not providing ID)
            
        Returns:
            str: Extracted claims
        """
        task = FactCheckingTask.create_claim_extraction_task(
            agent=agent_instance or agent_id,
            transcript_content=transcript_content
        )
        
        return BaseTask.execute_with_agent(
            task=task,
            agent_id=agent_id,
            agent_instance=agent_instance
        )
    
    @staticmethod
    def execute_verification(claim, context="", agent_id="fact_checker", agent_instance=None):
        """
        Execute claim verification directly
        
        Args:
            claim: The claim to verify
            context: Optional context for verification
            agent_id: ID of fact checker agent (if not providing instance)
            agent_instance: Fact checker agent instance (if not providing ID)
            
        Returns:
            str: Verification result
        """
        input_data = {
            "claim": claim,
            "context": context
        }
        
        task = FactCheckingTask.create_verification_task(
            agent=agent_instance or agent_id,
            input_data=input_data
        )
        
        return BaseTask.execute_with_agent(
            task=task,
            agent_id=agent_id,
            agent_instance=agent_instance
        )