import io
import os
from datetime import datetime
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="SRI MANIKANTA TRADERS", page_icon="📈", layout="wide"
)

# Custom Styles
st.markdown(
    """
<style>
.stApp { background-color: #fdfbf7; }
.stButton>button { background-color: #8b0000; color: white; border-radius: 6px; font-weight: bold; border: none; }
.stButton>button:hover { background-color: #5c0000; color: white; }
</style>
""",
    unsafe_allow_html=True,
)
