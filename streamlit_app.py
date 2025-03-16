# streamlit_app.py
import streamlit as st
import os
import tempfile
from datetime import datetime
import json
import base64

# Import custom modules
from utils.config import load_environment
from agents.crew import PodcastCrew
from api.assemblyai import transcribe_podcast
from api.composio import send_email_summary
from database.mongodb import get_mongodb_client, store_podcast_data, get_all_podcast_titles
from database.qdrant import store_vectors, search_similar_content
from app.chatbot import generate_answer
from api.tts import text_to_speech, chunk_text_for_tts

# Load environment variables
load_environment()

def get_audio_player_html(file_path):
    """
    Create an HTML audio player for the given audio file
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        str: HTML audio player code
    """
    # Read audio file
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        
        # Encode audio bytes to base64
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        
        # Get file extension
        file_ext = os.path.splitext(file_path)[1][1:].lower()
        mime_type = f"audio/{file_ext}"
        
        # Create HTML audio player
        audio_html = f'''
        <audio controls style="width: 100%;">
            <source src="data:{mime_type};base64,{audio_base64}" type="{mime_type}">
            Your browser does not support the audio element.
        </audio>
        '''
        
        return audio_html
    except Exception as e:
        print(f"Error creating audio player: {e}")
        return f'<div style="color: red;">Error creating audio player: {str(e)}</div>'

