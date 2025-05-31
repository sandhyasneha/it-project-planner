import os
import streamlit as st
import sqlite3
import hashlib
from openai import OpenAI
import pyperclip

# ----- CONFIG -----
st.set_page_config(page_title="IT Project Planner", page_icon="🛠️")
api_key = os.getenv("OPENAI_API_KEY")
st.write(f"API Key loaded: {api_key is not None}")
client = OpenAI(api_key=api_key)

# ----- DB HELPERS -----
def make_hashes(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def create_usertable():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS userstable(email TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS plans(email TEXT, plan TEXT)')
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

def save_plan(email, plan):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT INTO plans(email, plan) VALUES (?, ?)', (email, plan))
    conn.commit()
    conn.close()

def get_user_plans(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT plan FROM plans WHERE email = ?', (email,))
    plans = c.fetchall()
    conn.close()
    return [p[0] for p in plans]

# ----- LOGIN -----
create_usertable()
menu = ["Login", "SignUp"]
choice = st.sidebar.selectbox("Menu", menu)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""

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
            st.session_state.email = email
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

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "generated_plan" not in st.session_state:
        st.session_state.generated_plan = ""

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
                plan = response.choices[0].message.content
                st.session_state.generated_plan = plan
                save_plan(st.session_state.email, plan)
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.generated_plan:
        st.subheader("Generated Plan")
        st.markdown(st.session_state.generated_plan)

        if st.button("📋 Copy Plan"):
            pyperclip.copy(st.session_state.generated_plan)
            st.success("Copied to clipboard!")

        # Play and Dictate features are disabled to avoid PyAudio dependency issue
        st.info("Voice features temporarily disabled due to PyAudio deployment limitations.")

        st.download_button(
            label="📄 Download Plan as .txt",
            data=st.session_state.generated_plan,
            file_name="project_plan.txt",
            mime="text/plain"
        )

    if st.checkbox("Show Plan History"):
        st.subheader("Your Past Plans")
        past_plans = get_user_plans(st.session_state.email)
        for i, p in enumerate(past_plans[::-1]):
            st.markdown(f"**Plan {len(past_plans) - i}:**\n{p}")
