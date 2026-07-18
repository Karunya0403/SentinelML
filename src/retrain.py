import os
import json
import joblib
import pandas as pd
import sklearn
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient

from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

print("Python Executable:", os.sys.executable)
print("Scikit-learn Version:", sklearn.__version__)

DATA_PATH = "data/creditcard.csv"
MODELS_FOLDER = "models"


def train_new_model():

    print("Loading dataset...")

    mlflow.set_experiment("SentinelML Fraud Detection")

    df = pd.read_csv(DATA_PATH)

    # Faster retraining using a sample
    df = df.sample(50000, random_state=42)

    with mlflow.start_run():

        X = df.drop("Class", axis=1)
        y = df["Class"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        print("Training model...")

        model = RandomForestClassifier(
            n_estimators=50,
            random_state=42,
            n_jobs=-1
        )

        # -----------------------------
        # Log Parameters
        # -----------------------------
        mlflow.log_param("algorithm", "RandomForest")
        mlflow.log_param("n_estimators", 50)
        mlflow.log_param("dataset_size", len(df))

        model.fit(X_train, y_train)

        print("Evaluating model...")

        predictions = model.predict(X_test)

        accuracy = round(
            accuracy_score(y_test, predictions) * 100,
            2
        )

        precision = round(
            precision_score(
                y_test,
                predictions,
                zero_division=0
            ) * 100,
            2
        )

        recall = round(
            recall_score(
                y_test,
                predictions,
                zero_division=0
            ) * 100,
            2
        )

        f1 = round(
            f1_score(
                y_test,
                predictions,
                zero_division=0
            ) * 100,
            2
        )

        # -----------------------------
        # Log Metrics
        # -----------------------------
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        version = 1

        while os.path.exists(
            os.path.join(
                MODELS_FOLDER,
                f"model_v{version}.pkl"
            )
        ):
            version += 1

        model_name = f"model_v{version}.pkl"

        model_path = os.path.join(
            MODELS_FOLDER,
            model_name
        )

        # Save local model
        joblib.dump(model, model_path)

        # -----------------------------
        # Log & Register Model
        # -----------------------------
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="fraud_detection_model"
        )

        client = MlflowClient()

        model_uri = model_info.model_uri

        try:
            client.create_registered_model("SentinelML Fraud Detector")
        except Exception:
            pass

        client.create_model_version(
            name="SentinelML Fraud Detector",
            source=model_uri,
            run_id=mlflow.active_run().info.run_id
        )

        # -----------------------------
        # Tags
        # -----------------------------
        mlflow.set_tag("project", "SentinelML")
        mlflow.set_tag("model_version", model_name)

        metadata_path = os.path.join(
            MODELS_FOLDER,
            "metadata.json"
        )

        with open(metadata_path, "r") as file:
            current_metadata = json.load(file)

        current_f1 = current_metadata["f1_score"]

        if f1 >= current_f1:
            metadata = {
                "latest_model": model_name,
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "dataset_size": len(df),
                "algorithm": "RandomForest",
                "n_estimators": 50
            }

            with open(metadata_path, "w") as file:
                json.dump(metadata, file, indent=4)

            history_path = os.path.join(
                MODELS_FOLDER,
                "model_history.json"
            )

            if os.path.exists(history_path):

                with open(history_path, "r") as file:
                    history = json.load(file)

            else:

                history = []

            # Archive previous production model
            for model_entry in history:

                if model_entry["status"] == "Production":
                    model_entry["status"] = "Archived"

            # Add new production model
            history.append(
                {
                    "model": model_name,
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1,
                    "trained_at": metadata["trained_at"],
                    "status": "Production"
                }
            )

            with open(history_path, "w") as file:
                json.dump(history, file, indent=4)

            print("\n✅ New model promoted to production!")

        else:

            print("\n❌ New model rejected.")
            print(
                f"Current F1: {current_f1} | New F1: {f1}"
            )

        print(f"\nModel saved as {model_name}")

        print("\nModel Metrics")
        print("-------------------------")
        print(f"Accuracy : {accuracy}%")
        print(f"Precision: {precision}%")
        print(f"Recall   : {recall}%")
        print(f"F1 Score : {f1}%")


if __name__ == "__main__":
    train_new_model()