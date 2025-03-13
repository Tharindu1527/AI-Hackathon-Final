from crewai import Task
from tools import audio_tools, transcription_tools, analysis_tools, summary_tools, delivery_tools
from agents import audio_processing_agent, transcription_agent, analysis_agent, summary_generation_agent, delivery_agent
from textwrap import dedent

def create_tasks(audio_file_path, recipient_emails):
    """Generate task descriptions using only the audio file and recipient emails"""
    
    # Audio Processing Task
    audio_processing_task = Task(
        description=dedent(f"""
            Process the provided audio file to prepare it for transcription.
            
            This task involves:
            - Loading the audio file from {audio_file_path}
            - Converting the audio to a standard format suitable for transcription
            - Applying noise reduction and audio enhancement techniques
            - Identifying and separating different speakers where possible
            - Preparing the processed audio file for accurate transcription
            
            Your final answer must include the location of the processed audio file
            and a brief quality assessment of the audio (clarity, noise level, speaker distinction).
            
            Audio File: {audio_file_path}
        """),
        agent=audio_processing_agent,
        tools=[audio_tools],
        expected_output="Processed audio file location and quality assessment report."
    )
    
    # Transcription Task
    transcription_task = Task(
        description=dedent(f"""
            Convert the processed audio file into an accurate text transcription with
            clear speaker identification and timestamps.
            
            This task involves:
            - Utilizing speech recognition technology to convert speech to text
            - Identifying and labeling different speakers in the conversation
            - Adding precise timestamps throughout the transcription
            - Ensuring accurate punctuation and formatting of the text
            - Handling specialized terminology and acronyms appropriately
            
            Your final answer must be a complete, formatted transcript of the audio
            with clear speaker labels and timestamps.
        """),
        agent=transcription_agent,
        tools=[transcription_tools],
        expected_output="Complete text transcription with speaker labels and timestamps."
    )
    
    # Analysis Task
    analysis_task = Task(
        description=dedent(f"""
            Perform deep content analysis on the transcribed text to identify key topics,
            insights, and information structure.
            
            This task involves:
            - Identifying main topics and subtopics discussed
            - Extracting key points, decisions, and action items
            - Analyzing sentiment and tone of the discussion
            - Mapping the flow of conversation and argument structure
            - Identifying important quotes or statements
            
            Your final answer must include a structured analysis of the content with
            categorized topics, key insights, and important elements that should be
            included in the summary.
        """),
        agent=analysis_agent,
        tools=[analysis_tools],
        expected_output="Structured content analysis with topics, key points, and important elements."
    )
    
    # Summary Generation Task
    summary_generation_task = Task(
        description=dedent(f"""
            Create a comprehensive summary of the audio content based on the transcription
            and content analysis, formatted in multiple useful formats.
            
            This task involves:
            - Distilling the most important information from the analysis
            - Creating an executive summary (1-2 paragraphs)
            - Developing a detailed summary with key points and insights
            - Listing all action items and decisions made
            - Including relevant context and background information
            
            Your final answer must be a complete, well-structured summary package that effectively
            captures the essential content of the audio in multiple formats for different reading purposes.
        """),
        agent=summary_generation_agent,
        tools=[summary_tools],
        expected_output="Complete multi-format summary package (executive, detailed, and action items)."
    )
    
    # Delivery Task
    delivery_task = Task(
        description=dedent(f"""
            Package and deliver the generated summary to all recipients via email.
            
            This task involves:
            - Converting the summary to an email-friendly format
            - Preparing the email with an appropriate subject line and introduction
            - Sending the summary via email to: {recipient_emails}
            - Confirming successful delivery
            - Storing a copy of the delivered summary for future reference
            
            Your final answer must include confirmation of successful delivery to all recipients
            and a copy of the email that was sent.
            
            Recipient Emails: {recipient_emails}
        """),
        agent=delivery_agent,
        tools=[delivery_tools],
        expected_output="Confirmation of successful email delivery with copy of sent email."
    )
    
    return [audio_processing_task, transcription_task, analysis_task, summary_generation_task, delivery_task]