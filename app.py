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

# Files for Data Storage
INVENTORY_FILE = "inventory.xlsx"
SALES_FILE = "sales_history.xlsx"

# Initialize Inventory File if not exists
def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        return pd.read_excel(INVENTORY_FILE)
    else:
        df = pd.DataFrame(columns=["Item Name", "Category", "Quantity", "Price (₹)"])
        df.to_excel(INVENTORY_FILE, index=False)
        return df

# Save Inventory
def save_inventory(df):
    df.to_excel(INVENTORY_FILE, index=False)

# Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Check Authentication Status
if not st.session_state["authenticated"]:
    # Split Screen Login Layout
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:38px; font-weight:bold; color:#1b4d3e;">🌾 SRI MANIKANTA TRADERS</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:16px; color:#555;">Advanced Inventory & Billing Management System<br>D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal</p>', unsafe_allow_html=True)
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
    # Sidebar Navigation
    st.sidebar.title("🌾 SRI MANIKANTA TRADERS")
    menu = st.sidebar.radio("Navigation", ["Billing & Sales", "Manage Inventory"])
    
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
        
    inventory_df = load_inventory()

    if menu == "Manage Inventory":
        st.title("📦 Inventory & Stock Management")
        st.write("Add new products, seeds, fertilizers, or pesticides along with their prices.")
        
        with st.form("add_item_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_item = st.text_input("Product / Item Name")
                new_category = st.selectbox("Category", ["Seeds", "Fertilizers", "Pesticides", "Animal Feed", "Others"])
            with col2:
                new_qty = st.number_input("Initial Quantity / Stock", min_value=0.0, value=10.0)
                new_price = st.number_input("Price per Unit (₹)", min_value=0.0, value=100.0)
                
            submit_item = st.form_submit_button("Add Item to Inventory")
            
            if submit_item:
                if new_item:
                    new_row = pd.DataFrame([[new_item, new_category, new_qty, new_price]], columns=["Item Name", "Category", "Quantity", "Price (₹)"])
                    inventory_df = pd.concat([inventory_df, new_row], ignore_index=True)
                    save_inventory(inventory_df)
                    st.success(f"✅ Successfully added '{new_item}' to inventory!")
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter the item name.")

        st.markdown("### 📋 Current Stock List")
        if not inventory_df.empty:
            st.dataframe(inventory_df, use_container_width=True)
        else:
            st.info("No items added yet. Use the form above to add products.")

    elif menu == "Billing & Sales":
        st.title("🧾 Sales Invoice & Billing Grid")
        st.write("D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343")
        st.markdown("---")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            bill_no = st.text_input("Bill No", value="SMT-001")
        with col_b2:
            bill_date = st.date_input("Date", value=datetime.now())
        with col_b3:
            mobile_no = st.text_input("Mobile No (10 Digits)", max_chars=10)
            
        cust_name = st.text_input("Customer / Farmer Name")

        st.markdown("### 🛒 Item Selection & Billing")
        
        if inventory_df.empty:
            st.warning("⚠️ No items found in inventory! Please go to 'Manage Inventory' from the sidebar and add products first.")
        else:
            item_list = inventory_df["Item Name"].tolist()
            
            col_item1, col_item2, col_item3 = st.columns(3)
            with col_item1:
                selected_item = st.selectbox("Select Product", item_list)
            
            # Fetch default price based on selection
            default_price = float(inventory_df.loc[inventory_df["Item Name"] == selected_item, "Price (₹)"].values[0])
            
            with col_item2:
                qty = st.number_input("Quantity", min_value=1.0, value=1.0)
            with col_item3:
                price = st.number_input("Price per Unit (₹)", min_value=0.0, value=default_price)
                
            total_amount = qty * price
            st.info(f"**Total Calculated Amount: ₹ {total_amount:.2f}**")

            if st.button("Save & Generate Bill", use_container_width=True):
                if cust_name:
                    st.success(f"✅ Bill generated successfully for {cust_name}! Total Amount: ₹ {total_amount:.2f}")
                else:
                    st.warning("⚠️ Please enter the Customer / Farmer Name before generating the bill.")
