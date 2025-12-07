import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("ElectricityPredictor.pkl")

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
    }
    input, .stTextInput>div>input, .stNumberInput>div>input {
        background-color: #000000;
        color: #FFFFFF;
        border: 1px solid #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True
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
# Login / Signup
# ----------------------------
if not st.session_state.logged_in:
    st.title("Login or Sign Up")
    
    mode = st.radio("Select Mode", ["Login", "Sign Up"])
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    name = ""
    
    if mode == "Sign Up":
        name = st.text_input("Full Name")
    
    login_signup_clicked = st.button(mode)

    if login_signup_clicked:
        if mode == "Login":
            if email in st.session_state.users and st.session_state.users[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user = st.session_state.users[email]["name"]
            else:
                st.error("Invalid email or password")
        elif mode == "Sign Up":
            if email in st.session_state.users:
                st.error("Email already registered")
            elif not name:
                st.error("Please enter your full name")
            else:
                st.session_state.users[email] = {"password": password, "name": name}
                st.success("Account created! You can now log in.")

# ----------------------------
# Dashboard
# ----------------------------
if st.session_state.logged_in:
    st.title(f"Welcome, {st.session_state.user}!")
    st.subheader("Electricity Bill Predictor")
    
    fan = st.number_input("Fan hours", min_value=0)
    ac = st.number_input("AC hours", min_value=0)
    ref = st.number_input("Refrigerator hours", min_value=0)
    tv = st.number_input("TV hours", min_value=0)
    monitor = st.number_input("Monitor hours", min_value=0)
    pump = st.number_input("Motor Pump hours", min_value=0)
    
    if st.button("Predict Electricity Bill"):
        data = pd.DataFrame([{
            "FanHours": fan,
            "ACHours": ac,
            "RefHours": ref,
            "TVHours": tv,
            "MonitorHours": monitor,
            "PumpHours": pump
        }])
        prediction = model.predict(data)[0]
        st.success(f"Estimated Electricity Bill: ₱{prediction:.2f}")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.experimental_rerun()
