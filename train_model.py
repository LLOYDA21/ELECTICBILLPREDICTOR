import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# --- 1. LOAD FIXED DATASET ---x
# Make sure this file is in the same folder as this script
data = pd.read_csv("cepalco_household_usage_fixed.csv")

print("Dataset Loaded Successfully!")
print("Columns:", data.columns.tolist())

# --- 2. SELECT INPUT COLUMNS AND TARGET COLUMN ---
X = data[["month", "kwh_usage", "peak_hours", "appliances"]]  # FEATURES
y = data["bill"]  # TARGET

# --- 3. SPLIT DATA ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- 4. TRAIN MODEL ---
model = RandomForestRegressor(
    n_estimators=400,
    random_state=42
)

print("Training model...")
model.fit(X_train, y_train)

# --- 5. CHECK ACCURACY ---
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print("\nTraining Complete!")
print("Mean Squared Error:", mse)

# --- 6. SAVE MODEL ---
joblib.dump(model, "cepalco_model.pkl")
print("\nModel saved as cepalco_model.pkl")
