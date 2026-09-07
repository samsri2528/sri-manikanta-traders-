import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="SRI MANIKANTA TRADERS",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS for Professional Focus-style Layout
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .login-container {
        padding: 40px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .brand-title {
        font-size: 38px;
        font-weight: bold;
        color: #1b4d3e;
    }
    .brand-subtitle {
        font-size: 16px;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Check Authentication Status
if not st.session_state["authenticated"]:
    # Create two columns for Split Screen Login (Like Focus App)
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<p class="brand-title">🌾 SRI MANIKANTA TRADERS</p>', unsafe_allow_html=True)
        st.markdown('<p class="brand-subtitle">Advanced Inventory & Billing Management System<br>D.No 6/159/25, Pedda Harivanam Village, Adoni Mandal</p>', unsafe_allow_html=True)
        st.info("💡 Secure access for authorized personnel only. Please sign in with your credentials to manage stock and generate bills.")

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.markdown("### 🔐 LOGIN")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Sign In", use_container_width=True):
                if username == "admin" and password == "samsri2528":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Username or Password")
else:
    # Main Application After Successful Login
    st.sidebar.title("Navigation")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()
        
    st.title("🌾 SRI MANIKANTA TRADERS - Dashboard")
    st.success("Welcome! You are successfully logged in.")
    
    # Your existing Inventory & Billing components can go here
    st.markdown("### 📊 Billing & Inventory Grid")
    st.write("System is ready for operations.")
