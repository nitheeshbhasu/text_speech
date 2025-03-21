import base64
import streamlit as st
import sounddevice as sd
import numpy as np
import whisper
from gtts import gTTS

# Load Whisper model
model = whisper.load_model("base")

# Function to record audio
def record_audio(duration=5, samplerate=44100):
    st.info("Recording... Speak now!")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    return audio

# Function to transcribe speech using Whisper
def speech_to_text():
    audio_data = record_audio()
    np.save("audio.npy", audio_data)  # Save as .npy file
    result = model.transcribe("audio.npy")  # Transcribe using Whisper
    text = result["text"]
    st.success(f"You said: {text}")
    return text

# Function to convert text to speech
def text_to_speech(text, language, filename='output.mp3'):
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
