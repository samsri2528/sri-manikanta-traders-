import io
import os
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="SRI MANIKANTA TRADERS", page_icon="🌾", layout="wide"
)

# Custom Styles
st.markdown(
    """
    <style>
    .stApp { background-color: #fdfbf7; }
    .stButton>button { background-color: #8b0000; color: white; border-radius: 6px; font-weight: bold; }
    .stButton>button:hover { background-color: #5c0000; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Data Files
INVENTORY_FILE = "inventory.xlsx"
SALES_FILE = "sales_history.xlsx"
CASH_BOOK_FILE = "cash_book_deposits.xlsx"


def load_inventory():
  if os.path.exists(INVENTORY_FILE):
    return pd.read_excel(INVENTORY_FILE)
  else:
    df = pd.DataFrame(
        columns=["Item Name", "Category", "Quantity", "Price (₹)"]
    )
    df.to_excel(INVENTORY_FILE, index=False)
    return df


def save_inventory(df):
  df.to_excel(INVENTORY_FILE, index=False)


def load_sales():
  if os.path.exists(SALES_FILE):
    return pd.read_excel(SALES_FILE)
  else:
    return pd.DataFrame(
        columns=[
            "Bill No",
            "Date",
            "Customer Name",
            "Mobile",
            "Item Name",
            "Quantity",
            "Price",
            "Total Amount",
            "Aadhaar No",
            "Village",
        ]
    )


def save_sales(df):
  df.to_excel(SALES_FILE, index=False)


def load_cash_deposits():
  if os.path.exists(CASH_BOOK_FILE):
    return pd.read_excel(CASH_BOOK_FILE)
  else:
    return pd.DataFrame(
        columns=[
            "Date",
            "Description",
            "Deposit Amount (₹)",
            "Receipt Name",
            "Bill No",
        ]
    )


def save_cash_deposits(df):
  df.to_excel(CASH_BOOK_FILE, index=False)


# Authentication State
if "authenticated" not in st.session_state:
  st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
  st.markdown(
      """
      <div style="border: 2px solid #8b0000; padding: 15px; border-radius: 10px; background-color: #ffffff; text-align: center; margin: 15px auto;">
          <h2 style="color: #8b0000; margin: 0;">SRI MANIKANTA TRADERS</h2>
          <p style="color: #444; font-size: 15px; font-weight: 500; margin: 0;">D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
      </div>
      """,
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns([1.2, 1])
  with col1:
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists("banner.png"):
      st.image("banner.png", use_container_width=True)
    st.markdown("### 🌾 Welcome to Sri Manikanta Traders")
    st.write("Manage inventory, sales, and digital billing seamlessly.")
  with col2:
    with st.container():
      st.markdown("### 🔐 ADMIN LOGIN")
      username = st.text_input("Username")
      password = st.text_input("Password", type="password")
      if st.button("Sign In"):
        if username == "admin" and password == "samsri2528":
          st.session_state["authenticated"] = True
          st.rerun()
        else:
          st.error("❌ Invalid Username or Password")
else:
  st.sidebar.title("SRI MANIKANTA TRADERS")
  menu = st.sidebar.radio(
      "Navigation",
      [
          "Billing & Sales",
          "Manage Inventory",
          "Present / Closing Stock",
          "Sales History & Reports",
          "Cash Book",
      ],
  )

  if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    if "cart" in st.session_state:
      st.session_state["cart"] = []
    st.rerun()

  # 1. Billing & Sales Module
  if menu == "Billing & Sales":
    st.markdown(
        """
        <div style="border: 2px solid #8b0000; padding: 12px; border-radius: 8px; background-color: #ffffff; text-align: center; margin-bottom: 15px;">
            <h2 style="color: #8b0000; margin: 0;">Sales Invoice & Billing</h2>
            <p style="color: #444; font-size: 13px; margin: 0;">D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    inv_df = load_inventory()
    sales_df = load_sales()
    cash_df = load_cash_deposits()

    if "cart" not in st.session_state:
      st.session_state["cart"] = []

    col_bill1, col_bill2, col_bill3 = st.columns(3)
    with col_bill1:
      existing_bills = sales_df["Bill No"].unique() if not sales_df.empty else []
      next_bill_no = (
          f"SMT-{len(existing_bills)+1:03d}" if len(existing_bills) > 0 else "SMT-001"
      )
      bill_no = st.text_input("Bill No", value=next_bill_no)
    with col_bill2:
      bill_date = st.text_input(
          "Date (DD-MM-YYYY)", value=pd.Timestamp.now().strftime("%d-%m-%Y")
      )
    with col_bill3:
      customer_mobile = st.text_input("Mobile No (10 Digits)")

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
      customer_name = st.text_input("Customer / Farmer Name")
    with col_c2:
      village_name = st.text_input(
          "Village Name", value="Pedda Harivanam"
      )
    with col_c3:
      aadhaar_no = st.text_input("Aadhaar No (Optional)")

    st.markdown("### 🛒 Add Items to Bill Cart")
    if not inv_df.empty:
      col_item1, col_item2, col_item3 = st.columns([2, 1, 1])
      with col_item1:
        selected_item = st.selectbox(
            "Select Product", inv_df["Item Name"].tolist()
        )
      item_row = inv_df[inv_df["Item Name"] == selected_item].iloc[0]
      available_qty = item_row["Quantity"]
      item_price = item_row["Price (₹)"]

      with col_item2:
        qty_to_buy = st.number_input(
            "Quantity",
            min_value=1.0,
            max_value=float(max(1.0, available_qty)),
            step=1.0,
        )
      with col_item3:
        custom_price = st.number_input(
            "Price (₹)", value=float(item_price), step=1.0
        )

      st.write(
          f"📦 **Available Stock for {selected_item}:** {available_qty}"
          " units/kg"
      )

      if st.button("➕ Add Item"):
        if qty_to_buy > available_qty:
          st.error("❌ Not enough stock available!")
        else:
          st.session_state["cart"].append({
              "Item Name": selected_item,
              "Quantity": qty_to_buy,
              "Price": custom_price,
              "Total Amount": qty_to_buy * custom_price,
          })
          st.success("✅ Item added to cart!")

    if st.session_state["cart"]:
      st.markdown("### 📋 Cart Items")
      cart_df = pd.DataFrame(st.session_state["cart"])
      st.dataframe(cart_df, use_container_width=True)

      grand_total = cart_df["Total Amount"].sum()
      st.markdown(f"### 💰 Grand Total: ₹ {grand_total:,.2f}")

      col_act1, col_act2 = st.columns(2)
      with col_act1:
        if st.button("💾 Save Bill & Complete Sale"):
          if not customer_name:
            st.warning("⚠️ Please enter Customer Name.")
          else:
            new_sales_rows = []
            for item in st.session_state["cart"]:
              new_sales_rows.append({
                  "Bill No": bill_no,
                  "Date": bill_date,
                  "Customer Name": customer_name,
                  "Mobile": customer_mobile,
                  "Item Name": item["Item Name"],
                  "Quantity": item["Quantity"],
                  "Price": item["Price"],
                  "Total Amount": item["Total Amount"],
                  "Aadhaar No": aadhaar_no,
                  "Village": village_name,
              })

              inv_df.loc[
                  inv_df["Item Name"] == item["Item Name"], "Quantity"
              ] -= item["Quantity"]

            save_inventory(inv_df)

            updated_sales_df = pd.concat(
                [sales_df, pd.DataFrame(new_sales_rows)], ignore_index=True
            )
            save_sales(updated_sales_df)

            if "Bill No" not in cash_df.columns:
              cash_df["Bill No"] = ""

            new_cash_row = pd.DataFrame(
                [[
                    bill_date,
                    f"Bill Collection - {customer_name} ({bill_no})",
                    grand_total,
                    "Sales Bill",
                    bill_no,
                ]],
                columns=[
                    "Date",
                    "Description",
                    "Deposit Amount (₹)",
                    "Receipt Name",
                    "Bill No",
                ],
            )
            updated_cash_df = pd.concat(
                [cash_df, new_cash_row], ignore_index=True
            )
            save_cash_deposits(updated_cash_df)

            st.session_state["cart"] = []
            st.success(
                f"🎉 Bill {bill_no} saved, stock updated, and cash book"
                " credited!"
            )
            st.rerun()

      with col_act2:
        bill_text = f"""
        ========================================
                SRI MANIKANTA TRADERS
        D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal
        Ph: 7995217343
        ========================================
        Bill No   : {bill_no}
        Date      : {bill_date}
        Customer  : {customer_name}
        Mobile    : {customer_mobile}
        Village   : {village_name}
        Aadhaar   : {aadhaar_no}
        ----------------------------------------
        """
        for item in st.session_state["cart"]:
          bill_text += f"{item['Item Name']} | Qty: {item['Quantity']} | Price: ₹{item['Price']} | Total: ₹{item['Total Amount']}\n"
        bill_text += f"----------------------------------------\n"
        bill_text += f"GRAND TOTAL: ₹ {grand_total:,.2f}\n"
        bill_text += f"========================================\n"
        bill_text += f"Thank You! Visit Again.\n"

        st.download_button(
            label="🖨️ Print / Download Bill Text",
            data=bill_text,
            file_name=f"{bill_no}_{customer_name}.txt",
            mime="text/plain",
        )

  # 2. Manage Inventory Module
  elif menu == "Manage Inventory":
    st.markdown(
        """
        <div style="border: 2px solid #8b0000; padding: 12px; border-radius: 8px; background-color: #ffffff; text-align: center; margin-bottom: 15px;">
            <h2 style="color: #8b0000; margin: 0;">Inventory & Stock Management</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    inv_df = load_inventory()

    with st.form("add_item_form"):
      st.subheader("Add New Item / Restock")
      col_i1, col_i2 = st.columns(2)
      with col_i1:
        new_item = st.text_input("Product / Item Name")
        new_cat = st.selectbox(
            "Category", ["Fertilizers", "Pesticides", "Seeds", "Others"]
        )
      with col_i2:
        new_qty = st.number_input("Initial Quantity", min_value=0.0, step=1.0)
        new_price = st.number_input(
            "Price per Unit (₹)", min_value=0.0, step=1.0
        )
      submit_item = st.form_submit_button("💾 Save Item to Inventory")

      if submit_item and new_item:
        if new_item in inv_df["Item Name"].values:
          inv_df.loc[inv_df["Item Name"] == new_item, "Quantity"] += new_qty
          inv_df.loc[inv_df["Item Name"] == new_item, "Price (₹)"] = new_price
        else:
          new_row = pd.DataFrame(
              [[new_item, new_cat, new_qty, new_price]],
              columns=["Item Name", "Category", "Quantity", "Price (₹)"],
          )
          inv_df = pd.concat([inv_df, new_row], ignore_index=True)
        save_inventory(inv_df)
        st.success("✅ Inventory updated successfully!")
        st.rerun()

    st.markdown("### 📦 Current Stock List")
    st.dataframe(inv_df, use_container_width=True)

  # 3. Closing Stock Module (Fixed Export)
  elif menu == "Present / Closing Stock":
    st.markdown(
        """
        <div style="border: 2px solid #8b0000; padding: 12px; border-radius: 8px; background-color: #ffffff; text-align: center; margin-bottom: 15px;">
            <h2 style="color: #8b0000; margin: 0;">Store Closing Stock Details</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    inv_df = load_inventory()
    st.dataframe(inv_df, use_container_width=True)

    if not inv_df.empty:
      total_val = (inv_df["Quantity"] * inv_df["Price (₹)"]).sum()
      st.markdown(f"### 💎 Total Stock Valuation: ₹ {total_val:,.2f}")

      col_dl1, col_dl2 = st.columns(2)
      with col_dl1:
        csv_data = inv_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Closing Stock as CSV",
            data=csv_data,
            file_name=f"Closing_Stock_{pd.Timestamp.now().strftime('%d-%m-%Y')}.csv",
            mime="text/csv",
        )
      with col_dl2:
        txt_data = inv_df.to_string(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Closing Stock Summary",
            data=txt_data,
            file_name=f"Closing_Stock_{pd.Timestamp.now().strftime('%d-%m-%Y')}.txt",
            mime="text/plain",
        )

  # 4. Sales History & Delete Bill Module
  elif menu == "Sales History & Reports":
    st.markdown(
        """
        <div style="border: 2px solid #8b0000; padding: 12px; border-radius: 8px; background-color: #ffffff; text-align: center; margin-bottom: 15px;">
            <h2 style="color: #8b0000; margin: 0;">Sales History & Management</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    sales_df = load_sales()

    if not sales_df.empty:
      st.markdown("### 🗑️ Delete Bill, Restore Stock & Update Cash Book")
      unique_bills = sales_df["Bill No"].unique().tolist()
      bill_to_delete = st.selectbox("Select Bill No to Delete", unique_bills)

      if st.button("⚠️ Delete Bill & Auto-Update Stock & Cash Book"):
        bill_items = sales_df[sales_df["Bill No"] == bill_to_delete]
        inv_df = load_inventory()

        for index, row in bill_items.iterrows():
          item_name = row["Item Name"]
          qty_to_restore = row["Quantity"]
          if item_name in inv_df["Item Name"].values:
            inv_df.loc[inv_df["Item Name"] == item_name, "Quantity"] += (
                qty_to_restore
            )
        save_inventory(inv_df)

        sales_df = sales_df[sales_df["Bill No"] != bill_to_delete]
        save_sales(sales_df)

        cash_df = load_cash_deposits()
        if "Bill No" in cash_df.columns:
          cash_df = cash_df[cash_df["Bill No"] != bill_to_delete]
        else:
          cash_df = cash_df[~cash_df["Description"].str.contains(bill_to_delete)]
        save_cash_deposits(cash_df)

        st.success(
            f"✅ Bill {bill_to_delete} deleted successfully! Stock restored and"
            " Cash Book updated."
        )
        st.rerun()

      st.markdown("### 📜 All Bills History (Newest on Top)")
      st.dataframe(sales_df.iloc[::-1], use_container_width=True)
    else:
      st.info("No sales records found.")

  # 5. Cash Book Module (With Net Balance)
  elif menu == "Cash Book":
    st.markdown(
        """
        <div style="border: 2px solid #8b0000; padding: 12px; border-radius: 8px; background-color: #ffffff; text-align: center; margin-bottom: 15px;">
            <h2 style="color: #8b0000; margin: 0;">Cash Book & Bank Ledger</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cash_df = load_cash_deposits()

    with st.form("cash_form"):
      col_cb1, col_cb2 = st.columns(2)
      with col_cb1:
        deposit_date = st.text_input(
            "Deposit Date", value=pd.Timestamp.now().strftime("%d-%m-%Y")
        )
        desc = st.text_input("Description / Bank Name")
      with col_cb2:
        amount = st.number_input("Deposit Amount (₹)", min_value=0.0, step=10.0)
        receipt_file = st.text_input(
            "Receipt Name / Notes (Optional)", value="No Receipt"
        )

      submitted = st.form_submit_button("💾 Save Bank Deposit & Receipt")
      if submitted and desc:
        if "Bill No" not in cash_df.columns:
          cash_df["Bill No"] = ""
        new_entry = pd.DataFrame(
            [[deposit_date, desc, amount, receipt_file, "Manual"]],
            columns=[
                "Date",
                "Description",
                "Deposit Amount (₹)",
                "Receipt Name",
                "Bill No",
            ],
        )
        cash_df = pd.concat([cash_df, new_entry], ignore_index=True)
        save_cash_deposits(cash_df)
        st.success("✅ Cash entry added successfully!")
        st.rerun()

    st.markdown("### 📊 Bank Deposit History & Receipts")
    display_cash_df = (
        cash_df[["Date", "Description", "Deposit Amount (₹)", "Receipt Name"]]
        if "Receipt Name" in cash_df.columns
        else cash_df
    )
    st.dataframe(display_cash_df, use_container_width=True)

    if not cash_df.empty and "Deposit Amount (₹)" in cash_df.columns:
      total_deposit = cash_df["Deposit Amount (₹)"].sum()
      st.markdown(
          f"### 💎 Total Net Cash Balance (Closing Balance): ₹"
          f" {total_deposit:,.2f}"
      )
