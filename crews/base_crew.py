# crews/base_crew.py
import json
import os
from crewai import Crew
from agents.registry import get_agent, set_default_model, get_all_agents
from utils.result_parser import parse_crew_result

class BaseCrew:
    """Base class for podcast analysis crews"""
    
    def __init__(self, model="gpt-4o"):
        """
        Initialize a base crew
        
        Args:
            model: LLM model to use for all agents
        """
        self.model = model
        self.agents = {}
        self.tasks = []
        
        # Set the default model for all agents
        set_default_model(model)
    
    def add_agent(self, agent_id):
        """
        Add an agent to the crew
        
        Args:
            agent_id: ID of the agent to add
            
        Returns:
            BaseCrew: Self for chaining
        """
        if agent_id not in self.agents:
            agent = get_agent(agent_id)
            self.agents[agent_id] = agent
        
        return self
    
    def add_task(self, task):
        """
        Add a task to the crew
        
        Args:
            task: Task to add
            
        Returns:
            BaseCrew: Self for chaining
        """
        self.tasks.append(task)
        return self
    
    def run(self):
        """
        Run the crew with all configured agents and tasks
        
        Returns:
            str: JSON string with results
        """
        try:
            # Create CrewAI agent instances for all agents
            crew_agents = [agent.create_agent() for agent in self.agents.values()]
            
            # Create and run the crew
            crew = Crew(
                agents=crew_agents,
                tasks=self.tasks,
                verbose=True
            )
            
            # Run the analysis
            result = crew.kickoff()
            
            # Handle the result type
            if hasattr(result, 'raw_output'):
                raw_result = result.raw_output  # CrewOutput with raw_output
            elif hasattr(result, '__str__'):
                raw_result = str(result)  # Stringable object
            else:
                raw_result = "Failed to extract raw result from crew output"
            
            # Save raw result for debugging
            self._save_debug_output(raw_result)
            
            # Parse and structure the results
            structured_result = self._structure_results(raw_result)
            
            # Return as JSON string
            return json.dumps(structured_result)
            
        except Exception as e:
            print(f"Error in crew execution: {str(e)}")
            
            # Return fallback result
            fallback_result = {
                "error": True,
                "message": f"The analysis encountered an error: {str(e)}",
                "summary": "The analysis could not be completed due to an error.",
                "key_topics": ["Error occurred", "Analysis incomplete"],
                "sentiment_analysis": "Sentiment analysis could not be completed.",
                "action_items": ["Try again with different settings", "Check agent configuration"]
            }
            
            return json.dumps(fallback_result)
    
    def _save_debug_output(self, raw_result):
        """
        Save raw result for debugging
        
        Args:
            raw_result: Raw result string from CrewAI
        """
        debug_dir = "debug_output"
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
        
        with open(os.path.join(debug_dir, "raw_crew_result.txt"), "w", encoding="utf-8") as f:
            f.write(raw_result)
        
        print(f"Raw result from crew (first 500 chars): {raw_result[:500]}...")
    
    def _structure_results(self, raw_result):
        """
        Structure the raw results from the crew into a clean format
        
        Args:
            raw_result: Raw result string from CrewAI
            
        Returns:
            dict: Structured results
        """
        try:
            # Parse the crew result
            structured_result = parse_crew_result(raw_result)
            
            # Validate results
            self._validate_results(structured_result)
            
            return structured_result
            
        except Exception as e:
            print(f"Error in _structure_results: {e}")
            
            # Create a fallback structure for the results
            fallback_result = {
                "error": True,
                "message": f"Result parsing error: {str(e)}",
                "summary": "The analysis could not be properly structured due to an error in processing.",
                "key_topics": ["Error in topic extraction", "Please check the agent configuration"],
                "sentiment_analysis": "Sentiment analysis could not be structured properly.",
                "action_items": ["Review the transcript format", "Check agent configuration"]
            }
            
            return fallback_result
    
    def _validate_results(self, structured_result):
        """
        Validate the structured results and log warnings for missing data
        
        Args:
            structured_result: Structured results dictionary
        """
        validation_fields = [
            ("summary", "Summary is empty after parsing"),
            ("key_topics", "Key topics list is empty after parsing"),
            ("sentiment_analysis", "Sentiment analysis is empty after parsing"),
            ("action_items", "Action items list is empty after parsing")
        ]
        
        for field, warning in validation_fields:
            if not structured_result.get(field):
                print(f"Warning: {warning}")
                
            # For list fields, check if they're empty lists
            if field in structured_result and isinstance(structured_result[field], list) and not structured_result[field]:
                print(f"Warning: {warning}")