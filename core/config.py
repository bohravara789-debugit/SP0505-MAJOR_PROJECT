import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def get_google_api_key():
    if "GOOGLE_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_API_KEY"]
    return os.getenv("GOOGLE_API_KEY")
