from src.drift import check_data_drift


def calculate_health_score(drift=None):

    score = 100

    if drift is None:
        drift = check_data_drift()

    reasons = []

    # -------------------------
    # Drift Penalty
    # -------------------------

    if drift["drift_detected"]:

        drift_count = len(drift["drifted_features"])

        if drift_count >= 5:
            score -= 30
            reasons.append("High Data Drift")

        elif drift_count >= 3:
            score -= 20
            reasons.append("Moderate Data Drift")

        else:
            score -= 10
            reasons.append("Minor Data Drift")

    # -------------------------
    # Determine Health Status
    # -------------------------

    if score >= 90:
        status = "Excellent"

    elif score >= 75:
        status = "Healthy"

    elif score >= 60:
        status = "Warning"

    else:
        status = "Critical"

    return {
        "health_score": score,
        "status": status,
        "issues": reasons
    }