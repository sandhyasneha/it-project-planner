import streamlit as st
st.set_page_config(page_title="IT Project Planner", page_icon="🛠️")

import os
import openai

# Debug: check API key is loaded
st.write("API Key loaded:", os.getenv("OPENAI_API_KEY") is not None)

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("🛠️ IT Project Planner")
user_input = st.text_area("Describe your project:")

if st.button("Generate Plan") and user_input:
    with st.spinner("Generating..."):
        try:
            client = openai.OpenAI(api_key=openai.api_key)
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

