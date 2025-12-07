import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# ----------------------------------------------------------
# Load data
# ----------------------------------------------------------
df = pd.read_csv("datasets.csv")
print("Loaded rows:", len(df))

# ----------------------------------------------------------
# Convert day
# ----------------------------------------------------------
day_map = {
    "Monday":0,"Tuesday":1,"Wednesday":2,
    "Thursday":3,"Friday":4,"Saturday":5,"Sunday":6
}

df["day_of_week"] = df["day_of_week"].map(day_map)

# ----------------------------------------------------------
# Feature selection
# ----------------------------------------------------------
features = [
    "temperature",
    "humidity",
    "occupancy",
    "number_of_appliances_used",
    "day_of_week",
    "tariff_rs_per_kwh"
]

target = "total_energy_kwh"

# weather columns
if "weather" in df.columns:
    df = pd.get_dummies(df, columns=["weather"], drop_first=True)
    weather_cols = [c for c in df.columns if c.startswith("weather_")]
    features += weather_cols
else:
    weather_cols = []

# ----------------------------------------------------------
# Split
# ----------------------------------------------------------
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ----------------------------------------------------------
# Models
# ----------------------------------------------------------
rf = RandomForestRegressor(
    n_estimators=600,
    random_state=42,
    n_jobs=-1
)

gb = GradientBoostingRegressor(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)

print("Training RandomForest...")
rf.fit(X_train, y_train)

print("Training GradientBoosting...")
gb.fit(X_train, y_train)

# ----------------------------------------------------------
# Ensemble prediction
# ----------------------------------------------------------
pred_rf = rf.predict(X_test)
pred_gb = gb.predict(X_test)

preds = (pred_rf + pred_gb) / 2
preds = np.clip(preds, 0, None)

# ----------------------------------------------------------
# Scores
# ----------------------------------------------------------
print("\nMODEL PERFORMANCE:")
print("MAE =", mean_absolute_error(y_test, preds))
print("R² =", r2_score(y_test, preds))

# ----------------------------------------------------------
# Save
# ----------------------------------------------------------
joblib.dump(
    {
        "model": (rf, gb),
        "features": features
    },
    "datasets.pkl",
    compress=9
)

print("\nMODEL SAVED SUCCESSFULLY ✅")


# ----------------------------------------------------------
# Example prediction
# ----------------------------------------------------------
example = {
    "temperature": 30,
    "humidity": 70,
    "occupancy": 4,
    "number_of_appliances_used": 12,
    "day_of_week": 2,
    "tariff_rs_per_kwh": 12.52
}

for col in weather_cols:
    example[col] = 0

sample = pd.DataFrame([example])[features]

kwh = (rf.predict(sample)[0] + gb.predict(sample)[0]) / 2
bill = kwh * example["tariff_rs_per_kwh"]

print("\nExample Prediction:")
print("Predicted kWh =", round(kwh,2))
print("Monthly bill =", round(bill,2))
