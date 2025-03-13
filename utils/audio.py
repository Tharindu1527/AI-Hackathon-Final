# utils/audio.py
import os
import tempfile

def save_uploaded_file(uploaded_file):
    """
    Save an uploaded file to a temporary location
    
    Args:
        uploaded_file: The Streamlit uploaded file object
        
    Returns:
        str: Path to the saved file
    """
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        # Write the file content
        tmp_file.write(uploaded_file.getvalue())
        # Return the file path
        return tmp_file.name
        
def cleanup_files(file_paths):
    """
    Clean up temporary files
    
    Args:
        file_paths: List of file paths to remove
    """
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.unlink(path)
        except Exception as e:
            print(f"Error removing temporary file {path}: {str(e)}")