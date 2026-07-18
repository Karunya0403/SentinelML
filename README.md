# 🛡️ SentinelML

> **Production AI Monitoring & Automated Retraining Platform**

SentinelML is an end-to-end MLOps platform that monitors machine learning models in production. It combines model serving, prediction logging, performance monitoring, drift detection, automated retraining, and model version management into a unified system.

The project demonstrates how production-ready AI systems can continuously monitor model health, detect performance degradation, and automatically retrain models when necessary.

---

# ✨ Features

- 🔮 Fraud Detection API using FastAPI
- 📊 Real-time Monitoring Dashboard with Streamlit
- 🗄️ PostgreSQL Prediction Logging
- 📈 Data Drift Detection
- ❤️ AI Health Score
- 📚 Model Registry & Version History
- 🤖 Automated Model Retraining
- 📋 Prediction History
- 📊 Prediction Statistics
- 📉 Prediction Trend Visualization
- 📊 Confusion Matrix
- 🚀 Production Model Metadata
- 🔄 Automatic Production Model Promotion

---

# 🏗️ System Architecture

```text
                     User
                       │
                       ▼
             Streamlit Dashboard
                       │
                       ▼
                 FastAPI Backend
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
 Prediction API                 Monitoring APIs
       │                               │
       ▼                               ▼
 PostgreSQL Database            Model Metrics
       │                               │
       ▼                               ▼
 Prediction Logs              Drift Detection
                                       │
                                       ▼
                            Automatic Retraining
                                       │
                                       ▼
                             Model Registry Update
                                       │
                                       ▼
                              Production Model
```

---

# 🔄 Project Workflow

```text
Incoming Transaction
        │
        ▼
 FastAPI Prediction API
        │
        ▼
 Generate Prediction
        │
        ▼
 Save Prediction to PostgreSQL
        │
        ▼
 Dashboard Monitoring
        │
        ▼
 Drift Detection
        │
        ▼
 Auto Retraining
        │
        ▼
 Model Evaluation
        │
        ▼
 Best Model Promoted to Production
```

---

# 🚀 Dashboard Features

The Streamlit dashboard provides complete monitoring of the production ML system.

### 🩺 AI Health Score

- Overall AI Health
- System Status
- Active Issues
- Health Progress Indicator

### 📌 AI System Overview

- Models Trained
- Production Model
- Total Predictions
- AI Health Score

### 🚀 Production Model

- Model Version
- Algorithm
- Dataset Size
- Accuracy
- Precision
- Recall
- F1 Score
- Last Training Time

### 🟢 Infrastructure Monitoring

- API Status
- Database Status
- Model Status
- MLflow Status
- Docker Status
- n8n Status

### 📈 Drift Monitoring

- Drift Detection
- Drifted Features
- Total Features
- Recommended Actions

### 🚨 Active Alerts

- High Priority Alerts
- Drift Notifications
- Retraining Recommendations

### 📊 Analytics

- Prediction Statistics
- Prediction Distribution
- Prediction Trend
- Prediction History
- Confusion Matrix

### 📚 Model Registry

- Model Version History
- Search Models
- Production Model Tracking

### 🤖 Model Management

- Automatic Retraining
- Training Time
- Retraining Summary
- Drift Summary
- Retraining Logs

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| API Framework | FastAPI |
| Dashboard | Streamlit |
| Database | PostgreSQL |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Charts | Matplotlib |
| Heatmaps | Seaborn |
| Model Serialization | Joblib |
| Automation | n8n |
| Version Control | Git |
| Containerization | Docker |

---

# 📂 Project Structure

```text
ML-Monitoring-System/
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│   └── creditcard.csv
│
├── models/
│   ├── model_v1.pkl
│   ├── model_v2.pkl
│   └── ...
│
├── src/
│   ├── app.py
│   ├── train.py
│   ├── retrain.py
│   ├── database.py
│   ├── drift.py
│   ├── health_score.py
│   ├── metrics.py
│   ├── model_registry.py
│   ├── model_history.py
│   └── incident_report.py
│
├── tests/
│
├── requirements.txt
├── docker-compose.yml
├── Dockerfile.api
├── Dockerfile.dashboard
├── .env
└── README.md
```

---

# 🌐 API Endpoints

| Endpoint | Description |
|-----------|-------------|
| `/predict` | Generate a new prediction |
| `/predict-fraud` | Predict a fraud sample |
| `/stats` | Prediction statistics |
| `/history` | Recent prediction history |
| `/trend` | Prediction trend |
| `/metrics` | Model performance metrics |
| `/drift` | Detect data drift |
| `/health-score` | AI health score |
| `/model-info` | Production model information |
| `/model-history` | Model registry |
| `/incident-report` | System incidents |
| `/auto-retrain` | Retrain production model |
| `/dashboard` | Combined dashboard endpoint |

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/ML-Monitoring-System.git

cd ML-Monitoring-System
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file.

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sentinelml
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## Start PostgreSQL

Make sure PostgreSQL is running.

---

## Run FastAPI

```bash
uvicorn src.app:app --reload
```

API Documentation:

```
http://localhost:8000/docs
```

---

## Run Streamlit Dashboard

```bash
streamlit run dashboard/dashboard.py
```

Dashboard:

```
http://localhost:8501
```

---

# 📸 Dashboard Preview

> Add screenshots here after pushing the project.

### 🩺 AI Health Score

*(Screenshot)*

---

### 📌 AI System Overview

*(Screenshot)*

---

### 🚀 Production Model

*(Screenshot)*

---

### 📈 Drift Monitoring

*(Screenshot)*

---

### 📊 Prediction Distribution

*(Screenshot)*

---

### 📚 Model Registry

*(Screenshot)*

---

### 🤖 Model Management

*(Screenshot)*

---

# 💡 Future Improvements

- 🔔 Email Notifications
- 💬 Slack Alerts
- 📈 Prometheus Monitoring
- 📊 Grafana Dashboards
- ☸ Kubernetes Deployment
- 🔄 CI/CD Pipeline
- 🔐 Authentication & Role-Based Access
- ☁ Cloud Deployment (AWS, Azure, GCP)
- 🌍 Distributed Model Serving
- 🧪 A/B Model Testing

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Building production-ready ML APIs
- Monitoring deployed ML models
- Detecting data drift
- Logging predictions
- Model version management
- Automated retraining workflows
- Production dashboard development
- Backend API development
- Database integration
- End-to-end MLOps concepts

---

# 👩‍💻 Author

**Karunya G. K.**

B.Tech – Artificial Intelligence & Data Science

AI Engineer | Machine Learning | MLOps | Production AI Systems

---

## ⭐ If you found this project useful, consider giving it a star!