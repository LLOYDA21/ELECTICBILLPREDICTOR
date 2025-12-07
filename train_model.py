import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# Load dataset
df = pd.read_csv("appliance_usage_dataset.csv")

# Features (input)
X = df[['FanHours', 'ACHours', 'RefHours', 'TVHours', 'MonitorHours', 'PumpHours']]

# Outputs (targets)
y = df[['KwhConsumption', 'ElectricityBill']]   # two columns to predict

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Multi-output Linear Regression
model = MultiOutputRegressor(LinearRegression())
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluation for each output
r2_kwh = r2_score(y_test['KwhConsumption'], y_pred[:, 0])
r2_bill = r2_score(y_test['ElectricityBill'], y_pred[:, 1])

mae_kwh = mean_absolute_error(y_test['KwhConsumption'], y_pred[:, 0])
mae_bill = mean_absolute_error(y_test['ElectricityBill'], y_pred[:, 1])

print("\nMODEL TRAINING COMPLETE!")
print(f"KWH   → R²: {r2_kwh:.4f}, MAE: {mae_kwh:.2f}")
print(f"BILL  → R²: {r2_bill:.4f}, MAE: {mae_bill:.2f}")

# Save model
joblib.dump(model, 'ElectricityKwhPredictor.pkl')
print("\nModel saved as ElectricityKwhPredictor.pkl")
