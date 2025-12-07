import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

csv_file = "datasets.csv"
df = pd.read_csv(csv_file)

print("Loaded rows:", len(df))
print("Columns:", df.columns.tolist())

day_map = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

df["day_of_week"] = df["day_of_week"].map(day_map)

features = [
    "temperature",
    "humidity",
    "occupancy",
    "number_of_appliances_used",
    "day_of_week",
    "tariff_rs_per_kwh",
]

target = "total_energy_kwh"

if "weather" in df.columns:
    df = pd.get_dummies(df, columns=["weather"], drop_first=True)
    weather_cols = [col for col in df.columns if col.startswith("weather_")]
    features += weather_cols
else:
    weather_cols = []

X = df[features]
y = df[target]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
    n_estimators=400,
    max_depth=None,
    min_samples_split=4,
    min_samples_leaf=2,
    max_features="sqrt",
    n_jobs=-1,
    random_state=42,
)

print("Training model...")
model.fit(X_train, y_train)


preds = np.clip(model.predict(X_test), 0, None)

mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

print("\nModel Performance:")
print(f"  MAE: {mae:.3f}")
print(f"  R² Score: {r2:.3f}")


model_file = "cepalco_monthly_model.pkl"
joblib.dump({
    "model": model,
    "scaler": scaler,
    "features": features
}, model_file, compress=3)

print(f"\nModel saved as: {model_file}")

example = {
    "temperature": 30,
    "humidity": 70,
    "occupancy": 4,
    "number_of_appliances_used": 12,
    "day_of_week": 2,  # Wednesday
    "tariff_rs_per_kwh": 12.52,
}

# Add encoded weather columns = 0
for col in weather_cols:
    example[col] = 0

input_df = pd.DataFrame([example])
input_scaled = scaler.transform(input_df[features])

predicted_kwh = model.predict(input_scaled)[0]
predicted_kwh = max(predicted_kwh, 0)

monthly_bill = predicted_kwh * example["tariff_rs_per_kwh"]

print(f"\nPredicted Monthly Consumption: {predicted_kwh:.2f} kWh")
print(f"Estimated Monthly Bill: {monthly_bill:.2f} PHP")
