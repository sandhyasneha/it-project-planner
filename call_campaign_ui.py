import os
import streamlit as st
import pandas as pd
from twilio.rest import Client
from tempfile import NamedTemporaryFile

# --- Branding ---
st.set_page_config(
    page_title="TruckTaxOnline 2290 Call Campaign",
    page_icon="📞",
    layout="centered"
)

# --- Custom Styles ---
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

# --- Upload Section ---
st.subheader("📁 Upload Customer List")
uploaded_excel = st.file_uploader("Choose a CSV or Excel file with a 'Phone' column:", type=["csv", "xlsx"])

st.subheader("🎵 Upload Audio File")
uploaded_audio = st.file_uploader("Choose an audio file (MP3 or WAV)", type=["mp3", "wav"])

# --- Launch Button ---
deploy_btn = st.button("🚀 Launch Voice Campaign")

# --- Twilio Setup ---
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# --- Helper to Load Phone Numbers ---
@st.cache_data
def load_phone_numbers(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    return df['Phone'].dropna().astype(str).tolist()

# --- Campaign Logic ---
if deploy_btn:
    if not uploaded_excel or not uploaded_audio:
        st.warning("Please upload both a phone list and an audio file.")
    else:
        phone_numbers = load_phone_numbers(uploaded_excel)

        # Save the uploaded audio file temporarily
        with NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_audio.name)[-1]) as temp_audio:
            temp_audio.write(uploaded_audio.read())
            temp_audio_path = temp_audio.name

        st.success(f"📞 Preparing to call {len(phone_numbers)} customers...")

        for number in phone_numbers:
            try:
                call = client.calls.create(
                    to=number,
                    from_=TWILIO_PHONE_NUMBER,
                    twiml=f'<Response><Play>{temp_audio_path}</Play></Response>'
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
