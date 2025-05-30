import os
import streamlit as st
import openai

# Set API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI setup
st.set_page_config(page_title="IT Project Planner", page_icon="🛠️")
st.title("🛠️ IT Project Planner")

# User input
user_input = st.text_area("Describe your project:")

# Generate plan using OpenAI
if st.button("Generate Plan") and user_input:
    with st.spinner("Generating..."):
        try:
            response = openai.ChatCompletion.create(
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
