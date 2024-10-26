import streamlit as st
from chat_utils import chat_request, content_examples


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
                # Add selected example to messages and trigger rerun to enter chat mode
                st.session_state.messages.append({"role": "user", "content": example})

                response_generator = chat_request(example, content_type)

                ai_message = st.write_stream(response_generator)
                if ai_message:
                    st.session_state.messages.append(
                        {"role": "assistant", "content": ai_message}
                    )

                    st.rerun()
                else:
                    st.error("Failed to generate AI response. Please try again.")
