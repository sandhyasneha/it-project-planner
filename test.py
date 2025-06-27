import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Test Planner", page_icon="✅")

api_key = os.getenv("OPENAI_API_KEY")
st.write(f"API Key loaded: {api_key is not None}")
client = OpenAI(api_key=api_key)

user_input = st.text_area("Describe your project:")

if st.button("Generate"):
    st.write("Input:", user_input)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert IT project manager."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=800
        )
        st.write("Response:", response)
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error: {e}")
        st.exception(e)
