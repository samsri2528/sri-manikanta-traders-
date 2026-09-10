import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="SRI MANIKANTA TRADERS", page_icon="🛒", layout="wide"
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

st.title("Sri Manikanta Traders - Billing & Inventory System")

# గూగుల్ షీట్ లింక్
SHEET_URL = "https://docs.google.com/spreadsheets/d/1aHHApE3alu_NYigh343N_FSoza0wEWkJooZUmH-HuM/edit?gid=82672227#gid=82672227"

tab1, tab2, tab3 = st.tabs(["📦 Inventory", "🛒 Sales", "📖 CashBook"])

with tab1:
  st.subheader("Inventory Management")
  st.write("ఇక్కడ మీ స్టాక్ వివరాలు కనిపిస్తాయి.")

with tab2:
  st.subheader("Sales & Billing")
  st.write("ఇక్కడ బిల్లింగ్ చేసుకోవచ్చు.")

with tab3:
  st.subheader("Cash Book")
  st.write("ఇక్కడ క్యాష్ లెక్కలు చూసుకోవచ్చు.")
