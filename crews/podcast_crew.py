# crews/podcast_crew.py
import json
from crews.base_crew import BaseCrew
from agents.registry import get_agent
from agents.tasks.transcription import TranscriptionTask
from agents.tasks.analysis import AnalysisTask
from agents.tasks.summary import SummaryTask
from agents.tasks.sentiment import SentimentTask
from agents.tasks.action_items import ActionItemsTask
from agents.tasks.fact_checking import FactCheckingTask
from agents.tasks.research import ResearchTask
from agents.tasks.translation import TranslationTask

class PodcastCrew(BaseCrew):
    """Standard crew for Meeting analysis"""
    
    def __init__(self, model="gpt-4o"):
        """
        Initialize the Meeting crew
        
        Args:
            model: LLM model to use
        """
        super().__init__(model=model)
        
        # Add the standard agents
        self.add_agent("transcriber")
        self.add_agent("analyzer")
        self.add_agent("summarizer")
        self.add_agent("sentiment")
        self.add_agent("action_item")
    
    def run_analysis(self, transcript_content):
        """
        Run Meeting analysis with all agents
        
        Args:
            transcript_content: Raw transcript content
            
        Returns:
            str: JSON string with analysis results
        """
        # Reset tasks
        self.tasks = []
        
        # Get agent instances
        transcriber = get_agent("transcriber")
        analyzer = get_agent("analyzer")
        summarizer = get_agent("summarizer")
        sentiment = get_agent("sentiment")
        action_item = get_agent("action_item")
        
        # Process transcript directly first
        print("Processing transcript with transcriber agent...")
        transcript_result = transcriber.process_transcript(transcript_content)
        
        # Create tasks for the crew
        analyze_task = AnalysisTask.create_content_analysis_task(analyzer, transcript_result)
        self.add_task(analyze_task)
        
        summarize_task = SummaryTask.create_summary_task(summarizer, analyze_task)
        self.add_task(summarize_task)
        
        sentiment_task = SentimentTask.create_sentiment_task(sentiment, transcript_result, analyze_task)
        self.add_task(sentiment_task)
        
        action_task = ActionItemsTask.create_action_items_task(action_item, summarize_task, sentiment_task)
        self.add_task(action_task)
        
        # Run the crew
        return self.run()

class EnhancedPodcastCrew(PodcastCrew):
    """Enhanced Meeting crew with fact checking and research"""
    
    def __init__(self, model="gpt-4o"):
        """
        Initialize the enhanced Meeting crew
        
        Args:
            model: LLM model to use
        """
        super().__init__(model=model)
        
        # Add additional agents
        self.add_agent("fact_checker")
        self.add_agent("researcher")
    
    def run_analysis(self, transcript_content):
        """
        Run enhanced Meeting analysis with all agents including fact checking and research
        
        Args:
            transcript_content: Raw transcript content
            
        Returns:
            str: JSON string with enhanced analysis results
        """
        # Reset tasks
        self.tasks = []
        
        # Get agent instances
        transcriber = get_agent("transcriber")
        analyzer = get_agent("analyzer")
        summarizer = get_agent("summarizer")
        sentiment = get_agent("sentiment")
        action_item = get_agent("action_item")
        fact_checker = get_agent("fact_checker")
        researcher = get_agent("researcher")
        
        # Process transcript directly first
        print("Processing transcript with transcriber agent...")
        transcript_result = transcriber.process_transcript(transcript_content)
        
        # Create core analysis tasks
        analyze_task = AnalysisTask.create_content_analysis_task(analyzer, transcript_result)
        self.add_task(analyze_task)
        
        # Add fact checking task
        fact_check_task = FactCheckingTask.create_claim_extraction_task(fact_checker, transcript_result)
        self.add_task(fact_check_task)
        
        # Create summary task that uses both analysis and fact checking
        summarize_task = SummaryTask.create_enhanced_summary_task(
            summarizer, 
            {
                "analysis": analyze_task,
                "fact_check": fact_check_task
            }
        )
        self.add_task(summarize_task)
        
        # Add research augmentation task
        research_task = ResearchTask.create_analysis_augmentation_task(researcher, analyze_task)
        self.add_task(research_task)
        
        # Sentiment analysis task
        sentiment_task = SentimentTask.create_sentiment_task(sentiment, transcript_result, analyze_task)
        self.add_task(sentiment_task)
        
        # Action items task that incorporates research
        action_task = ActionItemsTask.create_enhanced_action_items_task(
            action_item,
            {
                "summary": summarize_task,
                "sentiment": sentiment_task,
                "research": research_task
            }
        )
        self.add_task(action_task)
        
        # Run the crew
        return self.run()

