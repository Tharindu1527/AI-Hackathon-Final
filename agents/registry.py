# agents/registry.py

class AgentRegistry:
    """
    Registry for managing podcast analysis agents
    
    This registry allows for centralized agent registration, configuration,
    and retrieval. It makes it easy to add new agents and integrate them
    into the processing workflow.
    """
    
    def __init__(self):
        """Initialize the agent registry"""
        self.agents = {}
        self.agent_classes = {}
        self.default_model = "gpt-4o"
    
    def register(self, agent_id, agent_class):
        """
        Register an agent class
        
        Args:
            agent_id (str): Unique identifier for the agent
            agent_class (class): Agent class extending BaseAgent
            
        Returns:
            bool: True if registration successful
        """
        if agent_id in self.agent_classes:
            print(f"Warning: Agent '{agent_id}' already registered. Overwriting.")
            
        self.agent_classes[agent_id] = agent_class
        return True
    
    def get_agent(self, agent_id, model=None):
        """
        Get an instance of an agent
        
        Args:
            agent_id (str): Agent identifier
            model (str, optional): Model to use for this agent
            
        Returns:
            BaseAgent: Agent instance
        """
        # Use provided model or default
        agent_model = model or self.default_model
        
        # Check if we already have an instance with this model
        instance_key = f"{agent_id}_{agent_model}"
        
        if instance_key in self.agents:
            return self.agents[instance_key]
            
        # Create a new instance if we don't have one yet
        if agent_id in self.agent_classes:
            agent_class = self.agent_classes[agent_id]
            agent = agent_class(model=agent_model)
            self.agents[instance_key] = agent
            return agent
        else:
            raise ValueError(f"Agent '{agent_id}' not registered")
    
    def get_all_agents(self, model=None):
        """
        Get all registered agents
        
        Args:
            model (str, optional): Model to use for all agents
            
        Returns:
            dict: Dictionary of agent instances by ID
        """
        agent_model = model or self.default_model
        
        agents = {}
        for agent_id in self.agent_classes:
            agents[agent_id] = self.get_agent(agent_id, agent_model)
            
        return agents
    
    def set_default_model(self, model):
        """
        Set the default model for all agents
        
        Args:
            model (str): Default model name
        """
        self.default_model = model


# Create a global registry instance
registry = AgentRegistry()


# Helper function to register an agent
def register_agent(agent_id):
    """
    Decorator to register an agent class with the registry
    
    Args:
        agent_id (str): Unique identifier for the agent
        
    Returns:
        function: Decorator function
    """
    def decorator(agent_class):
        registry.register(agent_id, agent_class)
        return agent_class
    return decorator


# Helper function to get an agent
def get_agent(agent_id, model=None):
    """
    Get an agent instance from the registry
    
    Args:
        agent_id (str): Agent identifier
        model (str, optional): Model to use
        
    Returns:
        BaseAgent: Agent instance
    """
    return registry.get_agent(agent_id, model)


# Helper function to get all agents
def get_all_agents(model=None):
    """
    Get all registered agents
    
    Args:
        model (str, optional): Model to use for all agents
        
    Returns:
        dict: Dictionary of agent instances by ID
    """
    return registry.get_all_agents(model)


# Helper function to set the default model
def set_default_model(model):
    """
    Set the default model for all agents
    
    Args:
        model (str): Default model name
    """
    registry.set_default_model(model)