import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sri Manikanta Traders", layout="wide")

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'bank_deposits' not in st.session_state:
    st.session_state.bank_deposits = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Login Page
def login_page():
    st.title("Sri Manikanta Traders - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        valid_users = [
            ("admin", "manikanta123"),
            ("admin", "samsri2528"),
            ("manikanta", "samsri2528")
        ]
        
        if (username, password) in valid_users:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# Main Dashboard & Navigation
def main_app():
    st.sidebar.title("SRI MANIKANTA TRADERS")
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    
    menu = st.sidebar.selectbox("Navigation", [
        "Billing & Sales", 
        "Manage Inventory", 
        "Present / Closing Stock", 
        "Sales History & Reports", 
        "Cash Book",
        "Add Bank Deposit",
        "Add Expense"
    ])
    
    if menu == "Billing & Sales":
        st.header("Billing & Sales Grid")
        st.write("Billing interface is active here.")

    elif menu == "Manage Inventory":
        st.header("Manage Inventory")
        st.write("Stock management options.")

    elif menu == "Present / Closing Stock":
        st.header("Present / Closing Stock")
        st.write("View current stock details.")

    elif menu == "Sales History & Reports":
        st.header("Sales History & Reports")
        st.write("Past sales reports and analytics.")

    elif menu == "Cash Book":
        st.header("Cash Book (Bank Deposits & Expenses)")
        
        st.subheader("Bank Deposits List")
        if st.session_state.bank_deposits:
            st.dataframe(pd.DataFrame(st.session_state.bank_deposits))
        else:
            st.info("No bank deposits recorded yet.")
            
        st.subheader("Expenses List")
        if st.session_state.expenses:
            st.dataframe(pd.DataFrame(st.session_state.expenses))
        else:
            st.info("No expenses recorded yet.")

    elif menu == "Add Bank Deposit":
        st.header("+ Add Bank Deposit Entry & Attach Receipt")
        with st.form("deposit_form"):
            deposit_date = st.text_input("Deposit Date (DD-MM-YYYY)", value="10-09-2026")
            deposit_amount = st.number_input("Deposit Amount (₹)", min_value=0.0, value=1000.0)
            description = st.text_input("Description / Bank Name", value="Bank Deposit")
            uploaded_file = st.file_uploader("Upload Deposit Receipt / Slip (Image/PDF)", type=["png", "jpg", "jpeg", "pdf"])
            
            submit_deposit = st.form_submit_button("Save Bank Deposit & Receipt")
            if submit_deposit:
                st.session_state.bank_deposits.append({
                    "Date": deposit_date,
                    "Amount": deposit_amount,
                    "Description": description
                })
                st.success("Bank Deposit entry saved successfully!")

    elif menu == "Add Expense":
        st.header("+ Add Expense Entry")
        with st.form("expense_form"):
            expense_date = st.text_input("Expense Date (DD-MM-YYYY)", value="10-09-2026")
            expense_purpose = st.text_input("Expense Description / Purpose")
            expense_amount = st.number_input("Expense Amount (₹)", min_value=0.0, value=100.0)
            
            submit_expense = st.form_submit_button("Save Expense")
            if submit_expense:
                st.session_state.expenses.append({
                    "Date": expense_date,
                    "Purpose": expense_purpose,
                    "Amount": expense_amount
                })
                st.success("Expense entry saved successfully!")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# Run application
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
