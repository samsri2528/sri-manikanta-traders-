import os
import streamlit as st
import pandas as pd
from datetime import datetime

# --- FILE PATHS ---
INVENTORY_FILE = "inventory.xlsx"
SALES_FILE = "Sales_History.xlsx"
EXPENSES_FILE = "expenses.xlsx"
CASH_BOOK_FILE = "cash_book_deposits.xlsx"

# Initialize DataFrames with default structures if missing
def init_files():
    if not os.path.exists(INVENTORY_FILE):
        df = pd.DataFrame(columns=["Item", "Purchase Price", "Selling Price", "Stock"])
        df.to_excel(INVENTORY_FILE, index=False)
    if not os.path.exists(SALES_FILE):
        df = pd.DataFrame(columns=["Date", "Item", "Quantity", "Selling Price", "Total"])
        df.to_excel(SALES_FILE, index=False)
    if not os.path.exists(EXPENSES_FILE):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Status", "Receipt Name"])
        df.to_excel(EXPENSES_FILE, index=False)
    if not os.path.exists(CASH_BOOK_FILE):
        df = pd.DataFrame(columns=["Date", "Type", "Amount", "Status", "Receipt Name"])
        df.to_excel(CASH_BOOK_FILE, index=False)
    os.makedirs("receipts", exist_ok=True)

init_files()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sri Manikanta Traders", layout="wide")
st.title("🌾 Sri Manikanta Traders - Billing & Inventory System")

# --- LOGIN & ROLE MANAGEMENT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.subheader("🔐 Login Portal")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "manikanta123":
            st.session_state.logged_in = True
            st.session_state.role = "Admin"
            st.success("Admin Login Successful!")
            st.rerun()
        elif username == "manikanta" and password == "samsri2528":
            st.session_state.logged_in = True
            st.session_state.role = "Staff"
            st.success("Staff Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Username or Password")
