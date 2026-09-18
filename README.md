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

core Engineering Idea

SentinelML does not treat drift as equivalent to model failure.

That distinction matters.

A distribution can change without immediately making predictions worse.

Therefore:

Drift detected
      ↓
Investigate system health
      ↓
Evaluate model performance
      ↓
Decide whether intervention is justified
      ↓
Retrain
      ↓
Evaluate candidate model
      ↓
Promote only when appropriate

The objective is not:

"Retrain whenever something changes."

The objective is:

"Detect meaningful changes and make model intervention measurable and controlled."

System Components
1. FastAPI Model Serving

The inference layer exposes the machine-learning model through an API.

Responsibilities include:

Receiving prediction requests
Running model inference
Returning predictions
Connecting inference with the monitoring lifecycle

This creates a clear boundary between the model and the surrounding production system.

2. Prediction Logging

Predictions are persisted in PostgreSQL.

This creates historical data that can later be used for:

Monitoring
Distribution analysis
Prediction trends
Performance analysis
Drift investigation

Without historical prediction data, production monitoring becomes largely observational.

With it, the system can compare behaviour over time.

3. Drift Detection

SentinelML monitors changes in incoming data and model behaviour.

The monitoring layer considers:

Data drift
Feature drift
Model drift
Performance degradation

Threshold-based alerting is used to identify conditions requiring attention.

The important design principle is that drift becomes an observable signal rather than an invisible production problem.

4. AI Health Score

The dashboard provides an overall view of system health.

The health layer combines signals from the ML system and infrastructure to make degradation easier to understand.

Instead of forcing an engineer to inspect multiple components independently, the dashboard surfaces:

System Health
      │
      ├── Model status
      ├── Drift status
      ├── Performance signals
      ├── Infrastructure status
      └── Recommended action
5. Automated Retraining

When monitoring identifies a condition requiring intervention, SentinelML can initiate the retraining workflow.

The retraining pipeline:

Loads the fraud dataset.
Samples training data.
Creates stratified train/test splits.
Trains a Random Forest classifier.
Calculates evaluation metrics.
Logs parameters and metrics to MLflow.
Saves the trained model.
Versions the resulting model.
Registers the model with MLflow.

The retraining implementation uses a 50,000-row sample and evaluates:

Accuracy
Precision
Recall
F1

The purpose is not simply to produce a new model.

The purpose is to produce a measurable candidate model.

6. Model Versioning

MLflow provides experiment tracking and model-version management.

This makes it possible to reason about:

Model v1
   ↓
Model v2
   ↓
Model v3

rather than treating the currently deployed model as an anonymous artifact.

Version history provides a foundation for:

Reproducibility
Comparison
Auditing
Rollback strategies
Controlled promotion
7. Evaluation-Gated Promotion

One of the most important ideas in SentinelML is separating:

training a model

from

deciding whether that model should become production.

A newly trained model should not automatically replace the existing production model merely because retraining completed successfully.

The candidate should first be evaluated.

Conceptually:

Candidate Model
      │
      ▼
Evaluation
      │
      ├── Meets promotion criteria ──→ Candidate eligible
      │
      └── Fails criteria ────────────→ Keep current model

This introduces a safety boundary between experimentation and production.

Failure Modes Considered

A production-oriented system needs to consider what happens when components fail.

SentinelML was designed with several failure scenarios in mind.

Drift without performance degradation

The input distribution changes, but the model continues performing adequately.

Risk: unnecessary retraining.

Response: treat drift as a signal requiring evaluation, not automatic proof of model failure.

Retrained model performs worse

A new model can be trained successfully while producing inferior results.

Risk: blindly replacing a working production model.

Response: compare candidate performance before promotion.

Accuracy hides poor recall

Fraud detection is particularly sensitive to class imbalance.

A high accuracy value does not necessarily mean the system is catching enough fraudulent transactions.

Response: evaluate multiple metrics, including precision, recall, and F1.

PostgreSQL becomes unavailable

Prediction logging can fail independently of inference.

Risk: the model may still respond while the monitoring pipeline loses observability.

This demonstrates an important production principle:

A system can continue serving predictions while simultaneously becoming less observable.

Monitoring itself fails

A monitoring system cannot be considered reliable merely because the model is reliable.

If monitoring stops producing trustworthy signals, automated intervention can become unsafe.

This creates a second-order reliability problem:

Model reliability
        +
Monitoring reliability
        +
Retraining reliability
        =
