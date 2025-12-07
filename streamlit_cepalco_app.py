import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("ElectricityPredictor.pkl")

# ----------------------------
# Simulated Login System
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    # Simulated user database
    users = {
        "user1@gmail.com": {"password": "123456", "name": "User One"},
        "user2@gmail.com": {"password": "abcdef", "name": "User Two"}
    }
    
    if st.button("Login"):
        if email in users and users[email]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = users[email]["name"]
        else:
            st.error("Invalid email or password")
    
    st.markdown("No account? Sign up functionality can be added here.")
    
else:
    # ----------------------------
    # Dashboard for Prediction
    # ----------------------------
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
        st.experimental_rerun()
