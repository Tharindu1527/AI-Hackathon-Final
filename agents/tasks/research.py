# agents/tasks/research.py
from agents.tasks.task_base import BaseTask

class ResearchTask(BaseTask):
    """Tasks related to research and information augmentation"""
    
    @staticmethod
    def create_topic_research_task(agent, input_data):
        """
        Create a topic research task
        
        Args:
            agent: Researcher agent (ID or instance)
            input_data: Dict with topic, depth, and optional context
            
        Returns:
            Task: Topic research task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to research the specified topic and provide valuable insights:
            
            1. Provide key background information on the topic
            2. Identify major concepts, theories, or frameworks related to it
            3. Highlight important developments or changes in understanding
            4. Note any controversies or competing perspectives
            5. Connect the topic to broader contexts or applications
            6. Consider implications for relevant industries or fields
            
            Focus on providing accurate, balanced, and insightful information.
            """,
            expected_output="A well-structured research report on the topic with key insights and context.",
            input_data=input_data
        )
    
    @staticmethod
    def create_source_finding_task(agent, topic, num_sources=3):
        """
        Create a source finding task
        
        Args:
            agent: Researcher agent (ID or instance)
            topic: Topic to find sources for
            num_sources: Number of sources to recommend
            
        Returns:
            Task: Source finding task
        """
        input_data = {
            "topic": topic,
            "num_sources": num_sources
        }
        
        return BaseTask.create_task(
            agent=agent,
            description=f"""
            Your task is to recommend {num_sources} high-quality sources about this topic:
            
            1. Suggest specific books, articles, research papers, or other resources
            2. Focus on authoritative, reliable, and reputable sources
            3. Provide a brief description of each source and its relevance
            4. Include a mix of accessible and in-depth sources when appropriate
            5. Consider sources that offer different perspectives on the topic
            
            The goal is to provide valuable resources for someone wanting to learn more about this topic.
            """,
            expected_output=f"A list of {num_sources} recommended sources with brief descriptions.",
            input_data=input_data
        )
    
    @staticmethod
    def create_analysis_augmentation_task(agent, analysis_content):
        """
        Create an analysis augmentation task
        
        Args:
            agent: Researcher agent (ID or instance)
            analysis_content: Content to augment with research
            
        Returns:
            Task: Analysis augmentation task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to augment the podcast analysis with additional research:
            
            1. Identify 3-5 key topics in the analysis that would benefit from context
            2. For each topic, add relevant background information
            3. Provide industry context, historical perspective, or expert insights
            4. Integrate the research seamlessly with the existing analysis
            5. Maintain a balanced perspective, noting different viewpoints when relevant
            6. Keep additions concise and focused on enhancing understanding
            
            The augmented analysis should enrich the original content while maintaining its structure.
            """,
            expected_output="An enhanced version of the analysis with valuable additional context and research.",
            input_data=analysis_content
        )
    
    @staticmethod
    def create_topic_extraction_task(agent, summary_content, max_topics=3):
        """
        Create a topic extraction for research task
        
        Args:
            agent: Researcher agent (ID or instance)
            summary_content: Content to extract topics from
            max_topics: Maximum number of topics to extract
            
        Returns:
            Task: Topic extraction task
        """
        input_data = {
            "content": summary_content,
            "max_topics": max_topics
        }
        
        return BaseTask.create_task(
            agent=agent,
            description=f"""
            Your task is to identify {max_topics} key topics from the content that would benefit most from additional research:
            
            1. Focus on complex or specialized topics mentioned in the content
            2. Select topics that are central to understanding the main ideas
            3. Identify areas where additional context would be most valuable
            4. For each topic, briefly explain why it deserves further research
            5. Prioritize topics based on importance and knowledge gaps
            
            List the topics in order of research priority.
            """,
            expected_output=f"A prioritized list of {max_topics} topics for further research with brief justifications.",
            input_data=input_data
        )
    
    @staticmethod
    def execute_topic_research(topic, depth="medium", agent_id="researcher", agent_instance=None):
        """
        Execute topic research directly
        
        Args:
            topic: Topic to research
            depth: Research depth
            agent_id: ID of researcher agent (if not providing instance)
            agent_instance: Researcher agent instance (if not providing ID)
            
        Returns:
            str: Research result
        """
        input_data = {
            "topic": topic,
            "depth": depth
        }
        
        task = ResearchTask.create_topic_research_task(
            agent=agent_instance or agent_id,
            input_data=input_data
        )
        
        return BaseTask.execute_with_agent(
            task=task,
            agent_id=agent_id,
            agent_instance=agent_instance
        )