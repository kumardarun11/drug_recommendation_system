import speech_recognition as sr
import pyttsx3
import streamlit as st

# Function: Voice input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand."
        except sr.RequestError:
            return "Speech service unavailable."

# Function: Text-to-speech
def voice_output(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()