from datetime import datetime
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="SRI MANIKANTA TRADERS", page_icon="📦", layout="wide"
)

# Custom Styles
st.markdown(
    """
<style>
    .stApp { background-color: #fdfbf7; }
    .stButton>button { background-color: #b80000; color: white; border-radius: 6px; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #5c0000; color: white; }
</style>
""",
    unsafe_allow_html=True,
)

# Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1aH4PE3alu_NYigh343N_FSoza0wEwk3oZlKmF-Hdf/edit?gid=82672227#gid=82672227"


# 1. Login Function
def check_login():
  if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

  if not st.session_state.authenticated:
    st.title("🔒 Sri Manikanta Traders - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
      if username == "manikanta" and password == "samsri2528":
        st.session_state.authenticated = True
        st.rerun()
      else:
        st.error("తప్పు యూజర్‌నేమ్ లేదా పాస్‌వర్డ్")
    return False
  return True


# 2. Stock Add Password Check Function
def check_stock_password():
  if "stock_auth" not in st.session_state:
    st.session_state.stock_auth = False

  if not st.session_state.stock_auth:
    st.subheader("🔐 New Stock Authorization Required")
    s_pass = st.text_input(
        "Enter Stock Password to Add/Modify", type="password", key="s_pass_input"
    )
    if st.button("Verify Stock Password"):
      if s_pass == "samsri25285":
        st.session_state.stock_auth = True
        st.rerun()
      else:
        st.error("Invalid Password!")
    return False
  return True


# Main App Execution
if check_login():
  st.title("Sri Manikanta Traders - Billing & Inventory System")

  # Sidebar Navigation
  menu = st.sidebar.selectbox(
      "Select Menu", ["Billing", "Deposit", "Cash Book", "Closing Stock"]
  )

  # --- BILLING TAB ---
  if menu == "Billing":
    st.header("🛒 Billing Section")
    st.write("ఇక్కడ కొత్త బిల్లు తయారు చేయవచ్చు.")

    with st.form("billing_form"):
      customer_name = st.text_input("Customer Name")
      product_list = ["Item A", "Item B", "Item C"]
      selected_product = st.selectbox("Select Product", product_list)

      quantity = st.number_input("Quantity", min_value=1, step=1)
      price_per_item = st.number_input("Price per Unit", min_value=0.0, step=0.1)

      total_amount = quantity * price_per_item
      st.info(f"**Total Amount: ₹ {total_amount:.2f}**")

      submit_bill = st.form_submit_button("Generate & Save Bill")

      if submit_bill:
        if customer_name:
          st.success(
              f"సక్సెస్‌ఫుల్‌గా బిల్ క్రియేట్ చేయబడింది! కస్టమర్:"
              f" {customer_name}, మొత్తం: ₹{total_amount:.2f}"
          )
        else:
          st.error("దయచేసి కస్టమర్ పేరు నమోదు చేయండి!")

  # --- DEPOSIT TAB ---
  elif menu == "Deposit":
    st.header("💰 Deposit Section")
    st.write("ఇక్కడ క్యాష్ డిపాజిట్ వివరాలు నమోదు చేయండి.")

  # --- CASH BOOK TAB ---
  elif menu == "Cash Book":
    st.header("📖 Cash Book")
    st.write("రోజవారీ లావాదేవీలు (Cash In / Cash Out).")

  # --- CLOSING STOCK TAB ---
  elif menu == "Closing Stock":
    st.header("📦 Closing Stock (Excel / Google Sheet)")
    st.write("ఇక్కడ మీ ప్రస్తుత స్టాక్ వివరాలు కనిపిస్తాయి.")

    try:
      data = {
          "Product Name": ["Item A", "Item B", "Item C"],
          "Quantity": [100, 50, 200],
          "Price": [500, 1200, 300],
          "Last Updated": [
              str(datetime.now().date()),
              str(datetime.now().date()),
              str(datetime.now().date()),
          ],
      }
      df = pd.DataFrame(data)
      st.dataframe(df, use_container_width=True)
    except Exception as e:
      st.warning("గూగుల్ షీట్ డేటా లోడ్ కాలేదు.")

    st.markdown("---")
    st.subheader("➕ Add New Stock")

    if check_stock_password():
      with st.form("new_stock_form"):
        new_item = st.text_input("Product Name")
        new_qty = st.number_input("Quantity", min_value=0, step=1)
        new_price = st.number_input("Price", min_value=0.0, step=0.1)
        submit_stock = st.form_submit_button("Save Stock")

        if submit_stock:
          st.success(
              f"సక్సెస్‌ఫుల్‌గా '{new_item}' స్టాక్ యాడ్ చేయబడింది!"
          )
