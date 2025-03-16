# crews/__init__.py
"""
Podcast Analysis Crews Package

This package contains crew definitions for orchestrating agents
to analyze podcasts with different capabilities and specializations.
"""

# Import base crew
from crews.base_crew import BaseCrew

# Import standard podcast crews
from crews.podcast_crew import (
    PodcastCrew,  
    EnhancedPodcastCrew, 
    MultilingualPodcastCrew,
    ResearchPodcastCrew
)

# Import specialized research crews
from crews.research_crew import (
    DeepResearchCrew,
    FactCheckingCrew
)

# Import specialized multilingual crews
from crews.multilingual_crew import (
    AdvancedMultilingualCrew,
    LocalizationCrew
)

# Dictionary of available crews for easy access
AVAILABLE_CREWS = {
    "standard": PodcastCrew,
    "enhanced": EnhancedPodcastCrew,
    "multilingual": MultilingualPodcastCrew,
    "research": ResearchPodcastCrew,
    "deep_research": DeepResearchCrew,
    "fact_checking": FactCheckingCrew,
    "advanced_multilingual": AdvancedMultilingualCrew,
    "localization": LocalizationCrew
}

def get_crew(crew_type="standard", **kwargs):
    """
    Get a crew by type with optional configuration
    
    Args:
        crew_type: Type of crew to create
        **kwargs: Additional arguments to pass to the crew constructor
        
    Returns:
        BaseCrew: Configured crew instance
    """
    if crew_type not in AVAILABLE_CREWS:
        raise ValueError(f"Unknown crew type: {crew_type}. Available types: {list(AVAILABLE_CREWS.keys())}")
    
    # Create and return the crew instance
    return AVAILABLE_CREWS[crew_type](**kwargs)

def list_available_crews():
    """
    List all available crew types
    
    Returns:
        list: List of available crew types
    """
    return list(AVAILABLE_CREWS.keys())