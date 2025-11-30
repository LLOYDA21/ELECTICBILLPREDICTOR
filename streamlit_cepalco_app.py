import streamlit as st
import pandas as pd
import joblib
import base64

# Page configuration
st.set_page_config(
    page_title="⚡ CEPALCO Electricity Bill Predictor",
    layout="wide",
    page_icon="⚡"
)

# ---- FUNCTION TO SET LOCAL BACKGROUND IMAGE ----
def set_bg_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        /* Set background image */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}

        /* Make text readable over dark background */
        .stApp * {{
            color: white !important;
        }}

        /* Style number input boxes to be yellow */
        div.stNumberInput > div > div > input {{
            background-color: #FFEB3B !important;  /* Bright yellow */
            color: #000000 !important;           /* Black text for good contrast */
            border: 2px solid #F57F17 !important;  /* Orange border for visibility */
            border-radius: 8px !important;
            padding: 10px !important;
            font-weight: bold;
        }}

        /* Additional styling for number input containers */
        div.stNumberInput > div > div {{
            background-color: rgba(255, 235, 59, 0.1) !important;
            border-radius: 8px !important;
            padding: 5px;
        }}

        /* Style the input widget containers */
        div.element-container .stNumberInput {{
            background-color: rgba(255, 235, 59, 0.1);
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }}

        /* Style buttons */
        .stButton > button {{
            background-color: rgba(0,0,0,0.6);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
        }}

        /* Ensure the input focus state is also yellow */
        div.stNumberInput > div > div > input:focus {{
            background-color: #FFEB3B !important;
            border-color: #F57F17 !important;
            box-shadow: 0 0 0 2px rgba(245, 127, 23, 0.3) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set your local image here
set_bg_local("background.jpg")  # Replace with your file path

# Load ML model
model = joblib.load("cepalco_model.pkl")

# ---- HEADER ----
st.markdown(
    """
    <h1 style='text-align: center; color: #FFD700; text-shadow: 2px 2px 4px #000000;'>⚡ CEPALCO Electricity Bill Predictor ⚡</h1>
    <p style='text-align: center; font-size:16px; text-shadow: 1px 1px 2px #000000;'>Estimate your monthly electricity bill based on usage and appliances.</p>
    """,
    unsafe_allow_html=True
)

st.write("---")

# ---- INPUT SECTION ----
st.header("📥 Enter Household Details")

col1, col2 = st.columns(2)

with col1:
    month = st.number_input(
        "Month (1–12)",
        min_value=1,
        max_value=12,
        help="Enter the current month as a number (e.g., January = 1)"
    )
    kwh = st.number_input(
        "Monthly kWh Usage",
        min_value=0,
        help="Total electricity consumed in kilowatt-hours"
    )

with col2:
    peak = st.number_input(
        "Daily Peak Hours",
        min_value=0,
        help="Average number of hours per day during peak electricity usage"
    )
    apps = st.number_input(
        "Number of Active Appliances",
        min_value=0,
        help="Number of appliances regularly used at home"
    )

st.write("---")

# ---- PREDICTION BUTTON ----
if st.button("💡 Predict Electricity Bill"):
    input_data = pd.DataFrame([[month, kwh, peak, apps]],
                              columns=["month", "kwh_usage", "peak_hours", "appliances"])
    prediction = model.predict(input_data)[0]

    st.markdown(
        f"""
        <div style='background-color: rgba(0,0,0,0.6); padding:20px; border-radius:10px; text-align:center;'>
            <h2 style='color:#FFD700;'>Estimated Electricity Bill</h2>
            <h1 style='color:#00FF00;'>₱{prediction:,.2f}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- FOOTER ----
st.write("---")
st.markdown(
    "<p style='text-align:center; font-size:12px; color:lightgray;'>Powered by Machine Learning Model | CEPALCO</p>",
    unsafe_allow_html=True

)
