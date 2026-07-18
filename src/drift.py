import pandas as pd
from src.database import save_drift_event

REFERENCE_DATA = "data/creditcard.csv"

# -----------------------------
# Load dataset ONCE
# -----------------------------
reference = pd.read_csv(REFERENCE_DATA)

reference = reference.drop("Class", axis=1)

reference_means = reference.mean()


def check_data_drift():
    """
    Fast data drift detection.
    """

    # Simulate current production data
    current = reference.sample(
        n=500,
        random_state=None
    )

    drift_features = []

    for column in reference.columns:

        difference = abs(
            reference_means[column]
            - current[column].mean()
        )

        if difference > 0.1:
            drift_features.append(column)

    drift_detected = len(drift_features) > 0

    if drift_detected:

        if len(drift_features) >= 5:
            severity = "High"
            recommendation = "Retrain Model"

        elif len(drift_features) >= 3:
            severity = "Medium"
            recommendation = "Monitor Closely"

        else:
            severity = "Low"
            recommendation = "No Action Needed"

        save_drift_event(
            drift_detected,
            drift_features,
            severity,
            recommendation
        )

    return {
        "drift_detected": drift_detected,
        "drifted_features": drift_features,
        "total_features": len(reference.columns)
    }