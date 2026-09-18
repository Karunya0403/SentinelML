import os
import json
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

print("DB_HOST =", os.getenv("DB_HOST"))
print("DB_PASSWORD =", os.getenv("DB_PASSWORD"))


def get_connection():

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "sentinelml"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD")
    )

    return conn

def get_current_model_version():

    metadata_path = os.path.join(
        Path(__file__).resolve().parent.parent,
        "models",
        "metadata.json"
    )

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    return metadata["latest_model"]

def save_prediction(prediction, actual, model_version):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO predictions
        (prediction, actual, model_version)
        VALUES (%s, %s, %s)
        """,
        (prediction, actual, model_version)
    )

    conn.commit()

    cur.close()
    conn.close()


def get_stats():

    conn = get_connection()

    cur = conn.cursor()

    # Total predictions
    cur.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cur.fetchone()[0]

    # Fraud predictions
    cur.execute(
        "SELECT COUNT(*) FROM predictions WHERE prediction = 1"
    )
    fraud_predictions = cur.fetchone()[0]

    # Normal predictions
    normal_predictions = total_predictions - fraud_predictions

    # Fraud rate
    fraud_rate = 0

    if total_predictions > 0:
        fraud_rate = round(
            (fraud_predictions / total_predictions) * 100,
            2
        )

    cur.close()
    conn.close()

   return {
    "total_predictions": total_predictions,
    "fraud_predictions": fraud_predictions,
    "normal_predictions": normal_predictions,
    "fraud_rate": fraud_rate,
    "model_version": get_current_model_version()
}


def get_recent_predictions(limit=10):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT created_at,
               prediction,
               actual,
               model_version
        FROM predictions
        ORDER BY created_at DESC
        LIMIT %s
        """,
        (limit,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


def get_prediction_trend():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT created_at
        FROM predictions
        ORDER BY created_at
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows
def get_metrics():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT prediction, actual
        FROM predictions
        WHERE actual IS NOT NULL
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    tp = fp = tn = fn = 0

    for prediction, actual in rows:

        if prediction == 1 and actual == 1:
            tp += 1

        elif prediction == 1 and actual == 0:
            fp += 1

        elif prediction == 0 and actual == 0:
            tn += 1

        elif prediction == 0 and actual == 1:
            fn += 1

    total = tp + tn + fp + fn

    accuracy = 0
    precision = 0
    recall = 0
    f1_score = 0

    if total > 0:
        accuracy = round(((tp + tn) / total) * 100, 2)

    if (tp + fp) > 0:
        precision = round((tp / (tp + fp)) * 100, 2)

    if (tp + fn) > 0:
        recall = round((tp / (tp + fn)) * 100, 2)

    if (precision + recall) > 0:
        f1_score = round(
            2 * precision * recall / (precision + recall),
            2
        )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn
    }
def initialize_database():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS predictions (

            id SERIAL PRIMARY KEY,

            prediction INT,

            actual INT,

            model_version VARCHAR(50),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    conn.commit()

    cur.close()
    conn.close()

    print("✅ Database initialized successfully!")
def save_drift_event(
    drift_detected,
    drifted_features,
    severity,
    recommendation
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO drift_history
        (
            drift_detected,
            drifted_features,
            severity,
            recommendation
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            drift_detected,
            ", ".join(drifted_features),
            severity,
            recommendation
        )
    )

    conn.commit()

    cur.close()
    conn.close()
