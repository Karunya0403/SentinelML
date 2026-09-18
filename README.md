# SentinelML

### Production ML Monitoring & Automated Retraining Platform

**Detect → Diagnose → Evaluate → Retrain → Version → Deploy**

SentinelML is a production-oriented machine-learning reliability platform designed around a simple problem:

> A model can be accurate when it is deployed and still become unreliable later. How do we detect that change and respond safely?

SentinelML combines model serving, prediction logging, drift detection, health monitoring, automated retraining, model versioning, and CI/CD into a single ML reliability workflow.

The system was built around a fraud-detection use case using a dataset containing **284,807 transactions**.

---

## Why SentinelML?

Training a model is only one part of the ML lifecycle.

After deployment, the environment around a model can change:

- Input distributions can shift.
- Individual features can drift.
- Prediction behaviour can change.
- Model performance can degrade.
- A retrained model can perform worse than the current model.
- Infrastructure failures can make monitoring unreliable.
- Model artifacts and metadata can become inconsistent.

A production ML system therefore needs more than inference.

It needs a mechanism for answering:

> **"Is the model still behaving as expected, and if not, what should happen next?"**

SentinelML treats monitoring and retraining as part of the same engineering lifecycle.

---

# Architecture

```text
                         ┌────────────────────┐
                         │      Incoming      │
                         │        Data        │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │   ML Model / API   │
                         │      FastAPI       │
                         └─────────┬──────────┘
                                   │
                          predictions
                                   │
                                   ▼
                         ┌────────────────────┐
                         │     PostgreSQL     │
                         │  Prediction Logs   │
                         └─────────┬──────────┘
                                   │
                                   ▼
                  ┌─────────────────────────────────┐
                  │       Monitoring Layer          │
                  │                                 │
                  │  • Data Drift                   │
                  │  • Feature Drift                │
                  │  • Model Drift                  │
                  │  • Performance Degradation      │
                  └───────────────┬─────────────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │   AI Health Score  │
                       │  + Alerting Logic  │
                       └─────────┬──────────┘
                                 │
                         threshold breach?
                          ┌──────┴──────┐
                         No             Yes
                         │               │
                         ▼               ▼
                  Continue Serving   Retraining
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Model Training   │
                              │ + Evaluation     │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │     MLflow       │
                              │ Model Versioning │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Promotion /      │
                              │ Deployment       │
                              └──────────────────┘
