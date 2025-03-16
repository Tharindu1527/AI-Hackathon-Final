# agents/tasks/task_base.py
from crewai import Task
from agents.registry import get_agent

class BaseTask:
    """
    Base class for all task types
    
    This provides common functionality for creating and configuring tasks
    that can be executed by agents in the podcast analysis system.
    """
    
    @staticmethod
    def create_task(agent, description, expected_output, context=None, input_data=None, max_input_length=5000):
        """
        Create a CrewAI task with standardized formatting
        
        Args:
            agent: Agent that will execute the task (ID string or agent instance)
            description (str): Task description/instructions
            expected_output (str): Expected output format
            context (dict, optional): Additional context for the task
            input_data (str/dict/object, optional): Input data for the task
            max_input_length (int, optional): Maximum length of input data to include
            
        Returns:
            Task: CrewAI task
        """
        # Get agent instance if string is provided
        if isinstance(agent, str):
            agent_instance = get_agent(agent).create_agent()
        elif hasattr(agent, 'create_agent'):
            agent_instance = agent.create_agent()
        else:
            agent_instance = agent
        
        # Process input data if provided
        if input_data:
            # Handle different input types
            processed_input = BaseTask.process_input_data(input_data, max_input_length)
            
            # Add input content to description
            full_description = f"{description}\n\nINPUT:\n{processed_input}"
        else:
            full_description = description
            
        # Create the task
        task = Task(
            description=full_description,
            agent=agent_instance,
            expected_output=expected_output,
            context=context
        )
        
        return task
    
    @staticmethod
    def process_input_data(input_data, max_length=5000):
        """
        Process and format input data for a task
        
        Args:
            input_data: Input data in various formats
            max_length: Maximum length to include
            
        Returns:
            str: Processed input data
        """
        # Handle string inputs
        if isinstance(input_data, str):
            return input_data[:max_length]
            
        # Handle task objects
        elif hasattr(input_data, 'get'):
            return input_data.get("output", "")[:max_length]
            
        # Handle objects with output attribute
        elif hasattr(input_data, 'output'):
            return str(input_data.output)[:max_length]
            
        # Handle dictionaries with multiple inputs
        elif isinstance(input_data, dict):
            sections = []
            for key, value in input_data.items():
                if isinstance(value, str):
                    content = value[:max_length//len(input_data)]
                else:
                    content = str(value)[:max_length//len(input_data)]
                sections.append(f"{key.upper()}:\n{content}")
            return "\n\n".join(sections)
            
        # Handle other types
        else:
            return str(input_data)[:max_length]
    
    @staticmethod
    def execute_with_agent(task, agent_id=None, agent_instance=None, max_attempts=1):
        """
        Execute a task with a specified agent
        
        Args:
            task: Task to execute
            agent_id: ID of agent to use (alternative to agent_instance)
            agent_instance: Agent instance to use (alternative to agent_id)
            max_attempts: Maximum number of execution attempts
            
        Returns:
            str: Task result
        """
        # Get the agent if ID is provided
        if agent_id and not agent_instance:
            agent_instance = get_agent(agent_id)
            
        if not agent_instance:
            raise ValueError("Either agent_id or agent_instance must be provided")
            
        # Execute the task
        return agent_instance.execute_task(task, max_iterations=max_attempts)