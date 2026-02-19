import streamlit as st

def render_sidebar():
    st.sidebar.header("🧭 Navigation")

    page = st.sidebar.radio(
        "Main Menu",
        ["Home", "Chat"],
        label_visibility="collapsed"
    )

    return page
