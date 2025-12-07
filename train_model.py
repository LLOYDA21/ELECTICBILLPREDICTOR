import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from lightgbm import LGBMRegressor, early_stopping

df = pd.read_csv("datasets.csv")
print("Loaded rows:", len(df))

day_map = {
    "Monday":0,"Tuesday":1,"Wednesday":2,
    "Thursday":3,"Friday":4,
    "Saturday":5,"Sunday":6
}

df["day_of_week"] = df["day_of_week"].map(day_map)

features = [
    "temperature",
    "humidity",
    "occupancy",
    "number_of_appliances_used",
    "day_of_week",
    "tariff_rs_per_kwh"
]
target = "total_energy_kwh"

if "weather" in df.columns:
    df = pd.get_dummies(df, columns=["weather"], drop_first=True)
    weather_cols = [c for c in df.columns if c.startswith("weather_")]
    features += weather_cols
else:
    weather_cols = []


X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = LGBMRegressor(
    n_estimators=1200,
    learning_rate=0.03,
    num_leaves=63,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=0.1,
    random_state=42
)

print("Training HIGH-ACCURACY model...")


try:
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        eval_metric='l2',
        callbacks=[early_stopping(stopping_rounds=50)],
        verbose=False
    )
except:
    print("Early stopping not supported in this version.")
    model.fit(X_train, y_train)

preds = np.clip(model.predict(X_test), 0, None)

print("\nMODEL PERFORMANCE:")
print("MAE =", mean_absolute_error(y_test, preds))
print("R² =", r2_score(y_test, preds))

joblib.dump(
    {
        "model": model,
        "features": features
    },
    "cepalco_monthly_model.pkl",
    compress=9
)

print("\nMODEL SAVED SUCCESSFULLY ✅")


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

input_df = pd.DataFrame([example])[features]
kwh = max(model.predict(input_df)[0], 0)
bill = kwh * example["tariff_rs_per_kwh"]

print("\nExample Prediction:")
print("Predicted kWh =", kwh)
print("Monthly bill =", bill)
