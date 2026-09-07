import streamlit as st
import pandas as pd
import openpyxl
import os
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="SRI MANIKANTA TRADERS", layout="wide")

EXCEL_FILE = "Book1.xlsx"
SALES_FILE = "Sales_History.xlsx"
CASH_FILE = "Cash_Register.xlsx"

# Load Inventory
def load_data():
    if os.path.exists(EXCEL_FILE):
        try:
            return pd.read_excel(EXCEL_FILE)
        except Exception as e:
            st.error(f"Error reading Excel: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# Load Sales
def load_sales_history():
    if os.path.exists(SALES_FILE):
        try:
            return pd.read_excel(SALES_FILE)
        except:
            pass
    return pd.DataFrame(columns=["Bill No", "Date", "Customer Name", "Mobile", "Items", "Total Amount"])

# Load Cash Register
def load_cash_register():
    if os.path.exists(CASH_FILE):
        try:
            return pd.read_excel(CASH_FILE)
        except:
            pass
    return pd.DataFrame(columns=["Date", "Opening Cash", "Cash Sales", "Cash Deposits", "Closing Cash"])

df = load_data()

# Initialize Session States
if "invoice_items" not in st.session_state:
    st.session_state.invoice_items = []
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.markdown("<h2 style='text-align: center;'>🌾 SRI MANIKANTA TRADERS 🌾</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>D:No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>", unsafe_allow_html=True)
st.divider()

# ==================== HOME / MODE SELECTION ====================
mode = st.sidebar.radio("Select Operating Mode", ["🧾 Billing Mode (Staff)", "🔒 Admin Mode"])

if mode == "🧾 Billing Mode (Staff)":
    st.sidebar.success("🟢 Running in Staff Billing Mode")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        sales_df = load_sales_history()
        bill_no = st.text_input("Bill No", value=f"SMT-{len(sales_df) + 1:03d}")
    with c2:
        bill_date = st.date_input("Date", datetime.now())
    with c3:
        cust_name = st.text_input("Customer / Farmer Name", value="LAKSHMANNA")
    with c4:
        mobile_no = st.text_input("Mobile No (10 Digits)", value="7702601442")

    st.subheader("📦 Item Selection & Stock Grid")

    if not df.empty:
        cols = list(df.columns)
        item_col = next((c for c in cols if any(k in str(c).lower() for k in ["item", "product", "particular"])), cols[1] if len(cols) > 1 else cols[0])
        stock_col = next((c for c in cols if any(k in str(c).lower() for k in ["qty", "stock", "quantity"])), cols[2] if len(cols) > 2 else cols[-1])
        rate_col = next((c for c in cols if any(k in str(c).lower() for k in ["rate", "price", "mrp"])), cols[3] if len(cols) > 3 else cols[-1])
        cat_col = next((c for c in cols if any(k in str(c).lower() for k in ["cat", "group"])), None)

        g1, g2, g3, g4 = st.columns([2, 4, 2, 2])
        
        with g1:
            categories = ["All Categories"] + (list(df[cat_col].dropna().unique()) if cat_col else [])
            selected_cat = st.selectbox("Filter Category", categories)

        filtered_df = df if selected_cat == "All Categories" else df[df[cat_col] == selected_cat]

        with g2:
            selected_item = st.selectbox("Search Item / Product Name", filtered_df[item_col].dropna().unique())

        item_row = filtered_df[filtered_df[item_col] == selected_item].iloc[0]
        
        try: current_stock = int(item_row[stock_col]) if pd.notnull(item_row[stock_col]) else 0
        except: current_stock = 0

        try: unit_price = float(item_row[rate_col]) if pd.notnull(item_row[rate_col]) else 0.0
        except: unit_price = 0.0

        with g3:
            qty = st.number_input(f"Qty (Stock: {current_stock})", min_value=1, max_value=max(1, current_stock), value=1)

        with g4:
            st.write("")
            st.write("")
            if st.button("+ Add Item", use_container_width=True):
                st.session_state.invoice_items.append({
                    "SNo": len(st.session_state.invoice_items) + 1,
                    "Category": item_row[cat_col] if cat_col else "General",
                    "Item Name": selected_item,
                    "Quantity": qty,
                    "Rate (₹)": unit_price,
                    "Total Amount (₹)": qty * unit_price
                })
                st.rerun()

    st.subheader("🧾 Sales Invoice Grid")
    if st.session_state.invoice_items:
        cart_df = pd.DataFrame(st.session_state.invoice_items)
        st.dataframe(cart_df, use_container_width=True, hide_index=True)
        
        total_bill = sum(item["Total Amount (₹)"] for item in st.session_state.invoice_items)
        st.markdown("---")
        
        b1, b2, b3 = st.columns(3)
        b1.metric("Total Bill Amount", f"₹ {total_bill:.2f}")
        cash_paid = b2.number_input("Amount Received", value=float(total_bill))
        b3.metric("Balance / Change", f"₹ {cash_paid - total_bill:.2f}")

        if st.button("💾 Save Bill & Deduct Stock", type="primary", use_container_width=True):
            try:
                full_df = pd.read_excel(EXCEL_FILE)
                items_summary = []

                for cart_item in st.session_state.invoice_items:
                    sold_name = cart_item["Item Name"]
                    sold_qty = cart_item["Quantity"]
                    items_summary.append(f"{sold_name} ({sold_qty})")

                    match_mask = full_df[item_col].astype(str).str.strip() == str(sold_name).strip()
                    if match_mask.any():
                        full_df.loc[match_mask, stock_col] = full_df.loc[match_mask, stock_col].apply(lambda x: max(0, int(x) - int(sold_qty)) if pd.notnull(x) else 0)

                full_df.to_excel(EXCEL_FILE, index=False)

                sales_df = load_sales_history()
                new_sale = pd.DataFrame([{
                    "Bill No": bill_no,
                    "Date": bill_date.strftime("%Y-%m-%d"),
                    "Customer Name": cust_name,
                    "Mobile": mobile_no,
                    "Items": ", ".join(items_summary),
                    "Total Amount": total_bill
                }])
                pd.concat([sales_df, new_sale], ignore_index=True).to_excel(SALES_FILE, index=False)

                st.session_state.last_bill = {
                    "bill_no": bill_no,
                    "date": bill_date.strftime("%Y-%m-%d"),
                    "customer": cust_name,
                    "mobile": mobile_no,
                    "items": st.session_state.invoice_items,
                    "total": total_bill
                }
                st.session_state.invoice_items = []
                st.success("✅ Bill Saved & Stock Deducted Successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Error saving bill: {e}")

    if "last_bill" in st.session_state:
        st.markdown("---")
        st.subheader("🖨️ Printable A4 Bill & WhatsApp Share")
        lb = st.session_state.last_bill

        wa_text = f"🌾 *SRI MANIKANTA TRADERS* 🌾\n" \
                  f"D:No 6/159/25, Pedda Harivanam\n" \
                  f"Ph: 7995217343\n\n" \
                  f"📄 *Bill No:* {lb['bill_no']}\n" \
                  f"📅 *Date:* {lb['date']}\n" \
                  f"👤 *Customer:* {lb['customer']}\n\n" \
                  f"*Items Purchased:*\n"
        for idx, itm in enumerate(lb['items'], 1):
            wa_text += f"{idx}. {itm['Item Name']} - {itm['Quantity']} x ₹{itm['Rate (₹)']} = ₹{itm['Total Amount (₹)']}\n"
        
        wa_text += f"\n💰 *Total Amount: ₹{lb['total']:.2f}*\n" \
                   f"_Thank you! Visit Again 🙏_"

        encoded_wa_text = urllib.parse.quote(wa_text)
        clean_mob = "".join(filter(str.isdigit, str(lb['mobile'])))
        if len(clean_mob) == 10:
            clean_mob = "91" + clean_mob
        
        wa_url = f"https://api.whatsapp.com/send?phone={clean_mob}&text={encoded_wa_text}"

        st.markdown(f"""
            <a href="{wa_url}" target="_blank">
                <button style="background-color: #25D366; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; width: 100%; margin-bottom: 15px;">
                    💬 Send Bill to Farmer WhatsApp ({lb['mobile']})
                </button>
            </a>
        """, unsafe_allow_html=True)

        def generate_receipt_html(copy_title):
            rows_html = ""
            for idx, item in enumerate(lb['items'], 1):
                rows_html += f"""
                <tr>
                    <td style="border: 1px solid #ddd; padding: 4px; text-align: center;">{idx}</td>
                    <td style="border: 1px solid #ddd; padding: 4px;">{item['Item Name']}</td>
                    <td style="border: 1px solid #ddd; padding: 4px; text-align: center;">{item['Quantity']}</td>
                    <td style="border: 1px solid #ddd; padding: 4px; text-align: right;">₹{item['Rate (₹)']:.2f}</td>
                    <td style="border: 1px solid #ddd; padding: 4px; text-align: right;">₹{item['Total Amount (₹)']:.2f}</td>
                </tr>
                """

            return f"""
            <div style="border: 2px solid #333; padding: 12px; margin-bottom: 10px; border-radius: 6px; background-color: #fff; font-family: Arial, sans-serif;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #333; padding-bottom: 5px;">
                    <div>
                        <h2 style="margin:0; color: #2e7d32;">🌾 SRI MANIKANTA TRADERS</h2>
                        <p style="margin:2px 0; font-size: 12px;">D:No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
                    </div>
                    <div style="text-align: right;">
                        <span style="border: 1px solid #333; padding: 3px 8px; font-weight: bold; background: #f0f0f0; font-size: 12px;">{copy_title}</span>
                    </div>
                </div>
                
                <table style="width: 100%; margin-top: 8px; font-size: 12px;">
                    <tr>
                        <td><b>Bill No:</b> {lb['bill_no']}</td>
                        <td><b>Date:</b> {lb['date']}</td>
                        <td style="text-align: right;"><b>Customer:</b> {lb['customer']} ({lb['mobile']})</td>
                    </tr>
                </table>

                <table style="width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 12px;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                            <th style="border: 1px solid #ddd; padding: 4px; width: 5%;">#</th>
                            <th style="border: 1px solid #ddd; padding: 4px; text-align: left;">Item Name</th>
                            <th style="border: 1px solid #ddd; padding: 4px; width: 10%;">Qty</th>
                            <th style="border: 1px solid #ddd; padding: 4px; width: 15%; text-align: right;">Rate</th>
                            <th style="border: 1px solid #ddd; padding: 4px; width: 15%; text-align: right;">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; font-size: 13px;">
                    <div><i>Thank You! Visit Again 🙏</i></div>
                    <div><b>Total Bill Amount: <span style="font-size: 15px; color: #d32f2f;">₹{lb['total']:.2f}</span></b></div>
                </div>
            </div>
            """

        a4_html = f"""
        <html>
        <head>
            <style>
                @media print {{
                    body {{ margin: 0; padding: 0; }}
                    .no-print {{ display: none; }}
                }}
            </style>
        </head>
        <body style="padding: 10px;">
            <button class="no-print" onclick="window.print()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; margin-bottom: 10px;">🖨️ Click to Print A4 Bill (2 Copies)</button>
            {generate_receipt_html("STORE COPY")}
            <div style="border-top: 1px dashed #666; margin: 15px 0; text-align: center; font-size: 10px; color: #666;">✂️ Cut Here ✂️</div>
            {generate_receipt_html("FARMER COPY")}
        </body>
        </html>
        """
        st.components.v1.html(a4_html, height=600, scrolling=True)

elif mode == "🔒 Admin Mode":
    st.sidebar.subheader("🔒 Admin Login Verification")
    
    if not st.session_state.admin_logged_in:
        with st.form("admin_login_form"):
            u_name = st.text_input("Username", value="admin")
            p_word = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login to Admin Panel", use_container_width=True)
            
            if login_btn:
                if u_name == "admin" and p_word == "samsri2528":
                    st.session_state.admin_logged_in = True
                    st.success("✅ Admin Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password!")
        st.stop()
    
    st.sidebar.success("🔓 Logged in as Admin")
    if st.sidebar.button("🚪 Logout Admin", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()

    admin_menu = st.sidebar.radio("Admin Management Menu", [
        "📊 Day-wise & Category Sales Report", 
        "💰 Cash Register (Opening/Closing)", 
        "🛠️ Stock, Price & Expiry Management"
    ])

    # ==================== REPORTS ====================
    if admin_menu == "📊 Day-wise & Category Sales Report":
        st.subheader("📊 Sales Analysis & Reports")
        sales_df = load_sales_history()

        if not sales_df.empty:
            tab1, tab2 = st.tabs(["📅 Day-wise Sales Report", "🏷️ Category-wise Report"])
            
            with tab1:
                filter_date = st.date_input("Select Date", datetime.now())
                selected_date_str = filter_date.strftime("%Y-%m-%d")
                filtered_sales = sales_df[sales_df["Date"] == selected_date_str]

                if not filtered_sales.empty:
                    st.success(f"Total Bills on {selected_date_str}: {len(filtered_sales)}")
                    st.dataframe(filtered_sales, use_container_width=True, hide_index=True)
                    st.metric("Total Day Collection", f"₹ {filtered_sales['Total Amount'].sum():.2f}")
                else:
                    st.warning(f"No sales recorded on {selected_date_str}.")

            with tab2:
                st.info("Category-wise sales & inventory breakdown.")
                if not df.empty:
                    cols = list(df.columns)
                    cat_col = next((c for c in cols if any(k in str(c).lower() for k in ["cat", "group"])), cols[0])
                    st.dataframe(df.groupby(cat_col).size().reset_index(name="Total Products in Category"), use_container_width=True)
        else:
            st.info("No sales history available yet.")

    # ==================== CASH REGISTER ====================
    elif admin_menu == "💰 Cash Register (Opening/Closing)":
        st.subheader("💰 Daily Cash Register")
        cash_df = load_cash_register()
        today_str = datetime.now().strftime("%Y-%m-%d")

        c1, c2, c3 = st.columns(3)
        with c1:
            opening_cash = st.number_input("Opening Cash Today (₹)", value=1000.0)
        with c2:
            cash_deposits = st.number_input("Cash Deposits / Bank Transfer (₹)", value=0.0)
        
        sales_df = load_sales_history()
        today_sales = sales_df[sales_df["Date"] == today_str]["Total Amount"].sum() if not sales_df.empty else 0.0
        
        st.metric("Today's Total Cash Sales", f"₹ {today_sales:.2f}")

        closing_cash = opening_cash + today_sales - cash_deposits
        st.markdown(f"### 💵 Calculated Closing Cash: ₹ {closing_cash:.2f}")

        if st.button("💾 Save Cash Register Entry", type="primary"):
            new_entry = pd.DataFrame([{
                "Date": today_str,
                "Opening Cash": opening_cash,
                "Cash Sales": today_sales,
                "Cash Deposits": cash_deposits,
                "Closing Cash": closing_cash
            }])
            if not cash_df.empty:
                cash_df = cash_df[cash_df["Date"] != today_str]
            pd.concat([cash_df, new_entry], ignore_index=True).to_excel(CASH_FILE, index=False)
            st.success("✅ Cash Register Saved Successfully!")

        if not cash_df.empty:
            st.markdown("---")
            st.subheader("📁 Cash History Log")
            st.dataframe(cash_df, use_container_width=True, hide_index=True)

    # ==================== ADMIN MANAGEMENT ====================
    elif admin_menu == "🛠️ Stock, Price & Expiry Management":
        st.subheader("🛠️ Inventory & Product Management (Admin)")
        
        if os.path.exists(EXCEL_FILE):
            with open(EXCEL_FILE, "rb") as f:
                st.download_button(
                    label="📥 Download Live Stock Excel (For Auditing)",
                    data=f,
                    file_name="Sri_Manikanta_Traders_Stock_Audit.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

        st.markdown("---")

        if not df.empty:
            cols = list(df.columns)
            item_col = next((c for c in cols if any(k in str(c).lower() for k in ["item", "product", "particular"])), cols[1] if len(cols) > 1 else cols[0])
            
            rate_matches = [c for c in cols if any(k in str(c).lower() for k in ["rate", "price", "mrp"])]
            rate_c = rate_matches[0] if rate_matches else cols[3] if len(cols) > 3 else cols[-1]

            stock_matches = [c for c in cols if any(k in str(c).lower() for k in ["qty", "stock", "quantity"])]
            stock_c = stock_matches[0] if stock_matches else cols[2] if len(cols) > 2 else cols[-1]

            cat_matches = [c for c in cols if any(k in str(c).lower() for k in ["cat", "group"])]
            cat_c = cat_matches[0] if cat_matches else cols[0]

            selected_edit_item = st.selectbox("Select Product to Modify", df[item_col].dropna().unique())
            item_idx = df[df[item_col] == selected_edit_item].index[0]

            st.write("Current Product Details:")
            st.dataframe(df[df[item_col] == selected_edit_item], use_container_width=True)

            with st.form("edit_form"):
                st.markdown("#### Update Details")
                current_p = float(df.loc[item_idx, rate_c]) if pd.notnull(df.loc[item_idx, rate_c]) else 0.0
                current_q = int(df.loc[item_idx, stock_c]) if pd.notnull(df.loc[item_idx, stock_c]) else 0

                new_price = st.number_input("New Rate / Price (₹)", value=current_p)
                new_qty = st.number_input("New Stock Quantity", value=current_q)
                
                update_btn = st.form_submit_button("Update Product in Excel")
                if update_btn:
                    df.loc[item_idx, rate_c] = new_price
                    df.loc[item_idx, stock_c] = new_qty
                    df.to_excel(EXCEL_FILE, index=False)
                    st.success(f"✅ Successfully updated {selected_edit_item}!")
                    st.rerun()

            st.markdown("---")
            st.markdown("#### ➕ Add New Product to Inventory")
            with st.form("new_product_form"):
                new_name = st.text_input("New Item Name")
                new_cat = st.text_input("Category (e.g., Pesticides, Fertilizers)", value="Pesticides")
                new_p = st.number_input("Price (₹)", value=100.0)
                new_q = st.number_input("Initial Quantity", value=50)
                
                add_sub_btn = st.form_submit_button("Add New Item")
                if add_sub_btn and new_name:
                    new_row = {col: None for col in cols}
                    new_row[item_col] = new_name
                    new_row[rate_c] = new_p
                    new_row[stock_c] = new_q
                    new_row[cat_c] = new_cat

                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_excel(EXCEL_FILE, index=False)
                    st.success(f"✅ Added {new_name} successfully!")
                    st.rerun()
