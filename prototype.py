import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from gtts import gTTS

# Function to recognize speech
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, could not understand what you said.")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results: {e}")
        return None

# Function to convert text to speech
def text_to_speech(text, language="en", filename="output.mp3"):
    tts = gTTS(text=text, lang=language)
    tts.save(filename)
    return filename

# Streamlit UI
st.title("🎤 Multi-Language Speech-to-Text & Text-to-Speech")

option = st.radio("Choose an action:", ["Speech-to-Text", "Text-to-Speech"])

if option == "Speech-to-Text":
    st.subheader("🎙️ Speech-to-Text")
    if st.button("Start Speech Recognition"):
        text = speech_to_text()
        if text:
            st.text_area("Recognized Text:", text)

elif option == "Text-to-Speech":
    st.subheader("🔊 Text-to-Speech")
    user_text = st.text_area("Enter text to convert into speech:", "")

    if st.button("Convert to Speech"):
        if user_text.strip():
            audio_file = text_to_speech(user_text, "en")
            with open(audio_file, "rb") as file:
                st.download_button("Download Speech", file, file_name="output.mp3", mime="audio/mp3")
        else:
            st.warning("Please enter some text before converting.")
