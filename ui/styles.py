import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7fa;
        }
        h1 {
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