def main():
    st.title("Podcast Analyzer & Chatbot")

    # Add a database status indicator
    try:
        # Try to connect to MongoDB
        client = get_mongodb_client()
        client.admin.command('ping')
        st.success("✅ Database connection successful")
    except Exception as e:
        st.warning(f"⚠️ Database connection unavailable (using mock data): {str(e)}")
    
    tab1, tab2, tab3 = st.tabs(["Analyze Podcast", "Chat about Podcasts", "Listen to Summaries"])
    
    with tab1:
        st.header("Upload and Analyze Podcast")
        
        uploaded_file = st.file_uploader("Choose a podcast audio file", type=["mp3", "wav", "m4a"])
        
        podcast_title = st.text_input("Podcast Title")
        board_emails = st.text_area("Board Member Emails (one per line)")
        
        if st.button("Analyze Podcast") and uploaded_file is not None:
            if not podcast_title:
                st.error("Please enter a podcast title")
                return
                
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                audio_path = tmp_file.name
            
            try:
                with st.spinner("Analyzing podcast..."):
                    # Use AssemblyAI for transcription
                    st.info("Transcribing podcast...")
                    try:
                        transcript = transcribe_podcast(audio_path)
                        st.success("Transcription complete!")
                    except Exception as e:
                        st.error(f"Transcription error: {str(e)}")
                        # For testing, generate a mock transcript
                        transcript = f"This is a mock transcript for '{podcast_title}'. The real transcription failed."
                    
                    # Run the CrewAI analysis directly with the transcript content
                    st.info("Running multi-agent analysis...")
                    podcast_crew = PodcastCrew()
                    
                    # Pass the transcript content directly to run_analysis
                    result = podcast_crew.run_analysis(transcript)
                    
                    # Parse the results
                    analysis_result = json.loads(result)
                    
                    # Prepare data for storage
                    podcast_data = {
                        "title": podcast_title,
                        "date_analyzed": datetime.now().isoformat(),
                        "transcript": transcript,
                        "summary": analysis_result.get("summary", "Summary not available"),
                        "key_topics": analysis_result.get("key_topics", ["Topic information not available"]),
                        "sentiment": analysis_result.get("sentiment_analysis", "Sentiment analysis not available"),
                        "action_items": analysis_result.get("action_items", ["Action items not available"])
                    }
                    
                    # Store in MongoDB
                    st.info("Storing results in MongoDB...")
                    try:
                        summary_id = store_podcast_data(podcast_data)
                        st.success("Data stored successfully!")
                    except Exception as e:
                        st.error(f"Error storing data: {str(e)}")
                        summary_id = "mock_id_12345"
                    
                    # Store in Qdrant for vector search
                    st.info("Storing vectors in Qdrant...")
                    try:
                        store_vectors(podcast_data, summary_id)
                        st.success("Vectors stored successfully!")
                    except Exception as e:
                        st.error(f"Error storing vectors: {str(e)}")
                    
                    # Send email to board members
                    if board_emails:
                        recipient_list = [email.strip() for email in board_emails.split("\n") if email.strip()]
                        st.info(f"Sending summary email to {len(recipient_list)} recipients...")
                        try:
                            send_email_summary(podcast_data, recipient_list)
                            st.success("Email sent successfully!")
                        except Exception as e:
                            st.error(f"Error sending email: {str(e)}")
                    
                    # Display summary with better error handling
                    st.success("Podcast analysis complete!")

                    # Print raw result for debugging
                    print(f"Analysis result structure: {analysis_result}")

                    # Executive Summary
                    st.subheader("Executive Summary")
                    if analysis_result.get("summary") and len(analysis_result["summary"]) > 10:
                        st.write(analysis_result["summary"])
                        
                        # Add a button to generate TTS for the summary
                        if st.button("Listen to Summary"):
                            with st.spinner("Generating audio..."):
                                summary_text = analysis_result["summary"]
                                audio_file = text_to_speech(summary_text)
                                if audio_file:
                                    st.success("Audio generated successfully!")
                                    st.audio(audio_file)
                                else:
                                    st.error("Failed to generate audio summary")
                    else:
                        st.info("The executive summary could not be generated completely.")
                        # Provide fallback summary
                        st.write(analysis_result.get("summary", "This podcast covers various topics and insights. The complete analysis is still processing."))

                    # Key Topics
                    st.subheader("Key Topics")
                    if analysis_result.get("key_topics") and len(analysis_result["key_topics"]) > 0:
                        for topic in analysis_result["key_topics"]:
                            if topic and len(topic) > 3:  # Ensure topic is not empty or too short
                                st.write(f"- {topic}")
                    else:
                        st.info("Key topics could not be identified completely.")
                        # Provide fallback topics
                        st.write("- Topic information not available")
                        st.write("- Please try reanalyzing the podcast")

                    # Sentiment Analysis
                    st.subheader("Sentiment Analysis")
                    if analysis_result.get("sentiment_analysis") and len(analysis_result["sentiment_analysis"]) > 10:
                        st.write(analysis_result["sentiment_analysis"])
                    else:
                        st.info("Sentiment analysis could not be generated completely.")
                        # Provide fallback sentiment
                        st.write(analysis_result.get("sentiment_analysis", "The sentiment analysis for this podcast is pending."))

                    # Action Items
                    st.subheader("Action Items")
                    if analysis_result.get("action_items") and len(analysis_result["action_items"]) > 0:
                        for item in analysis_result["action_items"]:
                            if item and len(item) > 3:  # Ensure item is not empty or too short
                                st.write(f"- {item}")
                                
                        # Add a button to generate TTS for action items
                        if st.button("Listen to Action Items"):
                            with st.spinner("Generating audio..."):
                                action_items_text = "Action Items: " + ". ".join(analysis_result["action_items"])
                                audio_file = text_to_speech(action_items_text)
                                if audio_file:
                                    st.success("Audio generated successfully!")
                                    st.audio(audio_file)
                                else:
                                    st.error("Failed to generate audio for action items")
                    else:
                        st.info("Action items could not be identified completely.")
                        # Provide fallback action items
                        st.write("- Action items not available")
                        st.write("- Consider reanalyzing with adjusted agent parameters")
                    
                    # Clean up temporary files
                    os.unlink(audio_path)
            except Exception as main_error:
                st.error(f"An error occurred during analysis: {str(main_error)}")
                st.info("Please try again with a different podcast or check the logs for more details.")                
    
    with tab2:
        st.header("Chat about Analyzed Podcasts")
        
        # Display available podcasts
        podcast_titles = get_all_podcast_titles()
        if not podcast_titles:
            st.warning("No analyzed podcasts found. Please analyze some podcasts first.")
            return
        
        # Create a selection box for podcasts
        selected_podcast = st.selectbox(
            "Select a podcast to chat about:",
            options=podcast_titles,
            index=0,
            key="chat_podcast_select"
        )
            
        st.write(f"Selected podcast: **{selected_podcast}**")
        
        user_question = st.text_input("Ask a question about this podcast")
        
        if st.button("Ask") and user_question:
            with st.spinner("Searching for answer..."):
                try:
                    # Get podcast data from MongoDB by title
                    from database.mongodb import get_podcast_by_title
                    podcast_data = get_podcast_by_title(selected_podcast)
                    
                    if not podcast_data:
                        st.error(f"Could not find podcast data for '{selected_podcast}'")
                        return
                    
                    # Generate answer
                    from app.chatbot import generate_answer
                    answer = generate_answer(podcast_data, user_question)
                    
                    st.subheader("Answer")
                    st.write(answer)
                    
                    # Add TTS option for the answer
                    if st.button("Listen to Answer"):
                        with st.spinner("Generating audio..."):
                            audio_file = text_to_speech(answer)
                            if audio_file:
                                st.success("Audio generated successfully!")
                                st.audio(audio_file)
                            else:
                                st.error("Failed to generate audio for answer")
                    
                    st.subheader("Source")
                    st.write(f"Based on podcast: {podcast_data.get('title', 'Unknown Podcast')}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Using fallback search method...")
                    
                    try:
                        # Fallback to vector search
                        search_results = search_similar_content(user_question)
                        
                        if not search_results:
                            st.warning("No relevant podcast information found for your question.")
                            return
                        
                        # Get the most relevant podcast data
                        podcast_data = search_results[0].payload
                        
                        # Generate answer
                        answer = generate_answer(podcast_data, user_question)
                        
                        st.subheader("Answer")
                        st.write(answer)
                        
                        st.subheader("Source")
                        st.write(f"Based on podcast: {podcast_data.get('title', 'Unknown Podcast')}")
                    except Exception as e2:
                        st.error(f"Fallback search also failed: {str(e2)}")
                        st.warning("Please try again with a different question or podcast.")
                        
    with tab3:
        st.header("Listen to Podcast Summaries")
        
        # Display available podcasts
        podcast_titles = get_all_podcast_titles()
        if not podcast_titles:
            st.warning("No analyzed podcasts found. Please analyze some podcasts first.")
            return
        
        # Create a selection box for podcasts
        selected_podcast = st.selectbox(
            "Select a podcast summary to listen to:",
            options=podcast_titles,
            index=0,
            key="listen_podcast_select"
        )
        
        # Voice selection
        voice_options = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        selected_voice = st.selectbox(
            "Select a voice:",
            options=voice_options,
            index=0
        )
        
        if st.button("Generate Audio Summary"):
            with st.spinner("Generating audio summary..."):
                try:
                    # Get podcast data from MongoDB by title
                    from database.mongodb import get_podcast_by_title
                    podcast_data = get_podcast_by_title(selected_podcast)
                    
                    if not podcast_data:
                        st.error(f"Could not find podcast data for '{selected_podcast}'")
                        return
                    
                    # Prepare the summary content
                    summary_text = podcast_data.get("summary", "Summary not available.")
                    
                    # Include key topics in the audio summary
                    key_topics = podcast_data.get("key_topics", [])
                    if key_topics and len(key_topics) > 0:
                        topics_text = "Key topics include: " + ", ".join(key_topics[:5])  # Limit to first 5 topics
                        summary_text += "\n\n" + topics_text
                    
                    # Include a condensed version of action items
                    action_items = podcast_data.get("action_items", [])
                    if action_items and len(action_items) > 0:
                        actions_text = "Action items include: " + ". ".join(action_items[:3])  # Limit to first 3 items
                        summary_text += "\n\n" + actions_text
                    
                    # Generate the audio file
                    audio_file = text_to_speech(summary_text, voice=selected_voice)
                    
                    if audio_file:
                        st.success(f"Audio summary for '{selected_podcast}' generated successfully!")
                        
                        # Display audio player
                        st.audio(audio_file)
                        
                        # Display the text that was converted to speech
                        with st.expander("Show summary text"):
                            st.write(summary_text)
                            
                        # Add download link
                        with open(audio_file, "rb") as file:
                            audio_bytes = file.read()
                            file_name = f"{selected_podcast.replace(' ', '_')}_summary.mp3"
                            st.download_button(
                                label="Download Audio Summary",
                                data=audio_bytes,
                                file_name=file_name,
                                mime="audio/mp3"
                            )
                    else:
                        st.error("Failed to generate audio summary")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Please try again or select a different podcast.")

if __name__ == "__main__":
    main()