def create_review_view(drift_result):
    drifted_features = drift_result.get("drifted_features", [])

    return {
        "name": "SentinelML Drift Review",
        "description": "Review samples associated with detected model-data drift.",
        "drift_detected": drift_result.get("drift_detected", False),
        "drifted_features": drifted_features,
        "review_action": "Flag affected samples for visual inspection"
    }


if __name__ == "__main__":
    sample_drift = {
        "drift_detected": True,
        "drifted_features": ["V4", "V12", "V14"],
        "total_features": 30
    }

    import json
    print(json.dumps(create_review_view(sample_drift), indent=2))