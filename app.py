import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Sri Manikanta Traders",
    page_icon="🌾",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        max-width: 900px;
        padding: 20px;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Authentication and Data
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "inventory" not in st.session_state:
    # Sample initial inventory data
    st.session_state.inventory = pd.DataFrame([
        {"Item Name": "Paddy (Rice)", "Quantity (kg)": 500, "Price per kg (₹)": 30},
        {"Item Name": "Wheat", "Quantity (kg)": 300, "Price per kg (₹)": 25},
        {"Item Name": "Fertilizer", "Quantity (kg)": 150, "Price per kg (₹)": 40}
    ])
if "sales" not in st.session_state:
    st.session_state.sales = []

# Login Function
def login_screen():
    st.title("🌾 Sri Manikanta Traders - Login")
    
    with st.form("login_form"):
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Login")
        
        if submit_btn:
            if username_input == "admin" and password_input == "manikanta123":
                st.session_state.authenticated = True
                st.session_state.username = "admin"
                st.success("Login successful as Admin!")
                st.rerun()
            elif username_input == "manikanta" and password_input == "samsri2528":
                st.session_state.authenticated = True
                st.session_state.username = "manikanta"
                st.success("Login successful as User!")
                st.rerun()
            else:
                st.error("Invalid Username or Password")

# Main Application Dashboard
def main_dashboard():
    st.sidebar.title(f"Welcome, {st.session_state.username.capitalize()}!")
    
    menu = ["Billing & Dashboard", "Inventory Management"]
    choice = st.sidebar.selectbox("Navigation", menu)
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

    if choice == "Billing & Dashboard":
        st.title("📊 Billing & Sales Dashboard")
        
        # Display Current Inventory
        st.subheader("Available Stock")
        st.dataframe(st.session_state.inventory, use_container_width=True)
        
        # Billing Section
        st.subheader("Create New Bill")
        with st.form("billing_form"):
            customer_name = st.text_input("Customer Name")
            selected_item = st.selectbox("Select Item", st.session_state.inventory["Item Name"].tolist())
            
            # Find current price and max quantity for selected item
            item_row = st.session_state.inventory[st.session_state.inventory["Item Name"] == selected_item].iloc[0]
            available_qty = item_row["Quantity (kg)"]
            unit_price = item_row["Price per kg (₹)"]
            
            st.info(f"Available Quantity: {available_qty} kg | Price per kg: ₹{unit_price}")
            
            quantity_sold = st.number_input("Quantity to Sell (kg)", min_value=1.0, max_value=float(available_qty), step=1.0)
            
            submit_bill = st.form_submit_button("Generate Bill & Update Stock")
            
            if submit_bill:
                if not customer_name:
                    st.warning("Please enter the customer name.")
                else:
                # Calculate total amount
                    total_amount = quantity_sold * unit_price
                    
                    # Update inventory stock
                    st.session_state.inventory.loc[
                        st.session_state.inventory["Item Name"] == selected_item, "Quantity (kg)"
                    ] -= quantity_sold
                    
                    # Record Sale
                    sale_record = {
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Customer": customer_name,
                        "Item": selected_item,
                        "Quantity (kg)": quantity_sold,
                        "Total Price (₹)": total_amount
                    }
                    st.session_state.sales.append(sale_record)
                    
                    st.success(f"Bill generated successfully! Total Amount: ₹{total_amount}")
                    st.rerun()

        # Sales History
        if st.session_state.sales:
            st.subheader("Recent Sales History")
            sales_df = pd.DataFrame(st.session_state.sales)
            st.dataframe(sales_df, use_container_width=True)

    elif choice == "Inventory Management":
        st.title("📦 Inventory Management")
        
        st.subheader("Current Inventory Grid")
        st.dataframe(st.session_state.inventory, use_container_width=True)
        
        # Add New Stock (Restricted or Password Protected based on instructions)
        st.subheader("Add New Stock")
        with st.form("add_stock_form"):
            new_item_name = st.text_input("Item Name")
            new_qty = st.number_input("Quantity (kg)", min_value=0.0, step=1.0)
            new_price = st.number_input("Price per kg (₹)", min_value=0.0, step=0.5)
            
            # Security confirmation code to add stock
            confirmation_code = st.text_input("Enter Authorization Code to Add Stock", type="password")
            
            submit_stock = st.form_submit_button("Add Stock")
            
            if submit_stock:
                if confirmation_code == "samsri25285":
                    if new_item_name:
                        # Check if item already exists
                        if new_item_name in st.session_state.inventory["Item Name"].values:
                            st.session_state.inventory.loc[
                                st.session_state.inventory["Item Name"] == new_item_name, "Quantity (kg)"
                            ] += new_qty
                            st.success(f"Updated quantity for {new_item_name}!")
                        else:
                            new_row = pd.DataFrame([{
                                "Item Name": new_item_name,
                                "Quantity (kg)": new_qty,
                                "Price per kg (₹)": new_price
                            }])
                            st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                            st.success(f"Added new item {new_item_name} successfully!")
                        st.rerun()
                    else:
                        st.error("Please enter a valid item name.")
                else:
                    st.error("Incorrect authorization code! (Hint: must be samsri25285)")

# Run App Logic
if not st.session_state.authenticated:
    login_screen()
else:
    main_dashboard()
