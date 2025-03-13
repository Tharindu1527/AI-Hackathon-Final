# api/assemblyai.py
import assemblyai as aai
from utils.config import get_assemblyai_api_key

def initialize_assemblyai():
    """Initialize AssemblyAI client with API key"""
    api_key = get_assemblyai_api_key()
    aai.settings.api_key = api_key
    return api_key

def transcribe_podcast(audio_file_path):
    """
    Transcribe a podcast audio file using AssemblyAI
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        str: Transcription text
    """
    # Initialize the API
    initialize_assemblyai()
    
    # Create a transcriber
    transcriber = aai.Transcriber()
    
    # Transcribe the audio file
    print(f"Transcribing audio file: {audio_file_path}")
    transcript = transcriber.transcribe(audio_file_path)
    
    # Check if transcription was successful
    if transcript.status == "completed":
        return transcript.text
    else:
        error_msg = f"Transcription failed with status: {transcript.status}"
        if hasattr(transcript, "error"):
            error_msg += f" - Error: {transcript.error}"
        raise Exception(error_msg)
    
def transcribe_with_speaker_diarization(audio_file_path):
    """
    Transcribe with speaker diarization (who said what)
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        dict: Transcription result with speaker labels
    """
    # Initialize the API
    initialize_assemblyai()
    
    # Create a transcriber
    transcriber = aai.Transcriber()
    
    # Configure transcription options
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        speakers_expected=2  # You can adjust this based on expected speakers
    )
    
    # Transcribe the audio file
    transcript = transcriber.transcribe(audio_file_path, config=config)
    
    # Return utterances with speaker information
    return transcript.utterances

def transcribe_with_topic_detection(audio_file_path):
    """
    Transcribe with automatic topic detection
    
    Args:
        audio_file_path: Path to the audio file
        
    Returns:
        dict: Transcription and detected topics
    """
    # Initialize the API
    initialize_assemblyai()
    
    # Create a transcriber
    transcriber = aai.Transcriber()
    
    # Configure transcription options with topic detection
    config = aai.TranscriptionConfig(
        auto_chapters=True  # This enables topic detection
    )
    
    # Transcribe the audio file
    transcript = transcriber.transcribe(audio_file_path, config=config)
    
    # Return the transcript and chapters (topics)
    return {
        "text": transcript.text,
        "chapters": transcript.chapters
    }