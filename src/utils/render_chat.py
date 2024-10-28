import streamlit as st

from src.utils.chat_utils import audiocast_categories


def set_content_category():
    with st.chat_message("ai"):
        st.write("Select a content type to start the conversation.")

    def on_value_change():
        content_category = st.session_state.selected_content_category

        if content_category:
            content = f"You want to listen to an audiocast of type: {content_category.capitalize()}"
            st.session_state.messages.append({"role": "human", "content": content})
            st.session_state.content_category = content_category

            st.rerun()

    with st.container():
        st.selectbox(
            "Select Content Type",
            audiocast_categories,
            format_func=lambda x: x.title(),
            key="selected_content_category",
            on_change=on_value_change,
        )


def render_chat_history():
    """
    Render chat history
    """
    st.info("Chat session to understand your content preferences")

    with st.chat_message("user"):
        message = st.session_state.messages[0]
        st.write(message["content"])

    if not st.session_state.content_category:
        set_content_category()
    else:
        # Display chat history
        for message in st.session_state.messages[1:]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
