# streamlit_app.py
import streamlit as st
import os
import tempfile
from datetime import datetime
import json

# Import custom modules
from utils.config import load_environment
from agents.crew import PodcastCrew
from api.assemblyai import transcribe_podcast
from api.composio import send_email_summary
from database.mongodb import get_mongodb_client, store_podcast_data, get_all_podcast_titles
from database.qdrant import store_vectors, search_similar_content
from app.chatbot import generate_answer

# Load environment variables
load_environment()

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
    
    tab1, tab2 = st.tabs(["Analyze Podcast", "Chat about Podcasts"])
    
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
            
            with st.spinner("Analyzing podcast..."):
                # Use AssemblyAI for transcription
                st.info("Transcribing podcast...")
                transcript = transcribe_podcast(audio_path)
                
                # Write transcript to a file for the agents to use
                transcript_path = f"{audio_path}_transcript.txt"
                with open(transcript_path, "w") as f:
                    f.write(transcript)
                
                # Run the CrewAI analysis
                st.info("Running multi-agent analysis...")
                podcast_crew = PodcastCrew()
                result = podcast_crew.run_analysis(transcript_path)
                
                # Parse the results
                analysis_result = json.loads(result)
                
                # Prepare data for storage
                podcast_data = {
                    "title": podcast_title,
                    "date_analyzed": datetime.now().isoformat(),
                    "transcript": transcript,
                    "summary": analysis_result["summary"],
                    "key_topics": analysis_result["key_topics"],
                    "sentiment": analysis_result["sentiment_analysis"],
                    "action_items": analysis_result["action_items"]
                }
                
                # Store in MongoDB
                st.info("Storing results in MongoDB...")
                summary_id = store_podcast_data(podcast_data)
                
                # Store in Qdrant for vector search
                st.info("Storing vectors in Qdrant...")
                store_vectors(podcast_data, summary_id)
                
                # Send email to board members
                if board_emails:
                    recipient_list = [email.strip() for email in board_emails.split("\n") if email.strip()]
                    st.info(f"Sending summary email to {len(recipient_list)} recipients...")
                    try:
                        send_email_summary(podcast_data, recipient_list)
                        st.success("Email sent successfully!")
                    except Exception as e:
                        st.error(f"Error sending email: {str(e)}")
                
                # Display summary
                st.success("Podcast analysis complete!")
                st.subheader("Executive Summary")
                st.write(podcast_data["summary"])
                
                st.subheader("Key Topics")
                for topic in podcast_data["key_topics"]:
                    st.write(f"- {topic}")
                
                st.subheader("Sentiment Analysis")
                st.write(podcast_data["sentiment"])
                
                st.subheader("Action Items")
                for item in podcast_data["action_items"]:
                    st.write(f"- {item}")
                
                # Clean up temporary files
                os.unlink(audio_path)
                os.unlink(transcript_path)
    
    with tab2:
        st.header("Chat about Analyzed Podcasts")
        
        # Display available podcasts
        podcast_titles = get_all_podcast_titles()
        if not podcast_titles:
            st.warning("No analyzed podcasts found. Please analyze some podcasts first.")
            return
            
        st.write(f"Available podcasts: {', '.join(podcast_titles)}")
        
        user_question = st.text_input("Ask a question about any analyzed podcast")
        
        if st.button("Ask") and user_question:
            with st.spinner("Searching for answer..."):
                # Search Qdrant for similar content
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
                st.write(f"Based on podcast: {podcast_data['title']}")

if __name__ == "__main__":
    main()