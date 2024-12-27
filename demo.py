import streamlit as st
import requests
from PyPDF2 import PdfReader

# Default behavior prompt
DEFAULT_BEHAVIOR_PROMPT = """You are a visa expert whose role is to explain to the client their visa roadmap, which was drafted by a solution architect. Here's how the conversation will flow:

Greet the client and ask if you can proceed to their roadmap.
Wait for their confirmation before starting.
Explain the roadmap one section at a time.
Pause after each section to ensure the client understands. Ask if they are following along or if they have any questions.
Answer any questions briefly and continue when they are ready.
Avoid jargon unless necessary. Use simple language and keep explanations short.
Speak naturally donn't use special symbols."""

# Title
st.title("Solution Advisor")

# Create two columns
col1, col2 = st.columns(2)

# Column 1: Behavior Prompt
with col1:
    st.subheader("Behavior Prompt")
    behavior_prompt = st.text_area("Enter your prompt here:", value=DEFAULT_BEHAVIOR_PROMPT)

# Column 2: Roadmap
with col2:
    st.subheader("Roadmap")
    roadmap = st.text_area("Enter your roadmap here:")
    uploaded_file = st.file_uploader("Upload Roadmap File (PDF)", type="pdf")

    # Convert uploaded PDF to text
    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        roadmap = "\n".join([page.extract_text() for page in pdf_reader.pages])
        st.success("File uploaded and content extracted!")

# Submit Button
if st.button("Submit"):
    # Only validate roadmap since behavior prompt has a default
    if not roadmap:
        st.error("Please provide a Roadmap either by input or file upload.")
    else:
        # Use default prompt if behavior_prompt is empty
        final_behavior_prompt = behavior_prompt.strip() or DEFAULT_BEHAVIOR_PROMPT
        
        # Prepare data for API
        payload = {
            "behavior_prompt": final_behavior_prompt,
            "roadmap": roadmap
        }

        # Connect to the endpoint
        try:
            response = requests.post(
                "https://visaroadmap-pipeline-pratik1-1001.fly.dev/",
                json=payload
            )
            response.raise_for_status()

            # Parse API response
            data = response.json()
            room_url = data.get("room_url")
            
            if room_url:
                st.success("Successfully connected! Click below to join the room:")
                st.markdown(f"[Join Now]({room_url})", unsafe_allow_html=True)
            else:
                st.error("Room URL not found in the API response.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the server: {e}")