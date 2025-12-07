import streamlit as st
import pandas as pd
import joblib
from firebase_config import auth

# Load model
model = joblib.load("ElectricityKwhPredictor.pkl")

# Set page layout
st.set_page_config(page_title="Electricity Bill Calculator", layout="wide")

# -----------------------------
# Background and styling
# -----------------------------
st.markdown(
    """
    <style>
    body {
        background-image: url('https://i.ibb.co/0sTZVfk/geometry-light.png');
        background-size: cover;
        color: #000000;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: #FFFFFF;
        border-radius: 5px;
    }
    input, .stTextInput>div>input, .stNumberInput>div>input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #000000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# -----------------------------
# LOGIN PAGE
# -----------------------------
if st.session_state.page == "login" and not st.session_state.logged_in:
    st.title("Login")
    login_email = st.text_input("Email")
    login_pass = st.text_input("Password", type="password")
    
    if st.button("Login"):
        try:
            auth.sign_in_with_email_and_password(login_email, login_pass)
            st.session_state.logged_in = True
            st.session_state.user_email = login_email
            st.session_state.user_name = login_email.split("@")[0].capitalize()
            st.session_state.page = "dashboard"
            st.experimental_rerun()
        except:
            st.error("Invalid email or password")

    if st.button("Forgot Password?"):
        if login_email:
            try:
                auth.send_password_reset_email(login_email)
                st.success(f"Password reset email sent to {login_email}")
            except:
                st.error("Failed to send reset email")
        else:
            st.warning("Enter email first")

    if st.button("Sign Up"):
        st.session_state.page = "signup"
        st.experimental_rerun()

# -----------------------------
# SIGN UP PAGE
# -----------------------------
if st.session_state.page == "signup" and not st.session_state.logged_in:
    st.title("Create Account")
    signup_email = st.text_input("Email")
    signup_pass = st.text_input("Password", type="password")
    signup_name = st.text_input("Full Name")
    
    if st.button("Create Account"):
        try:
            auth.create_user_with_email_and_password(signup_email, signup_pass)
            st.success("Account created! You may login.")
            st.session_state.page = "login"
            st.experimental_rerun()
        except:
            st.error("Failed to create account")
    
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.experimental_rerun()

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
if st.session_state.page == "dashboard" and st.session_state.logged_in:
    st.title(f"Welcome, {st.session_state.user_name}!")
    st.subheader("Electricity Usage & Bill Predictor")

    # Input hours
    fan = st.number_input("Fan hours", min_value=0)
    ac = st.number_input("AC hours", min_value=0)
    ref = st.number_input("Refrigerator hours", min_value=0)
    tv = st.number_input("TV hours", min_value=0)
    monitor = st.number_input("Monitor hours", min_value=0)
    pump = st.number_input("Motor Pump hours", min_value=0)

    if st.button("Predict"):
        data = pd.DataFrame([{
            "FanHours": fan,
            "ACHours": ac,
            "RefHours": ref,
            "TVHours": tv,
            "MonitorHours": monitor,
            "PumpHours": pump
        }])
        
        pred_kwh, _ = model.predict(data)[0]  # We use only kWh from model
        estimated_bill = pred_kwh * 12.52   # Bill = kWh * 12.52

        # Show summary metrics only
        st.subheader("Summary")
        col1, col2 = st.columns(2)
        col1.metric("Total Estimated kWh", round(pred_kwh, 2))
        col2.metric("Total Estimated Bill (₱)", round(estimated_bill, 2))

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.user_email = None
        st.session_state.user_name = None
        st.experimental_rerun()
