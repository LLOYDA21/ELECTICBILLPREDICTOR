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
        pred_kwh, pred_bill = model.predict(data)[0]

        # Create table like the template
        df = pd.DataFrame({
            "Appliance": ["Fan","AC","Refrigerator","TV","Monitor","Pump"],
            "Hours": [fan, ac, ref, tv, monitor, pump],
            "Estimated kWh": [round(pred_kwh*fan/pred_kwh,2), 
                              round(pred_kwh*ac/pred_kwh,2),
                              round(pred_kwh*ref/pred_kwh,2),
                              round(pred_kwh*tv/pred_kwh,2),
                              round(pred_kwh*monitor/pred_kwh,2),
                              round(pred_kwh*pump/pred_kwh,2)],
            "Estimated Bill": [round(pred_bill*fan/pred_bill,2),
                               round(pred_bill*ac/pred_bill,2),
                               round(pred_bill*ref/pred_bill,2),
                               round(pred_bill*tv/pred_bill,2),
                               round(pred_bill*monitor/pred_bill,2),
                               round(pred_bill*pump/pred_bill,2)]
        })

        # Show table
        st.subheader("Monthly Usage & Estimated Bill")
        st.dataframe(df, use_container_width=True)

        # Summary metrics
        total_due = df["Estimated Bill"].sum()
        st.subheader("Summary")
        col1, col2 = st.columns(2)
        col1.metric("Total Estimated kWh", round(pred_kwh,2))
        col2.metric("Total Estimated Bill (₱)", round(total_due,2))

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.user_email = None
        st.session_state.user_name = None
        st.experimental_rerun()
