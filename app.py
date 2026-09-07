import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="SRI MANIKANTA TRADERS",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS for Professional Layout
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .brand-title {
        font-size: 38px;
        font-weight: bold;
        color: #1b4d3e;
    }
    .brand-subtitle {
        font-size: 16px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Check Authentication Status
if not st.session_state["authenticated"]:
    # Split Screen Login Layout
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<p class="brand-title">🌾 SRI MANIKANTA TRADERS</p>', unsafe_allow_html=True)
        st.markdown('<p class="brand-subtitle">Advanced Inventory & Billing Management System<br>D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal</p>', unsafe_allow_html=True)
        st.info("💡 Secure access for authorized personnel only. Please sign in with your credentials to manage stock and generate bills.")

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.markdown("### 🔐 LOGIN")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Sign In", use_container_width=True):
                if username == "admin" and password == "samsri2528":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password")
else:
    # Main Application After Successful Login
    st.sidebar.title("Navigation")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
        
    st.title("🌾 SRI MANIKANTA TRADERS - Dashboard")
    st.write("D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343")
    st.markdown("---")
    
    # Billing & Inventory Section
    st.markdown("### 🧾 Sales Invoice & Billing Grid")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        bill_no = st.text_input("Bill No", value="SMT-001")
    with col_b2:
        bill_date = st.date_input("Date", value=datetime.now())
    with col_b3:
        mobile_no = st.text_input("Mobile No (10 Digits)", max_chars=10)
        
    cust_name = st.text_input("Customer / Farmer Name")

    st.markdown("### 📦 Item Selection & Stock Grid")
    
    # Item row input
    col_item1, col_item2, col_item3 = st.columns(3)
    with col_item1:
        item_name = st.selectbox("Select Product", ["Pesticides", "Seeds", "Fertilizers", "Animal Feed", "Fungicide"])
    with col_item2:
        qty = st.number_input("Quantity", min_value=1.0, value=1.0)
    with col_item3:
        price = st.number_input("Price per Unit (₹)", min_value=0.0, value=500.0)
        
    total_amount = qty * price
    st.info(f"**Total Calculated Amount: ₹ {total_amount:.2f}**")

    if st.button("Save & Generate Bill", use_container_width=True):
        if cust_name:
            st.success(f"✅ Bill saved successfully for {cust_name}! Total Amount: ₹ {total_amount:.2f}")
        else:
            st.warning("⚠️ Please enter the Customer / Farmer Name before generating the bill.")
