import streamlit as st

from utils_pkg.chat_utils import content_examples


def display_example_cards():
    """Display example content cards if there are no messages"""
    st.markdown("##### You can start with one of the following")

    # CSS for fixed-height buttons and responsive columns
    st.markdown(
        """
        <style>
            .stButton button {
                height: 125px;
                white-space: normal;
                word-wrap: break-word;
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
    for content_category, example in content_examples.items():
        with col1 if content_category in [
            "podcast",
            "soundbite",
            "sermon",
            "audiodrama",
        ] else col2:
            if st.button(example, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": example})
                st.session_state.example_prompt = example
                st.session_state.content_category = content_category

                st.rerun()
