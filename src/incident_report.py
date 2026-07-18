from datetime import datetime
import random


def generate_incident_report(drift_result):

    severity = "Low"
    recommendation = "Continue Monitoring"

    drift_count = len(drift_result["drifted_features"])

    if drift_count >= 5:
        severity = "High"
        recommendation = "Retrain Production Model"

    elif drift_count >= 3:
        severity = "Medium"
        recommendation = "Monitor Closely"

    confidence = random.randint(85, 98)

    if severity == "High":
        impact = (
            "Model performance may degrade significantly."
        )

    elif severity == "Medium":
        impact = (
            "Some prediction quality degradation expected."
        )

    else:
        impact = (
            "No immediate business impact expected."
        )

    report = {

        "incident_id":
            f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}",

        "generated_at":
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "severity":
            severity,

        "drifted_features":
            drift_result["drifted_features"],

        "business_impact":
            impact,

        "recommendation":
            recommendation,

        "confidence":
            f"{confidence}%"
    }

    return report