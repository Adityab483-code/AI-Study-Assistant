import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = (
    st.secrets.get("GEMINI_API_KEY")
    if hasattr(st, "secrets")
    and "GEMINI_API_KEY" in st.secrets
    else os.getenv("GEMINI_API_KEY")
)

if not api_key:
    raise ValueError(
        "Gemini API key not found."
    )

genai.configure(
    api_key=api_key
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)