import streamlit as st


def render_footer():
    st.markdown(
        """
        <style>
        .footer {
            position: absolute;
            bottom: 0;
            text-align: center;
            padding: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        """
        <div class="footer">
            <p> a <a href="https://veedo.ai">veedoai</a> project. (c) 2024 </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
