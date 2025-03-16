# crews/multilingual_crew.py
import json
from crews.base_crew import BaseCrew
from agents.registry import get_agent
from agents.tasks.transcription import TranscriptionTask
from agents.tasks.analysis import AnalysisTask
from agents.tasks.summary import SummaryTask
from agents.tasks.sentiment import SentimentTask
from agents.tasks.action_items import ActionItemsTask
from agents.tasks.translation import TranslationTask

class AdvancedMultilingualCrew(BaseCrew):
    """Advanced multilingual crew for comprehensive translation and localization"""
    
    def __init__(self, model="gpt-4o", source_language="english", target_languages=None):
        """
        Initialize the advanced multilingual crew
        
        Args:
            model: LLM model to use
            source_language: Source language of the podcast
            target_languages: List of languages to translate to
        """
        super().__init__(model=model)
        
        # Add required agents
        self.add_agent("transcriber")
        self.add_agent("analyzer")
        self.add_agent("summarizer")
        self.add_agent("sentiment")
        self.add_agent("action_item")
        self.add_agent("translator")
        
        # Set languages
        self.source_language = source_language.lower()
        self.target_languages = target_languages or ["english", "spanish", "french", "german"]
        
        # Ensure source language is not in target languages to avoid redundant translation
        if self.source_language in self.target_languages:
            self.target_languages.remove(self.source_language)
    
    def run_analysis(self, transcript_content):
        """
        Run multilingual analysis with comprehensive translation
        
        Args:
            transcript_content: Raw transcript content
            
        Returns:
            str: JSON string with multilingual analysis results
        """
        # Reset tasks
        self.tasks = []
        
        # Get agent instances
        transcriber = get_agent("transcriber")
        analyzer = get_agent("analyzer")
        summarizer = get_agent("summarizer")
        sentiment = get_agent("sentiment")
        action_item = get_agent("action_item")
        translator = get_agent("translator")
        
        # Process transcript directly first
        print("Processing transcript with transcriber agent...")
        transcript_result = transcriber.process_transcript(transcript_content)
        
        # Create core analysis tasks
        analyze_task = AnalysisTask.create_content_analysis_task(analyzer, transcript_result)
        self.add_task(analyze_task)
        
        sentiment_task = SentimentTask.create_sentiment_task(sentiment, transcript_result, analyze_task)
        self.add_task(sentiment_task)
        
        # Create a summary task
        summary_task = SummaryTask.create_summary_task(summarizer, analyze_task)
        self.add_task(summary_task)
        
        # Create action items task
        action_task = ActionItemsTask.create_action_items_task(action_item, summary_task, sentiment_task)
        self.add_task(action_task)
        
        # Create multilingual summary task
        multilingual_task = TranslationTask.create_multilingual_summary_task(
            translator,
            summary_task,
            self.target_languages
        )
        self.add_task(multilingual_task)
        
        # Run the crew
        result_json = self.run()
        
        try:
            # Structure the multilingual results
            result = json.loads(result_json)
            
            # Add source language
            result["source_language"] = self.source_language
            
            # Add target languages
            result["target_languages"] = self.target_languages
            
            # Ensure translations section exists
            if "translations" not in result:
                result["translations"] = {}
            
            # Add original language content as default
            result["translations"][self.source_language] = {
                "summary": result.get("summary", "Summary not available"),
                "key_topics": result.get("key_topics", []),
                "action_items": result.get("action_items", [])
            }
            
            # Process multilingual content if available
            for language in self.target_languages:
                lang_key = language.lower()
                
                # Look for language-specific content in the result
                if f"{lang_key}_summary" in result:
                    if lang_key not in result["translations"]:
                        result["translations"][lang_key] = {}
                    
                    result["translations"][lang_key]["summary"] = result[f"{lang_key}_summary"]
                    
                    # Clean up the main result by removing language-specific keys
                    del result[f"{lang_key}_summary"]
                
                if f"{lang_key}_action_items" in result:
                    if lang_key not in result["translations"]:
                        result["translations"][lang_key] = {}
                        
                    # Handle action items as either text or list
                    action_items = result[f"{lang_key}_action_items"]
                    if isinstance(action_items, str):
                        # Try to parse text into list
                        items = []
                        for line in action_items.split('\n'):
                            line = line.strip()
                            if line and (line.startswith('-') or line.startswith('*')):
                                items.append(line[1:].strip())
                            elif line:
                                items.append(line)
                        
                        if items:
                            result["translations"][lang_key]["action_items"] = items
                        else:
                            result["translations"][lang_key]["action_items"] = [action_items]
                    else:
                        result["translations"][lang_key]["action_items"] = action_items
                    
                    # Clean up the main result
                    del result[f"{lang_key}_action_items"]
            
            return json.dumps(result)
        except Exception as e:
            print(f"Error processing multilingual results: {e}")
            return result_json

