# agents/tasks/action_items.py
from agents.tasks.task_base import BaseTask

class ActionItemsTask(BaseTask):
    """Tasks related to extracting action items from podcast content"""
    
    @staticmethod
    def create_action_items_task(agent, summary_data, sentiment_data=None):
        """
        Create an action items extraction task
        
        Args:
            agent: Action item agent (ID or instance)
            summary_data: Summary data (string or task result)
            sentiment_data: Optional sentiment data (string or task result)
            
        Returns:
            Task: Action items task
        """
        input_dict = {"summary": summary_data}
        if sentiment_data:
            input_dict["sentiment"] = sentiment_data
            
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to extract actionable insights and recommendations from the podcast summary and sentiment analysis.
            
            Focus on:
            
            1. Concrete action items mentioned or implied in the podcast
            2. Strategic recommendations based on the insights discussed
            3. Potential business opportunities highlighted
            4. Areas requiring further research or investigation
            5. Explicit next steps suggested by podcast participants
            6. Prioritization of actions based on impact and feasibility
            
            Format the output as a clear list of action items, each with a brief context and potential benefit.
            The goal is to provide board members with a practical roadmap based on the podcast content.
            """,
            expected_output="A prioritized list of actionable insights and recommendations with clear next steps.",
            input_data=input_dict
        )
    
    @staticmethod
    def create_enhanced_action_items_task(agent, input_data):
        """
        Create an enhanced action items task with multiple inputs
        
        Args:
            agent: Action item agent (ID or instance)
            input_data: Dictionary with summary, sentiment, and research data
            
        Returns:
            Task: Enhanced action items task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to extract comprehensive, high-value action items from all the provided inputs.
            
            Focus on:
            
            1. Synthesizing insights from all input sources to identify actionable recommendations
            2. Providing well-researched, strategic action items with clear implementation paths
            3. Prioritizing recommendations based on potential impact, urgency, and feasibility
            4. Including both short-term tactical steps and long-term strategic initiatives
            5. Addressing different stakeholder perspectives and needs
            6. Connecting recommendations to business objectives and outcomes
            
            For each action item, provide:
            - A clear, specific recommendation title
            - Context explaining why this action matters
            - Implementation guidance (how to execute)
            - Expected benefit or outcome
            
            Format as a structured, prioritized list that executives can easily review and implement.
            """,
            expected_output="A comprehensive set of prioritized action items with context, implementation guidance, and expected benefits.",
            input_data=input_data
        )
    
    @staticmethod
    def create_categorized_action_items_task(agent, summary_data, categories=None):
        """
        Create a categorized action items task
        
        Args:
            agent: Action item agent (ID or instance)
            summary_data: Summary data (string or task result)
            categories: Optional list of categories to use
            
        Returns:
            Task: Categorized action items task
        """
        input_dict = {"summary": summary_data}
        
        if categories:
            if isinstance(categories, list):
                categories_str = ", ".join(categories)
            else:
                categories_str = categories
                
            input_dict["categories"] = categories_str
        
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to extract and categorize action items from the podcast content:
            
            1. Identify all actionable insights and recommendations from the podcast
            2. Categorize each action item by type (e.g., strategic, operational, research)
            3. If specific categories were provided, use those for classification
            4. For each action item, provide context and expected benefit
            5. Within each category, prioritize items by importance
            6. Ensure all key areas from the podcast are represented
            
            Format the output as a categorized list of action items with clear headings for each category.
            """,
            expected_output="A categorized and prioritized list of action items organized by type.",
            input_data=input_dict
        )
    
    @staticmethod
    def execute_action_items_extraction(summary_data, sentiment_data=None, agent_id="action_item", agent_instance=None):
        """
        Execute action items extraction directly
        
        Args:
            summary_data: Summary data
            sentiment_data: Optional sentiment data
            agent_id: ID of action item agent (if not providing instance)
            agent_instance: Action item agent instance (if not providing ID)
            
        Returns:
            str: Action items result
        """
        task = ActionItemsTask.create_action_items_task(
            agent=agent_instance or agent_id,
            summary_data=summary_data,
            sentiment_data=sentiment_data
        )
        
        return BaseTask.execute_with_agent(
            task=task,
            agent_id=agent_id,
            agent_instance=agent_instance
        )