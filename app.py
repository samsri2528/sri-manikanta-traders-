import streamlit as st
import pandas as pd
import os
from datetime import datetime
import streamlit.components.v1 as components

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
</style>
""", unsafe_allow_html=True)

# Data Files
INVENTORY_FILE = "inventory.xlsx"
SALES_FILE = "sales_history.xlsx"
CASH_BOOK_FILE = "cash_book_deposits.xlsx"
EXPENSES_FILE = "expenses.xlsx"

def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        return pd.read_excel(INVENTORY_FILE)
    else:
        df = pd.DataFrame(columns=["Item Name", "Category", "Quantity", "Price (₹)", "Invoice Receipt"])
        df.to_excel(INVENTORY_FILE, index=False)
        return df

def save_inventory(df):
    df.to_excel(INVENTORY_FILE, index=False)

def load_sales():
    if os.path.exists(SALES_FILE):
        df = pd.read_excel(SALES_FILE)
        if not df.empty and "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime('%d-%m-%Y').fillna(df["Date"])
        if "Aadhaar No" not in df.columns:
            df["Aadhaar No"] = ""
        return df
    else:
        df = pd.DataFrame(columns=["Bill No", "Date", "Customer Name", "Village", "Mobile", "Aadhaar No", "Item Name", "Quantity", "Price", "Total Amount"])
        df.to_excel(SALES_FILE, index=False)
        return df

def save_sales(df):
    df.to_excel(SALES_FILE, index=False)

def load_cash_deposits():
    if os.path.exists(CASH_BOOK_FILE):
        df = pd.read_excel(CASH_BOOK_FILE)
        if "Receipt Name" not in df.columns:
            df["Receipt Name"] = "No Receipt"
        if "Status" not in df.columns:
            df["Status"] = "Approved"
        if not df.empty and "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime('%d-%m-%Y').fillna(df["Date"])
        df.to_excel(CASH_BOOK_FILE, index=False)
        return df
    else:
        df = pd.DataFrame(columns=["Date", "Description", "Deposit Amount (₹)", "Receipt Name", "Status"])
        df.to_excel(CASH_BOOK_FILE, index=False)
        return df

def save_cash_deposits(df):
    df.to_excel(CASH_BOOK_FILE, index=False)

def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        df = pd.read_excel(EXPENSES_FILE)
        if "Receipt Name" not in df.columns:
            df["Receipt Name"] = "No Receipt"
        if "Status" not in df.columns:
            df["Status"] = "Approved"
        if not df.empty and "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime('%d-%m-%Y').fillna(df["Date"])
        df.to_excel(EXPENSES_FILE, index=False)
        return df
    else:
        df = pd.DataFrame(columns=["Date", "Expense Name", "Amount (₹)", "Receipt Name", "Status"])
        df.to_excel(EXPENSES_FILE, index=False)
        return df

def save_expenses(df):
    df.to_excel(EXPENSES_FILE, index=False)

# Session State Authentication & Cart
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "role" not in st.session_state:
    st.session_state["role"] = "Admin"

if "cart" not in st.session_state:
    st.session_state["cart"] = []

if not st.session_state["authenticated"]:
    if os.path.exists("banner.png"):
        st.image("banner.png", use_container_width=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fffef9 0%, #f4ebd0 100%); border: 3px solid #8b0000; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 25px;">
            <div style="font-size: 55px; color: #b8860b; margin-bottom: -5px;">🕉️</div>
            <h1 style="color: #8b0000; font-family: 'Georgia', serif; font-size: 44px; font-weight: bold; margin: 10px 0 0 0;">SRI MANIKANTA TRADERS</h1>
            <hr style="border: 0; height: 1px; background: #b8860b; width: 60%; margin: 15px auto;">
            <p style="color: #444; font-size: 15px; font-weight: 500; margin: 0;">D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🙏 Welcome to Sri Manikanta Traders")
        st.write("Manage inventory, sales, staff entries, and digital billing seamlessly.")
    with col2:
        with st.container():
            st.markdown("### 🔐 LOGIN PORTAL")
            login_option = st.selectbox("Select Role", ["Admin (Owner)", "Staff / Billing Operator"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Sign In", use_container_width=True):
                if login_option == "Admin (Owner)":
                    if username == "admin" and password == "samsri2528":
                        st.session_state["authenticated"] = True
                        st.session_state["role"] = "Admin"
                        st.rerun()
                    else:
                        st.error("❌ Invalid Admin Username or Password")
                else:
                    if username == "manikanta" and password == "samsri2528":
                        st.session_state["authenticated"] = True
                        st.session_state["role"] = "Staff"
                        st.rerun()
                    else:
                        st.error("❌ Invalid Staff Username or Password")
else:
    st.sidebar.title("🌾 SRI MANIKANTA TRADERS")
    st.sidebar.markdown(f"**Logged in as:** `{st.session_state['role']}`")
    
    # Dynamic Navigation based on Role
    if st.session_state["role"] == "Admin":
        menu = st.sidebar.radio("Navigation", ["Manage Inventory", "Cash Book & Expenses"])
    else:
        menu = st.sidebar.radio("Navigation", ["Billing & Sales", "Present / Closing Stock", "Sales History & Reports", "Cash Book & Expenses"])
    
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state["cart"] = []
        if "last_bill" in st.session_state:
            del st.session_state["last_bill"]
        st.rerun()
        
    inventory_df = load_inventory()
    sales_df = load_sales()
    cash_df = load_cash_deposits()
    expenses_df = load_expenses()

    # Admin Dashboard Notification Alert
    if st.session_state["role"] == "Admin":
        pend_dep_count = len(cash_df[cash_df["Status"] == "Pending"]) if not cash_df.empty and "Status" in cash_df.columns else 0
        pend_exp_count = len(expenses_df[expenses_df["Status"] == "Pending"]) if not expenses_df.empty and "Status" in expenses_df.columns else 0
        if pend_dep_count > 0 or pend_exp_count > 0:
            st.warning(f"🔔 **Notification:** You have **{pend_dep_count}** pending bank deposit(s) and **{pend_exp_count}** pending expense(s) awaiting your authorization in 'Cash Book & Expenses'.")

    if menu == "Manage Inventory":
        st.title("📦 Inventory & Stock Management (Admin)")
        with st.form("add_item_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_item = st.text_input("Product / Item Name")
                new_category = st.selectbox("Category", ["Seeds", "Fertilizers", "Pesticides", "Animal Feed", "Others"])
                inv_receipt = st.file_uploader("📎 Attach Purchase Invoice / Bill (Image/PDF)", type=["png", "jpg", "jpeg", "pdf"])
            with col2:
                new_qty = st.number_input("Initial Quantity", min_value=0.0, value=10.0)
                new_price = st.number_input("Price per Unit (₹)", min_value=0.0, value=100.0)
            
            if st.form_submit_button("Add Item to Inventory"):
                if new_item:
                    receipt_filename = "No Invoice"
                    if inv_receipt is not None:
                        receipt_filename = inv_receipt.name
                        os.makedirs("receipts", exist_ok=True)
                        with open(os.path.join("receipts", inv_receipt.name), "wb") as f:
                            f.write(inv_receipt.getbuffer())

                    if "Invoice Receipt" not in inventory_df.columns:
                        inventory_df["Invoice Receipt"] = "No Invoice"

                    new_row = pd.DataFrame([[new_item, new_category, new_qty, new_price, receipt_filename]], columns=["Item Name", "Category", "Quantity", "Price (₹)", "Invoice Receipt"])
                    inventory_df = pd.concat([inventory_df, new_row], ignore_index=True)
                    save_inventory(inventory_df)
                    st.success(f"✅ Added '{new_item}' successfully with invoice!")
                    st.rerun()
                else:
                    st.warning("⚠️ Enter item name.")

        st.markdown("### 📋 Current Stock List & Invoices")
        if not inventory_df.empty:
            st.dataframe(inventory_df, use_container_width=True)

    elif menu == "Present / Closing Stock":
        st.title("📊 Present Stock & Closing Stock Report")
        st.write("D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343")
        st.markdown("---")

        if not inventory_df.empty:
            st.markdown("### 📦 Store Closing Stock Details")
            st.dataframe(inventory_df, use_container_width=True)

            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                @st.cache_data
                def convert_df_to_excel(df):
                    from io import BytesIO
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Closing Stock')
                    processed_data = output.getvalue()
                    return processed_data

                excel_data = convert_df_to_excel(inventory_df)
                st.download_button(
                    label="📥 Download Closing Stock as Excel",
                    data=excel_data,
                    file_name=f"closing_stock_{datetime.now().strftime('%d-%m-%Y')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            with col_ex2:
                stock_rows_html = ""
                for _, row in inventory_df.iterrows():
                    stock_rows_html += f"""
                    <tr>
                        <td>{row['Item Name']}</td>
                        <td>{row['Category']}</td>
                        <td class="center">{row['Quantity']}</td>
                        <td class="right">₹{row['Price (₹)']}</td>
                    </tr>
                    """

                stock_print_html = f"""
                <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; background: #fff; margin: 0; padding: 20px; }}
                        .box {{ max-width: 800px; margin: auto; padding: 20px; border: 1px solid #ddd; }}
                        h2 {{ text-align: center; color: #8b0000; margin: 0; }}
                        p {{ text-align: center; font-size: 12px; color: #555; }}
                        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 13px; }}
                        th, td {{ padding: 8px; border: 1px solid #ddd; text-align: left; }}
                        th {{ background: #f1f5f9; color: #333; }}
                        .right {{ text-align: right; }}
                        .center {{ text-align: center; }}
                        .print-btn {{ display: block; width: 100%; background: #8b0000; color: white; padding: 12px; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-bottom: 20px; text-align: center; }}
                        @media print {{ .print-btn {{ display: none; }} body {{ padding: 0; }} }}
                    </style>
                </head>
                <body>
                    <button class="print-btn" onclick="window.print()">🖨️ Click Here to Print / Save as PDF</button>
                    <div class="box">
                        <h2>🕉️ SRI MANIKANTA TRADERS</h2>
                        <p>D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
                        <h3 style="text-align: center; color: #333; margin-bottom: 5px;">Present Closing Stock Report</h3>
                        <p>Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</p>
                        <table>
                            <tr><th>Item Name</th><th>Category</th><th class="center">Quantity</th><th class="right">Price (₹)</th></tr>
                            {stock_rows_html}
                        </table>
                    </div>
                </body>
                </html>
                """
            
            components.html(stock_print_html, height=550, scrolling=True)

        else:
            st.info("No items found in inventory.")

    elif menu == "Billing & Sales":
        st.title("🧾 Sales Invoice & Billing")
        st.write("D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343")
        st.markdown("---")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            next_bill_no = f"SMT-{len(sales_df['Bill No'].unique())+1:03d}" if not sales_df.empty else "SMT-001"
            bill_no = st.text_input("Bill No", value=next_bill_no)
        with col_b2:
            bill_date_str = st.text_input("Date (DD-MM-YYYY)", value=datetime.now().strftime('%d-%m-%Y'))
        with col_b3:
            mobile_no = st.text_input("Mobile No (10 Digits)", max_chars=10)
            
        # Smart Farmer Auto-Fill based on mobile input (supports 4+ digits)
        default_cust_name = ""
        default_village = "Pedda Harivanam"
        default_aadhaar = ""
        
        if mobile_no and len(mobile_no) >= 4 and not sales_df.empty:
            matched_farmers = sales_df[sales_df["Mobile"].astype(str).str.startswith(str(mobile_no))]
            if not matched_farmers.empty:
                unique_farmers = matched_farmers[["Customer Name", "Village", "Mobile", "Aadhaar No"]].drop_duplicates().values.tolist()
                if len(unique_farmers) == 1:
                    default_cust_name = unique_farmers[0][0]
                    default_village = unique_farmers[0][1] if pd.notna(unique_farmers[0][1]) else "Pedda Harivanam"
                    default_aadhaar = str(unique_farmers[0][2]) if pd.notna(unique_farmers[0][2]) else ""
                    if default_aadhaar == "nan": default_aadhaar = ""
                else:
                    st.info(f"💡 Found {len(unique_farmers)} matching farmer(s) in history for prefix `{mobile_no}`")
                    farmer_options = [f"{f[0]} - {f[2]} ({f[1]})" for f in unique_farmers]
                    chosen_farmer = st.selectbox("Select Existing Farmer", farmer_options)
                    for f in unique_farmers:
                        if f"{f[0]} - {f[2]} ({f[1]})" == chosen_farmer:
                            default_cust_name = f[0]
                            default_village = f[1] if pd.notna(f[1]) else "Pedda Harivanam"
                            default_aadhaar = str(f[3]) if pd.notna(f[3]) else ""
                            if default_aadhaar == "nan": default_aadhaar = ""
                            break

        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            cust_name = st.text_input("Customer / Farmer Name", value=default_cust_name)
        with col_c2:
            village_name = st.text_input("Village Name", value=default_village)
        with col_c3:
            aadhaar_no = st.text_input("Aadhaar No (Optional)", value=default_aadhaar, max_chars=12)

        st.markdown("### 🛒 Add Items to Bill Cart")
        if inventory_df.empty:
            st.warning("⚠️ Please ask Admin to add items in 'Manage Inventory' first!")
        else:
            item_list = inventory_df["Item Name"].tolist()
            col_item1, col_item2, col_item3, col_item4 = st.columns([2, 1, 1, 1])
            with col_item1:
                selected_item = st.selectbox("Select Product", item_list)
            
            item_row = inventory_df[inventory_df["Item Name"] == selected_item]
            available_stock = float(item_row["Quantity"].values[0]) if not item_row.empty else 0.0
            default_price = float(item_row["Price (₹)"].values[0]) if not item_row.empty else 100.0
            
            st.info(f"📦 Available Stock for **{selected_item}**: **{available_stock}** units/kg | Price: ₹{default_price} (Fixed by Admin)")

            with col_item2:
                qty = st.number_input("Quantity", min_value=0.1, max_value=max(0.1, available_stock), value=1.0)
            with col_item3:
                # Staff cannot edit price, showing fixed price box
                price = st.number_input("Price (₹)", value=default_price, disabled=True)
            with col_item4:
                st.markdown("<br>", unsafe_allow_html=True)
                add_to_cart_btn = st.button("➕ Add Item")

            if add_to_cart_btn:
                if qty > available_stock:
                    st.error(f"❌ Cannot add! Only {available_stock} available in stock.")
                else:
                    total_item_amt = qty * default_price
                    st.session_state["cart"].append({
                        "Item Name": selected_item,
                        "Qty": qty,
                        "Price": default_price,
                        "Total": total_item_amt
                    })
                    st.success(f"Added {selected_item} to cart!")

            if len(st.session_state["cart"]) > 0:
                st.markdown("#### 🛍️ Current Cart Items")
                cart_df = pd.DataFrame(st.session_state["cart"])
                st.dataframe(cart_df, use_container_width=True, hide_index=True)
                
                grand_total = cart_df["Total"].sum()
                st.info(f"**Grand Total Amount: ₹ {grand_total:.2f}**")

                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    if st.button("🗑️ Clear Cart", use_container_width=True):
                        st.session_state["cart"] = []
                        st.rerun()
                with col_act2:
                    if st.button("💾 Save & Generate Final Bill", use_container_width=True):
                        if cust_name and mobile_no:
                            for item in st.session_state["cart"]:
                                new_sale = pd.DataFrame([[
                                    bill_no, bill_date_str, cust_name, village_name, str(mobile_no), str(aadhaar_no),
                                    item["Item Name"], item["Qty"], item["Price"], item["Total"]
                                ]], columns=["Bill No", "Date", "Customer Name", "Village", "Mobile", "Aadhaar No", "Item Name", "Quantity", "Price", "Total Amount"])
                                sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
                                
                                idx = inventory_df[inventory_df["Item Name"] == item["Item Name"]].index
                                if not idx.empty:
                                    current_stock = inventory_df.loc[idx[0], "Quantity"]
                                    inventory_df.loc[idx[0], "Quantity"] = max(0.0, current_stock - item["Qty"])
                            
                            save_sales(sales_df)
                            save_inventory(inventory_df)
                            
                            st.session_state["last_bill"] = {
                                "bill_no": bill_no,
                                "date": bill_date_str,
                                "cust_name": cust_name,
                                "village": village_name,
                                "mobile": str(mobile_no),
                                "aadhaar": str(aadhaar_no),
                                "items": st.session_state["cart"].copy(),
                                "grand_total": grand_total
                            }
                            st.success(f"✅ Bill Generated Successfully & Stock Updated for {cust_name}!")
                            st.session_state["cart"] = []
                            st.rerun()
                        else:
                            st.warning("⚠️ Please enter both Customer Name and Mobile Number.")

        if "last_bill" in st.session_state:
            b = st.session_state["last_bill"]
            st.markdown("---")
            st.markdown("### 🖨️ Bill Ready for Print")
            
            items_rows_html = ""
            for itm in b['items']:
                items_rows_html += f"""
                <tr>
                    <td>{itm['Item Name']}</td>
                    <td class="center">{itm['Qty']}</td>
                    <td class="right">₹{itm['Price']}</td>
                    <td class="right">₹{itm['Total']}</td>
                </tr>
                """
            
            complete_invoice_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background: #fff; margin: 0; padding: 10px; }}
                    .invoice-box {{ max-width: 700px; margin: auto; padding: 10px; border: 1px solid #eee; background: #fff; }}
                    .copy-section {{ border: 2px solid #8b0000; padding: 10px; border-radius: 6px; margin-bottom: 10px; }}
                    .store-copy {{ border: 2px solid #333 !important; }}
                    h3 {{ text-align: center; color: #8b0000; margin: 0; font-size: 16px; }}
                    .store-copy h3 {{ color: #333; }}
                    p {{ text-align: center; font-size: 11px; margin: 2px 0; }}
                    .badge {{ text-align: center; font-weight: bold; background: #fdfbf7; color: #8b0000; margin: 5px 0; padding: 3px; font-size: 12px; border: 1px solid #b8860b; }}
                    .store-badge {{ background: #e2e8f0; color: #333; border: 1px solid #999; }}
                    table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 5px; }}
                    th, td {{ padding: 5px; border: 1px solid #ddd; text-align: left; }}
                    th {{ background: #f1f5f9; }}
                    .right {{ text-align: right; }}
                    .center {{ text-align: center; }}
                    .dashed-line {{ border-bottom: 2px dashed #999; margin: 10px 0; text-align: center; font-size: 12px; color: #666; }}
                    .print-btn {{ display: block; width: 100%; background: #8b0000; color: white; padding: 12px; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-bottom: 15px; text-align: center; }}
                    @media print {{ .print-btn {{ display: none; }} body {{ padding: 0; }} }}
                </style>
            </head>
            <body>
                <button class="print-btn" onclick="window.print()">🖨️ Click Here to Print Both Copies</button>
                <div class="invoice-box">
                    <div class="copy-section">
                        <h3>🕉️ SRI MANIKANTA TRADERS</h3>
                        <p>D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
                        <div class="badge">FARMER COPY</div>
                        <hr style="margin: 5px 0;">
                        <table style="border:none;">
                            <tr style="border:none;"><td style="border:none;"><b>Bill No:</b> {b['bill_no']}</td><td style="border:none;"><b>Date:</b> {b['date']}</td></tr>
                            <tr style="border:none;"><td style="border:none;"><b>Customer:</b> {b['cust_name']}</td><td style="border:none;"><b>Village:</b> {b['village']}</td></tr>
                            <tr style="border:none;"><td style="border:none;"><b>Mobile:</b> {b['mobile']}</td><td style="border:none;"><b>Aadhaar:</b> {b['aadhaar'] if b['aadhaar'] else 'N/A'}</td></tr>
                        </table>
                        <table>
                            <tr><th>Item Name</th><th class="center">Qty</th><th class="right">Price</th><th class="right">Total</th></tr>
                            {items_rows_html}
                        </table>
                        <h4 style="text-align: right; margin: 5px 0 0 0; color: #8b0000;">Grand Total: ₹ {b['grand_total']:.2f}</h4>
                    </div>
                    <div class="dashed-line">✂ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ✂</div>
                    <div class="copy-section store-copy">
                        <h3 style="color: #333;">SRI MANIKANTA TRADERS</h3>
                        <p>D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
                        <div class="badge store-badge">STORE COPY</div>
                        <hr style="margin: 5px 0;">
                        <table style="border:none;">
                            <tr style="border:none;"><td style="border:none;"><b>Bill No:</b> {b['bill_no']}</td><td style="border:none;"><b>Date:</b> {b['date']}</td></tr>
                            <tr style="border:none;"><td style="border:none;"><b>Customer:</b> {b['cust_name']}</td><td style="border:none;"><b>Village:</b> {b['village']}</td></tr>
                            <tr style="border:none;"><td style="border:none;"><b>Mobile:</b> {b['mobile']}</td><td style="border:none;"><b>Aadhaar:</b> {b['aadhaar'] if b['aadhaar'] else 'N/A'}</td></tr>
                        </table>
                        <table>
                            <tr><th>Item Name</th><th class="center">Qty</th><th class="right">Price</th><th class="right">Total</th></tr>
                            {items_rows_html}
                        </table>
                        <h4 style="text-align: right; margin: 5px 0 0 0; color: #333;">Grand Total: ₹ {b['grand_total']:.2f}</h4>
                    </div>
                </div>
            </body>
            </html>
            """
            components.html(complete_invoice_html, height=780, scrolling=True)

    elif menu == "Sales History & Reports":
        st.title("📊 Sales History & Bill Reprint")
        if not sales_df.empty:
            display_sales_df = sales_df.iloc[::-1].reset_index(drop=True)

            st.markdown("### 🔍 Search & Reprint Old Bill")
            search_query = st.text_input("Enter Bill No, Customer Name or Mobile No to Reprint:")
            
            if search_query:
                filtered_bills = display_sales_df[(display_sales_df["Bill No"].str.contains(search_query, case=False, na=False)) | 
                                                  (display_sales_df["Customer Name"].str.contains(search_query, case=False, na=False)) |
                                                  (display_sales_df["Mobile"].astype(str).str.contains(search_query, na=False))]
                if not filtered_bills.empty:
                    unique_matched_bills = filtered_bills["Bill No"].unique()
                    selected_reprint_bill = st.selectbox("Select Bill to Print", unique_matched_bills)
                    
                    if st.button("🖨️ Generate Reprint Preview"):
                        bill_rows = sales_df[sales_df["Bill No"] == selected_reprint_bill]
                        b_date = bill_rows.iloc[0]["Date"]
                        b_cust = bill_rows.iloc[0]["Customer Name"]
                        b_vill = bill_rows.iloc[0]["Village"] if "Village" in bill_rows.columns else "Pedda Harivanam"
                        b_mob = bill_rows.iloc[0]["Mobile"]
                        b_aadhaar = bill_rows.iloc[0]["Aadhaar No"] if "Aadhaar No" in bill_rows.columns else ""
                        if pd.isna(b_aadhaar): b_aadhaar = ""
                        
                        reprint_items = []
                        for _, row in bill_rows.iterrows():
                            reprint_items.append({
                                "Item Name": row["Item Name"],
                                "Qty": row["Quantity"],
                                "Price": row["Price"],
                                "Total": row["Total Amount"]
                            })
                        
                        reprint_grand_total = sum(i["Total"] for i in reprint_items)
                        reprint_items_html = ""
                        for itm in reprint_items:
                            reprint_items_html += f"""
                            <tr>
                                <td>{itm['Item Name']}</td>
                                <td class="center">{itm['Qty']}</td>
                                <td class="right">₹{itm['Price']}</td>
                                <td class="right">₹{itm['Total']}</td>
                            </tr>
                            """
                        
                        reprint_html = f"""
                        <html>
                        <head>
                            <style>
                                body {{ font-family: Arial, sans-serif; background: #fff; margin: 0; padding: 10px; }}
                                .invoice-box {{ max-width: 700px; margin: auto; padding: 10px; border: 1px solid #eee; background: #fff; }}
                                .copy-section {{ border: 2px solid #8b0000; padding: 10px; border-radius: 6px; margin-bottom: 10px; }}
                                h3 {{ text-align: center; color: #8b0000; margin: 0; font-size: 16px; }}
                                p {{ text-align: center; font-size: 11px; margin: 2px 0; }}
                                .badge {{ text-align: center; font-weight: bold; background: #fdfbf7; color: #8b0000; margin: 5px 0; padding: 3px; font-size: 12px; border: 1px solid #b8860b; }}
                                table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 5px; }}
                                th, td {{ padding: 5px; border: 1px solid #ddd; text-align: left; }}
                                th {{ background: #f1f5f9; }}
                                .right {{ text-align: right; }}
                                .center {{ text-align: center; }}
                                .print-btn {{ display: block; width: 100%; background: #8b0000; color: white; padding: 12px; font-size: 16px; font-weight: bold; border: none; border-radius: 6px; cursor: pointer; margin-bottom: 15px; text-align: center; }}
                                @media print {{ .print-btn {{ display: none; }} body {{ padding: 0; }} }}
                            </style>
                        </head>
                        <body>
                            <button class="print-btn" onclick="window.print()">🖨️ Click Here to Print Duplicate Copy</button>
                            <div class="invoice-box">
                                <div class="copy-section">
                                    <h3>🕉️ SRI MANIKANTA TRADERS (DUPLICATE)</h3>
                                    <p>D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
                                    <div class="badge">FARMER COPY</div>
                                    <hr style="margin: 5px 0;">
                                    <table style="border:none;">
                                        <tr style="border:none;"><td style="border:none;"><b>Bill No:</b> {selected_reprint_bill}</td><td style="border:none;"><b>Date:</b> {b_date}</td></tr>
                                        <tr style="border:none;"><td style="border:none;"><b>Customer:</b> {b_cust}</td><td style="border:none;"><b>Village:</b> {b_vill}</td></tr>
                                        <tr style="border:none;"><td style="border:none;"><b>Mobile:</b> {b_mob}</td><td style="border:none;"><b>Aadhaar:</b> {b_aadhaar if b_aadhaar else 'N/A'}</td></tr>
                                    </table>
                                    <table>
                                        <tr><th>Item Name</th><th class="center">Qty</th><th class="right">Price</th><th class="right">Total</th></tr>
                                        {reprint_items_html}
                                    </table>
                                    <h4 style="text-align: right; margin: 5px 0 0 0; color: #8b0000;">Grand Total: ₹ {reprint_grand_total:.2f}</h4>
                                </div>
                            </div>
                        </body>
                        </html>
                        """
                        components.html(reprint_html, height=620, scrolling=True)
                else:
                    st.warning("⚠️ No matching bills found.")

            st.markdown("---")
            st.markdown("### 📋 All Bills History (Newest on Top)")
            st.dataframe(display_sales_df, use_container_width=True)
            
            st.markdown("### 📈 Category-wise Sales Summary")
            merged_df = pd.merge(sales_df, inventory_df[["Item Name", "Category"]], on="Item Name", how="left")
            category_summary = merged_df.groupby("Category")["Total Amount"].sum().reset_index()
            st.dataframe(category_summary, use_container_width=True)

    elif menu == "Cash Book & Expenses":
        st.title("📒 Cash Book, Bank Deposits & Expenses")
        
        total_revenue = sales_df["Total Amount"].sum() if not sales_df.empty else 0.0
        approved_deposits = cash_df[cash_df["Status"] == "Approved"]["Deposit Amount (₹)"].sum() if not cash_df.empty and "Status" in cash_df.columns else 0.0
        approved_expenses = expenses_df[expenses_df["Status"] == "Approved"]["Amount (₹)"].sum() if not expenses_df.empty and "Status" in expenses_df.columns else 0.0
        
        hand_cash_balance = total_revenue - (approved_deposits + approved_expenses)
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric(label="💵 Total Sales Collection", value=f"₹ {total_revenue:.2f}")
        with col_m2:
            st.metric(label="🏦 Approved Bank Deposits", value=f"₹ {approved_deposits:.2f}")
        with col_m3:
            st.metric(label="💸 Approved Expenses", value=f"₹ {approved_expenses:.2f}")
        with col_m4:
            st.metric(label="💰 Hand Cash Balance", value=f"₹ {hand_cash_balance:.2f}")
            
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["➕ Add Entry (Staff / Admin)", "🛡️ Owner Authorization / Approvals"])
        
        with tab1:
            st.markdown("### 🏦 Add Bank Deposit Entry & Attach Receipt")
            with st.form("bank_deposit_form"):
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    dep_date_str = st.text_input("Deposit Date (DD-MM-YYYY)", value=datetime.now().strftime('%d-%m-%Y'), key="dep_date_txt_input")
                    dep_desc = st.text_input("Description / Bank Name", value="Bank Deposit")
                with col_d2:
                    dep_amount = st.number_input("Deposit Amount (₹)", min_value=1.0, value=1000.0)
                    receipt_file = st.file_uploader("📎 Upload Deposit Receipt / Slip (Image/PDF)", type=["png", "jpg", "jpeg", "pdf"], key="dep_file_up")
                    
                if st.form_submit_button("Submit Bank Deposit"):
                    receipt_name = "No Receipt"
                    if receipt_file is not None:
                        receipt_name = receipt_file.name
                        os.makedirs("receipts", exist_ok=True)
                        with open(os.path.join("receipts", receipt_file.name), "wb") as f:
                            f.write(receipt_file.getbuffer())

                    initial_status = "Approved" if st.session_state["role"] == "Admin" else "Pending"
                    new_dep = pd.DataFrame([[dep_date_str, dep_desc, dep_amount, receipt_name, initial_status]], columns=["Date", "Description", "Deposit Amount (₹)", "Receipt Name", "Status"])
                    cash_df = pd.concat([cash_df, new_dep], ignore_index=True)
                    save_cash_deposits(cash_df)
                    st.success(f"✅ Bank deposit of ₹ {dep_amount:.2f} submitted successfully! Status: **{initial_status}**")
                    st.rerun()

            st.markdown("---")
            st.markdown("### 💸 Add Expense Entry & Attach Receipt")
            with st.form("expense_add_form"):
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    exp_date_str = st.text_input("Expense Date (DD-MM-YYYY)", value=datetime.now().strftime('%d-%m-%Y'), key="exp_date_txt")
                    exp_name = st.text_input("Expense Description / Reason", value="Shop Rent / Electricity / Transport")
                with col_e2:
                    exp_amount = st.number_input("Expense Amount (₹)", min_value=1.0, value=500.0)
                    exp_receipt_file = st.file_uploader("📎 Upload Expense Receipt / Bill (Image/PDF)", type=["png", "jpg", "jpeg", "pdf"], key="exp_file_up")
                
                if st.form_submit_button("Submit Expense"):
                    exp_receipt_name = "No Receipt"
                    if exp_receipt_file is not None:
                        exp_receipt_name = exp_receipt_file.name
                        os.makedirs("receipts", exist_ok=True)
                        with open(os.path.join("receipts", exp_receipt_file.name), "wb") as f:
                            f.write(exp_receipt_file.getbuffer())

                    initial_exp_status = "Approved" if st.session_state["role"] == "Admin" else "Pending"
                    new_exp = pd.DataFrame([[exp_date_str, exp_name, exp_amount, exp_receipt_name, initial_exp_status]], columns=["Date", "Expense Name", "Amount (₹)", "Receipt Name", "Status"])
                    expenses_df = pd.concat([expenses_df, new_exp], ignore_index=True)
                    save_expenses(expenses_df)
                    st.success(f"✅ Expense of ₹ {exp_amount:.2f} submitted successfully! Status: **{initial_exp_status}**")
                    st.rerun()

        with tab2:
            st.markdown("### 🛡️ Owner Authorization & Approvals")
            if st.session_state["role"] != "Admin":
                st.warning("⚠️ Only the Owner (Admin) can authorize pending entries. Please login as Admin to approve.")
            else:
                st.markdown("#### ⏳ Pending Bank Deposits")
                pending_deposits = cash_df[cash_df["Status"] == "Pending"] if not cash_df.empty and "Status" in cash_df.columns else pd.DataFrame()
                
                if not pending_deposits.empty:
                    for idx, row in pending_deposits.iterrows():
                        col_p1, col_p2, col_p3 = st.columns([3, 1, 1])
                        with col_p1:
                            st.write(f"📅 **Date:** {row['Date']} | 🏦 **Desc:** {row['Description']} | 💵 **Amount:** ₹{row['Deposit Amount (₹)']} | 📎 **Receipt:** {row['Receipt Name']}")
                            rec_path = os.path.join("receipts", str(row['Receipt Name']))
                            if row['Receipt Name'] != "No Receipt" and os.path.exists(rec_path):
                                if row['Receipt Name'].lower().endswith(('.png', '.jpg', '.jpeg')):
                                    st.image(rec_path, caption="Deposit Receipt", width=250)
                                with open(rec_path, "rb") as file_btn:
                                    st.download_button(label="📥 Download Deposit Receipt", data=file_btn, file_name=row['Receipt Name'], key=f"dl_pend_dep_{idx}")
                        with col_p2:
                            if st.button("✅ Authorize / Approve", key=f"app_dep_{idx}"):
                                cash_df.loc[idx, "Status"] = "Approved"
                                save_cash_deposits(cash_df)
                                st.success("Deposit authorized successfully!")
                                st.rerun()
                        with col_p3:
                            if st.button("❌ Reject / Delete", key=f"rej_dep_{idx}"):
                                cash_df = cash_df.drop(idx).reset_index(drop=True)
                                save_cash_deposits(cash_df)
                                st.warning("Deposit entry removed!")
                                st.rerun()
                else:
                    st.info("No pending bank deposits.")

                st.markdown("#### ⏳ Pending Expenses")
                pending_expenses = expenses_df[expenses_df["Status"] == "Pending"] if not expenses_df.empty and "Status" in expenses_df.columns else pd.DataFrame()
                
                if not pending_expenses.empty:
                    for idx, row in pending_expenses.iterrows():
                        col_ex1, col_ex2, col_ex3 = st.columns([3, 1, 1])
                        with col_ex1:
                            st.write(f"📅 **Date:** {row['Date']} | 💸 **Expense:** {row['Expense Name']} | 💵 **Amount:** ₹{row['Amount (₹)']} | 📎 **Receipt:** {row['Receipt Name']}")
                            rec_path = os.path.join("receipts", str(row['Receipt Name']))
                            if row['Receipt Name'] != "No Receipt" and os.path.exists(rec_path):
                                if row['Receipt Name'].lower().endswith(('.png', '.jpg', '.jpeg')):
                                    st.image(rec_path, caption="Expense Receipt", width=250)
                                with open(rec_path, "rb") as file_btn:
                                    st.download_button(label="📥 Download Expense Receipt", data=file_btn, file_name=row['Receipt Name'], key=f"dl_pend_exp_{idx}")
                        with col_ex2:
                            if st.button("✅ Authorize / Approve", key=f"app_exp_{idx}"):
                                expenses_df.loc[idx, "Status"] = "Approved"
                                save_expenses(expenses_df)
                                st.success("Expense authorized successfully!")
                                st.rerun()
                        with col_ex3:
                            if st.button("❌ Reject / Delete", key=f"rej_exp_{idx}"):
                                expenses_df = expenses_df.drop(idx).reset_index(drop=True)
                                save_expenses(expenses_df)
                                st.warning("Expense entry removed!")
                                st.rerun()
                else:
                    st.info("No pending expenses.")

        st.markdown("---")
        st.markdown("### 🏦 Bank Deposit History & Receipts")
        if not cash_df.empty:
            display_cash_df = cash_df.iloc[::-1].reset_index(drop=True)
            for idx, row in display_cash_df.iterrows():
                rec_name = row['Receipt Name'] if 'Receipt Name' in row and pd.notna(row['Receipt Name']) else "No Receipt"
                status_badge = "🟢 Approved" if row.get('Status', 'Approved') == 'Approved' else "🟡 Pending Authorization"
                with st.expander(f"[{status_badge}] Date: {row['Date']} | 🏦 {row['Description']} | Amount: ₹ {row['Deposit Amount (₹)']}"):
                    col_r1, col_r2 = st.columns([2, 1])
                    with col_r1:
                        st.write(f"**Deposit Date:** {row['Date']}")
                        st.write(f"**Bank / Description:** {row['Description']}")
                        st.write(f"**Amount Deposited:** ₹ {row['Deposit Amount (₹)']}")
                        st.write(f"**Status:** {row.get('Status', 'Approved')}")
                        st.write(f"**Attached File:** {rec_name}")
                        
                        rec_path = os.path.join("receipts", str(rec_name))
                        if rec_name != "No Receipt" and os.path.exists(rec_path):
                            if rec_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                                st.image(rec_path, caption="Deposit Receipt Preview", use_container_width=True)
                            with open(rec_path, "rb") as file_btn:
                                st.download_button(
                                    label="📥 Download Receipt File",
                                    data=file_btn,
                                    file_name=rec_name,
                                    mime="application/octet-stream",
                                    key=f"dl_rec_{idx}"
                                )
                        else:
                            st.info("No receipt uploaded for this entry.")
                            
                    with col_r2:
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        orig_idx = len(cash_df) - 1 - idx
                        if st.button(f"🗑️ Delete Entry", key=f"del_dep_{idx}T"):
                            cash_df = cash_df.drop(orig_idx).reset_index(drop=True)
                            save_cash_deposits(cash_df)
                            st.success("Deleted deposit record successfully!")
                            st.rerun()
        else:
            st.info("No bank deposits recorded yet.")

        st.markdown("---")
        st.markdown("### 💸 Expenses History & Receipts")
        if not expenses_df.empty:
            display_exp_df = expenses_df.iloc[::-1].reset_index(drop=True)
            for idx, row in display_exp_df.iterrows():
                rec_name = row['Receipt Name'] if 'Receipt Name' in row and pd.notna(row['Receipt Name']) else "No Receipt"
                status_badge = "🟢 Approved" if row.get('Status', 'Approved') == 'Approved' else "🟡 Pending Authorization"
                with st.expander(f"[{status_badge}] Date: {row['Date']} | 💸 {row['Expense Name']} | Amount: ₹ {row['Amount (₹)']}"):
                    col_e1, col_e2 = st.columns([2, 1])
                    with col_e1:
                        st.write(f"**Expense Date:** {row['Date']}")
                        st.write(f"**Description:** {row['Expense Name']}")
                        st.write(f"**Amount:** ₹ {row['Amount (₹)']}")
                        st.write(f"**Status:** {row.get('Status', 'Approved')}")
                        st.write(f"**Attached File:** {rec_name}")
                        
                        rec_path = os.path.join("receipts", str(rec_name))
                        if rec_name != "No Receipt" and os.path.exists(rec_path):
                            if rec_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                                st.image(rec_path, caption="Expense Receipt Preview", use_container_width=True)
                            with open(rec_path, "rb") as file_btn:
                                st.download_button(
                                    label="📥 Download Expense Receipt File",
                                    data=file_btn,
                                    file_name=rec_name,
                                    mime="application/octet-stream",
                                    key=f"dl_exp_rec_{idx}"
                                )
                        else:
                            st.info("No receipt uploaded for this expense.")
                    with col_e2:
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        orig_idx = len(expenses_df) - 1 - idx
                        if st.button(f"🗑️ Delete Expense", key=f"del_exp_{idx}T"):
                            expenses_df = expenses_df.drop(orig_idx).reset_index(drop=True)
                            save_expenses(expenses_df)
                            st.success("Deleted expense record successfully!")
                            st.rerun()
        else:
            st.info("No expense entries recorded yet.")

        if st.session_state["role"] == "Staff":
            st.markdown("### 💰 Sales Revenue Transaction Ledger")
            if not sales_df.empty:
                display_sales_ledger = sales_df.iloc[::-1].reset_index(drop=True)
                cols_to_show = [c for c in ["Date", "Bill No", "Customer Name", "Village", "Total Amount"] if c in display_sales_ledger.columns]
                st.dataframe(display_sales_ledger[cols_to_show], use_container_width=True)
