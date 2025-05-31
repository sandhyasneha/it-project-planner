import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="IT Project Planner", page_icon="🛠️")
st.title("🛠️ IT Project Planner")

api_key = os.getenv("OPENAI_API_KEY")
st.write("API Key loaded:", bool(api_key))  # Debug

client = OpenAI(api_key=api_key)

user_input = st.text_area("Describe your project:")

if st.button("Generate Plan") and user_input:
    with st.spinner("Generating..."):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert IT project manager."},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=800
            )
            plan = response.choices[0].message.content
            st.markdown(plan)
        except Exception as e:
            st.error(f"Error: {e}")

