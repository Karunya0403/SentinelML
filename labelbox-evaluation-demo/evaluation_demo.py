import json


def evaluate_model(metrics, thresholds):
    results = {}

    for metric, threshold in thresholds.items():
        value = metrics.get(metric, 0)

        results[metric] = {
            "value": value,
            "threshold": threshold,
            "passed": value >= threshold
        }

    approved = all(item["passed"] for item in results.values())

    return {
        "approved": approved,
        "results": results
    }


def analyze_failure_slices(slices):
    failures = []

    for name, metrics in slices.items():
        if metrics["recall"] < 60:
            failures.append({
                "slice": name,
                "issue": "Low recall",
                "recall": metrics["recall"]
            })

    return failures


if __name__ == "__main__":

    metrics = {
        "accuracy": 99.92,
        "precision": 90.91,
        "recall": 58.82,
        "f1_score": 71.43
    }

    thresholds = {
        "precision": 85.0,
        "recall": 50.0,
        "f1_score": 70.0
    }

    slices = {
        "overall": {
            "precision": 90.91,
            "recall": 58.82,
            "f1": 71.43
        },
        "fraud_detection": {
            "precision": 90.91,
            "recall": 58.82,
            "f1": 71.43
        }
    }

    evaluation = evaluate_model(metrics, thresholds)
    failures = analyze_failure_slices(slices)

    evaluation["failure_analysis"] = failures

    print(json.dumps(evaluation, indent=2))

    