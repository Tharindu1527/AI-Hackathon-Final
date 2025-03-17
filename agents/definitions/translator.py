# agents/definitions/translator.py
from agents.base import BaseAgent
from agents.registry import register_agent

@register_agent("translator")
class TranslatorAgent(BaseAgent):
    """Agent specialized in translating Meeting content to different languages"""
    
    def __init__(self, model="gpt-4o"):
        """Initialize the Translator Agent"""
        super().__init__(
            role="Content Translator",
            goal="Accurately translate Meeting content while preserving meaning, tone, and context",
            backstory="I am a multilingual expert with deep knowledge of language nuances and cultural contexts. "
                    "With fluency in multiple languages and expertise in linguistics, "
                    "I can translate content while preserving the original meaning, style, and cultural references. "
                    "I understand the importance of context and idiomatic expressions in achieving natural translations.",
            model=model
        )
    
    def translate_text(self, text, target_language, source_language=None):
        """
        Translate text to the target language
        
        Args:
            text: Text to translate
            target_language: Target language code or name
            source_language: Optional source language (if known)
            
        Returns:
            str: Translated text
        """
        from agents.tasks.translation import TranslationTask
        
        # Create input data
        input_data = {
            "text": text,
            "target_language": target_language
        }
        
        if source_language:
            input_data["source_language"] = source_language
        
        # Create and execute a translation task
        task = TranslationTask.create_translation_task(self, input_data)
        return self.execute_task(task)
    
    def translate_summary(self, summary_content, target_language):
        """
        Translate a Meeting summary to the target language
        
        Args:
            summary_content: Meeting summary content
            target_language: Target language code or name
            
        Returns:
            str: Translated summary
        """
        from agents.tasks.translation import TranslationTask
        
        # Create and execute a summary translation task
        task = TranslationTask.create_summary_translation_task(
            agent=self,
            summary_content=summary_content,
            target_language=target_language
        )
        
        return self.execute_task(task)
    
    def localize_content(self, content, target_region):
        """
        Localize content for a specific region/culture
        
        Args:
            content: Content to localize
            target_region: Target region or culture
            
        Returns:
            str: Localized content
        """
        from agents.tasks.translation import TranslationTask
        
        # Create input data
        input_data = {
            "content": content,
            "target_region": target_region
        }
        
        # Create and execute a localization task
        task = TranslationTask.create_localization_task(self, input_data)
        return self.execute_task(task)
    
    def generate_multilingual_summary(self, summary_content, languages):
        """
        Generate a multilingual summary in multiple languages
        
        Args:
            summary_content: Original summary content
            languages: List of target languages
            
        Returns:
            dict: Dictionary with language keys and translated summaries
        """
        results = {}
        
        # Add the original content (assuming English)
        results["english"] = summary_content
        
        # Translate to each requested language
        for language in languages:
            if language.lower() != "english":
                translated = self.translate_summary(summary_content, language)
                results[language.lower()] = translated
        
        return results