import base64
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os

# Load custom CSS
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Available languages
LANGUAGES = {
    "English": "en",
    "Kannada": "kn",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta"
}

# Function to recognize speech from microphone
def speech_to_text(language):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, could not understand what you said.")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results: {e}")
        return None

# Function to convert text to speech
def text_to_speech(text, language, filename='output.mp3'):
    tts = gTTS(text=text, lang=language)
    tts.save(filename)
    return filename

# Streamlit UI
st.title("🎤 Multi-Language Speech-to-Text & Text-to-Speech")
load_css()
st.markdown('<p class="black-text">Select an option and language below to proceed:</p>', unsafe_allow_html=True)

# Select Speech-to-Text or Text-to-Speech
option = st.radio("Choose an action:", ["Speech-to-Text", "Text-to-Speech"])

# Language Selection
selected_language = st.selectbox("Select Language:", list(LANGUAGES.keys()))

if option == "Speech-to-Text":
    st.subheader("🎙️ Speech-to-Text")
    if st.button("Start Speech Recognition"):
        text = speech_to_text(LANGUAGES[selected_language])
        if text:
            st.session_state['spoken_text'] = text

    if 'spoken_text' in st.session_state:
        st.text_area("Recognized Text:", st.session_state['spoken_text'])

elif option == "Text-to-Speech":
    st.subheader("🔊 Text-to-Speech")
    user_text = st.text_area("Enter text to convert into speech:", "")

    if st.button("Convert to Speech"):
        if user_text.strip():
            audio_file = text_to_speech(user_text, LANGUAGES[selected_language])
            st.success("Speech generated successfully! 🎶")
            with open(audio_file, "rb") as file:
                st.download_button("Download Speech", file, file_name="output.mp3", mime="audio/mp3")
        else:
            st.warning("Please enter some text before converting.")
