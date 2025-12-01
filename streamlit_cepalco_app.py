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

# CALL THE BACKGROUND IMAGE HERE
set_bg_local("backgrd.jpg")  # <-- Change this to your image filename

# ---------------------------------------------------
# PAGE CONTENT
# ---------------------------------------------------
st.set_page_config(page_title="⚡ CEPALCO Electricity Bill Predictor", layout="wide")
st.title("⚡ CEPALCO Electricity Bill Predictor")

model_file = "cepalco_model_from_csv.pkl"
# Note: Assuming this file exists and loads correctly for the code to run
try:
    data = joblib.load(model_file)
    model = data["model"]
    scaler = data["scaler"]
    features = data["features"]
except FileNotFoundError:
    st.error(f"Error: Model file '{model_file}' not found. Please ensure it is in the same directory.")
    st.stop()
except KeyError:
    st.error("Error: The model file is missing 'model', 'scaler', or 'features' keys.")
    st.stop()


st.header("Enter Your Household Data")

num_appliances = st.number_input("Number of Appliances", min_value=0, step=1)
daily_peak_hours = st.number_input("Daily Peak Hours", min_value=0.0, step=0.1)
aircon_hours = st.number_input("Aircon Usage Hours", min_value=0.0, step=0.1)
fridge_count = st.number_input("Number of Refrigerators", min_value=0, step=1)
washing_machine_hours = st.number_input("Washing Machine Usage Hours", min_value=0.0, step=0.1)
household_size = st.number_input("Household Size", min_value=1, step=1)
month = st.number_input("Month (1-12)", min_value=1, max_value=12, step=1)

# Variables to hold the result displays - not strictly needed for the custom box, 
# but kept to maintain general structure if needed later
# result_kwh = st.empty() 
# result_bill = st.empty()

# Custom CSS for the white box with green label
st.markdown("""
<style>
.prediction-box {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    border: 3px solid #4CAF50; /* Green border for the 'box' effect */
}
.green-label {
    background-color: #4CAF50; /* Green color */
    color: white;
    padding: 8px 15px;
    border-radius: 5px;
    font-size: 1.2em;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 10px;
}
.prediction-value {
    font-size: 1.5em;
    font-weight: bold;
    color: #333;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)


# ... (Previous code including inputs and CSS styling definitions)

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

    # Calculation for Total_Appliance_Hours
    input_data["Total_Appliance_Hours"] = (
        input_data["Number_of_Appliances"] * input_data["Daily_Peak_Hours"]
    )

    # Prepare and scale data for prediction (assuming this block is correct)
    input_df = pd.DataFrame([input_data])
    input_scaled = scaler.transform(input_df[features])
    prediction = model.predict(input_scaled)[0]

    # Calculations
    kwh_rate = 12.52
    expected_bill = prediction * kwh_rate
    
    # --- FIX: Display Both Results Correctly in the Custom Box ---
    # The image shows the first prediction is outside the intended box 
    # and the second has unrendered HTML tags.
    # This single st.markdown block ensures both are rendered as desired.
    st.markdown(
        f"""
        <div class="prediction-box">
            
            <div class="green-label">Predicted Daily kWh Consumption</div>
            <div class="prediction-value">{prediction:.2f} kWh</div>
            
            <hr style="border-top: 1px solid #eee; margin: 15px 0;">
            
            <div class="green-label">Expected Daily Electric Bill</div>
            <div class="prediction-value">{expected_bill:.2f} currency units</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    # -----------------------------------------------------------
