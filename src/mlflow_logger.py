import mlflow

# Use SQLite as the tracking backend
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# Create or use the experiment
mlflow.set_experiment("SentinelML")

with mlflow.start_run():

    mlflow.log_param("project", "SentinelML")
    mlflow.log_param("algorithm", "Random Forest")

    mlflow.log_metric("accuracy", 0.999)

print("✅ MLflow experiment created successfully!")