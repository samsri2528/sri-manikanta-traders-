import sqlite3
import streamlit as st

# డేటాబేస్ కనెక్షన్
conn = sqlite3.connect('stock_db.db', check_same_thread=False)
cursor = conn.cursor()

# టేబుల్ క్రియేట్ చేయడం
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS stock_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
"""
)
conn.commit()

# సెషన్ స్టేట్ ఇనిషియలైజేషన్
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
  st.session_state.role = ""

st.title("స్టాక్ మేనేజ్‌మెంట్ సిస్టమ్")

# 1. లాగిన్ సెక్షన్
if not st.session_state.logged_in:
  st.subheader("లాగిన్ అవ్వండి")
  username = st.text_input("యూజర్‌నేమ్")
  password = st.text_input("పాస్‌వర్డ్", type="password")

  if st.button("లాగిన్"):
    if username == "admin" and password == "manikanta123":
      st.session_state.logged_in = True
      st.session_state.role = "admin"
      st.rerun()
    elif username == "manikanta" and password == "samsri2528":
      st.session_state.logged_in = True
      st.session_state.role = "staff"
      st.rerun()
    else:
      st.error("యూజర్‌నేమ్ లేదా పాస్‌వర్డ్ తప్పుగా ఉంది!")

# 2. స్టాక్ యాడ్ చేసే సెక్షన్
else:
  if st.button("లాగౌట్ (Logout)"):
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.rerun()

  st.subheader("కొత్త స్టాక్ యాడ్ చేయండి")
  item_name = st.text_input("వస్తువు పేరు (Item Name)")
  quantity = st.number_input("పరిమాణం (Quantity)", min_value=1, step=1)
  price = st.number_input("ధర (Price)", min_value=0.0, format="%.2f")
  auth_code = st.text_input(
      "స్టాక్ కోడ్ (samsri25285)", type="password", placeholder="samsri25285"
  )

  if st.button("స్టాక్ సేవ్ చేయి"):
    if auth_code == "samsri25285":
      cursor.execute(
          "INSERT INTO stock_items (item_name, quantity, price) VALUES (?, ?,"
          " ?)",
          (item_name, quantity, price),
      )
      conn.commit()
      st.success("కొత్త స్టాక్ విజయవంతంగా యాడ్ చేయబడింది!")
    else:
      st.error("స్టాక్ యాడ్ చేయడానికి తప్పు సీక్రెట్ కోడ్ ఎంటర్ చేసారు!")
