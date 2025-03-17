# agents/definitions/summarizer.py
from agents.base import BaseAgent
from agents.registry import register_agent

@register_agent("summarizer")
class SummarizerAgent(BaseAgent):
    """Agent specialized in creating executive summaries"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Summarizer Agent"""
        super().__init__(
            role="Executive Summarizer",
            goal="Create concise, informative summaries of the Meeting content for business leaders",
            backstory="I specialize in distilling complex information into clear, actionable summaries "
                    "for executives. I understand what busy professionals need to know and can "
                    "highlight the most valuable insights from any content.",
            model=model
        )
    
    def create_summary(self, analysis_data):
        """
        Create an executive summary
        
        Args:
            analysis_data: Analysis data (string or task result)
            
        Returns:
            str: Summary result
        """
        from agents.tasks.summary import SummaryTask
        
        task = SummaryTask.create_summary_task(self, analysis_data)
        return self.execute_task(task)
    
    def create_enhanced_summary(self, input_data):
        """
        Create an enhanced summary using multiple inputs
        
        Args:
            input_data: Dictionary with analysis and other data
            
        Returns:
            str: Enhanced summary result
        """
        from agents.tasks.summary import SummaryTask
        
        task = SummaryTask.create_enhanced_summary_task(self, input_data)
        return self.execute_task(task)
    
    def create_bullet_summary(self, analysis_data):
        """
        Create a bullet-point summary
        
        Args:
            analysis_data: Analysis data (string or task result)
            
        Returns:
            str: Bullet summary result
        """
        from agents.tasks.summary import SummaryTask
        
        task = SummaryTask.create_bullet_summary_task(self, analysis_data)
        return self.execute_task(task)
    
    def create_tiered_summary(self, analysis_data):
        """
        Create a tiered summary (1-sentence, 1-paragraph, full)
        
        Args:
            analysis_data: Analysis data (string or task result)
            
        Returns:
            str: Tiered summary result
        """
        from agents.tasks.summary import SummaryTask
        
        task = SummaryTask.create_tiered_summary_task(self, analysis_data)
        return self.execute_task(task)