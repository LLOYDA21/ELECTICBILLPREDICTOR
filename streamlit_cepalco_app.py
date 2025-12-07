import streamlit as st
import pandas as pd
import joblib

# Load trained multi-output model (predicts kWh + Bill)
model = joblib.load("ElectricityKwhPredictor.pkl")

# Set page config and black & white theme
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
# Initialize session state
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "users" not in st.session_state:
    st.session_state.users = {
        "user1@gmail.com": {"password": "123456", "name": "User One"},
        "user2@gmail.com": {"password": "abcdef", "name": "User Two"}
    }

# ----------------------------
# LOGIN / SIGNUP (NO SELECT MODE)
# ----------------------------
if not st.session_state.logged_in:
    st.title("Welcome")
    st.subheader("Login")

    # LOGIN FIELDS
    login_email = st.text_input("Login Email")
    login_pass = st.text_input("Login Password", type="password")

    if st.button("Login"):
        if login_email in st.session_state.users and st.session_state.users[login_email]["password"] == login_pass:
            st.session_state.logged_in = True
            st.session_state.user = st.session_state.users[login_email]["name"]
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")

    st.subheader("Sign Up")

    # SIGN UP FIELDS
    signup_email = st.text_input("Sign Up Email")
    signup_pass = st.text_input("Sign Up Password", type="password")
    signup_name = st.text_input("Full Name")

    if st.button("Sign Up"):
        if signup_email in st.session_state.users:
            st.error("Email already exists")
        elif not signup_name:
            st.error("Please enter your name")
        else:
            st.session_state.users[signup_email] = {
                "password": signup_pass,
                "name": signup_name
            }
            st.success("Account created! You may now login.")

# ----------------------------
# DASHBOARD (AFTER LOGIN)
# ----------------------------
if st.session_state.logged_in:
    st.title(f"Welcome, {st.session_state.user}!")
    st.subheader("Electricity Usage & Bill Predictor")

    # Input fields
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

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.experimental_rerun()
