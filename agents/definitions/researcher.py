# agents/definitions/researcher.py
from agents.base import BaseAgent
from agents.registry import register_agent
from api.wiki_api import search_wikipedia, search_wikipedia_with_suggestions

@register_agent("researcher")
class ResearcherAgent(BaseAgent):
    """Agent specialized in researching additional context and information for Meeting topics"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Researcher Agent"""
        super().__init__(
            role="Topic Researcher",
            goal="Augment Meeting topics with additional research, context, and sources",
            backstory="I have a background in academic research with expertise in finding, "
                    "evaluating, and synthesizing information from diverse sources. "
                    "I excel at identifying knowledge gaps and providing valuable context "
                    "that enhances understanding of complex topics. My research is thorough, "
                    "balanced, and focused on providing practical insights.",
            model=model
        )
    
    def research_topic(self, topic, depth="medium"):
        """
        Research a specific topic
        
        Args:
            topic: Topic to research
            depth: Research depth (shallow, medium, deep)
            
        Returns:
            str: Research result
        """
        from agents.tasks.research import ResearchTask
        
        # First, try to get some Wikipedia context
        wiki_context = ""
        try:
            wiki_results = search_wikipedia(topic)
            if wiki_results:
                wiki_context = f"Wikipedia information: {wiki_results}"
        except Exception as e:
            print(f"Error accessing Wikipedia: {e}")
        
        # Create input data
        input_data = {
            "topic": topic,
            "depth": depth,
            "context": wiki_context
        }
        
        # Create and execute a research task
        task = ResearchTask.create_topic_research_task(self, input_data)
        return self.execute_task(task)
    
    def find_related_sources(self, topic, num_sources=3):
        """
        Find related sources for a topic
        
        Args:
            topic: Topic to find sources for
            num_sources: Number of sources to suggest
            
        Returns:
            list: List of suggested sources
        """
        from agents.tasks.research import ResearchTask
        
        # Create and execute a source finding task
        task = ResearchTask.create_source_finding_task(
            agent=self,
            topic=topic,
            num_sources=num_sources
        )
        
        result = self.execute_task(task)
        
        # Parse the result to extract sources
        # This assumes a particular format in the response
        sources = []
        for line in result.strip().split('\n'):
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                sources.append(line.strip()[2:])  # Remove the bullet
            elif line.strip().startswith('[') and ']' in line:
                # Extract from markdown format [title](link)
                parts = line.strip().split(']')
                if len(parts) > 1:
                    title = parts[0][1:]  # Remove the opening [
                    sources.append(title)
        
        return sources
    
    def augment_podcast_analysis(self, analysis_content):
        """
        Augment Meeting analysis with additional research
        
        Args:
            analysis_content: Meeting analysis content
            
        Returns:
            str: Augmented analysis with research
        """
        from agents.tasks.research import ResearchTask
        
        # Create and execute an augmentation task
        task = ResearchTask.create_analysis_augmentation_task(self, analysis_content)
        return self.execute_task(task)
    
    def extract_key_topics_for_research(self, summary_content, max_topics=3):
        """
        Extract key topics that need additional research
        
        Args:
            summary_content: Meeting summary content
            max_topics: Maximum number of topics to extract
            
        Returns:
            list: List of topics for research
        """
        from agents.tasks.research import ResearchTask
        
        # Create and execute a topic extraction task
        task = ResearchTask.create_topic_extraction_task(
            agent=self,
            summary_content=summary_content,
            max_topics=max_topics
        )
        
        result = self.execute_task(task)
        
        # Parse the result to extract topics
        topics = []
        for line in result.strip().split('\n'):
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                topics.append(line.strip()[2:])  # Remove the bullet
            elif ':' in line and len(line.split(':')[0]) < 30:
                # Format may be "Topic: description"
                topics.append(line.split(':')[0].strip())
        
        return topics[:max_topics]