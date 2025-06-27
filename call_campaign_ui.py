# --- Step 1: Set up ---
import os
import streamlit as st
import pandas as pd
from twilio.rest import Client
import requests
import base64

# --- Branding + Page Config ---
st.set_page_config(
    page_title="TruckTaxOnline 2290 Call Campaign",
    page_icon="📞",
    layout="centered"
)

st.markdown("""
<style>
body {background-color: #f6f9fc;}
[data-testid="stSidebar"] > div:first-child {
    background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
[data-testid="stAppViewContainer"] {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #333;
}
.block-container {
    padding: 2rem;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.image("https://www.trucktaxonline.com/assets/logo.png", width=200)
st.title("📢 TruckTaxOnline — 2290 Call Campaign")
st.markdown("Reach truckers faster with automated voice calls for 2290 tax reminders.")

# --- Upload section ---
st.subheader("📁 Upload Customer List")
uploaded_excel = st.file_uploader("Choose a CSV or Excel file with a 'Phone' column:", type=["csv", "xlsx"])

st.subheader("🎵 Upload Audio File")
audio_file = st.file_uploader("Upload a WAV or MP3 file", type=["wav", "mp3"])

# --- Start button ---
deploy_btn = st.button("🚀 Launch Voice Campaign")

# --- Twilio credentials ---
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# --- GitHub Info (from .streamlit/secrets.toml) ---
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPO = "sandhyasneha/streamlit-call-campaign"
GITHUB_PATH = "uploaded_audio"

# --- Upload to GitHub via API ---
def upload_to_github(audio_file):
    if not audio_file:
        return None

    audio_bytes = audio_file.read()
    b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    filename = audio_file.name.replace(" ", "_")
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_PATH}/{filename}"

    data = {
        "message": f"Add new audio file {filename}",
        "content": b64_audio
    }
    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [201, 200]:
        return f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{GITHUB_PATH}/{filename}"
    else:
        st.error(f"GitHub upload failed: {response.status_code} {response.text}")
        return None

# --- Load numbers ---
@st.cache_data
def load_phone_numbers(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df['Phone'].dropna().astype(str).tolist()

# --- Main Logic ---
if deploy_btn:
    if not uploaded_excel or not audio_file:
        st.warning("Please upload both phone list and audio file.")
    else:
        st.success("Uploading audio file to GitHub...")
        audio_url = upload_to_github(audio_file)

        if audio_url:
            phone_numbers = load_phone_numbers(uploaded_excel)
            st.success(f"📞 Preparing to call {len(phone_numbers)} customers...")

            for number in phone_numbers:
                try:
                    call = client.calls.create(
                        to=number,
                        from_=TWILIO_PHONE_NUMBER,
                        twiml=f'<Response><Play>{audio_url}</Play></Response>'
                    )
                    st.info(f"✅ Calling {number}... SID: {call.sid}")
                except Exception as e:
                    st.error(f"❌ Failed to call {number}: {e}")

            st.success("🎉 Campaign launched successfully!")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<center><small>Powered by <a href='https://www.trucktaxonline.com' target='_blank'>TruckTaxOnline.com</a></small></center>",
    unsafe_allow_html=True
)
