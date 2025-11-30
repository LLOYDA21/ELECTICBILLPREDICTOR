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

# ---- FUNCTION TO SET TEXT COLORS ----
def set_text_colors():
    st.markdown(
        """
        <style>
        /* Main title white */
        h1 {
            color: #FFFFFF !important;
        }

        /* All other text black */
        .stApp *:not(h1) {
            color: #000000 !important;
        }

        /* Style number input boxes */
        div.stNumberInput > div > div > input {
            background-color: #FFEB3B !important;  /* Bright yellow */
            color: #000000 !important;            /* Black text */
            border: 2px solid #F57F17 !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-weight: bold;
            font-size: 16px !important;
        }

        /* Input container styling */
        div.stNumberInput > div > div {
            background-color: rgba(255, 235, 59, 0.1) !important;
            border-radius: 8px !important;
            padding: 5px;
        }

        /* Style input labels bold and black */
        label[data-baseweb="label"] {
            font-weight: bold !important;
            color: black !important;
            font-size: 16px !important;
        }

        /* Buttons styling */
        .stButton > button {
            background-color: rgba(255,255,255,0.1);
            color: black;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
        }

        /* Input focus effect */
        div.stNumberInput > div > div > input:focus {
            background-color: #FFEB3B !important;
            border-color: #F57F17 !important;
            box-shadow: 0 0 0 2px rgba(245, 127, 23, 0.3) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply text color settings
set_text_colors()

# Load ML model
model = joblib.load("cepalco_model.pkl")

# ---- HEADER ----
st.markdown(
    """
    <h1 style='text-align: center; text-shadow: 2px 2px 4px #000000;'>⚡ CEPALCO Electricity Bill Predictor ⚡</h1>
    <p style='text-align: center; font-size:16px;'>Estimate your monthly electricity bill based on usage and appliances.</p>
    """,
    unsafe_allow_html=True
)

st.write("---")

# ---- INPUT SECTION ----
st.header("📥 Enter Household Details")

col1, col2 = st.columns(2)

with col1:
    month = st.number_input(
        "**Month (1–12)**",
        min_value=1,
        max_value=12,
        help="Enter the current month as a number (e.g., January = 1)"
    )
    kwh = st.number_input(
        "**Monthly kWh Usage**",
        min_value=0,
        help="Total electricity consumed in kilowatt-hours"
    )

with col2:
    peak = st.number_input(
        "**Daily Peak Hours**",
        min_value=0,
        help="Average number of hours per day during peak electricity usage"
    )
    apps = st.number_input(
        "**Number of Active Appliances**",
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
            <h2 style='color:black;'>Estimated Electricity Bill</h2>
            <h1 style='color:#00FF00;'>₱{prediction:,.2f}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---- FOOTER ----
st.write("---")
st.markdown(
    "<p style='text-align:center; font-size:12px; color:gray;'>Powered by Machine Learning Model | CEPALCO</p>",
    unsafe_allow_html=True
)
