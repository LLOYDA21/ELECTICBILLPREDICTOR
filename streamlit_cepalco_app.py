import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ----------------------------------------------------------
# Load trained model
# ----------------------------------------------------------
try:
    data = joblib.load("cepalco_monthly_model.pkl")
    model = data["model"]
    features = data["features"]
except:
    st.error("Model file not found! Make sure cepalco_monthly_model.pkl is in the same folder.")
    st.stop()


# ----------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------
st.title("📉 Monthly Electricity Consumption Predictor")
st.write("Predict monthly kWh consumption and electricity bill.")

# ----------------------------------------------------------
# Input fields
# ----------------------------------------------------------
temperature = st.number_input("Temperature (°C)", min_value=-50, max_value=60, value=30)
humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=70)
occupancy = st.number_input("Occupancy (people)", min_value=1, max_value=50, value=4)
appliances = st.number_input("Number of Appliances Used", min_value=1, max_value=50, value=12)

day = st.selectbox(
    "Day of Week",
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
)

tariff = st.number_input("Tariff (₱ per kWh)", min_value=0.01, value=12.52)

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
        weather_inputs[col] = st.checkbox(col.replace("weather_", "").capitalize(), value=False)

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

# add weather values
for col in weather_cols:
    input_dict[col] = int(weather_inputs[col])

input_df = pd.DataFrame([input_dict])[features]

# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------
if st.button("🔮 Predict"):

    kwh = float(model.predict(input_df)[0])
    kwh = max(kwh, 0)

    bill = kwh * tariff

    st.success(f"✅ Predicted Monthly Consumption: **{kwh:.2f} kWh**")
    st.success(f"💵 Estimated Monthly Bill: **₱{bill:.2f}**")

    st.subheader("Debug Input Data")
    st.dataframe(input_df)

import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ----------------------------------------------------------
# Load trained model
# ----------------------------------------------------------
try:
    data = joblib.load("cepalco_monthly_model.pkl")
    model = data["model"]
    features = data["features"]
except:
    st.error("Model file not found! Make sure cepalco_monthly_model.pkl is in the same folder.")
    st.stop()


# ----------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------
st.title("📉 Monthly Electricity Consumption Predictor")
st.write("Predict monthly kWh consumption and electricity bill.")

# ----------------------------------------------------------
# Input fields
# ----------------------------------------------------------
temperature = st.number_input("Temperature (°C)", min_value=-50, max_value=60, value=30)
humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=70)
occupancy = st.number_input("Occupancy (people)", min_value=1, max_value=50, value=4)
appliances = st.number_input("Number of Appliances Used", min_value=1, max_value=50, value=12)

day = st.selectbox(
    "Day of Week",
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
)

tariff = st.number_input("Tariff (₱ per kWh)", min_value=0.01, value=12.52)

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
        weather_inputs[col] = st.checkbox(col.replace("weather_", "").capitalize(), value=False)

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

# add weather values
for col in weather_cols:
    input_dict[col] = int(weather_inputs[col])

input_df = pd.DataFrame([input_dict])[features]

# ----------------------------------------------------------
# Prediction
# ----------------------------------------------------------
if st.button("🔮 Predict"):

    kwh = float(model.predict(input_df)[0])
    kwh = max(kwh, 0)

    bill = kwh * tariff

    st.success(f"✅ Predicted Monthly Consumption: **{kwh:.2f} kWh**")
    st.success(f"💵 Estimated Monthly Bill: **₱{bill:.2f}**")

    st.subheader("Debug Input Data")
    st.dataframe(input_df)

