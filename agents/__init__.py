# agents/__init__.py
"""
Podcast Analysis Agents Package

This package contains the agents, tasks, and registry for analyzing podcasts.
"""

# Import the registry for easy access
from agents.registry import (
    get_agent,
    get_all_agents,
    register_agent,
    set_default_model
)

# Import base classes
from agents.base import BaseAgent

# Import all definitions to ensure registration
from agents.definitions import *

# Import all tasks
from agents.tasks import *