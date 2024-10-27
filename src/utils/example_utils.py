import streamlit as st

from src.utils.chat_response import generate_stream_response
from src.utils.chat_utils import (
    ContentType,
    content_examples,
)


def display_example_cards():
    """Display example content cards if there are no messages"""
    st.subheader("Examples")
    st.markdown("**Click on an example to generate an audiocast.**")

    # CSS for fixed-height buttons and responsive columns
    st.markdown(
        """
        <style>
            .stButton button {
                height: 125px;
                white-space: normal;
                word-wrap: break-word;
                color: #030712
            }
            @media (max-width: 960px) {
                div[data-testid="stColumn"] {
                    width: 100% !important;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display example content cards
    col1, col2 = st.columns(2)
    for content_type, example in content_examples.items():
        with col1 if content_type in ["story", "podcast"] else col2:
            if st.button(example, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": example})
                st.session_state.seleted_example = example

                st.rerun()


def handle_selected_example(content_type: ContentType):
    """Handle selected example prompt"""
    prompt = st.session_state.seleted_example

    with st.chat_message("assistant"):
        response_generator = generate_stream_response(prompt, content_type)
        ai_message = st.write_stream(response_generator)
        st.session_state.seleted_example = None

        if ai_message:
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_message}
            )
            st.rerun()
        else:
            st.error("Failed to generate AI response. Please try again.")
