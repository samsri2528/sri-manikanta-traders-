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
            "Items",
            "Total Amount (₹)",
            "Paid (₹)",
            "Balance (₹)",
        ]
    )


def save_sales(df):
  df.to_excel(SALES_FILE, index=False)


def load_cash_deposits():
  if os.path.exists(CASH_BOOK_FILE):
    return pd.read_excel(CASH_BOOK_FILE)
  else:
    return pd.DataFrame(columns=["Date", "Description", "Amount (₹)"])


def save_cash_deposits(df):
  df.to_excel(CASH_BOOK_FILE, index=False)


# Authentication State
if "authenticated" not in st.session_state:
  st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
  col1, col2 = st.columns([1.2, 1])
  with col1:
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists("banner.png"):
      st.image("banner.png", use_container_width=True)
    st.markdown("### 🌾 Welcome to Sri Manikanta Traders")
    st.write(
        "Manage inventory, sales, and digital billing seamlessly at D.No"
        " 6/159/25, Pedda Harivanam."
    )
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
  st.sidebar.title("🌾 SRI MANIKANTA TRADERS")
  menu = st.sidebar.radio(
      "Navigation",
      [
          "Billing & Sales",
          "Manage Inventory",
          "Present / Closing Stock",
          "Sales History",
          "Cash Book",
      ],
  )

  if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    if "cart" in st.session_state:
      st.session_state["cart"] = []
    if "last_bill" in st.session_state:
      del st.session_state["last_bill"]
    st.rerun()

  # Module Implementation
  if menu == "Billing & Sales":
    st.title("🛒 Billing & Sales Dashboard")
    inv_df = load_inventory()

    if "cart" not in st.session_state:
      st.session_state["cart"] = []

    col_a, col_b = st.columns([2, 1])
    with col_a:
      customer_name = st.text_input("Customer Name")
      if not inv_df.empty:
        selected_item = st.selectbox(
            "Select Item", inv_df["Item Name"].tolist()
        )
        item_row = inv_df[inv_df["Item Name"] == selected_item].iloc[0]
        available_qty = item_row["Quantity"]
        item_price = item_row["Price (₹)"]

        st.write(
            f"Available Quantity: **{available_qty}** | Price per unit:"
            f" **₹{item_price}**"
        )
        qty_to_buy = st.number_input(
            "Quantity", min_value=1, max_value=int(max(1, available_qty)), step=1
        )

        if st.button("Add to Cart"):
          if qty_to_buy > available_qty:
            st.error("Not enough stock available!")
          else:
            st.session_state["cart"].append({
                "Item": selected_item,
                "Price": item_price,
                "Quantity": qty_to_buy,
                "Total": item_price * qty_to_buy,
            })
            st.success("Item added to cart!")

    with col_b:
      st.subheader("🛍️ Current Cart")
      if st.session_state["cart"]:
        cart_df = pd.DataFrame(st.session_state["cart"])
        st.dataframe(cart_df, use_container_width=True)
        grand_total = cart_df["Total"].sum()
        st.markdown(f"### Grand Total: ₹{grand_total}")

        paid_amount = st.number_input("Amount Paid (₹)", min_value=0.0, step=10.0)

        if st.button("Complete Sale & Generate Bill"):
          if not customer_name:
            st.warning("Please enter customer name.")
          else:
            sales_df = load_sales()
            new_bill_no = (
                len(sales_df) + 1
            )  # Simple incrementing bill number
            balance_amt = grand_total - paid_amount

            # Update Inventory
            for item in st.session_state["cart"]:
              inv_df.loc[
                  inv_df["Item Name"] == item["Item"], "Quantity"
              ] -= item["Quantity"]
            save_inventory(inv_df)

            # Save Sale Record
            new_sale = {
                "Bill No": new_bill_no,
                "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                "Customer Name": customer_name,
                "Items": str(st.session_state["cart"]),
                "Total Amount (₹)": grand_total,
                "Paid (₹)": paid_amount,
                "Balance (₹)": balance_amt,
            }
            sales_df = pd.concat(
                [sales_df, pd.DataFrame([new_sale])], ignore_index=True
            )
            save_sales(sales_df)

            st.session_state["last_bill"] = new_sale
            st.session_state["cart"] = []
            st.success("Sale completed successfully!")
      else:
        st.info("Cart is empty.")

  elif menu == "Manage Inventory":
    st.title("📦 Inventory Management")
    inv_df = load_inventory()

    with st.form("add_item_form"):
      st.subheader("Add New Item / Restock")
      new_item = st.text_input("Item Name")
      new_cat = st.text_input("Category")
      new_qty = st.number_input("Quantity", min_value=0, step=1)
      new_price = st.number_input("Price per Unit (₹)", min_value=0.0, step=1.0)
      submit_item = st.form_submit_button("Save Item")

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
        st.success("Inventory updated successfully!")
        st.rerun()

    st.dataframe(inv_df, use_container_width=True)

  elif menu == "Present / Closing Stock":
    st.title("📊 Present / Closing Stock Summary")
    inv_df = load_inventory()
    st.dataframe(inv_df, use_container_width=True)
    if not inv_df.empty:
      total_stock_value = (inv_df["Quantity"] * inv_df["Price (₹)"]).sum()
      st.markdown(f"### Total Stock Value: ₹{total_stock_value}")

  elif menu == "Sales History":
    st.title("📜 Sales History Records")
    sales_df = load_sales()
    st.dataframe(sales_df, use_container_width=True)

  elif menu == "Cash Book":
    st.title("📒 Cash Book Ledger")
    cash_df = load_cash_deposits()
    with st.form("cash_form"):
      desc = st.text_input("Description / Notes")
      amount = st.number_input("Amount (₹)", step=10.0)
      submitted = st.form_submit_button("Add Entry")
      if submitted and desc:
        new_entry = pd.DataFrame(
            [[pd.Timestamp.now().strftime("%Y-%m-%d"), desc, amount]],
            columns=["Date", "Description", "Amount (₹)"],
        )
        cash_df = pd.concat([cash_df, new_entry], ignore_index=True)
        save_cash_deposits(cash_df)
        st.success("Cash entry added!")
        st.rerun()
    st.dataframe(cash_df, use_container_width=True)
