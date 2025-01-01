import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Constants
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")
MAX_MESSAGES = 20  # Maximum number of messages (10 user + 10 assistant)

# Initialize OpenAI client
client = OpenAI(
    api_key=API_KEY,
    base_url=API_URL
)

st.set_page_config(
    page_title="Twins Talk By Cyber Tiwari",
    page_icon="🤖",
    layout="wide"
)

# Streamlit App Title and Disclaimer
st.title("Twins Talk By Cyber Tiwari")
with st.expander("ℹ️ Disclaimer"):
    st.caption(
        """
        Thank you for your interest! Please be aware that this demo supports up to 10 interactions 
        and may temporarily become unavailable during high usage periods. 
        It is built on top of a Pretrained LLM Model, so it might occasionally make mistakes. 
        We appreciate your patience, understanding, and proper feedback for improvements
        """
    )

# Initialize session state variables
st.session_state.setdefault("openai_model", LLM_MODEL_NAME)
st.session_state.setdefault("messages", [])

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check message limit
if len(st.session_state.messages) >= MAX_MESSAGES:
    st.info(
        """
        Notice: You’ve reached the message limit for this demo version. 
        We sincerely appreciate your interest! To continue exploring, 
        you can fork this project directly from our [GitHub repository](https://github.com/cybertiwari/twinstalk) and build your own version. 
        Thank you for your understanding and happy building!
        """
    )
else:
    # User input handling
    if prompt := st.chat_input("Type your message here..."):
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)

        # Display user's message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response handling
        with st.chat_message("assistant"):
            try:
                # Prepare messages for the API
                messages = (
                    [{"role": "system", "content": SYSTEM_PROMPT}] +
                    [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                )

                # Get assistant response
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=messages,
                    stream=True,
                )
                response = st.write_stream(stream)

                # Append assistant's response to session state
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                # Handle rate limit or other exceptions
                error_message = """
                Apologies! I'm unable to respond at the moment as this service has experienced high usage recently.
                """
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message}
                )
                st.rerun()