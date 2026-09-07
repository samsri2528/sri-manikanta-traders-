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

# Data Files
INVENTORY_FILE = "inventory.xlsx"
SALES_FILE = "sales_history.xlsx"

def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        return pd.read_excel(INVENTORY_FILE)
    else:
        df = pd.DataFrame(columns=["Item Name", "Category", "Quantity", "Price (₹)"])
        df.to_excel(INVENTORY_FILE, index=False)
        return df

def save_inventory(df):
    df.to_excel(INVENTORY_FILE, index=False)

def load_sales():
    if os.path.exists(SALES_FILE):
        return pd.read_excel(SALES_FILE)
    else:
        df = pd.DataFrame(columns=["Bill No", "Date", "Customer Name", "Mobile", "Item Name", "Quantity", "Price", "Total Amount"])
        df.to_excel(SALES_FILE, index=False)
        return df

def save_sales(df):
    df.to_excel(SALES_FILE, index=False)

# Session State Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:38px; font-weight:bold; color:#1b4d3e;">🌾 SRI MANIKANTA TRADERS</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:16px; color:#555;">Advanced Inventory & Billing Management System<br>D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal</p>', unsafe_allow_html=True)
        st.info("💡 Secure access for authorized personnel only. Please sign in with your credentials.")
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
    st.sidebar.title("🌾 SRI MANIKANTA TRADERS")
    menu = st.sidebar.radio("Navigation", ["Billing & Sales", "Manage Inventory", "Sales History & Reports", "Cash Book"])
    
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
        
    inventory_df = load_inventory()
    sales_df = load_sales()

    if menu == "Manage Inventory":
        st.title("📦 Inventory & Stock Management")
        with st.form("add_item_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_item = st.text_input("Product / Item Name")
                new_category = st.selectbox("Category", ["Seeds", "Fertilizers", "Pesticides", "Animal Feed", "Others"])
            with col2:
                new_qty = st.number_input("Initial Quantity", min_value=0.0, value=10.0)
                new_price = st.number_input("Price per Unit (₹)", min_value=0.0, value=100.0)
            if st.form_submit_button("Add Item to Inventory"):
                if new_item:
                    new_row = pd.DataFrame([[new_item, new_category, new_qty, new_price]], columns=["Item Name", "Category", "Quantity", "Price (₹)"])
                    inventory_df = pd.concat([inventory_df, new_row], ignore_index=True)
                    save_inventory(inventory_df)
                    st.success(f"✅ Added '{new_item}' successfully!")
                    st.rerun()
                else:
                    st.warning("⚠️ Enter item name.")

        st.markdown("### 📋 Current Stock List")
        if not inventory_df.empty:
            st.dataframe(inventory_df, use_container_width=True)

    elif menu == "Billing & Sales":
        st.title("🧾 Sales Invoice & Billing")
        st.write("D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343")
        st.markdown("---")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            next_bill_no = f"SMT-{len(sales_df)+1:03d}"
            bill_no = st.text_input("Bill No", value=next_bill_no)
        with col_b2:
            bill_date = st.date_input("Date", value=datetime.now())
        with col_b3:
            mobile_no = st.text_input("Mobile No (10 Digits)", max_chars=10)
            
        cust_name = st.text_input("Customer / Farmer Name")

        st.markdown("### 🛒 Item Selection")
        if inventory_df.empty:
            st.warning("⚠️ Please add items in 'Manage Inventory' first!")
        else:
            item_list = inventory_df["Item Name"].tolist()
            col_item1, col_item2, col_item3 = st.columns(3)
            with col_item1:
                selected_item = st.selectbox("Select Product", item_list)
            
            default_price = float(inventory_df.loc[inventory_df["Item Name"] == selected_item, "Price (₹)"].values[0])
            
            with col_item2:
                qty = st.number_input("Quantity", min_value=1.0, value=1.0)
            with col_item3:
                price = st.number_input("Price per Unit (₹)", min_value=0.0, value=default_price)
                
            total_amount = qty * price
            st.info(f"**Total Calculated Amount: ₹ {total_amount:.2f}**")

            if st.button("Save & Generate Bill", use_container_width=True):
                if cust_name:
                    new_sale = pd.DataFrame([[bill_no, str(bill_date), cust_name, mobile_no, selected_item, qty, price, total_amount]], 
                                            columns=["Bill No", "Date", "Customer Name", "Mobile", "Item Name", "Quantity", "Price", "Total Amount"])
                    sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
                    save_sales(sales_df)
                    st.success(f"✅ Bill Generated Successfully for {cust_name}! Total: ₹ {total_amount:.2f}")
                    
                    # Printable Bill Format Preview
                    st.markdown("---")
                    st.markdown("### 📄 Print / Download Invoice Preview")
                    st.markdown(f"""
                    <div style="border: 2px solid #1b4d3e; padding: 20px; border-radius: 10px; background: white; color: black;">
                        <h2 style="text-align: center; color: #1b4d3e;">SRI MANIKANTA TRADERS</h2>
                        <p style="text-align: center;">D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
                        <hr>
                        <p><b>Bill No:</b> {bill_no} &nbsp;&nbsp;&nbsp;&nbsp; <b>Date:</b> {bill_date}</p>
                        <p><b>Customer Name:</b> {cust_name} &nbsp;&nbsp;&nbsp;&nbsp; <b>Mobile:</b> {mobile_no}</p>
                        <hr>
                        <table width="100%" style="border-collapse: collapse;">
                            <tr><th>Item</th><th>Qty</th><th>Price</th><th>Total</th></tr>
                            <tr><td>{selected_item}</td><td>{qty}</td><td>₹{price}</td><td>₹{total_amount}</td></tr>
                        </table>
                        <hr>
                        <h3 style="text-align: right;">Grand Total: ₹ {total_amount:.2f}</h3>
                        <p style="text-align: center; color: #555;">Thank you! Visit Again.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("💡 Tip: You can press **Ctrl + P** on your keyboard to print this bill directly or save as PDF!")
                else:
                    st.warning("⚠️ Please enter Customer Name.")

    elif menu == "Sales History & Reports":
        st.title("📊 Total Bills & Category Sales Report")
        
        if sales_df.empty:
            st.info("No sales records found yet.")
        else:
            st.markdown("### 📋 All Bills History")
            st.dataframe(sales_df, use_container_width=True)
            
            st.markdown("### 📈 Category-wise Sales Summary")
            # Merge with inventory to get categories
            merged_df = pd.merge(sales_df, inventory_df[["Item Name", "Category"]], on="Item Name", how="left")
            category_summary = merged_df.groupby("Category")["Total Amount"].sum().reset_index()
            st.dataframe(category_summary, use_container_width=True)

    elif menu == "Cash Book":
        st.title("📒 Cash Book & Daily Ledger")
        if sales_df.empty:
            st.info("No cash transactions recorded yet.")
        else:
            total_revenue = sales_df["Total Amount"].sum()
            st.metric(label="💵 Total Cash Collected (Revenue)", value=f"₹ {total_revenue:.2f}")
            st.markdown("### 💰 Transaction Ledger")
            st.dataframe(sales_df[["Date", "Bill No", "Customer Name", "Total Amount"]], use_container_width=True)
