# agents/tasks/summary.py
from agents.tasks.task_base import BaseTask

class SummaryTask(BaseTask):
    """Tasks related to summarizing podcast content"""
    
    @staticmethod
    def create_summary_task(agent, analysis_data):
        """
        Create a summary task
        
        Args:
            agent: Summarizer agent (ID or instance)
            analysis_data: Analysis data (string or task result)
            
        Returns:
            Task: Summary task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to create an executive summary of the podcast based on the detailed analysis.
            
            The summary should:
            
            1. Be concise yet comprehensive (300-500 words)
            2. Highlight the most important insights and takeaways
            3. Be structured for easy consumption by busy executives
            4. Focus on actionable information and business value
            5. Use clear, direct language without technical jargon
            6. Include a brief overview of the podcast context
            
            The summary must be valuable to board members who need to understand the key points
            without listening to the entire podcast.
            """,
            expected_output="A concise executive summary highlighting the most important information.",
            input_data=analysis_data
        )
    
    @staticmethod
    def create_enhanced_summary_task(agent, input_data):
        """
        Create an enhanced summary task using multiple inputs
        
        Args:
            agent: Summarizer agent (ID or instance)
            input_data: Dictionary with analysis and other data
            
        Returns:
            Task: Enhanced summary task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to create a comprehensive executive summary of the podcast using all the provided inputs.
            
            The summary should:
            
            1. Be thorough yet accessible (400-600 words)
            2. Synthesize insights from all provided data sources
            3. Highlight the most important information and key takeaways
            4. Address any factual claims and their verification status
            5. Be structured in clear sections for easy consumption
            6. Use engaging, professional language appropriate for executives
            
            Provide a high-value summary that gives decision-makers a complete understanding
            of the podcast's content, context, and implications.
            """,
            expected_output="A comprehensive executive summary that integrates all input sources.",
            input_data=input_data
        )
    
    @staticmethod
    def create_bullet_summary_task(agent, analysis_data):
        """
        Create a bullet-point summary task
        
        Args:
            agent: Summarizer agent (ID or instance)
            analysis_data: Analysis data (string or task result)
            
        Returns:
            Task: Bullet summary task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to create a bullet-point summary of the podcast:
            
            1. Start with a 1-2 sentence overview of the podcast
            2. Create 5-7 bullet points highlighting key takeaways
            3. For each bullet point, provide a concise 1-2 sentence explanation
            4. Focus on the most important and actionable information
            5. Present points in order of importance or logical flow
            6. Use consistent formatting and parallel structure
            
            The summary should be scannable and easy to digest at a glance.
            """,
            expected_output="A bullet-point summary with brief explanations for each point.",
            input_data=analysis_data
        )
    
    @staticmethod
    def create_tiered_summary_task(agent, analysis_data):
        """
        Create a tiered summary task (1-sentence, 1-paragraph, full)
        
        Args:
            agent: Summarizer agent (ID or instance)
            analysis_data: Analysis data (string or task result)
            
        Returns:
            Task: Tiered summary task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to create a tiered summary of the podcast at three levels of detail:
            
            1. One-sentence summary: The most essential point in a single sentence
            2. One-paragraph summary: Key points in a concise paragraph (3-5 sentences)
            3. Full executive summary: Complete overview with all important details (300-500 words)
            
            Each level should be self-contained while maintaining consistency across all three.
            Structure the response with clear headings for each summary level.
            """,
            expected_output="A three-tiered summary with one-sentence, one-paragraph, and full versions.",
            input_data=analysis_data
        )
    
    @staticmethod
    def execute_summary(analysis_data, agent_id="summarizer", agent_instance=None):
        """
        Execute summary creation directly
        
        Args:
            analysis_data: Analysis data
            agent_id: ID of summarizer agent (if not providing instance)
            agent_instance: Summarizer agent instance (if not providing ID)
            
        Returns:
            str: Summary result
        """
        task = SummaryTask.create_summary_task(
            agent=agent_instance or agent_id,
            analysis_data=analysis_data
        )
        
        return BaseTask.execute_with_agent(
            task=task,
            agent_id=agent_id,
            agent_instance=agent_instance
        )