import os
import json
import joblib

MODELS_FOLDER = "models"


def get_latest_model():

    metadata_path = os.path.join(
        MODELS_FOLDER,
        "metadata.json"
    )

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    latest_model = metadata["latest_model"]

    model_path = os.path.join(
        MODELS_FOLDER,
        latest_model
    )

    return joblib.load(model_path)


def get_model_version():

    metadata_path = os.path.join(
        MODELS_FOLDER,
        "metadata.json"
    )

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    return metadata["latest_model"]