from datetime import datetime
import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="SRI MANIKANTA TRADERS", page_icon="🛒", layout="wide"
)

# Custom Styles (మీరు స్క్రీన్‌షాట్‌లో వాడిన స్టైల్స్)
st.markdown(
    """
<style>
    .stApp { background-color: #fdfbf7; }
    .stButton>button { background-color: #8b0000; color: white; border-radius: 6px; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #5c0000; color: white; }
</style>
""",
    unsafe_allow_html=True,
)

# --- డేటా పర్మనెంట్ స్టోరేజ్ (2 సంవత్సరాలు సేవ్ అయి ఉండటానికి) ---
SALES_FILE = "Sales_History.xlsx"
OWNER_ID = "admin123"  # మీ ఓనర్ ID ఇక్కడ సెట్ చేసుకోండి

if not os.path.exists(SALES_FILE):
  df_init = pd.DataFrame(
      columns=["Date", "Year", "Item", "Quantity", "Price", "Total", "Added_By"]
  )
  df_init.to_excel(SALES_FILE, index=False)


def load_data():
  return pd.read_excel(SALES_FILE)


def save_data(df):
  df.to_excel(SALES_FILE, index=False)


# Main Application Title
st.title("🛒 SRI MANIKANTA TRADERS - సేల్స్ మేనేజ్‌మెంట్ సిస్టమ్")

# సైడ్‌బార్‌లో యూజర్ / ఓనర్ లాగిన్
st.sidebar.header("యూజర్ / ఓనర్ లాగిన్")
user_id = st.sidebar.text_input("మీ ID నమోదు చేయండి:")

# ఎక్సెల్ నుండి డేటాను లోడ్ చేయడం (డేటా ఎప్పుడూ పోదు)
df = load_data()

# 1. కొత్త రికార్డ్ జోడించడం
st.subheader("కొత్త రికార్డ్ జోడించండి")
with st.form("sales_form"):
  item_name = st.text_input("ఐటమ్ పేరు")
  quantity = st.number_input("పరిమాణం (Quantity)", min_value=1, value=1)
  price = st.number_input("ధర (Price)", min_value=0.0, value=0.0)
  submit_btn = st.form_submit_button("సేవ్ చేయి")

  if submit_btn:
    if item_name:
      current_time = datetime.now()
      current_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
      current_year = str(current_time.year)

      new_data = {
          "Date": current_date,
          "Year": current_year,
          "Item": item_name,
          "Quantity": quantity,
          "Price": price,
          "Total": quantity * price,
          "Added_By": user_id if user_id else "Guest",
      }
      # డేటాను పర్మనెంట్‌గా ఎక్సెల్ ఫైల్‌లో సేవ్ చేయడం
      df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
      save_data(df)
      st.success("డేటా విజయవంతంగా సేవ్ చేయబడింది మరియు 2 సంవత్సరాలు భద్రంగా ఉంటుంది!")
      st.rerun()
    else:
      st.warning("దయచేసి ఐటమ్ పేరు నమోదు చేయండి.")

# 2. సేల్స్ హిస్టరీ మరియు ఇయర్ ఫిల్టర్
st.subheader("సేల్స్ హిస్టరీ (Sales History - 2 Years Record)")
if not df.empty:
  if "Year" in df.columns:
    years_list = sorted(df["Year"].dropna().unique().tolist(), reverse=True)
    selected_year = st.selectbox(
        "సంవత్సరం వారీగా ఫిల్టర్ చేయండి:", ["అన్ని సంవత్సరాలు"] + years_list
    )

    if selected_year != "అన్ని సంవత్సరాలు":
      filtered_df = df[df["Year"] == str(selected_year)]
    else:
      filtered_df = df

    st.dataframe(filtered_df, use_container_width=True)
  else:
    st.dataframe(df, use_container_width=True)
else:
  st.info("ఇതുవరకు ఎలాంటి డేటా లేదు.")

# 3. డేటా తొలగింపు నియంత్రణ (Owner Control - కేవలం ఓనర్ ఐడీ ఉన్నవారికే)
st.subheader("డేటా తొలగింపు నియంత్రణ (Owner Control)")
if user_id == OWNER_ID:
  st.success("✨ మీరు ఓనర్ లాగిన్‌లో ఉన్నారు. డేటాని డిలీట్ చేసే అవకాశం ఉంది.")

  if not df.empty:
    row_idx = st.number_input(
        "తొలగించవలసిన రో నంబర్ (Index) నమోదు చేయండి:",
        min_value=0,
        max_value=max(0, len(df) - 1),
        step=1,
    )
    if st.button("ఈ రో ను తొలగించు"):
      df = df.drop(row_idx).reset_index(drop=True)
      save_data(
          df
      )  # డిలీట్ చేసిన తర్వాత మార్పులను ఎక్సెల్ లో పర్మనెంట్‌గా సేవ్ చేయడం
      st.error(f"రో {row_idx} విజయవంతంగా తొలగించబడింది!")
      st.rerun()
  else:
    st.info("డిలీట్ చేయడానికి ఎలాంటి డేటా లేదు.")

elif user_id:
  st.warning(
      "🔒 మీరు ఓనర్ కాదు. కాబట్టి డేటాను డిలీట్ చేసే పర్మిషన్ మీకు లేదు. కేవలం"
      " డేటా చూడగలరు మరియు కొత్తది యాడ్ చేయగలరు."
  )
else:
  st.info(
      "డేటా డిలీట్ ఆప్షన్స్ కావాలంటే దయచేసి మీ ఓనర్ ID తో సైడ్‌బార్‌లో లాగిన్"
      " అవ్వండి."
  )
