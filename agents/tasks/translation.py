# agents/tasks/translation.py
from agents.tasks.task_base import BaseTask

class TranslationTask(BaseTask):
    """Tasks related to translation and localization of podcast content"""
    
    @staticmethod
    def create_translation_task(agent, input_data):
        """
        Create a general text translation task
        
        Args:
            agent: Translator agent (ID or instance)
            input_data: Dict with text and target_language (and optional source_language)
            
        Returns:
            Task: Translation task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to translate the provided text to the target language:
            
            1. Maintain the original meaning and tone
            2. Preserve formatting, paragraphs, and structure
            3. Adapt idioms and cultural references appropriately
            4. Keep any technical terminology accurate
            5. Ensure the translation sounds natural in the target language
            
            Provide only the translated text without explanations or notes.
            """,
            expected_output="The translated text in the target language.",
            input_data=input_data
        )
    
    @staticmethod
    def create_summary_translation_task(agent, summary_content, target_language):
        """
        Create a podcast summary translation task
        
        Args:
            agent: Translator agent (ID or instance)
            summary_content: Podcast summary content
            target_language: Target language code or name
            
        Returns:
            Task: Summary translation task
        """
        input_data = {
            "summary": summary_content,
            "target_language": target_language
        }
        
        return BaseTask.create_task(
            agent=agent,
            description=f"""
            Your task is to translate the podcast summary to {target_language}:
            
            1. Maintain the original meaning and tone
            2. Preserve the structure of the summary
            3. Adapt any industry-specific terminology appropriately
            4. Ensure the translation is clear and accessible
            5. Keep important names, brands, and key terms identifiable
            
            The translation should be suitable for international business audience.
            """,
            expected_output=f"The podcast summary translated to {target_language}.",
            input_data=input_data
        )
    
    @staticmethod
    def create_localization_task(agent, input_data):
        """
        Create a content localization task
        
        Args:
            agent: Translator agent (ID or instance)
            input_data: Dict with content and target_region
            
        Returns:
            Task: Localization task
        """
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to localize the content for the specified target region:
            
            1. Adapt cultural references to be relevant in the target region
            2. Use region-appropriate terminology and expressions
            3. Adjust examples and analogies to fit the local context
            4. Consider local sensitivities and taboos
            5. Maintain the overall meaning and purpose of the content
            
            The localized content should feel natural to someone from the target region.
            """,
            expected_output="The localized content adapted for the target region.",
            input_data=input_data
        )
    
    @staticmethod
    def create_multilingual_summary_task(agent, summary_content, languages):
        """
        Create a multilingual summary task
        
        Args:
            agent: Translator agent (ID or instance)
            summary_content: Original summary content
            languages: List of target languages
            
        Returns:
            Task: Multilingual summary task
        """
        input_data = {
            "summary": summary_content,
            "languages": ", ".join(languages)
        }
        
        return BaseTask.create_task(
            agent=agent,
            description="""
            Your task is to create a multilingual version of the podcast summary:
            
            1. For each requested language, provide a complete translation
            2. Maintain the structure and key points in all versions
            3. Adapt each translation to sound natural in its language
            4. Format clearly with language headers
            5. Ensure consistent meaning across all versions
            
            Provide a complete set of translations as specified.
            """,
            expected_output="The podcast summary in multiple languages, with clear language headers.",
            input_data=input_data
        )
    
    @staticmethod
    def execute_translation(text, target_language, source_language=None, agent_id="translator", agent_instance=None):
        """
        Execute translation directly
        
        Args:
            text: Text to translate
            target_language: Target language
            source_language: Optional source language
            agent_id: ID of translator agent (if not providing instance)
            agent_instance: Translator agent instance (if not providing ID)
            
        Returns:
            str: Translated text
        """
        input_data = {
            "text": text,
            "target_language": target_language
        }
        
        if source_language:
            input_data["source_language"] = source_language
        
        task = TranslationTask.create_translation_task(
            agent=agent_instance or agent_id,
            input_data=input_data
        )
        
        return BaseTask.execute_with_agent(
            task=task,
            agent_id=agent_id,
            agent_instance=agent_instance
        )