Production ML reliability
Engineering Trade-offs
Why Random Forest?

Random Forest was selected as a practical baseline for the fraud-detection workflow.

Advantages:

Strong baseline performance
Works well with tabular data
Straightforward training workflow
Relatively simple deployment
Supports fast experimentation

The trade-off is that a more sophisticated production environment could require different models depending on latency, scale, interpretability, and performance requirements.

Why PostgreSQL?

Prediction logging requires persistent storage.

PostgreSQL provides a structured relational store for prediction history and monitoring queries.

At larger scale, the architecture could evolve toward:

Partitioned tables
Better indexing strategies
Retention policies
Asynchronous logging
Dedicated analytical storage
Why MLflow?

MLflow provides experiment tracking and model-version management.

Instead of relying entirely on manually managed files, the system can associate:

Model
+
Parameters
+
Metrics
+
Training run
+
Version

This improves reproducibility and makes model lifecycle management more explicit.

Why Docker?

Containerization creates clearer boundaries between services and their environments.

This makes it easier to separate:

API serving
Monitoring
Retraining
Dashboard
Supporting infrastructure

It also provides a path toward deployment environments such as cloud infrastructure.

Scaling Thought Experiment

The current project is intentionally manageable enough to reason about locally.

But what changes if the system receives millions of predictions?

Several components become bottlenecks.

Prediction logging

Synchronous database writes can increase inference latency.

A scalable architecture could introduce:

Prediction API
      ↓
Message Queue
      ↓
Async Logging Workers
      ↓
Database / Data Store

This decouples prediction latency from persistence.

Drift detection

Instead of repeatedly scanning the entire dataset, production systems could maintain rolling windows.

Reference Window
       vs
Current Window
       ↓
Drift Calculation
Retraining

Retraining should not block the inference service.

A larger deployment could use:

Monitoring
    ↓
Event / Queue
    ↓
Training Worker
    ↓
Evaluation
    ↓
Registry
    ↓
Deployment

This separates model lifecycle operations from real-time inference.

Model deployment

At higher traffic volumes, model serving could move behind:

Load balancing
Horizontal scaling
Dedicated model-serving infrastructure
Health checks
Automated rollback
Canary releases

The architecture would therefore evolve from a project-scale system into a distributed ML platform.

What I Would Build Next

The next iteration could strengthen the system in several areas.

1. Canary deployment

Deploy a candidate model to a small percentage of traffic before full promotion.

Production Model
      │
      ├────────────── 95%
      │
Candidate Model
      │
      └────────────── 5%

Compare behaviour before increasing traffic.

2. Automatic rollback

If the candidate model violates production thresholds:

Candidate
   ↓
Degradation detected
   ↓
Rollback
   ↓
Previous production model
3. Stronger data validation

Detect:

Missing features
Unexpected feature ranges
Schema changes
Invalid categorical values
Sudden data-volume changes

before those issues reach the model.

4. Better observability

Add structured monitoring for:

API latency
Error rates
Prediction throughput
Database health
Retraining duration
Model performance
Drift frequency
What SentinelML Demonstrates

The project started from a machine-learning problem.

It evolved into a systems problem.

The central lesson is:

Deploying a model is not the end of machine learning engineering. It is the beginning of the reliability problem.

The interesting engineering work happens around the model:

How do we know it is still working?
How do we detect when assumptions change?
How do we distinguish drift from actual degradation?
How do we retrain safely?
How do we decide whether a new model deserves production traffic?
How do we recover when infrastructure fails?
How does the architecture change when traffic grows?

Those questions are what turn an ML experiment into an engineering system.

Technical Stack
Layer	Technology
Language	Python
Model	Scikit-learn
API	FastAPI
Database	PostgreSQL
Experiment Tracking	MLflow
Dashboard	Streamlit
Containerization	Docker
CI/CD	GitHub Actions
Data Processing	Pandas / NumPy
Model Persistence	Joblib
Project Metrics
284,807 transaction fraud dataset
50,000 samples used in the retraining workflow
3 tracked model versions
Drift monitoring across multiple signals
Automated retraining workflow
MLflow model tracking
PostgreSQL prediction logging
Dockerized architecture
CI/CD validation
Engineering Philosophy

SentinelML follows one principle:

Automation should reduce operational risk, not remove engineering judgment.

A production ML system should not automatically react to every change.

It should:

Observe → Measure → Evaluate → Decide → Act → Verify

That is the reliability loop behind SentinelML.
