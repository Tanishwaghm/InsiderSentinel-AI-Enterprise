import numpy as np

def calculate_risk_score(anomaly_score, row):
    risk = (1 - anomaly_score) * 50

    if row["after_hours_activity"] == 1:
        risk += 15

    if row["data_downloaded_MB"] > 300:
        risk += 20

    if row["failed_logins"] > 3:
        risk += 10

    if row["usb_activity"] == 1:
        risk += 10

    return round(min(risk, 100), 2)
