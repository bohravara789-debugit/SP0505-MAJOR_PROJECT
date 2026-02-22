import streamlit as st
import os

def get_google_api_keys():
    """
    Retrieves a list of Google API keys from Streamlit secrets or environment variables.
    Supports GOOGLE_API_KEY and GOOGLE_API_KEY_1, GOOGLE_API_KEY_2, etc.
    """
    keys = []
    
    # Helper to safely get from secrets or env
    def get_key(name):
        if name in st.secrets:
            return st.secrets[name]
        return os.getenv(name)

    # 1. Check for standard key
    key = get_key("GOOGLE_API_KEY")
    if key:
        keys.append(key)

    # 2. Check for numbered keys (GOOGLE_API_KEY_1, GOOGLE_API_KEY_2...)
    i = 1
    while True:
        key_name = f"GOOGLE_API_KEY_{i}"
        key = get_key(key_name)
        if key:
            keys.append(key)
            i += 1
        else:
            break
            
    return keys
