import base64

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import platform

# Load custom CSS
def load_css():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        # Function to load local image and convert to base64
        def get_base64_of_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()

        # Path to local background image (Change to your image file)
        image_path = "background.jpg"  # Make sure the image is in the same directory

        # Convert the image to base64 format
        bg_image_base64 = get_base64_of_image(image_path)

        # Custom CSS for background image and login overlay
        background_css = f"""
            <style>
            /* Background Image */
            .stApp {{
                background: url("data:image/jpeg;base64,{bg_image_base64}") no-repeat center center fixed;
                background-size: cover;
            }}

            /* Overlay Box */
            .login-box {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(255, 255, 255, 0.1);
                padding: 2rem;
                border-radius: 10px;
                text-align: center;
                backdrop-filter: blur(10px);
                color: white;
                box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2);
                width: 350px;
            }}

            /* Style Inputs */
            input {{
                background: rgba(255, 255, 255, 0.2);
                border: none;
                color: white;
            }}

            /* Center Content */
            .centered {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 20vh;
            }}
            </style>
        """
        st.markdown(background_css, unsafe_allow_html=True)


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

    # Play audio based on OS
    system_platform = platform.system()
    if system_platform == "Darwin":  # macOS
        os.system(f"afplay {filename}")
    elif system_platform == "Linux":
        os.system(f"mpg321 {filename}")
    elif system_platform == "Windows":
        os.system(f"start {filename}")

# Streamlit UI
st.title("🎤 Multi-Language Speech-to-Text & Text-to-Speech")
load_css()  # Apply CSS styles
st.markdown('<p class="black-text">Select an option and language below to proceed:</p>', unsafe_allow_html=True)


# Select Speech-to-Text or Text-to-Speech
option = st.radio("Choose an action:", ["Speech-to-Text", "Text-to-Speech"])

# Language Selection
selected_language = st.selectbox("Select Language:", list(LANGUAGES.keys()))

if option == "Speech-to-Text":
    st.subheader("🎙️ Speech-to-Text")
    if st.button("Start Speech Recognition"):
        text = speech_to_text(LANGUAGES[selected_language])
        if text:st.write("Select an option and language below to proceed:")
        st.session_state['spoken_text'] = text

    if 'spoken_text' in st.session_state:
        st.text_area("Recognized Text:", st.session_state['spoken_text'])

elif option == "Text-to-Speech":
    st.subheader("🔊 Text-to-Speech")
    user_text = st.text_area("Enter text to convert into speech:", "")

    if st.button("Convert to Speech"):
        if user_text.strip():
            text_to_speech(user_text, LANGUAGES[selected_language])
            st.success("Speech generated successfully! 🎶")
        else:
            st.warning("Please enter some text before converting.")
