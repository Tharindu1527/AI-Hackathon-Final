# crews/research_crew.py
import json
from crews.base_crew import BaseCrew
from agents.registry import get_agent
from agents.tasks.transcription import TranscriptionTask
from agents.tasks.analysis import AnalysisTask
from agents.tasks.summary import SummaryTask
from agents.tasks.action_items import ActionItemsTask
from agents.tasks.fact_checking import FactCheckingTask
from agents.tasks.research import ResearchTask

class DeepResearchCrew(BaseCrew):
    """Specialized crew for deep research of Meeting topics"""
    
    def __init__(self, model="gpt-4o"):
        """
        Initialize the deep research crew
        
        Args:
            model: LLM model to use
        """
        super().__init__(model=model)
        
        # Add required agents
        self.add_agent("transcriber")
        self.add_agent("analyzer")
        self.add_agent("researcher")
        self.add_agent("summarizer")
        self.add_agent("action_item")
    
    def run_analysis(self, transcript_content, research_depth="deep"):
        """
        Run deep research analysis on Meeting content
        
        Args:
            transcript_content: Raw transcript content
            research_depth: Research depth (shallow, medium, deep)
            
        Returns:
            str: JSON string with research results
        """
        # Reset tasks
        self.tasks = []
        
        # Get agent instances
        transcriber = get_agent("transcriber")
        analyzer = get_agent("analyzer")
        researcher = get_agent("researcher")
        summarizer = get_agent("summarizer")
        action_item = get_agent("action_item")
        
        # Process transcript directly first
        print("Processing transcript with transcriber agent...")
        transcript_result = transcriber.process_transcript(transcript_content)
        
        # Extract topics for research
        topics_task = AnalysisTask.create_topic_extraction_task(analyzer, transcript_result)
        self.add_task(topics_task)
        
        # Create research tasks for the extracted topics
        research_tasks = []
        research_input = {
            "topic_extraction": topics_task,
            "depth": research_depth
        }
        
        # Add a deep research task
        deep_research_task = ResearchTask.create_topic_research_task(
            researcher,
            research_input
        )
        self.add_task(deep_research_task)
        research_tasks.append(deep_research_task)
        
        # Add a source finding task
        sources_task = ResearchTask.create_source_finding_task(
            researcher,
            topics_task,
            num_sources=5
        )
        self.add_task(sources_task)
        
        # Create an enhanced research summary
        research_summary_task = SummaryTask.create_enhanced_summary_task(
            summarizer,
            {
                "topics": topics_task,
                "research": deep_research_task,
                "sources": sources_task
            }
        )
        self.add_task(research_summary_task)
        
        # Create actionable research recommendations
        action_task = ActionItemsTask.create_enhanced_action_items_task(
            action_item,
            {
                "summary": research_summary_task,
                "research": deep_research_task
            }
        )
        self.add_task(action_task)
        
        # Run the crew
        result_json = self.run()
        
        try:
            # Add structured research elements to the result
            result = json.loads(result_json)
            
            # Ensure we have a research section
            if "research" not in result:
                result["research"] = {}
            
            # Add a sources section if not present
            if "sources" not in result:
                result["sources"] = []
            
            # Add a method section explaining the research approach
            if "methodology" not in result["research"]:
                result["research"]["methodology"] = (
                    f"Deep research analysis performed at {research_depth} depth. "
                    "Topics were extracted from the Meeting transcript and researched "
                    "using multiple reference sources. The analysis includes context, "
                    "related concepts, and knowledge gaps identified during research."
                )
            
            return json.dumps(result)
        except Exception as e:
            print(f"Error enhancing research result: {e}")
            return result_json

class FactCheckingCrew(BaseCrew):
    """Specialized crew for fact checking Meeting content"""
    
    def __init__(self, model="gpt-4o"):
        """
        Initialize the fact checking crew
        
        Args:
            model: LLM model to use
        """
        super().__init__(model=model)
        
        # Add required agents
        self.add_agent("transcriber")
        self.add_agent("analyzer")
        self.add_agent("fact_checker")
        self.add_agent("summarizer")
    
    def run_fact_check(self, transcript_content, max_claims=10):
        """
        Run fact checking on Meeting content
        
        Args:
            transcript_content: Raw transcript content
            max_claims: Maximum number of claims to check
            
        Returns:
            str: JSON string with fact checking results
        """
        # Reset tasks
        self.tasks = []
        
        # Get agent instances
        transcriber = get_agent("transcriber")
        analyzer = get_agent("analyzer")
        fact_checker = get_agent("fact_checker")
        summarizer = get_agent("summarizer")
        
        # Process transcript directly first
        print("Processing transcript with transcriber agent...")
        transcript_result = transcriber.process_transcript(transcript_content)
        
        # Extract claims from the transcript
        claims_task = FactCheckingTask.create_claim_extraction_task(fact_checker, transcript_result)
        self.add_task(claims_task)
        
        # Analyze the content to provide context
        context_task = AnalysisTask.create_content_analysis_task(analyzer, transcript_result)
        self.add_task(context_task)
        
        # Create a comprehensive fact check
        fact_check_task = FactCheckingTask.create_comprehensive_fact_check_task(
            fact_checker,
            {
                "claims": claims_task,
                "context": context_task,
                "max_claims": max_claims
            }
        )
        self.add_task(fact_check_task)
        
        # Create a summary of the fact checking results
        summary_task = SummaryTask.create_enhanced_summary_task(
            summarizer,
            {
                "claims": claims_task,
                "fact_check": fact_check_task,
                "context": context_task
            }
        )
        self.add_task(summary_task)
        
        # Run the crew
        result_json = self.run()
        
        try:
            # Structure the fact checking results
            result = json.loads(result_json)
            
            # Format the fact check section
            if "fact_check" in result and isinstance(result["fact_check"], str):
                # Try to parse the fact check text into structured data
                fact_check_text = result["fact_check"]
                
                # Look for claims and their verification status
                claims = []
                claim_pattern = r"Claim:([^S]+)Status:([^S]+)"
                import re
                matches = re.findall(claim_pattern, fact_check_text, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    claim = match[0].strip()
                    status = match[1].strip()
                    claims.append({
                        "claim": claim,
                        "status": status
                    })
                
                if claims:
                    result["fact_check"] = {
                        "claims": claims,
                        "source": "Wikipedia and knowledge base verification"
                    }
            
            return json.dumps(result)
        except Exception as e:
            print(f"Error structuring fact check result: {e}")
            return result_json