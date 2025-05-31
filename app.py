import os
import streamlit as st
import sqlite3
import hashlib
from openai import OpenAI
import pyttsx3
import pyperclip
import speech_recognition as sr

# Set page config first
st.set_page_config(page_title="IT Project Planner", page_icon="🛠️")

# Initialize session state
if 'plan' not in st.session_state:
    st.session_state.plan = ""
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# API setup
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
st.write(f"API Key loaded: {api_key is not None}")

# DB helpers (same as before)...

# Login logic (same as before)...

# Main App after login
if logged_in:
    st.title("🛠️ IT Project Planner")

    st.session_state.user_input = st.text_area("Describe your project:", value=st.session_state.user_input)

    if st.button("Generate Plan") and st.session_state.user_input:
        with st.spinner("Generating..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert IT project manager."},
                        {"role": "user", "content": st.session_state.user_input}
                    ],
                    max_tokens=800
                )
                st.session_state.plan = response.choices[0].message.content
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.plan:
        st.markdown(st.session_state.plan)

        if st.button("📋 Copy Plan"):
            pyperclip.copy(st.session_state.plan)
            st.success("Copied to clipboard!")

        if st.button("🔊 Play Plan"):
            engine = pyttsx3.init()
            engine.say(st.session_state.plan)
            engine.runAndWait()

    if st.button("🎙️ Dictate (local mic only)"):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening...")
                audio = recognizer.listen(source)
            recognized_text = recognizer.recognize_google(audio)
            st.session_state.user_input = recognized_text
            st.success(f"Recognized: {recognized_text}")
        except Exception as e:
            st.error(f"Voice error: {e}")
