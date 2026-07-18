import os
import json

MODELS_FOLDER = "models"


def get_model_history():

    history = []

    metadata_path = os.path.join(
        MODELS_FOLDER,
        "metadata.json"
    )

    if os.path.exists(metadata_path):

        with open(metadata_path, "r") as file:
            latest = json.load(file)

        for file_name in os.listdir(MODELS_FOLDER):

            if (
                file_name.startswith("model_v")
                and file_name.endswith(".pkl")
            ):

                history.append(
                    {
                        "model": file_name,
                        "status": (
                            "Production"
                            if file_name == latest["latest_model"]
                            else "Archived"
                        ),
                        "accuracy": str(latest["accuracy"])
                        if file_name == latest["latest_model"]
                        else "N/A",

                        "f1_score": str(latest["f1_score"])
                        if file_name == latest["latest_model"]
                        else "N/A",

                        "trained_at": latest["trained_at"]
                        if file_name == latest["latest_model"]
                        else "N/A"
                    }
                )

    history.sort(key=lambda x: x["model"])

    return history