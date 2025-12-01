import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="⚡ CEPALCO Electricity Bill Predictor", layout="wide")
st.title("⚡ CEPALCO Electricity Bill Predictor")

model_file = "cepalco_model_from_csv.pkl"
data = joblib.load(model_file)
model = data["model"]
scaler = data["scaler"]
features = data["features"]

st.header("Enter Your Household Data")

input_data = {}
input_data["Number_of_Appliances"] = st.number_input("Number of Appliances", min_value=0, step=1)
input_data["Daily_Peak_Hours"] = st.number_input("Daily Peak Hours", min_value=0.0, step=0.1)
input_data["Aircon_Usage_Hours"] = st.number_input("Aircon Usage Hours", min_value=0.0, step=0.1)
input_data["Refrigerator_Count"] = st.number_input("Number of Refrigerators", min_value=0, step=1)
input_data["Washing_Machine_Usage"] = st.number_input("Washing Machine Usage Hours", min_value=0.0, step=0.1)
input_data["Household_Size"] = st.number_input("Household Size", min_value=1, step=1)
input_data["Month"] = st.number_input("Month (1-12)", min_value=1, max_value=12, step=1)

input_data["Total_Appliance_Hours"] = input_data["Number_of_Appliances"] * input_data["Daily_Peak_Hours"]

if st.button("Predict kWh Consumption"):
  input_df = pd.DataFrame([input_data])
input_scaled = scaler.transform(input_df[features])
prediction = model.predict(input_scaled)[0]
kwh_rate = 12.52
expected_bill = prediction * kwh_rate
st.success(f"Predicted Daily kWh Consumption: {prediction:.2f} kWh")
st.success(f"Expected Daily Electric Bill: {expected_bill:.2f} currency units")

