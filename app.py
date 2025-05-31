# Store user input and plan in session_state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "plan" not in st.session_state:
    st.session_state.plan = ""

st.title("🛠️ IT Project Planner")
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
            st.session_state.plan = response.choices[0].message.content
            st.markdown(st.session_state.plan)
        except Exception as e:
            st.error(f"Error: {e}")

# Show the generated plan if it exists
if st.session_state.plan:
    st.markdown("### Generated Plan:")
    st.markdown(st.session_state.plan)

    if st.button("📋 Copy Plan"):
        pyperclip.copy(st.session_state.plan)
        st.success("Copied to clipboard!")

    if st.button("🔊 Play Plan"):
        engine = pyttsx3.init()
        engine.say(st.session_state.plan)
        engine.runAndWait()

# 🎙️ Dictation — saves to session_state
if st.button("🎙️ Dictate (local mic only)"):
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = recognizer.listen(source)
        st.session_state.user_input = recognizer.recognize_google(audio)
        st.success(f"Recognized: {st.session_state.user_input}")
    except Exception as e:
        st.error(f"Voice error: {e}")
