# agents/definitions/action_item.py
from agents.base import BaseAgent
from agents.registry import register_agent

@register_agent("action_item")
class ActionItemAgent(BaseAgent):
    """Agent specialized in extracting actionable insights and recommendations"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Action Item Agent"""
        super().__init__(
            role="Action Item Extractor",
            goal="Identify and extract actionable insights and recommendations from the podcast",
            backstory="I excel at identifying practical next steps and business implications from discussions. "
                    "With a background in strategic consulting, I can translate insights into concrete "
                    "action items that organizations can implement for meaningful results.",
            model=model
        )
    
    def extract_action_items(self, summary_data, sentiment_data=None):
        """
        Extract action items from podcast content
        
        Args:
            summary_data: Summary data (string or task result)
            sentiment_data: Optional sentiment data (string or task result)
            
        Returns:
            str: Action items result
        """
        from agents.tasks.action_items import ActionItemsTask
        
        task = ActionItemsTask.create_action_items_task(self, summary_data, sentiment_data)
        return self.execute_task(task)
    
    def extract_enhanced_action_items(self, input_data):
        """
        Extract enhanced action items with multiple inputs
        
        Args:
            input_data: Dictionary with summary, sentiment, and research data
            
        Returns:
            str: Enhanced action items result
        """
        from agents.tasks.action_items import ActionItemsTask
        
        task = ActionItemsTask.create_enhanced_action_items_task(self, input_data)
        return self.execute_task(task)
    
    def extract_categorized_action_items(self, summary_data, categories=None):
        """
        Extract and categorize action items
        
        Args:
            summary_data: Summary data (string or task result)
            categories: Optional list of categories to use
            
        Returns:
            str: Categorized action items result
        """
        from agents.tasks.action_items import ActionItemsTask
        
        task = ActionItemsTask.create_categorized_action_items_task(self, summary_data, categories)
        return self.execute_task(task)