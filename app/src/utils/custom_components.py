from streamlit.components.v1 import html


def copy_button(text: str, label: str = "Copy"):
    """
    Copy button custom component
    """
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
