import streamlit as st

from src.utils.chat_utils import content_types


def set_content_type():
    with st.chat_message("ai"):
        st.write("Select a content type to start the conversation.")

    def on_value_change():
        content_type = st.session_state.selected_content_type

        if content_type:
            content = f"You want to listen to an audiocast of type: {content_type.capitalize()}"
            st.session_state.messages.append({"role": "human", "content": content})
            st.session_state.content_type = content_type

            st.rerun()

    with st.container():
        st.selectbox(
            "Select Content Type",
            content_types,
            format_func=lambda x: x.title(),
            key="selected_content_type",
            on_change=on_value_change,
        )


def render_chat_history():
    """
    Render chat history
    """
    st.info("Chat Session")

    with st.chat_message("user"):
        message = st.session_state.messages[0]
        st.write(message["content"])

    if not st.session_state.content_type:
        set_content_type()
    else:
        # Display chat history
        for message in st.session_state.messages[1:]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
