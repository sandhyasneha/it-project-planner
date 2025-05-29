import os
import streamlit as st
import pandas as pd
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

# Load Twilio credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# UI
st.set_page_config(page_title="📞 Call Campaign Dashboard", layout="centered")
st.title("📞 AI Call Campaign Launcher")
st.markdown("Upload a phone list to launch your Twilio call campaign using a pre-recorded GitHub audio.")

# Upload phone number list
uploaded_excel = st.file_uploader("Upload Customer List (Excel or CSV)", type=["csv", "xlsx"])
deploy_btn = st.button("🚀 Launch Call Campaign")

# Twilio audio URL from GitHub
audio_url = "https://raw.githubusercontent.com/sandhyasneha/streamlit-call-campaign/main/HumeAI_voice-preview_prefile.wav"

# Load phone numbers from uploaded file
@st.cache_data
def load_phone_numbers(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df['Phone'].dropna().astype(str).tolist()

# Run campaign
if deploy_btn:
    if not uploaded_excel:
        st.warning("Please upload a phone list.")
    else:
        phone_numbers = load_phone_numbers(uploaded_excel)
        st.success(f"Preparing to call {len(phone_numbers)} numbers...")

        for number in phone_numbers:
            try:
                call = client.calls.create(
                    to=number,
                    from_=TWILIO_PHONE_NUMBER,
                    twiml=f'<Response><Play>{audio_url}</Play></Response>'
                )
                st.info(f"📞 Calling {number}... SID: {call.sid}")
            except Exception as e:
                st.error(f"❌ Failed to call {number}: {e}")

        st.success("✅ Campaign launched!")
