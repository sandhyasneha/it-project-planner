import os
import streamlit as st
import sqlite3
import hashlib
from openai import OpenAI
import pyttsx3
import speech_recognition as sr

# Page configuration
st.set_page_config(page_title="IT Project Planner", page_icon="🛠️")

# Load API Key
api_key = os.getenv("OPENAI_API_KEY")
st.write(f"API Key loaded: {api_key is not None}")
client = OpenAI(api_key=api_key)

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "plan" not in st.session_state:
    st.session_state.plan = ""

# ----- DB HELPERS -----
def make_hashes(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def create_usertable():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS userstable(email TEXT, password TEXT)')
    conn.commit()
    conn.close()

def add_userdata(email, password):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT INTO userstable(email, password) VALUES (?, ?)', (email, make_hashes(password)))
    conn.commit()
    conn.close()

def login_user(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE email = ? AND password = ?', (email, make_hashes(password)))
    data = c.fetchall()
    conn.close()
    return data

# ----- LOGIN -----
create_usertable()
menu = ["Login", "SignUp"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.sidebar.subheader("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if not email.endswith("@nttdata.com"):
            st.sidebar.error("Only @nttdata.com emails allowed")
        elif login_user(email, password):
            st.sidebar.success(f"Welcome {email}")
            st.session_state.logged_in = True
        else:
            st.sidebar.error("Invalid credentials")

elif choice == "SignUp":
    st.sidebar.subheader("Create Account")
    email = st.sidebar.text_input("New Email")
    password = st.sidebar.text_input("New Password", type="password")
    if st.sidebar.button("Create Account"):
        if not email.endswith("@nttdata.com"):
            st.sidebar.error("Only @nttdata.com emails allowed")
        else:
            add_userdata(email, password)
            st.sidebar.success("Account created!")

# ----- MAIN APP -----
if st.session_state.logged_in:
    st.title("🛠️ IT Project Planner")

    st.session_state.user_input = st.text_area("Describe your project:", value=st.session_state.user_input)

    if st.button("Generate Plan"):
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

        # Download button
        st.download_button(
            label="📥 Download Plan (.txt)",
            data=st.session_state.plan,
            file_name="project_plan.txt",
            mime="text/plain"
        )

        if st.button("🔊 Play Plan"):
            try:
                engine = pyttsx3.init()
                engine.say(st.session_state.plan)
                engine.runAndWait()
            except Exception as e:
                st.error(f"Voice error: {e}")

    if st.button("🎙️ Dictate (local mic only)"):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening...")
                audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            st.session_state.user_input = text
            st.success(f"Recognized: {text}")
        except Exception as e:
            st.error(f"Voice error: {e}")

