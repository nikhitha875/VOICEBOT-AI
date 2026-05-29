
import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import tempfile
from gtts import gTTS

st.set_page_config(
    page_title="Nikhitha AI VoiceBot",
    page_icon="🎤",
    layout="centered"
)

st.markdown(
    '''
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #111827, #1e293b);
        color: white;
    }
    h1, h2, h3 {
        text-align: center;
        color: white;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.title("🎤 Nikhitha AI Voice Interview Bot")
st.write("Ask interview questions using your voice.")

api_key = st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("Gemini API key not found.")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = '''
You are Nikhitha, a Computer Science student passionate about AI,
full-stack development, and solving real-world problems.

Answer interview questions naturally and confidently as if speaking in a real interview.

Personality:
- hardworking
- curious
- growth-oriented
- adaptable
- calm communicator

Keep answers:
- concise
- human-like
- conversational
- professional
'''

st.subheader("🎯 Suggested Questions")
st.markdown(
    """
- Tell me about yourself
- What is your biggest strength?
- What motivates you?
- What are your growth areas?
- Why do you want to join 100x?
"""
)

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    key="recorder"
)

if audio:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio["bytes"])
        temp_audio_path = temp_audio.name

    recognizer = sr.Recognizer()

    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)

    try:
        question = recognizer.recognize_google(audio_data)

        st.markdown("### 🧑 You Asked")
        st.write(question)

        response = model.generate_content(
            SYSTEM_PROMPT + "\nUser Question: " + question
        )

        answer = response.text

        st.markdown("### 🤖 AI Response")
        st.write(answer)

        tts = gTTS(answer)
        tts.save("response.mp3")

        audio_file = open("response.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")

    except Exception as e:
        st.error(f"Error: {e}")
