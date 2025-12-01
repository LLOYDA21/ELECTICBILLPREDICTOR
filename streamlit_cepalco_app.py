import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

csv_file = "cepalco_synthetic_enhanced.csv"
df = pd.read_csv(csv_file)
print(f"Loaded {len(df)} rows from {csv_file}")

features = [
"Number_of_Appliances",
"Daily_Peak_Hours",
"Aircon_Usage_Hours",
"Refrigerator_Count",
"Washing_Machine_Usage",
"Household_Size",
"Month",
]

target = "kWh_Consumption"

df["Total_Appliance_Hours"] = df["Number_of_Appliances"] * df["Daily_Peak_Hours"]
features.append("Total_Appliance_Hours")

X = df[features]
y = df[target]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
X_scaled, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
n_estimators=300,
max_depth=20,
min_samples_split=2,
min_samples_leaf=1,
max_features='sqrt',
random_state=42,
n_jobs=-1,
)

print("Training model...")
model.fit(X_train, y_train)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

print(f"\nModel Performance:")
print(f"MAE: {mae:.3f}")
print(f"R² Score: {r2:.3f}")

save_data = {
"model": model,
"scaler": scaler,
"features": features,
}

model_file = "cepalco_model_from_csv.pkl"
joblib.dump(save_data, model_file, compress=3)
print(f"\nModel Saved: {model_file}")

example_input = {
"Number_of_Appliances": 10,
"Daily_Peak_Hours": 4,
"Aircon_Usage_Hours": 3,
"Refrigerator_Count": 2,
"Washing_Machine_Usage": 1,
"Household_Size": 5,
"Month": 12,
}

example_input["Total_Appliance_Hours"] = example_input["Number_of_Appliances"] * example_input["Daily_Peak_Hours"]

input_df = pd.DataFrame([example_input])
input_scaled = scaler.transform(input_df[features])

predicted_kwh = model.predict(input_scaled)[0]

kwh_rate = 12.52
expected_bill = predicted_kwh * kwh_rate

print(f"\nPredicted kWh Consumption: {predicted_kwh:.2f} kWh")
print(f"Expected Electric Bill: {expected_bill:.2f} currency units")
