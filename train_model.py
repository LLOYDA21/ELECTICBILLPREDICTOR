import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# =======================
# 1. LOAD OR GENERATE DATA
# =======================

try:
    data = pd.read_csv("cepalco_synthetic_dataset.csv")
    print("Loaded existing dataset: cepalco_synthetic_dataset.csv")
except:
    print("Dataset not found — generating new synthetic dataset...")

    np.random.seed(42)
    rows = 1000

    data = pd.DataFrame({
        "month": np.random.randint(1, 13, rows),
        "kwh_usage": np.random.uniform(100, 900, rows),
        "peak_hours": np.random.randint(1, 9, rows),
        "appliances": np.random.randint(1, 15, rows),
    })

    RATE = 12.52
    data["bill"] = data["kwh_usage"] * RATE

    data.to_csv("cepalco_synthetic_dataset.csv", index=False)
    print("Created and saved new dataset!")

print("\nDataset sample:")
print(data.head())

# =======================
# 2. FEATURES
# =======================

X = data[["month", "kwh_usage", "peak_hours", "appliances"]]
y = data["bill"]

# =======================
# 3. TRAIN-TEST SPLIT
# =======================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =======================
# 4. TRAIN OPTIMIZED MODEL
# =======================

model = RandomForestRegressor(
    n_estimators=100,     # Reduced from 500 → much smaller
    max_depth=12,
    random_state=42
)

print("\nTraining model...")
model.fit(X_train, y_train)

# =======================
# 5. EVALUATE MODEL
# =======================

predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)

print("\nTraining Complete!")
print(f"Mean Squared Error: {mse:,.4f}")
print(f"Root MSE: {mse**0.5:,.4f}")

# =======================
# 6. SAVE COMPRESSED MODEL
# =======================

joblib.dump(model, "cepalco_model.pkl", compress=3)
print("\nSaved compressed model as 'cepalco_model.pkl'")
