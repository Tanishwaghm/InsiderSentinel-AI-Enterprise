import streamlit as st
import pandas as pd
import joblib
from src.risk_engine import calculate_risk_score

st.set_page_config(page_title="InsiderSentinel Enterprise", layout="wide")

st.title("🛡 InsiderSentinel AI - Enterprise Edition")
st.markdown("User Behavior Analytics & Insider Threat Detection System")

model, scaler = joblib.load("models/trained_model.pkl")

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
