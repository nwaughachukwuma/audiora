import uuid

import httpx
import streamlit as st

from src.env_var import APP_URL, BACKEND_URL
from src.utils.chat_utils import ChatMessage, SessionChatRequest, content_types
from src.utils.example_utils import display_example_cards, handle_selected_example
from src.utils.main_utils import chat

# Initialize session state
if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_audiocast" not in st.session_state:
    st.session_state.current_audiocast = None
if "seleted_example" not in st.session_state:
    st.session_state.seleted_example = None

# Configure page
st.set_page_config(page_title="AudioCaster", page_icon="🎧", layout="wide")

# Sidebar for content type selection
st.sidebar.title("AudioCaster")
content_type = st.sidebar.selectbox(
    "Select Content Type",
    content_types,
    format_func=lambda x: x.title(),
)

# Main chat interface
st.title("🎧 AudioCaster")
st.write("Tell me what you'd like to listen to, and I'll create an audiocast for you!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if not st.session_state.messages:
    with st.container():
        if not st.session_state.seleted_example:
            display_example_cards()

if st.session_state.seleted_example:
    handle_selected_example(content_type)


# Chat input for custom prompts
if prompt := st.chat_input("What would you like to listen to?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response_generator = chat(
                st.session_state.chat_session_id,
                SessionChatRequest(
                    message=ChatMessage(role="user", content=prompt),
                    content_type=content_type,
                ),
            )

        ai_message = st.write_stream(response_generator)

        if ai_message:
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_message}
            )

        # Show generate button if enough context
        if len(st.session_state.messages) >= 2:
            if st.button("Generate Audiocast"):
                with st.spinner("Generating your audiocast..."):
                    # Generate audiocast
                    audiocast_response = httpx.post(
                        f"{BACKEND_URL}/api/generate-audiocast",
                        json={
                            "query": prompt,
                            "type": content_type,
                            "chat_history": st.session_state.messages,
                        },
                    )

                    if audiocast_response.status_code == 200:
                        st.session_state.current_audiocast = audiocast_response.json()
                        st.rerun()

# Display current audiocast if available
if st.session_state.current_audiocast:
    st.header("Your Audiocast")

    # Audio player
    st.audio(st.session_state.current_audiocast["audio_url"])

    # Transcript
    with st.expander("Show Transcript"):
        st.write(st.session_state.current_audiocast["transcript"])

    # Metadata
    st.sidebar.subheader("Audiocast Info")
    st.sidebar.json(st.session_state.current_audiocast["metadata"])

    # Share button
    share_url = f"{APP_URL}/audiocast/{st.session_state.current_audiocast['uuid']}/{st.session_state.current_audiocast['slug']}"
    st.sidebar.text_input("Share this audiocast:", share_url)