class LocalizationCrew(AdvancedMultilingualCrew):
    """Crew specialized in content localization for different cultures and regions"""
    
    def __init__(self, model="gpt-4o", source_culture="US", target_cultures=None):
        """
        Initialize the localization crew
        
        Args:
            model: LLM model to use
            source_culture: Source culture/region of the podcast
            target_cultures: List of cultures/regions to localize for
        """
        # Map cultures to languages
        culture_to_language = {
            "US": "english",
            "UK": "english",
            "CA": "english",
            "AU": "english",
            "MX": "spanish",
            "ES": "spanish",
            "FR": "french",
            "DE": "german",
            "JP": "japanese",
            "CN": "chinese",
            "BR": "portuguese",
            "IN": "english"  # Default to English for India, though multiple languages could be used
        }
        
        # Set default target cultures if none provided
        target_cultures = target_cultures or ["UK", "CA", "MX", "FR"]
        
        # Map cultures to languages
        source_language = culture_to_language.get(source_culture, "english")
        target_languages = [culture_to_language.get(culture, "english") for culture in target_cultures]
        
        # Initialize the multilingual crew
        super().__init__(model=model, source_language=source_language, target_languages=target_languages)
        
        # Store culture information
        self.source_culture = source_culture
        self.target_cultures = target_cultures
        
        # Create culture to language mapping
        self.culture_language_map = {}
        for culture in target_cultures:
            self.culture_language_map[culture] = culture_to_language.get(culture, "english")
    
    def run_analysis(self, transcript_content):
        """
        Run localized analysis for different cultures/regions
        
        Args:
            transcript_content: Raw transcript content
            
        Returns:
            str: JSON string with localized analysis results
        """
        # First, run the multilingual analysis
        result_json = super().run_analysis(transcript_content)
        result = json.loads(result_json)
        
        # Add localization information
        result["source_culture"] = self.source_culture
        result["target_cultures"] = self.target_cultures
        
        # Add culture-specific localizations
        if "localizations" not in result:
            result["localizations"] = {}
        
        # Reset tasks for localization
        self.tasks = []
        
        # Get translator agent
        translator = get_agent("translator")
        
        # Create localization tasks for each target culture
        for culture in self.target_cultures:
            language = self.culture_language_map.get(culture)
            
            # Create a localization task
            if "summary" in result:
                localization_task = TranslationTask.create_localization_task(
                    translator,
                    {
                        "content": result["summary"],
                        "target_region": culture
                    }
                )
                self.add_task(localization_task)
        
        # If we have tasks, run localization
        if self.tasks:
            # Run the localization tasks
            localization_result = self.run()
            
            try:
                # Parse localization results
                localization_data = json.loads(localization_result)
                
                # Process localization results
                for culture in self.target_cultures:
                    key = f"{culture.lower()}_localized"
                    if key in localization_data:
                        result["localizations"][culture] = {
                            "content": localization_data[key],
                            "language": self.culture_language_map.get(culture, "english")
                        }
            except Exception as e:
                print(f"Error processing localization results: {e}")
                result["localization_error"] = str(e)
        
        return json.dumps(result)