{"variant":"standard","id":"89716","title":"Train Model from User CSV"}
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

# ============================================================
# 1. ASK USER FOR CSV FILE
# ============================================================
csv_file = "cepalco_synthetic_enhanced.csv"

# Load the CSV
df = pd.read_csv(csv_file)
print(f"Loaded {len(df)} rows from {csv_file}")

# ============================================================
# 2. DEFINE FEATURES AND TARGET
# ============================================================
# Make sure your CSV has these columns:
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

# Optional feature engineering
df["Total_Appliance_Hours"] = df["Number_of_Appliances"] * df["Daily_Peak_Hours"]
features.append("Total_Appliance_Hours")

X = df[features]
y = df[target]

# ============================================================
# 3. SCALE FEATURES (optional)
# ============================================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ============================================================
# 4. TRAIN/TEST SPLIT
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# ============================================================
# 5. CREATE RANDOM FOREST MODEL
# ============================================================
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=20,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1,
)

# ============================================================
# 6. TRAIN MODEL
# ============================================================
print("Training model...")
model.fit(X_train, y_train)

# ============================================================
# 7. EVALUATE MODEL
# ============================================================
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)

print(f"\nModel Performance:")
print(f"MAE: {mae:.3f}")
print(f"R² Score: {r2:.3f}")

# ============================================================
# 8. SAVE MODEL
# ============================================================
save_data = {
    "model": model,
    "scaler": scaler,
    "features": features,
}

model_file = "cepalco_model_from_csv.pkl"
joblib.dump(save_data, model_file, compress=3)
print(f"\nModel Saved: {model_file}")
