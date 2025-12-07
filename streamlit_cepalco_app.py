import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ----------------------------------------------------------
# Load trained model & metadata
# ----------------------------------------------------------
try:
    data = joblib.load("datasets.pkl")
    model = data["model"]
    features = data["features"]
except Exception as e:
    st.error("❌ Could not load datasets.pkl. Check file location.")
    st.error(str(e))
    st.stop()


# ----------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------
st.title("📉 Monthly Electricity Consumption Predictor")
st.write("Predict monthly kWh consumption and electricity bill.")


# ----------------------------------------------------------
# Input fields
# ----------------------------------------------------------
temperature = st.number_input("Temperature (°C)", -50, 60, 30)
humidity = st.number_input("Humidity (%)", 0, 100, 70)
occupancy = st.number_input("Occupancy (people)", 1, 50, 4)
appliances = st.number_input("Number of Appliances Used", 1, 50, 12)

day = st.selectbox(
    "Day of Week",
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
)

tariff = st.number_input("Tariff (₱ per kWh)", 0.01, 50.00, 12.52)

# ----------------------------------------------------------
# Convert day to numeric
# ----------------------------------------------------------
day_map = {
    "Monday":0,"Tuesday":1,"Wednesday":2,
    "Thursday":3,"Friday":4,"Saturday":5,"Sunday":6
}

day_value = day_map[day]


# ----------------------------------------------------------
# Handle weather dummy columns automatically
# ----------------------------------------------------------
weather_cols = [c for c in features if c.startswith("weather_")]

weather_inputs = {}
if weather_cols:
    st.subheader("Weather Conditions")
    for col in weather_cols:
        weather_inputs[col] = st.checkbox(
            col.replace("weather_", "").capitalize(),
            value=False
        )


# ----------------------------------------------------------
# Build input dataframe
# ----------------------------------------------------------
input_dict = {
    "temperature": temperature,
    "humidity": humidity,
    "occupancy": occupancy,
    "number_of_appliances_used": appliances,
    "day_of_week": day_value,
    "tariff_rs_per_kwh": tariff
}

# add weather columns
for col in weather_cols:
    input_dict[col] = int(weather_inputs[col])

# reorder to match training
input_df = pd.DataFrame([input_dict])[features]


# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------
if st.button("🔮 Predict"):

    kwh = float(model.predict(input_df)[0])
    kwh = max(kwh, 0)   # avoid negative output
    bill = kwh * tariff

    st.success(f"✅ Predicted Monthly Consumption: **{kwh:.2f} kWh**")
    st.success(f"💵 Estimated Monthly Bill: **₱{bill:.2f}**")

    with st.expander("Debug Input Data"):
        st.dataframe(input_df)
