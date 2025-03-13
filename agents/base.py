# agents/base.py
from crewai import Agent
from langchain_openai import ChatOpenAI
from utils.config import get_openai_api_key

def create_openai_llm(model="gpt-4o"):
    """
    Create a LangChain OpenAI LLM instance
    
    Args:
        model: OpenAI model to use
        
    Returns:
        ChatOpenAI: LangChain OpenAI instance
    """
    api_key = get_openai_api_key()
    return ChatOpenAI(api_key=api_key, model=model)

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
        self.llm = create_openai_llm(model)
        
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