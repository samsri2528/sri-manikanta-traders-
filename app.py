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

# Custom Styles
st.markdown("""
<style>
    .stApp { background-color: #fdfbf7; }
    .stButton>button { background-color: #8b0000; color: white; border-radius: 6px; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #5c0000; color: white; }
    @media print {
        body * { visibility: hidden; }
        .printable-bill, .printable-bill * { visibility: visible; }
        .printable-bill { position: absolute; left: 0; top: 0; width: 100%; }
        .stSidebar, header, footer, .no-print { display: none !important; }
    }
</style>
""", unsafe_allow_html=True)

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
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fffef9 0%, #f4ebd0 100%); border: 3px solid #8b0000; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 25px;">
        <div style="font-size: 55px; color: #b8860b; margin-bottom: -5px;">🕉️</div>
        <h1 style="color: #8b0000; font-family: 'Georgia', serif; font-size: 44px; font-weight: bold; margin: 10px 0 0 0;">SRI MANIKANTA TRADERS</h1>
        <h2 style="color: #004d1a; font-family: 'Georgia', serif; font-size: 28px; font-weight: bold; margin: 0 0 10px 0;">TRADERS</h2>
        <hr style="border: 0; height: 1px; background: #b8860b; width: 60%; margin: 15px auto;">
        <p style="color: #444; font-size: 15px; font-weight: 500; margin: 0;">D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🙏 Welcome to Sri Manikanta Traders")
        st.write("Manage inventory, sales, and digital billing seamlessly.")
    with col2:
        with st.container():
            st.markdown("### 🔐 ADMIN LOGIN")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
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
                    st.session_state["last_bill"] = {
                        "bill_no": bill_no,
                        "date": str(bill_date),
                        "cust_name": cust_name,
                        "mobile": mobile_no,
                        "item": selected_item,
                        "qty": qty,
                        "price": price,
                        "total": total_amount
                    }
                    st.success(f"✅ Bill Generated Successfully for {cust_name}! Total: ₹ {total_amount:.2f}")
                else:
                    st.warning("⚠️ Please enter Customer Name.")

        # Display Bill Copies cleanly using structured containers
        if "last_bill" in st.session_state:
            b = st.session_state["last_bill"]
            st.markdown("---")
            st.markdown("### 🖨️ Bill Ready for Print")
            st.info("💡 కీబోర్డ్ మీద **Ctrl + P** నొక్కి ప్రింట్ చేయండి. రైతు కాపీ మరియు స్టోర్ కాపీ రెండూ కనిపిస్తాయి!")
            
            # Printable Container Start
            st.markdown('<div class="printable-bill">', unsafe_allow_html=True)
            
            # --- FARMER COPY ---
            with st.container():
                st.markdown("""
                <div style="border: 2px solid #8b0000; padding: 12px; border-radius: 6px; background: white; margin-bottom: 10px;">
                    <h3 style="text-align: center; color: #8b0000; margin: 0;">🕉️ SRI MANIKANTA TRADERS</h3>
                    <p style="text-align: center; font-size: 11px; margin: 2px 0; color: black;">D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
                    <p style="text-align: center; font-weight: bold; background: #fdfbf7; color: #8b0000; margin: 5px 0; padding: 3px; font-size: 12px; border: 1px solid #b8860b;">FARMER COPY</p>
                """, unsafe_allow_html=True)
                
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    st.markdown(f"**Bill No:** {b['bill_no']}")
                    st.markdown(f"**Customer:** {b['cust_name']}")
                with col_f2:
                    st.markdown(f"**Date:** {b['date']}")
                    st.markdown(f"**Mobile:** {b['mobile']}")
                
                bill_item_df = pd.DataFrame([{
                    "Item Name": b['item'],
                    "Qty": b['qty'],
                    "Price (₹)": b['price'],
                    "Total (₹)": b['total']
                }])
                st.dataframe(bill_item_df, use_container_width=True, hide_index=True)
                st.markdown(f"<h4 style='text-align: right; color: #8b0000;'>Grand Total: ₹ {b['total']:.2f}</h4>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-size: 10px; color: black;'>Thank you! Visit Again. 🌾</p></div>", unsafe_allow_html=True)

            # Divider line between copies
            st.markdown("<div style='border-bottom: 2px dashed #999; margin: 15px 0; text-align: center; font-size: 12px; color: #666;'>✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ✂</div>", unsafe_allow_html=True)

            # --- STORE COPY ---
            with st.container():
                st.markdown("""
                <div style="border: 2px solid #333; padding: 12px; border-radius: 6px; background: white;">
                    <h3 style="text-align: center; color: #333; margin: 0;">SRI MANIKANTA TRADERS</h3>
                    <p style="text-align: center; font-size: 11px; margin: 2px 0; color: black;">D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
                    <p style="text-align: center; font-weight: bold; background: #e2e8f0; color: #333; margin: 5px 0; padding: 3px; font-size: 12px;">STORE COPY</p>
                """, unsafe_allow_html=True)
                
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.markdown(f"**Bill No:** {b['bill_no']}")
                    st.markdown(f"**Customer:** {b['cust_name']}")
                with col_s2:
                    st.markdown(f"**Date:** {b['date']}")
                    st.markdown(f"**Mobile:** {b['mobile']}")
                
                st.dataframe(bill_item_df, use_container_width=True, hide_index=True)
                st.markdown(f"<h4 style='text-align: right; color: #333;'>Grand Total: ₹ {b['total']:.2f}</h4>", unsafe_allow_html=True)
                st.markdown("<p style='text-align: center; font-size: 10px; color: black;'>Store Office Copy</p></div>", unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            # Printable Container End

    elif menu == "Sales History & Reports":
        st.title("📊 Total Bills & Category Sales Report")
        if not sales_df.empty:
            st.markdown("### 📋 All Bills History")
            st.dataframe(sales_df, use_container_width=True)
            st.markdown("### 📈 Category-wise Sales Summary")
            merged_df = pd.merge(sales_df, inventory_df[["Item Name", "Category"]], on="Item Name", how="left")
            category_summary = merged_df.groupby("Category")["Total Amount"].sum().reset_index()
            st.dataframe(category_summary, use_container_width=True)

    elif menu == "Cash Book":
        st.title("📒 Cash Book & Daily Ledger")
        if not sales_df.empty:
            total_revenue = sales_df["Total Amount"].sum()
            st.metric(label="💵 Total Cash Collected (Revenue)", value=f"₹ {total_revenue:.2f}")
            st.markdown("### 💰 Transaction Ledger")
            st.dataframe(sales_df[["Date", "Bill No", "Customer Name", "Total Amount"]], use_container_width=True)
