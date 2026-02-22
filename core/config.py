import streamlit as st

def get_google_api_key():
    return st.secrets["GOOGLE_API_KEY"]
