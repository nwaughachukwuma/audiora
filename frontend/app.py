import uuid

import httpx
import streamlit as st
from env_var import APP_URL, BACKEND_URL
from example_utils import content_types, display_example_cards

# Initialize session state
if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_audiocast" not in st.session_state:
    st.session_state.current_audiocast = None

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

# Display example content cards if there are no messages
if not st.session_state.messages:
    display_example_cards()

# Chat input for custom prompts
if prompt := st.chat_input("What would you like to listen to?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Send message to backend
    response = httpx.post(
        f"{BACKEND_URL}/api/chat/{st.session_state.chat_session_id}",
        json={"role": "user", "content": prompt},
    )

    response.raise_for_status()

    if response.status_code == 200:
        ai_message = response.json()
        st.session_state.messages.append(ai_message)

        with st.chat_message("assistant"):
            st.write(ai_message["content"])

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
                            st.session_state.current_audiocast = (
                                audiocast_response.json()
                            )
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