class MultilingualPodcastCrew(PodcastCrew):
    """Multilingual Meeting crew with translation capabilities"""
    
    def __init__(self, model="gpt-4o", target_languages=None):
        """
        Initialize the multilingual Meeting crew
        
        Args:
            model: LLM model to use
            target_languages: List of languages to translate to
        """
        super().__init__(model=model)
        
        # Add translator agent
        self.add_agent("translator")
        
        # Set target languages (default to English and Spanish if not specified)
        self.target_languages = target_languages or ["English", "Spanish"]
    
    def run_analysis(self, transcript_content):
        """
        Run multilingual Meeting analysis
        
        Args:
            transcript_content: Raw transcript content
            
        Returns:
            str: JSON string with multilingual analysis results
        """
        # First, run standard analysis
        result_json = super().run_analysis(transcript_content)
        result = json.loads(result_json)
        
        # Add translations of the summary and action items
        translator = get_agent("translator")
        
        translated_summaries = {}
        translated_action_items = {}
        
        # Get the summary content
        summary = result.get("summary", "")
        
        # Get the action items
        action_items = result.get("action_items", [])
        action_items_text = "\n".join([f"- {item}" for item in action_items])
        
        # Reset tasks for translation
        self.tasks = []
        
        # Translate to each target language
        for language in self.target_languages:
            if language.lower() != "english":
                try:
                    # Create translation tasks
                    # Translate summary
                    summary_task = TranslationTask.create_summary_translation_task(
                        translator, summary, language
                    )
                    self.add_task(summary_task)
                    
                    # Translate action items
                    action_items_task = TranslationTask.create_translation_task(
                        translator, 
                        {
                            "text": action_items_text,
                            "target_language": language
                        }
                    )
                    self.add_task(action_items_task)
                    
                except Exception as e:
                    print(f"Error creating translation tasks for {language}: {e}")
        
        # If we have tasks, run translation
        if self.tasks:
            # Run the translation tasks
            translation_result = self.run()
            
            # Try to parse translation results
            try:
                translation_data = json.loads(translation_result)
                
                # Add translations to the result
                result["translations"] = {}
                
                for language in self.target_languages:
                    if language.lower() != "english":
                        language_key = language.lower()
                        if f"{language_key}_summary" in translation_data:
                            result["translations"][language_key] = {
                                "summary": translation_data[f"{language_key}_summary"],
                                "action_items": translation_data[f"{language_key}_action_items"]
                            }
            except Exception as e:
                print(f"Error processing translation results: {e}")
                result["translations"] = {
                    "error": f"Translation processing failed: {str(e)}"
                }
        
        return json.dumps(result)

class ResearchPodcastCrew(BaseCrew):
    """Research-focused Meeting crew that prioritizes factual information and references"""
    
    def __init__(self, model="gpt-4o"):
        """
        Initialize the research Meeting crew
        
        Args:
            model: LLM model to use
        """
        super().__init__(model=model)
        
        # Add required agents
        self.add_agent("transcriber")
        self.add_agent("analyzer")
        self.add_agent("researcher")
        self.add_agent("fact_checker")
        self.add_agent("summarizer")
        self.add_agent("action_item")
    
    def run_analysis(self, transcript_content):
        """
        Run research-focused Meeting analysis
        
        Args:
            transcript_content: Raw transcript content
            
        Returns:
            str: JSON string with research-focused analysis results
        """
        # Reset tasks
        self.tasks = []
        
        # Get agent instances
        transcriber = get_agent("transcriber")
        analyzer = get_agent("analyzer")
        researcher = get_agent("researcher")
        fact_checker = get_agent("fact_checker")
        summarizer = get_agent("summarizer")
        action_item = get_agent("action_item")
        
        # Process transcript directly first
        print("Processing transcript with transcriber agent...")
        transcript_result = transcriber.process_transcript(transcript_content)
        
        # Initial analysis task
        analyze_task = AnalysisTask.create_content_analysis_task(analyzer, transcript_result)
        self.add_task(analyze_task)
        
        # Topic extraction for targeted research
        topic_extraction_task = ResearchTask.create_topic_extraction_task(
            researcher, 
            analyze_task, 
            max_topics=5
        )
        self.add_task(topic_extraction_task)
        
        # Research task for each extracted topic
        research_task = ResearchTask.create_analysis_augmentation_task(researcher, analyze_task)
        self.add_task(research_task)
        
        # Fact checking task
        fact_check_task = FactCheckingTask.create_comprehensive_fact_check_task(
            fact_checker, 
            analyze_task
        )
        self.add_task(fact_check_task)
        
        # Create a research-enhanced summary
        summary_task = SummaryTask.create_enhanced_summary_task(
            summarizer,
            {
                "analysis": analyze_task,
                "research": research_task,
                "fact_check": fact_check_task
            }
        )
        self.add_task(summary_task)
        
        # Generate source recommendations
        source_task = ResearchTask.create_source_finding_task(
            researcher,
            topic_extraction_task,
            num_sources=5
        )
        self.add_task(source_task)
        
        # Action items based on research and fact checking
        action_task = ActionItemsTask.create_enhanced_action_items_task(
            action_item,
            {
                "summary": summary_task,
                "research": research_task,
                "fact_check": fact_check_task
            }
        )
        self.add_task(action_task)
        
        # Run the crew
        result_json = self.run()
        
        # Add structured references to the result
        try:
            result = json.loads(result_json)
            
            # Add a references section if not present
            if "references" not in result:
                result["references"] = []
                
                # Try to parse references from the source task
                if "sources" in result:
                    result["references"] = result["sources"]
                
            return json.dumps(result)
        except Exception as e:
            print(f"Error enhancing research crew result: {e}")
            return result_json