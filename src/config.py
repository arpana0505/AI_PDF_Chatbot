from dotenv import load_dotenv
import os

# load local .env file
load_dotenv()

# trying to get the API key from the local environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if not found, try streamlit secrets
if not OPENAI_API_KEY:
    try:
        import streamlit as st
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

# if neither location contains the key, raise an error
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY was not found. "
        "Add it to your .env file locally or Streamlit Secrets when deployed."
    )