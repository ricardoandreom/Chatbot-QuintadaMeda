import os
import streamlit as st
from dotenv import load_dotenv

# Load variables do .env
load_dotenv()
# api_key from secrets
api_key = st.secrets["openai"]["api_key"]
