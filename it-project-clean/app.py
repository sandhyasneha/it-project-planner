import os
import openai
import streamlit as st  # <--- You missed this

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI setup
st.set_page_config(page_title="IT Project Planner", page_icon="🛠️", layout="centered")
st.title("🛠️ IT Project Planner (AI-powered)")
st.markdown("Type your project need (e.g., 'steps for data center migration') and get a plan.")

# Text input from user
user_prompt = st.text_area("📝 Your Project Description", height=150)

if st.button("Generate Plan") and user_prompt:
    with st.spinner("Generating project plan..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert IT project manager. Respond with clear, structured project plans."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.4,
                max_tokens=800
            )
            plan = response['choices'][0]['message']['content']
            st.markdown("### 📋 Project Plan")
            st.markdown(plan)

            # Add download button
            st.download_button(
                label="📄 Download Plan",
                data=plan,
                file_name="project_plan.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {e}")
