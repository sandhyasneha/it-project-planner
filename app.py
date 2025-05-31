import os
import streamlit as st
from openai import OpenAI
import traceback
import time

# Set Streamlit page config
st.set_page_config(page_title="IT Project Planner", page_icon="🛠️")

# Load API key from environment
api_key = os.getenv("OPENAI_API_KEY")
st.write(f"API Key loaded: {api_key is not None}")

if not api_key:
    st.error("❌ OPENAI_API_KEY not found in environment!")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("🛠️ IT Project Planner")
user_input = st.text_area("Describe your project:")

# Retry wrapper (basic)
def fetch_plan_with_retry():
    for i in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert IT project manager."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            if i < 2:
                st.warning(f"Retry {i+1}/3... Error: {e}")
                time.sleep(2)
            else:
                raise

if st.button("Generate Plan") and user_input:
    with st.spinner("Generating plan..."):
        try:
            plan = fetch_plan_with_retry()
            st.markdown(plan)
        except Exception as e:
            st.error("Error: Could not fetch project plan.")
            st.text(traceback.format_exc())

