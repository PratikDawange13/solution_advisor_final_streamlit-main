import streamlit as st
import requests
from PyPDF2 import PdfReader
from make import send_link

# Default behavior prompt
DEFAULT_BEHAVIOR_PROMPT = """You are a visa expert whose role is to explain to the client their visa roadmap, which was drafted by a solution architect. Here's how the conversation will flow:

Greet the client and ask if you can proceed to their roadmap.
Wait for their confirmation before starting.
Explain the roadmap one section at a time.
Go in order over each section in detail, NEVER skip any section.
Pause after each section to ensure the client understands. Ask if they are following along or if they have any questions.
Prioritise discussing the NOCs given in the  roadmap first and  then only suggest additional NOCs when asked.
Answer any questions briefly and continue when they are ready.
Always ask for user confirmation before moving to the next section like "should we proceed" or "do you have any questions", never go ahead without users confirmation, if no confirmation is given then state that you are still waiting for eg "Once you confirm then we shall move ahead".
Avoid jargon unless necessary. Use simple language and keep explanations short.
Speak naturally donn't use special symbols."""

# Title
st.title("Solution Advisor")


# Create two columns
col1, col2 = st.columns(2)

# Column 1: Behavior Prompt
with col1:
    st.subheader("Behavior Prompt")
    behavior_prompt = st.text_area("Enter your prompt here:", value="")
    override= st.checkbox("Override Default Behaviour",value=False)
    emails=st.text_input(label="Enter a list of emails (comma-separated)")
    voice_avatar=st.selectbox(label="Voice Avatar",options=["en-NG-AbeoNeural",
                                                            "en-NG-EzinneNeural",
                                                            "en-IN-AashiNeural",
                                                            "en-IN-AaravNeural",
                                                            "en-GB-RyanNeural",
                                                            "en-GB-SoniaNeural",
                                                            "en-US-AvaMultilingualNeural",
                                                            "en-US-AndrewMultilingualNeural"])
    emails_list = [email.strip() for email in emails.split(",")]
    


# Column 2: Roadmap
with col2:
    st.subheader("Roadmap")
    roadmap = st.text_area("Enter your roadmap here:")
    uploaded_file = st.file_uploader("Upload Roadmap File (PDF)", type="pdf")
    expire_minutes=st.number_input("Enter the duration of the meeting",value=10)

    # Convert uploaded PDF to text
    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)
        roadmap = "\n".join([page.extract_text() for page in pdf_reader.pages])
        st.success("File uploaded successfully")

# Submit Button
if st.button("Submit"):
    # Only validate roadmap since behavior prompt can be empty
    if not roadmap:
        st.error("Please provide a Roadmap either by input or file upload.")
    elif not emails:
        st.error("Please enter email(s) to send the meet link to")
    else:
        # Use default prompt if no behavior prompt is provide
        final_behavior_prompt = behavior_prompt.strip() or DEFAULT_BEHAVIOR_PROMPT
        
        # Prepare data for API
        payload = {
                    "speed": "normal",
                    "emotion": [
                        "positivity:high",
                        "curiosity"
                    ],
                    "roadmap": roadmap,
                    "prompt": final_behavior_prompt,
                    "voice_id": voice_avatar,
                    "session_time": 10,
                    "emails": emails_list,
                    "override": override
                    } 

        # Connect to the endpoint
        try:
            response = requests.post(
                "https://solution-advisor-updated.fly.dev/",
                json=payload
            )
            response.raise_for_status()

            # Parse API response
            data = response.json()
            print(data)
            room_url = data.get("room_url")
            link_sent=send_link(room_url, emails_list)
            print(link_sent)
            
            if link_sent.status_code==200:
                st.success("Successfully sent meet link on mail.")
                st.write("Or access the meet directly using the link below.")
                st.code(room_url, language="python")
            else:
                st.error("Couldn't send the meet link over mail")
                st.write("Access the meet directly using the link below.")
                st.code(room_url, language="python")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the server: {e}")
