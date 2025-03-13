from crewai import Agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import audio_tools, transcription_tools, analysis_tools, summary_tools, delivery_tools
import os
import nest_asyncio  # Fix asyncio event loop issues for Streamlit

nest_asyncio.apply()

load_dotenv()

# Mixtral model via Groq
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,  # Getting all details
    temperature=0.5,  # Randomness
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Audio Processing Agent
audio_processing_agent = Agent(
    role="Audio Processing Agent",
    goal='Process Meeting audio files from various sources with high quality.',
    verbose=True,
    memory=True,
    backstory=(
        "You are an expert in audio processing with skills in format conversion, noise reduction, "
        "and speaker differentiation. Your mission is to prepare high-quality audio files "
        "for accurate transcription by removing background noise and enhancing speech clarity."
    ),
    tools=[audio_tools],
    llm=llm,
    allow_delegation=True
)

# Transcription Agent
transcription_agent = Agent(
    role="Transcription Agent",
    goal='Convert audio to accurate text transcriptions with clear speaker labeling and timestamps.',
    verbose=True,
    memory=True,
    backstory=(
        "As a speech recognition specialist, you excel at converting spoken words into accurate text. "
        "Your expertise includes speaker diarization, identifying different speakers in conversations, "
        "and generating precise timestamps for each segment of dialogue."
    ),
    tools=[transcription_tools],
    llm=llm,
    allow_delegation=True
)

# Analysis Agent
analysis_agent = Agent(
    role="Analysis Agent",
    goal='Perform deep content analysis on transcribed text to identify key topics, sentiment, and insights.',
    verbose=True,
    memory=True,
    backstory=(
        "With your background in natural language processing and semantic analysis, "
        "you excel at identifying the core themes, topics, and sentiment in conversations. "
        "You can map arguments, extract key points, and maintain context awareness across content."
    ),
    tools=[analysis_tools],
    llm=llm,
    allow_delegation=True
)

# Summary Generation Agent
summary_generation_agent = Agent(
    role="Summary Generation Agent",
    goal='Create multi-layered summaries in various formats tailored to user preferences.',
    verbose=True,
    memory=True,
    backstory=(
        "You are a master of concise communication, able to distill complex discussions into "
        "clear, structured summaries. Your expertise includes creating executive summaries, "
        "detailed notes, chapter markers, and extracting actionable insights from conversations."
    ),
    tools=[summary_tools],
    llm=llm,
    allow_delegation=True
)

# Delivery Agent
delivery_agent = Agent(
    role="Delivery Agent",
    goal='Package and deliver summaries in user-preferred formats through various channels.',
    verbose=True,
    memory=True,
    backstory=(
        "You specialize in formatting and delivering content across multiple platforms. "
        "Your skills include format conversion, personalization, and notification management, "
        "ensuring users receive summaries in their preferred format and through their preferred channels."
    ),
    tools=[delivery_tools],
    llm=llm,
    allow_delegation=True
)

# Chatbot Agent
