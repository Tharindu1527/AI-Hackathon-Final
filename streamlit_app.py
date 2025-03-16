# streamlit_app.py
import streamlit as st
import os
import tempfile
from datetime import datetime
import json
import base64

# Import custom modules
from utils.config import load_environment
from crews import get_crew, list_available_crews
from api.assemblyai import transcribe_podcast
from api.composio import send_email_summary
from database.mongodb import store_podcast_data, get_all_podcast_titles, get_podcast_by_title
from database.qdrant import store_vectors
from app.chatbot import generate_answer
from api.tts import text_to_speech

# Load environment variables
load_environment()

def main():
    st.title("Podcast Analyzer & Chatbot")

    # Add app version and sidebar config
    st.sidebar.title("Configuration")
    st.sidebar.caption("Version 2.0 - Enhanced Agent Architecture")
    
    # Crew selection
    available_crews = list_available_crews()
    crew_display_names = {
        "standard": "Standard",
        "enhanced": "Enhanced (with fact-checking)",
        "multilingual": "Multilingual",
        "research": "Research-focused",
        "deep_research": "Deep Research",
        "fact_checking": "Fact Checking",
        "advanced_multilingual": "Advanced Multilingual",
        "localization": "Localization"
    }
    
    crew_options = [crew_display_names.get(crew, crew.replace("_", " ").title()) for crew in available_crews[:5]]  # Limit to first 5 for simplicity
    
    crew_type = st.sidebar.radio(
        "Crew Type",
        crew_options
    )
    
    # Convert display name back to crew type
    reverse_mapping = {v: k for k, v in crew_display_names.items()}
    selected_crew_type = reverse_mapping.get(crew_type, "standard")
    
    # Model selection
    model_options = ["gpt-4o", "gpt-3.5-turbo"]
    selected_model = st.sidebar.selectbox("AI Model", options=model_options, index=0)
    
    # Multilingual options
    languages = ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Arabic"]
    if "Multilingual" in crew_type or "Localization" in crew_type:
        target_languages = st.sidebar.multiselect(
            "Target Languages",
            options=languages,
            default=["English", "Spanish"]
        )
    else:
        target_languages = ["English"]
    
    # Add database status indicator
    try:
        from database.mongodb import get_mongodb_client
        client = get_mongodb_client()
        client.admin.command('ping')
        st.sidebar.success("✅ Database connection successful")
    except Exception as e:
        st.sidebar.warning(f"⚠️ Database connection unavailable (using mock data): {str(e)}")
    
    # Create tabs for different functions
    tab1, tab2, tab3, tab4 = st.tabs(["Analyze Podcast", "Chat about Podcasts", "Listen to Summaries", "Fact Check"])
    
    with tab1:
        st.header("Upload and Analyze Podcast")
        
        uploaded_file = st.file_uploader("Choose a podcast audio file", type=["mp3", "wav", "m4a"])
        
        podcast_title = st.text_input("Podcast Title")
        board_emails = st.text_area("Board Member Emails (one per line)")
        
        if st.button("Analyze Podcast", key="analyze_podcast_btn"):
            if not podcast_title:
                st.error("Please enter a podcast title")
                return
                
            if uploaded_file is None:
                st.error("Please upload a podcast audio file")
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
                    
                    # Create the appropriate crew with the selected model
                    st.info(f"Running {crew_type} crew analysis with {selected_model}...")
                    
                    # Create crew with options
                    crew_kwargs = {"model": selected_model}
                    
                    # Add language options for multilingual crews
                    if "Multilingual" in crew_type or "Localization" in crew_type:
                        crew_kwargs["target_languages"] = target_languages
                    
                    podcast_crew = get_crew(selected_crew_type, **crew_kwargs)
                    
                    # Run the analysis
                    result_json = podcast_crew.run_analysis(transcript)
                    analysis_result = json.loads(result_json)
                    
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
                    
                    # Add translations if available
                    if "translations" in analysis_result:
                        podcast_data["translations"] = analysis_result["translations"]
                    
                    # Store in MongoDB
                    st.info("Storing results in database...")
                    try:
                        summary_id = store_podcast_data(podcast_data)
                        st.success("Data stored successfully!")
                    except Exception as e:
                        st.error(f"Error storing data: {str(e)}")
                        summary_id = "mock_id_12345"
                    
                    # Store in Qdrant for vector search
                    st.info("Storing vectors for semantic search...")
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
                    
                    # Display results
                    st.success("Podcast analysis complete!")
                    
                    # Executive Summary
                    st.subheader("Executive Summary")
                    st.write(analysis_result.get("summary", "The executive summary could not be generated completely."))
                    
                    # Key Topics
                    st.subheader("Key Topics")
                    for topic in analysis_result.get("key_topics", ["Topic information not available"]):
                        st.write(f"- {topic}")
                    
                    # Sentiment Analysis
                    st.subheader("Sentiment Analysis")
                    st.write(analysis_result.get("sentiment_analysis", "Sentiment analysis could not be generated completely."))
                    
                    # Action Items
                    st.subheader("Action Items")
                    for item in analysis_result.get("action_items", ["Action items not available"]):
                        st.write(f"- {item}")
                    
                    # Display translations if available (Multilingual crew)
                    if "translations" in analysis_result:
                        st.subheader("Translations")
                        
                        for language, content in analysis_result["translations"].items():
                            with st.expander(f"{language.capitalize()} Translation"):
                                if isinstance(content, dict):
                                    if "summary" in content:
                                        st.write("**Summary:**")
                                        st.write(content["summary"])
                                    
                                    if "action_items" in content:
                                        st.write("**Action Items:**")
                                        if isinstance(content["action_items"], list):
                                            for item in content["action_items"]:
                                                st.write(f"- {item}")
                                        else:
                                            st.write(content["action_items"])
                                else:
                                    st.write(content)
                    
                    # Enhanced features (Research, Fact Check)
                    if "research" in analysis_result:
                        st.subheader("Research Insights")
                        st.write(analysis_result["research"])
                    
                    if "fact_check" in analysis_result:
                        st.subheader("Fact Check Results")
                        fact_check = analysis_result["fact_check"]
                        
                        if isinstance(fact_check, dict):
                            if "results" in fact_check:
                                for result in fact_check["results"]:
                                    status_color = "green" if result["status"] == "Verified" else "red" if result["status"] == "Refuted" else "orange"
                                    st.markdown(f"- **Claim:** {result['claim']}  \n  **Status:** <span style='color:{status_color}'>{result['status']}</span>", unsafe_allow_html=True)
                            else:
                                st.write(fact_check)
                        else:
                            st.write(fact_check)
                    
                    # Add TTS option
                    if st.button("Generate Audio Summary", key="generate_audio_summary_btn1"):
                        with st.spinner("Generating audio..."):
                            summary_text = analysis_result.get("summary", "No summary available.")
                            voice = st.selectbox("Select voice:", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], key="voice_select1")
                            audio_file = text_to_speech(summary_text, voice=voice)
                            if audio_file:
                                st.success("Audio generated successfully!")
                                st.audio(audio_file)
                            else:
                                st.error("Failed to generate audio summary")
                    
                    # Clean up temporary files
                    os.unlink(audio_path)
            except Exception as main_error:
                st.error(f"An error occurred during analysis: {str(main_error)}")
                st.info("Please try again with a different podcast or check the logs for more details.")                
    
    with tab2:
        st.header("Chat about Analyzed Podcasts")
        
        # Podcast selection
        podcast_titles = get_all_podcast_titles()
        if not podcast_titles:
            st.warning("No analyzed podcasts found. Please analyze some podcasts first.")
        else:
            selected_podcast = st.selectbox(
                "Select a podcast to chat about:",
                options=podcast_titles,
                index=0,
                key="chat_podcast_select"
            )
                
            st.write(f"Selected podcast: **{selected_podcast}**")
            
            user_question = st.text_input("Ask a question about this podcast")
            
            if st.button("Ask", key="ask_question_btn"):
                if not user_question:
                    st.error("Please enter a question")
                    return
                    
                with st.spinner("Searching for answer..."):
                    try:
                        # Get podcast data
                        podcast_data = get_podcast_by_title(selected_podcast)
                        
                        if not podcast_data:
                            st.error(f"Could not find podcast data for '{selected_podcast}'")
                        else:
                            # Generate answer
                            answer = generate_answer(podcast_data, user_question)
                            
                            st.subheader("Answer")
                            st.write(answer)
                            
                            # Add TTS option for the answer
                            if st.button("Listen to Answer", key="listen_answer_btn"):
                                with st.spinner("Generating audio..."):
                                    voice = st.selectbox("Select voice:", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], key="voice_select2")
                                    audio_file = text_to_speech(answer, voice=voice)
                                    if audio_file:
                                        st.success("Audio generated successfully!")
                                        st.audio(audio_file)
                                    else:
                                        st.error("Failed to generate audio for answer")
                            
                            st.subheader("Source")
                            st.write(f"Based on podcast: {podcast_data.get('title', 'Unknown Podcast')}")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    
    with tab3:
        st.header("Listen to Podcast Summaries")
        
        # Podcast selection
        podcast_titles = get_all_podcast_titles()
        if not podcast_titles:
            st.warning("No analyzed podcasts found. Please analyze some podcasts first.")
        else:
            selected_podcast = st.selectbox(
                "Select a podcast to listen to:",
                options=podcast_titles,
                index=0,
                key="listen_podcast_select"
            )
            
            # Voice selection
            voice_options = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
            selected_voice = st.selectbox("Select a voice:", options=voice_options, index=0, key="voice_select3")
            
            # Language selection (for multilingual podcasts)
            podcast_data = get_podcast_by_title(selected_podcast)
            available_languages = ["English"]
            
            if podcast_data and "translations" in podcast_data:
                for language in podcast_data["translations"]:
                    if language.lower() != "english":
                        available_languages.append(language.capitalize())
            
            selected_language = st.selectbox("Select language:", options=available_languages, index=0, key="language_select")
            
            if st.button("Generate Audio Summary", key="generate_audio_summary_btn2"):
                with st.spinner("Generating audio summary..."):
                    try:
                        if not podcast_data:
                            st.error(f"Could not find podcast data for '{selected_podcast}'")
                        else:
                            # Get the appropriate summary based on language
                            if selected_language.lower() == "english":
                                summary_text = podcast_data.get("summary", "Summary not available.")
                            else:
                                language_key = selected_language.lower()
                                if "translations" in podcast_data and language_key in podcast_data["translations"]:
                                    if isinstance(podcast_data["translations"][language_key], dict):
                                        summary_text = podcast_data["translations"][language_key].get("summary", "Translation not available.")
                                    else:
                                        summary_text = podcast_data["translations"][language_key]
                                else:
                                    summary_text = "Translation not available for this language."
                            
                            # Generate audio
                            audio_file = text_to_speech(summary_text, voice=selected_voice)
                            
                            if audio_file:
                                st.success(f"Audio summary for '{selected_podcast}' generated successfully!")
                                st.audio(audio_file)
                                
                                # Add download option
                                with open(audio_file, "rb") as file:
                                    audio_bytes = file.read()
                                    file_name = f"{selected_podcast.replace(' ', '_')}_{selected_language}_summary.mp3"
                                    st.download_button(
                                        label="Download Audio Summary",
                                        data=audio_bytes,
                                        file_name=file_name,
                                        mime="audio/mp3",
                                        key="download_summary_btn"
                                    )
                            else:
                                st.error("Failed to generate audio summary")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    
    with tab4:
        st.header("Fact Check Podcast")
        
        # Podcast selection
        podcast_titles = get_all_podcast_titles()
        if not podcast_titles:
            st.warning("No analyzed podcasts found. Please analyze some podcasts first.")
        else:
            selected_podcast = st.selectbox(
                "Select a podcast to fact check:",
                options=podcast_titles,
                index=0,
                key="fact_check_podcast_select"
            )
            
            if st.button("Extract Claims", key="extract_claims_btn"):
                with st.spinner("Extracting claims from podcast..."):
                    try:
                        # Get podcast data
                        podcast_data = get_podcast_by_title(selected_podcast)
                        
                        if not podcast_data:
                            st.error(f"Could not find podcast data for '{selected_podcast}'")
                        else:
                            # Get the transcript
                            transcript = podcast_data.get("transcript", "")
                            
                            if not transcript:
                                st.error("No transcript available for fact checking")
                            else:
                                # Use the fact checker agent
                                from agents.registry import get_agent
                                fact_checker = get_agent("fact_checker")
                                
                                st.info("Extracting claims...")
                                claims = fact_checker.extract_claims(transcript)
                                
                                if not claims:
                                    st.warning("No factual claims were identified in this podcast")
                                else:
                                    st.success(f"Found {len(claims)} factual claims")
                                    
                                    # Store claims in session state for later use
                                    st.session_state.claims = claims
                                    
                                    # Display claims
                                    st.subheader("Identified Claims")
                                    for i, claim in enumerate(claims):
                                        st.write(f"{i+1}. {claim}")
                                    
                                    # Allow user to select claims to verify
                                    st.session_state.selected_claims = st.multiselect(
                                        "Select claims to verify:",
                                        options=claims,
                                        default=claims[:min(3, len(claims))]
                                    )
                    except Exception as e:
                        st.error(f"An error occurred during claim extraction: {str(e)}")
            
            # Check if we have selected claims in session state
            if hasattr(st.session_state, 'selected_claims') and st.session_state.selected_claims:
                if st.button("Verify Selected Claims", key="verify_claims_btn"):
                    st.subheader("Verification Results")
                    
                    # Get fact checker agent
                    from agents.registry import get_agent
                    fact_checker = get_agent("fact_checker")
                    
                    progress_bar = st.progress(0)
                    results = []
                    
                    # Verify each selected claim
                    for i, claim in enumerate(st.session_state.selected_claims):
                        with st.spinner(f"Verifying claim {i+1} of {len(st.session_state.selected_claims)}..."):
                            result = fact_checker.verify_claim(claim, use_wikipedia=True)
                            results.append(result)
                            
                            # Update progress
                            progress = (i + 1) / len(st.session_state.selected_claims)
                            progress_bar.progress(progress)
                    
                    # Display results
                    st.success("Verification complete!")
                    
                    for result in results:
                        status_color = "green" if result["status"] == "Verified" else "red" if result["status"] == "Refuted" else "orange"
                        
                        with st.expander(f"{result['claim']} - {result['status']}"):
                            st.markdown(f"**Status:** <span style='color:{status_color}'>{result['status']}</span>", unsafe_allow_html=True)
                            st.write("**Details:**")
                            st.write(result["details"])

if __name__ == "__main__":
    main()