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
    .bill-box { border: 2px solid #444; padding: 15px; border-radius: 5px; background-color: white; margin-bottom: 20px; font-family: Arial, sans-serif; }
    .header-title { text-align: center; font-weight: bold; font-size: 18px; color: #4a0000; }
    .sub-text { text-align: center; font-size: 12px; color: #333; }
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

    with st.form("billing_form"):
      col1, col2 = st.columns(2)
      with col1:
        customer_name = st.text_input("Customer Name (చక్)")
        mobile = st.text_input("Mobile Number", value="7995217343")
      with col2:
        bill_no = st.text_input("Bill No", value="SMT-003")
        village = st.text_input("Village", value="Pedda Harivanam")

      product_name = st.selectbox(
          "Item Name", ["Organick DAP 50KG", "Item B", "Item C"]
      )
      col3, col4 = st.columns(2)
      with col3:
        quantity = st.number_input("Quantity", min_value=1.0, value=1.0, step=1.0)
      with col4:
        price = st.number_input("Price", min_value=0.0, value=1000.0, step=10.0)

      submit_bill = st.form_submit_button("Generate Bill Preview")

    if submit_bill:
      total_val = quantity * price

      # Function to render a single copy (Farmer or Store)
      def render_bill_copy(copy_type):
        st.markdown(
            f"""
                <div class="bill-box">
                    <div class="header-title">SRI MANIKANTA TRADERS</div>
                    <div class="sub-text">D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal | Ph: 7995217343</div>
                    <div style="text-align: center; font-weight: bold; margin-top: 5px; color: #b80000;">{copy_type}</div>
                    <hr style="margin: 5px 0;">
                    <table width="100%" style="font-size: 13px;">
                        <tr>
                            <td><b>Bill No:</b> {bill_no}</td>
                            <td><b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}</td>
                        </tr>
                        <tr>
                            <td><b>Customer:</b> {customer_name}</td>
                            <td><b>Village:</b> {village}</td>
                        </tr>
                        <tr>
                            <td><b>Mobile:</b> {mobile}</td>
                            <td><b>Aadhaar:</b> N/A</td>
                        </tr>
                    </table>
                    <hr style="margin: 5px 0;">
                    <table width="100%" style="font-size: 13px; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid #ddd;">
                            <th align="left">Item Name</th>
                            <th align="center">Qty</th>
                            <th align="right">Price</th>
                            <th align="right">Total</th>
                        </tr>
                        <tr>
                            <td>{product_name}</td>
                            <td align="center">{quantity}</td>
                            <td align="right">₹{price:.1f}</td>
                            <td align="right">₹{total_val:.1f}</td>
                        </tr>
                    </table>
                    <hr style="margin: 5px 0;">
                    <div style="text-align: right; font-weight: bold; font-size: 14px;">
                        Grand Total: ₹ {total_val:.1f}
                    </div>
                    <br><br>
                    <table width="100%" style="font-size: 12px; margin-top: 20px;">
                        <tr>
                            <td>-----------------------------------------</td>
                            <td align="right">-----------------------------------------</td>
                        </tr>
                        <tr>
                            <td>Farmer Signature</td>
                            <td align="right">SMT Signature</td>
                        </tr>
                    </table>
                </div>
                """,
            unsafe_allow_html=True,
        )

      st.markdown("### 📄 Bill Preview (Farmer Copy & Store Copy)")

      # Farmer Copy
      render_bill_copy("FARMER COPY")

      # Dotted cutting line
      st.markdown(
          "<p style='text-align:center; border-bottom: 2px dashed"
          " gray;'></p>",
          unsafe_allow_html=True,
      )
      st.write("")

      # Store Copy
      render_bill_copy("STORE COPY")

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
