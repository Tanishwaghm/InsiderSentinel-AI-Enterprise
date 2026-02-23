import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../data/enterprise_employee_logs.csv")

features = [
    "login_hour",
    "files_accessed",
    "data_downloaded_MB",
    "failed_logins",
    "usb_activity",
    "weekend_activity",
    "after_hours_activity"
]

X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(X_scaled)

joblib.dump((model, scaler), "../models/trained_model.pkl")

print("Model trained and saved.")
