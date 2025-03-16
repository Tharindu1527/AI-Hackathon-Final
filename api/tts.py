# api/tts.py
import os
import requests
import tempfile
from utils.config import get_openai_api_key

def text_to_speech(text, output_format="mp3", voice="alloy", model="tts-1"):
    """
    Convert text to speech using OpenAI's text-to-speech API
    
    Args:
        text: Text to convert to speech
        output_format: Output format (mp3, opus, aac, flac)
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        
    Returns:
        str: Path to the audio file
    """
    # Get OpenAI API key
    api_key = get_openai_api_key()
    
    # Make API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Limit text length to avoid API errors (max 4096 chars recommended)
    if len(text) > 4000:
        text = text[:4000] + "... (summary truncated for audio conversion)"
    
    payload = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": output_format
    }
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers=headers,
            json=payload
        )
        
        # Check for errors
        if response.status_code != 200:
            print(f"TTS API error: {response.status_code}, {response.text}")
            return None
        
        # Save the audio to a temporary file
        temp_dir = os.path.join(tempfile.gettempdir(), "podcast_analyzer")
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_file = os.path.join(temp_dir, f"summary_audio.{output_format}")
        with open(temp_file, "wb") as f:
            f.write(response.content)
        
        return temp_file
    except Exception as e:
        print(f"Error in text_to_speech: {str(e)}")
        return None

def chunk_text_for_tts(text, max_chunk_size=4000):
    """
    Split text into appropriate chunks for TTS processing
    
    Args:
        text: Text to split into chunks
        max_chunk_size: Maximum characters per chunk
        
    Returns:
        list: List of text chunks
    """
    # If text is already small enough, return as single chunk
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    
    # Try to split on paragraph breaks first
    paragraphs = text.split('\n\n')
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph exceeds max size, start a new chunk
        if len(current_chunk) + len(paragraph) > max_chunk_size:
            # Only add the current chunk if it's not empty
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            # Add paragraph to current chunk
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # If any chunks are still too large, split them on sentences
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_chunk_size:
            final_chunks.append(chunk)
        else:
            # Split on sentences (try to detect sentence ends)
            sentence_ends = ['. ', '! ', '? ']
            current_sentence = ""
            current_sub_chunk = ""
            
            for char in chunk:
                current_sentence += char
                current_sub_chunk += char
                
                # Check if we've reached a sentence end
                is_sentence_end = False
                for end in sentence_ends:
                    if current_sentence.endswith(end):
                        is_sentence_end = True
                        break
                
                if is_sentence_end:
                    # If adding another sentence would exceed max size, start a new chunk
                    if len(current_sub_chunk) >= max_chunk_size:
                        final_chunks.append(current_sub_chunk.strip())
                        current_sub_chunk = ""
                    
                    current_sentence = ""
            
            # Add the last sub-chunk if it's not empty
            if current_sub_chunk:
                final_chunks.append(current_sub_chunk.strip())
    
    return final_chunks