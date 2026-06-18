import os

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

api_key = None

try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

# ── FIX: don't raise at import time; let the app start and show a clear error ──
model = None
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