else:
    # Logout Button in Sidebar
    st.sidebar.write(f"Logged in as: **{st.session_state.role}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.rerun()

    # --- MAIN APPLICATION NAVIGATION ---
    menu = ["Billing", "Inventory", "Expenses & Cash Book"]
    
    if st.session_state.role == "Admin":
        menu.append("Admin Monthly Report & Profits")

    choice = st.sidebar.selectbox("Navigation", menu)

    # 1. BILLING SECTION
    if choice == "Billing":
        st.subheader("🧾 Billing Counter")
        try:
            inv_df = pd.read_excel(INVENTORY_FILE)
        except:
            inv_df = pd.DataFrame(columns=["Item", "Purchase Price", "Selling Price", "Stock"])

        if not inv_df.empty:
            item_list = inv_df["Item"].tolist()
            selected_item = st.selectbox("Select Item", item_list)
            
            item_row = inv_df[inv_df["Item"] == selected_item].iloc[0]
            selling_price = item_row["Selling Price"]
            available_stock = item_row["Stock"]
            
            st.write(f"Available Stock: **{available_stock}** | Selling Price: **₹{selling_price}**")
            
            qty = st.number_input("Quantity", min_value=1, max_value=int(available_stock) if available_stock > 0 else 1, value=1)
            
            if st.button("Complete Sale & Print Bill"):
                total_amount = qty * selling_price
                inv_df.loc[inv_df["Item"] == selected_item, "Stock"] -= qty
                inv_df.to_excel(INVENTORY_FILE, index=False)
                
                new_sale = pd.DataFrame([{
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Item": selected_item,
                    "Quantity": qty,
                    "Selling Price": selling_price,
                    "Total": total_amount
                }])
                
                sales_df = pd.read_excel(SALES_FILE)
                sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
                sales_df.to_excel(SALES_FILE, index=False)
                
                st.success(f"Bill Generated Successfully! Total Amount: ₹{total_amount}")
        else:
            st.warning("No inventory available for billing.")

    # 2. INVENTORY SECTION
    elif choice == "Inventory":
        st.subheader("📦 Inventory Stock Management")
        try:
            inv_df = pd.read_excel(INVENTORY_FILE)
        except:
            inv_df = pd.DataFrame(columns=["Item", "Purchase Price", "Selling Price", "Stock"])

        if st.session_state.role == "Admin":
            st.write("### Add New Stock (Admin Only)")
            with st.form("add_stock_form"):
                new_item = st.text_input("Item Name")
                p_price = st.number_input("Purchase Price (కొన్న ధర - Hidden from Staff)", min_value=0.0)
                s_price = st.number_input("Selling Price (అమ్మే ధర)", min_value=0.0)
                stock_qty = st.number_input("Stock Quantity", min_value=0, step=1)
                submit_stock = st.form_submit_button("Add/Update Stock")
                
                if submit_stock and new_item:
                    if new_item in inv_df["Item"].values:
                        inv_df.loc[inv_df["Item"] == new_item, "Purchase Price"] = p_price
                        inv_df.loc[inv_df["Item"] == new_item, "Selling Price"] = s_price
                        inv_df.loc[inv_df["Item"] == new_item, "Stock"] += stock_qty
                    else:
                        new_row = pd.DataFrame([{"Item": new_item, "Purchase Price": p_price, "Selling Price": s_price, "Stock": stock_qty}])
                        inv_df = pd.concat([inv_df, new_row], ignore_index=True)
                    inv_df.to_excel(INVENTORY_FILE, index=False)
                    st.success(f"Stock updated for {new_item}!")
                    st.rerun()

        st.write("### Current Stock View")
        if st.session_state.role == "Staff":
            staff_view_df = inv_df[["Item", "Selling Price", "Stock"]] if "Purchase Price" in inv_df.columns else inv_df
            st.dataframe(staff_view_df)
        else:
            st.dataframe(inv_df)

    # 3. EXPENSES & CASH BOOK SECTION
    elif choice == "Expenses & Cash Book":
        st.subheader("💸 Expenses & Cash Book Management")
        
        tab1, tab2 = st.tabs(["Add Expense / Deposit", "View & Authorize"])
        
        with tab1:
            with st.form("expense_form"):
                exp_cat = st.text_input("Category (e.g., Transport, Electricity)")
                exp_amount = st.number_input("Amount", min_value=0.0)
                txn_type = st.selectbox("Type", ["Expense", "Bank Deposit"])
                uploaded_file = st.file_uploader("Upload Receipt (Optional)", type=["png", "jpg", "jpeg"])
                submit_exp = st.form_submit_button("Submit Entry")
                
                if submit_exp:
                    file_to_save = EXPENSES_FILE if txn_type == "Expense" else CASH_BOOK_FILE
                    receipt_name = "No Receipt"
                    if uploaded_file is not None:
                        receipt_name = uploaded_file.name
                        with open(os.path.join("receipts", receipt_name), "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    
                    initial_status = "Approved" if st.session_state.role == "Admin" else "Pending"
                    
                    try:
                        df = pd.read_excel(file_to_save)
                    except:
                        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Status", "Receipt Name"])
                    
                    new_rec = pd.DataFrame([{
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Category": exp_cat,
                        "Amount": exp_amount,
                        "Status": initial_status,
                        "Receipt Name": receipt_name
                    }])
                    df = pd.concat([df, new_rec], ignore_index=True)
                    df.to_excel(file_to_save, index=False)
                    st.success(f"Submitted successfully! Status: **{initial_status}**")
                    
        with tab2:
            st.write("### Records & Admin Authorizations")
            try:
                exp_df = pd.read_excel(EXPENSES_FILE)
            except:
                exp_df = pd.DataFrame(columns=["Date", "Category", "Amount", "Status", "Receipt Name"])
                
            try:
                cash_df = pd.read_excel(CASH_BOOK_FILE)
            except:
                cash_df = pd.DataFrame(columns=["Date", "Type", "Amount", "Status", "Receipt Name"])

            st.write("#### Expenses History")
            st.dataframe(exp_df)
            
            st.write("#### Bank Deposits History")
            st.dataframe(cash_df)

            if st.session_state.role == "Admin":
                st.markdown("---")
                st.write("#### 🛡️ Pending Approvals Authorization")
                
                # Handle pending expenses
                pending_exp = exp_df[exp_df["Status"] == "Pending"] if not exp_df.empty and "Status" in exp_df.columns else pd.DataFrame()
                if not pending_exp.empty:
                    st.write("Pending Expenses:")
                    for idx, row in pending_exp.iterrows():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"Date: {row['Date']} | Category: {row['Category']} | Amount: ₹{row['Amount']}")
                        with col2:
                            if st.button("Approve Expense", key=f"app_exp_{idx}"):
                                exp_df.loc[idx, "Status"] = "Approved"
                                exp_df.to_excel(EXPENSES_FILE, index=False)
                                st.success("Expense Approved!")
                                st.rerun()
                else:
                    st.info("No pending expenses to approve.")

    # 4. ADMIN MONTHLY REPORT & PROFITS
    elif choice == "Admin Monthly Report & Profits" and st.session_state.role == "Admin":
        st.subheader("📊 Admin Portal: Monthly Profit & Excel Reports")
        
        try:
            sales_df = pd.read_excel(SALES_FILE)
        except:
            sales_df = pd.DataFrame(columns=["Date", "Item", "Quantity", "Selling Price", "Total"])

        try:
            inventory_df = pd.read_excel(INVENTORY_FILE)
        except:
            inventory_df = pd.DataFrame(columns=["Item", "Purchase Price", "Selling Price", "Stock"])

        if not sales_df.empty and 'Date' in sales_df.columns:
            sales_df['Date'] = pd.to_datetime(sales_df['Date'], errors='coerce')
            sales_df['Month-Year'] = sales_df['Date'].dt.strftime('%B %Y')
            available_months = sales_df['Month-Year'].dropna().unique()
            
            if len(available_months) > 0:
                selected_month = st.selectbox("నెలవారీ రిపోర్ట్ ఎంచుకోండి (Select Month)", available_months)
                filtered_sales = sales_df[sales_df['Month-Year'] == selected_month]
                
                st.write(f"### {selected_month} - Sales Report")
                st.dataframe(filtered_sales)

                st.download_button(
                    label=f"📥 Download {selected_month} Sales Excel",
                    data=filtered_sales.to_csv(index=False).encode('utf-8'),
                    file_name=f"Manikanta_Traders_Sales_{selected_month}.csv",
                    mime="text/csv",
                )
            else:
                st.warning("No valid dates found in sales data.")
        else:
            st.warning("No sales history available yet.")

        st.markdown("---")
        with st.expander("🔒 Confidential: Stock Purchase Prices & Margins (Admin Only)"):
            st.warning("ఈ వివరాలు స్టాఫ్‌కి ఎక్కడా కనిపించవు. కొన్న ధర మరియు లాభాల అంచనా కోసం మాత్రమే.")
            if not inventory_df.empty:
                st.dataframe(inventory_df)
            else:
                st.info("Inventory is empty.")
