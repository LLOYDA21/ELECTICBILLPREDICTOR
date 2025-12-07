import streamlit as st
import pandas as pd
import joblib
from firebase_config import auth  # your pyrebase auth object

# Load trained multi-output model (predicts kWh + Bill)
model = joblib.load("ElectricityKwhPredictor.pkl")

# Page theme
st.set_page_config(page_title="Electricity Predictor", layout="centered")
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #FFFFFF;
        color: #000000;
        border-radius: 5px;
    }
    input, .stTextInput>div>input, .stNumberInput>div>input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Session State Initialization
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"  # login → signup → dashboard

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ----------------------------
# LOGIN PAGE
# ----------------------------
if st.session_state.page == "login" and not st.session_state.logged_in:
    st.title("Login")

    login_email = st.text_input("Login Email")
    login_pass = st.text_input("Login Password", type="password")

    # Horizontal alignment for Login, Forgot Password, Sign Up
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(login_email, login_pass)
                st.session_state.logged_in = True
                st.session_state.user_email = login_email
                st.session_state.user_name = login_email.split("@")[0].capitalize()
                st.session_state.page = "dashboard"
                st.success("Logged in successfully!")
                st.experimental_rerun()
            except:
                st.error("Invalid email or password")

    with col2:
        if st.button("Forgot Password?"):
            if login_email:
                try:
                    auth.send_password_reset_email(login_email)
                    st.success(f"Password reset email sent to {login_email}")
                except:
                    st.error("Failed to send reset email. Check the email address.")
            else:
                st.warning("Please enter your email first")

    with col3:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.experimental_rerun()

# ----------------------------
# SIGN UP PAGE
# ----------------------------
if st.session_state.page == "signup" and not st.session_state.logged_in:
    st.title("Create Account")

    signup_email = st.text_input("Email")
    signup_pass = st.text_input("Password", type="password")
    signup_name = st.text_input("Full Name")

    # Horizontal alignment for Create Account and Back to Login
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Account"):
            try:
                user = auth.create_user_with_email_and_password(signup_email, signup_pass)
                st.success("Account created! You may now login.")
                st.session_state.page = "login"
                st.experimental_rerun()
            except:
                st.error("Failed to create account. Email may already exist or password is weak.")

    with col2:
        if st.button("Back to Login"):
            st.session_state.page = "login"
            st.experimental_rerun()

# ----------------------------
# DASHBOARD PAGE
# ----------------------------
if st.session_state.page == "dashboard" and st.session_state.logged_in:
    st.title(f"Welcome, {st.session_state.user_name}!")
    st.subheader("Electricity Usage & Bill Predictor")

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

        pred_kwh, pred_bill = model.predict(data)[0]

        st.success(f"Predicted kWh Consumption: **{pred_kwh:.2f} kWh**")
        st.success(f"Estimated Electricity Bill: **₱{pred_bill:.2f}**")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.user_email = None
        st.session_state.user_name = None
        st.experimental_rerun()
