import streamlit as st
from streamlit.components.v1 import html

from src.utils.render_audiocast_utils import navigate_to_home


def audiocast_actions(text: str, label: str = "Copy"):
    """
    Action buttons using a hybrid approach - HTML for copy, Streamlit for navigation
    """
    col1, col2 = st.columns(2, vertical_alignment="center")

    with col1:
        # Copy button in HTML
        html(
            f"""
            <style>
                .custom-button {{
                    background: rgb(19, 23, 32);
                    color: #ffffff;
                    padding: 12px 24px;
                    border: 1px solid rgba(250, 250, 250, 0.2);
                    border-radius: 8px;
                    cursor: pointer;
                    font-family: system-ui, -apple-system;
                    width: 100%;
                    height: 100%;
                    font-size: 14px;
                    transition: all 0.2s ease;
                    display: inline-block;
                }}
                .custom-button:hover {{
                    border-color: #34d399;
                }}
            </style>
             <script>
                function copyToClipboard(text) {{
                    navigator.clipboard.writeText(text).then(function() {{
                        alert('Copied to clipboard!');
                    }}, function(err) {{
                        alert('Could not copy text: ', err);
                    }});
                }}
            </script>
            <button
                onclick="copyToClipboard(`{text}`)"
                class="custom-button"
                onmouseover="this.style.background='#2a2a2a'"
                onmouseout="this.style.background='rgb(19, 23, 32)'"
            >{label}</button>
            """,
            height=51,
        )

    with col2:
        if st.button("Create your Audiocast", key="create_audiocast", use_container_width=True):
            navigate_to_home()
