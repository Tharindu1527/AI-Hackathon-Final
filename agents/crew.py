# agents/crew.py
import json
from crewai import Crew
from agents.transcriber import TranscriberAgent
from agents.analyzer import AnalyzerAgent
from agents.summarizer import SummarizerAgent
from agents.sentiment import SentimentAgent
from agents.action_item import ActionItemAgent

class PodcastCrew:
    """Orchestrates a crew of agents to analyze podcasts"""
    
    def __init__(self, model="gpt-4o"):
        """
        Initialize the podcast crew with all required agents
        
        Args:
            model: OpenAI model to use for all agents
        """
        self.model = model
        self.setup_agents()
        
    def setup_agents(self):
        """Set up all the agents needed for podcast analysis"""
        self.transcriber_agent = TranscriberAgent(self.model)
        self.analyzer_agent = AnalyzerAgent(self.model)
        self.summarizer_agent = SummarizerAgent(self.model)
        self.sentiment_agent = SentimentAgent(self.model)
        self.action_agent = ActionItemAgent(self.model)
        
    def create_tasks(self, transcript_path):
        """
        Create all tasks for the podcast analysis
        
        Args:
            transcript_path: Path to the transcript file
            
        Returns:
            list: List of CrewAI tasks
        """
        # Task 1: Transcribe Podcast
        transcribe_task = self.transcriber_agent.create_task(transcript_path)
        
        # Task 2: Analyze Content
        analyze_task = self.analyzer_agent.create_task(transcribe_task)
        
        # Task 3: Create Summary
        summarize_task = self.summarizer_agent.create_task(analyze_task)
        
        # Task 4: Analyze Sentiment
        sentiment_task = self.sentiment_agent.create_task(transcribe_task, analyze_task)
        
        # Task 5: Extract Action Items
        action_task = self.action_agent.create_task(summarize_task, sentiment_task)
        
        return [transcribe_task, analyze_task, summarize_task, sentiment_task, action_task]
    
    def run_analysis(self, transcript_path):
        """
        Run the full podcast analysis with all agents
        
        Args:
            transcript_path: Path to the transcript file
            
        Returns:
            str: JSON string with analysis results
        """
        # Create all tasks
        tasks = self.create_tasks(transcript_path)
        
        # Create agents list for the crew
        agents = [
            self.transcriber_agent.create_agent(),
            self.analyzer_agent.create_agent(),
            self.summarizer_agent.create_agent(),
            self.sentiment_agent.create_agent(),
            self.action_agent.create_agent()
        ]
        
        # Create and run the crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True
        )
        
        # Run the analysis
        result = crew.kickoff()
        
        # Parse and structure the results
        structured_result = self._structure_results(result)
        
        # Return as JSON string
        return json.dumps(structured_result)
    
    def _structure_results(self, raw_result):
        """
        Structure the raw results from the crew into a clean format
        
        Args:
            raw_result: Raw result string from CrewAI
            
        Returns:
            dict: Structured results
        """
        # This is a simplified example - in a real implementation,
        # you'd want to parse the results more robustly
        
        # Create a structure for the results
        structured_result = {
            "summary": "",
            "key_topics": [],
            "sentiment_analysis": "",
            "action_items": []
        }
        
        # Extract the summary
        if "Executive Summary:" in raw_result:
            parts = raw_result.split("Executive Summary:")
            if len(parts) > 1:
                summary_text = parts[1].split("Key Topics:")[0].strip()
                structured_result["summary"] = summary_text
        
        # Extract key topics
        if "Key Topics:" in raw_result:
            parts = raw_result.split("Key Topics:")
            if len(parts) > 1:
                topics_text = parts[1].split("Sentiment Analysis:")[0].strip()
                topics = topics_text.split("\n")
                structured_result["key_topics"] = [t.strip("- ").strip() for t in topics if t.strip()]
        
        # Extract sentiment analysis
        if "Sentiment Analysis:" in raw_result:
            parts = raw_result.split("Sentiment Analysis:")
            if len(parts) > 1:
                sentiment_text = parts[1].split("Action Items:")[0].strip()
                structured_result["sentiment_analysis"] = sentiment_text
        
        # Extract action items
        if "Action Items:" in raw_result:
            parts = raw_result.split("Action Items:")
            if len(parts) > 1:
                action_text = parts[1].strip()
                actions = action_text.split("\n")
                structured_result["action_items"] = [a.strip("- ").strip() for a in actions if a.strip()]
        
        return structured_result