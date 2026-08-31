"""
SuperAnnotate → Hugging Face → SentinelML Evaluation Gate

Proof-of-work demonstrating an evaluation-first ML workflow:
1. Structured NLP dataset
2. Model evaluation
3. Per-category quality checks
4. Promotion gate

The SuperAnnotate step is represented as the data-labeling stage.
"""

from dataclasses import dataclass


@dataclass
class EvaluationResult:
    accuracy: float
    f1_score: float
    category_f1: dict


def evaluate_model(result: EvaluationResult, min_f1: float = 0.90):
    failures = []

    if result.f1_score < min_f1:
        failures.append(
            f"Overall F1 {result.f1_score:.2f} < {min_f1:.2f}"
        )

    for category, score in result.category_f1.items():
        if score < min_f1:
            failures.append(
                f"{category} F1 {score:.2f} < {min_f1:.2f}"
            )

    return {
        "approved": len(failures) == 0,
        "accuracy": result.accuracy,
        "f1_score": result.f1_score,
        "category_f1": result.category_f1,
        "failures": failures,
    }


if __name__ == "__main__":
    result = EvaluationResult(
        accuracy=0.96,
        f1_score=0.94,
        category_f1={
            "toxic": 0.95,
            "insult": 0.93,
            "threat": 0.91,
            "identity_hate": 0.94,
            "obscene": 0.96,
        },
    )

    evaluation = evaluate_model(result)

    import json

    print(json.dumps(evaluation, indent=2))