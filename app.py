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


def load_cash_deposits():
  if os.path.exists(CASH_BOOK_FILE):
    return pd.read_excel(CASH_BOOK_FILE)
  else:
    return pd.DataFrame(columns=["Date", "Description", "Amount (₹)"])


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

  # Main Module Logic Placeholder
  if menu == "Billing & Sales":
    st.title("🛒 Billing & Sales Dashboard")
    st.write("Billing module is active.")
  elif menu == "Manage Inventory":
    st.title("📦 Inventory Management")
    inv_df = load_inventory()
    st.dataframe(inv_df, use_container_width=True)
  elif menu == "Present / Closing Stock":
    st.title("📊 Closing Stock Summary")
  elif menu == "Sales History":
    st.title("📜 Sales History Records")
  elif menu == "Cash Book":
    st.title("📒 Cash Book Ledger")
