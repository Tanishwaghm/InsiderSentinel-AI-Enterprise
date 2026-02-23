import streamlit as st
import pandas as pd
import joblib
from src.risk_engine import calculate_risk_score

st.set_page_config(page_title="InsiderSentinel Enterprise", layout="wide")

st.title("🛡 InsiderSentinel AI - Enterprise Edition")
st.markdown("User Behavior Analytics & Insider Threat Detection System")

import os
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ---- Safe Path Handling (Cloud Compatible) ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "trained_model.pkl")

# Create models folder if not exists
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# ---- Load or Auto-Create Model ----
if not os.path.exists(MODEL_PATH):
    st.warning("Model not found. Creating new anomaly detection model...")

    # Create synthetic enterprise log data
    X_dummy = np.random.rand(1000, 7)

    scaler = StandardScaler()
    X_scaled_dummy = scaler.fit_transform(X_dummy)

    model = IsolationForest(contamination=0.1)
    model.fit(X_scaled_dummy)

    joblib.dump((model, scaler), MODEL_PATH)

else:
    model, scaler = joblib.load(MODEL_PATH)

uploaded_file = st.file_uploader("Upload Enterprise Log CSV")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    features = [
        "login_hour",
        "files_accessed",
        "data_downloaded_MB",
        "failed_logins",
        "usb_activity",
        "weekend_activity",
        "after_hours_activity"
    ]

    X_scaled = scaler.transform(df[features])

    anomaly_scores = model.decision_function(X_scaled)
    predictions = model.predict(X_scaled)

    df["Anomaly"] = predictions
    df["Risk_Score"] = [
        calculate_risk_score(score, df.iloc[i])
        for i, score in enumerate(anomaly_scores)
    ]

    st.subheader("Threat Summary")

    total = len(df)
    anomalies = len(df[df["Anomaly"] == -1])

    col1, col2 = st.columns(2)
    col1.metric("Total Users", total)
    col2.metric("High Risk Users", anomalies)

    st.dataframe(df.sort_values(by="Risk_Score", ascending=False))

    st.download_button(
        "Download Investigation Report",
        df.to_csv(index=False),
        "insider_threat_report.csv"
    )
