# agents/base.py
from crewai import Agent
from langchain_openai import ChatOpenAI
from utils.config import get_openai_api_key

class BaseAgent:
    """Base class for all podcast analysis agents"""
    
    def __init__(self, role, goal, backstory, model="gpt-4o"):
        """
        Initialize a base agent
        
        Args:
            role: Agent's role
            goal: Agent's goal
            backstory: Agent's backstory
            model: OpenAI model to use
        """
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model
        self.llm = self._create_llm(model)
        
    def _create_llm(self, model):
        """
        Create a LangChain OpenAI LLM instance
        
        Args:
            model: OpenAI model to use
            
        Returns:
            ChatOpenAI: LangChain OpenAI instance
        """
        api_key = get_openai_api_key()
        return ChatOpenAI(api_key=api_key, model=model)
        
    def create_agent(self):
        """
        Create a CrewAI agent
        
        Returns:
            Agent: CrewAI agent
        """
        agent = Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
        
        return agent
    
    def process_input(self, input_data):
        """
        Process input data, handling different types
        
        Args:
            input_data: The input data (string, Task object, or dict)
            
        Returns:
            str: Processed input as string
        """
        # Handle different input types
        if hasattr(input_data, 'get'):
            # It's a Task object or dictionary
            content = input_data.get("output", input_data)
        elif hasattr(input_data, 'output'):
            # It's a Task object with direct output attribute
            content = input_data.output
        else:
            # It's already a string or other type
            content = input_data
        
        # Convert to string if it's not already
        if not isinstance(content, str):
            content = str(content)
            
        return content
        
    def execute_task(self, task, max_iterations=1):
        """
        Execute a task directly with this agent
        
        Args:
            task: The task to execute
            max_iterations: Maximum number of execution attempts
            
        Returns:
            str: Task result
        """
        agent = self.create_agent()
        
        try:
            print(f"Executing task with {self.role} agent...")
            result = agent.execute_task(task)
            print(f"Task completed successfully with {self.role} agent")
            return result
        except Exception as e:
            print(f"Error in {self.role} agent: {str(e)}")
            if max_iterations > 1:
                print(f"Retrying... ({max_iterations-1} attempts remaining)")
                return self.execute_task(task, max_iterations-1)
            else:
                return f"Error executing task with {self.role} agent: {str(e)}"