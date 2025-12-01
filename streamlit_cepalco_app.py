import streamlit as st
import pandas as pd
import joblib
import base64
import os

def set_bg_local(image_file):
with open(image_file, "rb") as f:
data = f.read()
encoded = base64.b64encode(data).decode()
page_bg = f""" <style>
.stApp {{
background-image: url("data:image/jpg;base64,{encoded}");
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
}} </style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

set_bg_local("backgrd.jpg")

st.set_page_config(page_title="⚡ CEPALCO Electricity Bill Predictor", layout="wide")

USERS_FILE = "users.csv"
if not os.path.exists(USERS_FILE):
pd.DataFrame(columns=["email","password"]).to_csv(USERS_FILE, index=False)

users_df = pd.read_csv(USERS_FILE)

if "logged_in" not in st.session_state:
st.session_state.logged_in = False
if "user_email" not in st.session_state:
st.session_state.user_email = None

def signup_user(email, password):
if not email.endswith("@gmail.com"):
return "❌ Email must be a Gmail account (@gmail.com)."
if email in users_df["email"].values:
return "❌ This email is already registered."
pd.DataFrame({"email":[email],"password":[password]}).to_csv(USERS_FILE, mode="a", header=False, index=False)
return "✅ Account created successfully! You can now log in."

def login_user(email, password):
if email in users_df["email"].values:
stored_pw = users_df[users_df["email"]==email]["password"].values[0]
if stored_pw==password:
st.session_state.logged_in=True
st.session_state.user_email=email
return "✅ Login successful!"
else:
return "❌ Incorrect password."
return "❌ Account not found."

if not st.session_state.logged_in:
st.markdown(
""" <style>
.center-card {
background-color: rgba(255,255,255,0.95);
padding: 40px;
max-width: 450px;
margin: 50px auto;
border-radius: 15px;
box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.center-card h2 {
text-align: center;
margin-bottom: 20px;
} </style>
""", unsafe_allow_html=True
)

```
tabs = st.tabs(["Login", "Sign Up"])

with tabs[0]:
    st.markdown('<div class="center-card"><h2>🔐 Login</h2></div>', unsafe_allow_html=True)
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_pw")
    if st.button("Login"):
        msg = login_user(login_email, login_password)
        st.info(msg)

with tabs[1]:
    st.markdown('<div class="center-card"><h2>📝 Sign Up</h2></div>', unsafe_allow_html=True)
    signup_email = st.text_input("Gmail Address", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_pw")
    if st.button("Sign Up"):
        msg = signup_user(signup_email, signup_password)
        st.info(msg)

st.stop()
```

st.markdown(f"<h1 style='text-align: center;'>⚡ Welcome, {st.session_state.user_email}!</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>CEPALCO Electricity Bill Predictor</h3>", unsafe_allow_html=True)

model_file = "cepalco_model_from_csv.pkl"
data = joblib.load(model_file)
model = data["model"]
scaler = data["scaler"]
features = data["features"]

st.markdown(
""" <style>
.input-card {
background-color: rgba(255,255,255,0.95);
padding: 30px;
border-radius: 15px;
box-shadow: 0 4px 12px rgba(0,0,0,0.2);
max-width: 700px;
margin: 30px auto;
}
input, .stNumberInput>div>input {
color: black !important;
background-color: white !important;
} </style>
""", unsafe_allow_html=True
)
st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
num_appliances = st.number_input("Number of Appliances", min_value=0, step=1)
daily_peak_hours = st.number_input("Daily Peak Hours", min_value=0.0, step=0.1)
aircon_hours = st.number_input("Aircon Usage Hours", min_value=0.0, step=0.1)
fridge_count = st.number_input("Number of Refrigerators", min_value=0, step=1)
with col2:
washing_machine_hours = st.number_input("Washing Machine Usage Hours", min_value=0.0, step=0.1)
household_size = st.number_input("Household Size", min_value=1, step=1)
month = st.number_input("Month (1-12)", min_value=1, max_value=12, step=1)

result_kwh = st.empty()
result_bill = st.empty()

if st.button("Predict kWh Consumption"):
input_data = {
"Number_of_Appliances": num_appliances,
"Daily_Peak_Hours": daily_peak_hours,
"Aircon_Usage_Hours": aircon_hours,
"Refrigerator_Count": fridge_count,
"Washing_Machine_Usage": washing_machine_hours,
"Household_Size": household_size,
"Month": month
}
input_data["Total_Appliance_Hours"] = input_data["Number_of_Appliances"] * input_data["Daily_Peak_Hours"]
input_df = pd.DataFrame([input_data])
input_scaled = scaler.transform(input_df[features])
prediction = model.predict(input_scaled)[0]

```
kwh_rate = 12.52
expected_bill = prediction * kwh_rate

result_kwh.success(f"Predicted Daily kWh Consumption: {prediction:.2f} kWh")
result_bill.success(f"Expected Daily Electric Bill: {expected_bill:.2f} currency units")
```

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Logout"):
st.session_state.logged_in = False
st.session_state.user_email = None
st.rerun()
