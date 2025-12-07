import streamlit as st
import pandas as pd
import joblib
import base64

# ---------------------------------------------------
# Set Background Image (LOCAL)
# ---------------------------------------------------
def set_bg_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    page_bg = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

set_bg_local("backgrd.jpg")

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="⚡ CEPALCO Monthly Bill Predictor", layout="wide")
st.title("⚡ CEPALCO Monthly Electricity Bill Predictor")

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------
model_file = "cepalco_monthly_model.pkl"
data = joblib.load(model_file)
model = data["model"]
scaler = data["scaler"]
features = data["features"]   # includes weather_* columns

# List of weather conditions from training
weather_options = [col.replace("weather_", "") for col in features if col.startswith("weather_")]

# ---------------------------------------------------
# USER INPUT FORM
# ---------------------------------------------------
st.header("Enter Required Information")

col1, col2, col3 = st.columns(3)

with col1:
    temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, step=0.1)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=0.1)
    occupancy = st.number_input("Number of People in Household", min_value=1, step=1)

with col2:
    appliances = st.number_input("Number of Appliances Used", min_value=0, step=1)
    day_of_week = st.selectbox("Day of Week", 
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    
with col3:
    tariff = st.number_input("CEPALCO Rate per kWh (₱)", min_value=1.0, value=12.52, step=0.1)
    weather = st.selectbox("Weather Condition", weather_options)

# Mapping day to number
day_map = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6
}

# Containers for results
result_kwh = st.empty()
result_bill = st.empty()

# ---------------------------------------------------
# PREDICTION
# ---------------------------------------------------
if st.button("Predict Monthly Consumption"):
    
    # Base input
    input_data = {
        "temperature": temperature,
        "humidity": humidity,
        "occupancy": occupancy,
        "number_of_appliances_used": appliances,
        "day_of_week": day_map[day_of_week],
        "tariff_rs_per_kwh": tariff
    }

    # Add weather encoded columns
    for col in features:
        if col.startswith("weather_"):
            condition = col.replace("weather_", "")
            input_data[col] = 1 if condition == weather else 0

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Scale numeric data
    input_scaled = scaler.transform(input_df[features])

    # Predict monthly kWh
    predicted_kwh = model.predict(input_scaled)[0]
    predicted_kwh = max(predicted_kwh, 0)

    # Compute bill
    expected_bill = predicted_kwh * tariff

    # ---------------------------------------------------
    # DISPLAY RESULTS
    # ---------------------------------------------------
    result_kwh.success(f"📊 **Predicted Monthly Consumption:** {predicted_kwh:.2f} kWh")
    result_bill.success(f"💡 **Estimated Monthly Bill:** ₱{expected_bill:.2f}")

