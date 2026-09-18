from fastapi import FastAPI
import pandas as pd
import subprocess
import json
import os
import sys

from src.database import (
    initialize_database,
    save_prediction,
    get_stats,
    get_recent_predictions,
    get_prediction_trend,
    get_metrics
)

from src.model_registry import (
    get_latest_model,
    get_model_version
)

from src.model_history import get_model_history
from src.drift import check_data_drift
from src.incident_report import generate_incident_report
from src.health_score import calculate_health_score

app = FastAPI(
    title="SentinelML Fraud Detection API"
)


# -----------------------------------
# Startup
# -----------------------------------

@app.on_event("startup")
def startup():

    initialize_database()

    print("✅ Database initialized successfully!")

    print("✅ SentinelML API Started")


# -----------------------------------
# Load Production Model
# -----------------------------------

model = get_latest_model()


# -----------------------------------
# Home
# -----------------------------------

@app.get("/")
def home():

    return {
        "message": "SentinelML API is running successfully"
    }


# -----------------------------------
# Predict Random Transaction
# -----------------------------------

@app.get("/predict")
def predict():

    df = pd.read_csv("data/creditcard.csv")

    random_row = df.sample(n=1)

    sample = random_row.drop("Class", axis=1)

    actual = int(random_row["Class"].iloc[0])

    prediction = int(model.predict(sample)[0])

    save_prediction(
        prediction=prediction,
        actual=actual,
        model_version=get_model_version()
    )

    return {
        "prediction": prediction,
        "actual": actual
    }


# -----------------------------------
# Predict Fraud Transaction
# -----------------------------------

@app.get("/predict-fraud")
def predict_fraud():

    df = pd.read_csv("data/creditcard.csv")

    fraud_df = df[df["Class"] == 1]

    random_row = fraud_df.sample(n=1)

    sample = random_row.drop("Class", axis=1)

    actual = int(random_row["Class"].iloc[0])

    prediction = int(model.predict(sample)[0])

    save_prediction(
        prediction=prediction,
        actual=actual,
        model_version=get_model_version()
    )

    return {
        "prediction": prediction,
        "actual": actual
    }


# -----------------------------------
# Dashboard Statistics
# -----------------------------------

@app.get("/stats")
def stats():

    return get_stats()


# -----------------------------------
# Prediction History
# -----------------------------------

@app.get("/history")
def history():

    rows = get_recent_predictions()

    history = []

    for row in rows:

        history.append(
            {
                "created_at": row[0].strftime("%Y-%m-%d %H:%M:%S"),
                "prediction": "Fraud" if row[1] == 1 else "Normal",
                "actual": "Fraud" if row[2] == 1 else "Normal",
                "model_version": row[3]
            }
        )

    return history


# -----------------------------------
# Prediction Trend
# -----------------------------------

@app.get("/trend")
def trend():

    rows = get_prediction_trend()

    trend = []

    for i, row in enumerate(rows, start=1):

        trend.append(
            {
                "created_at": row[0].strftime("%Y-%m-%d %H:%M:%S"),
                "prediction_number": i
            }
        )

    return trend


# -----------------------------------
# Model Metrics
# -----------------------------------

@app.get("/metrics")
def metrics():

    return get_metrics()


# -----------------------------------
# Drift Detection
# -----------------------------------

@app.get("/drift")
def drift():

    return check_data_drift()


# -----------------------------------
# Auto Retraining
# -----------------------------------

@app.get("/auto-retrain")
def auto_retrain():

    print("STEP 1")

    drift = check_data_drift()

    print("STEP 2")

    if not drift["drift_detected"]:
        print("STEP 3")

        return {
            "status": "No retraining needed",
            "reason": "No data drift detected",
            "drift": drift
        }

    print("STEP 4")

    recommendation = drift.get(
        "recommendation",
        "No Action Needed"
    )

    if recommendation != "Retrain Model":

        print("STEP 5")

        return {
            "status": "Retraining skipped",
            "reason": recommendation,
            "drift": drift
        }

    print("STEP 6")

    result = subprocess.run(
        [sys.executable, "src/retrain.py"],
        capture_output=True,
        text=True
    )

    print("STEP 7")

    return {
        "status": "Retraining completed",
        "output": result.stdout,
        "drift": drift
    }
# -----------------------------------
# Production Model Information
# -----------------------------------

@app.get("/model-info")
def model_info():

    metadata_path = os.path.join(
        "models",
        "metadata.json"
    )

    with open(metadata_path, "r") as file:

        metadata = json.load(file)

    return metadata


# -----------------------------------
# Model Registry
# -----------------------------------

@app.get("/model-history")
def model_history():

    return get_model_history()

@app.get("/incident-report")
def incident_report():

    drift = check_data_drift()

    report = generate_incident_report(drift)

    return report

@app.get("/dashboard")
def dashboard():

    drift = check_data_drift()

    metadata_path = os.path.join(
        "models",
        "metadata.json"
    )

    with open(metadata_path, "r") as file:
        model_info = json.load(file)

    # -------- History --------

    history_rows = get_recent_predictions()

    history = []

    for row in history_rows:
        history.append({
            "created_at": row[0].strftime("%Y-%m-%d %H:%M:%S"),
            "prediction": "Fraud" if row[1] == 1 else "Normal",
            "actual": "Fraud" if row[2] == 1 else "Normal",
            "model_version": row[3]
        })

    # -------- Trend --------

    trend_rows = get_prediction_trend()

    trend = []

    for i, row in enumerate(trend_rows, start=1):
        trend.append({
            "created_at": row[0].strftime("%Y-%m-%d %H:%M:%S"),
            "prediction_number": i
        })

    return {
        "stats": get_stats(),
        "model_info": model_info,
        "metrics": get_metrics(),
        "history": history,
        "trend": trend,
        "model_history": get_model_history(),
        "drift": drift,
        "health": calculate_health_score()
    }
# -----------------------------------
# AI Health Score
# -----------------------------------

@app.get("/health-score")
def health_score():

    return calculate_health_score()

