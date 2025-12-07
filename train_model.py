import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

# Load data
df = pd.read_csv("appliance_usage_dataset.csv")

# Select features
X = df[['FanHours', 'ACHours', 'RefHours', 'TVHours', 'MonitorHours', 'PumpHours']]
y = df['ElectricityBill']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluation
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print("\nMODEL TRAINING COMPLETE!")
print(f"R² Score: {r2:.4f}")
print(f"Mean Absolute Error: {mae:.2f}")

# Save trained model
joblib.dump(model, 'ElectricityPredictor.pkl')
print("\nModel saved as ElectricityPredictor.pkl")
