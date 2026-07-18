import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import os
import subprocess


API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000"
)


import time

def fetch_api(endpoint):

    print(f"Calling {endpoint}...")

    start = time.time()

    try:
        response = requests.get(
            f"{API_URL}/{endpoint}",
            timeout=300
        )

        elapsed = time.time() - start

        print(f"{endpoint}: {response.status_code} ({elapsed:.2f} sec)")

        if response.status_code == 200:
            return response.json()

        print("Response:", response.text)

    except Exception as e:
        print(f"{endpoint} ERROR:", e)
        st.error(f"{endpoint}: {e}")

    return None

st.set_page_config(
    page_title="SentinelML Dashboard",
    page_icon="🛡️",
    layout="wide"
)
st_autorefresh(
    interval=60000,   # 60 seconds
    key="dashboard_refresh"
)
st.markdown("""
<style>

.block-container{
    padding-top:1.2rem;
}

.health-card{

background:linear-gradient(135deg,#1E293B,#0F172A);

border-radius:20px;

padding:30px;

border:1px solid #334155;

box-shadow:0px 8px 25px rgba(0,0,0,.35);

margin-bottom:30px;

}

.health-title{

text-align:center;

font-size:32px;

font-weight:bold;

margin-bottom:10px;

}

.health-score{

text-align:center;

font-size:72px;

font-weight:bold;

}

.health-status{

text-align:center;

font-size:24px;

font-weight:bold;

margin-top:15px;

}

.health-issue{

text-align:center;

font-size:18px;

margin-top:12px;

color:#CBD5E1;

}

.progress{

height:16px;

background:#334155;

border-radius:10px;

overflow:hidden;

margin-top:20px;

}

.progress-bar{

height:100%;

border-radius:10px;

}

div[data-testid="metric-container"]{

background:#1E293B;

border-radius:15px;

padding:20px;

border:1px solid #334155;

box-shadow:0px 3px 10px rgba(0,0,0,.25);

}
</style>
""", unsafe_allow_html=True)



st.markdown("""
# 🛡️ SentinelML

### Production AI Reliability Platform
""")

st.markdown(
    """
<small>

Monitor • Detect • Explain • Retrain • Govern

</small>
""",
    unsafe_allow_html=True
)

st.caption(
    "FastAPI  |  PostgreSQL  |  Docker  |  Streamlit  |  MLflow  |  n8n"
)


st.divider()

st.divider()
dashboard = fetch_api("dashboard")

stats = dashboard["stats"]
model_info = dashboard["model_info"]
health = dashboard["health"]
drift = dashboard["drift"]
metrics = dashboard["metrics"]
history = dashboard["history"]
trend = dashboard["trend"]
model_history = dashboard["model_history"]
# -----------------------------
# AI Health Score
# -----------------------------

if health:

    score = health["health_score"]
    status = health["status"]
    issues = health["issues"]

    if score >= 90:
        color = "#22c55e"

    elif score >= 75:
        color = "#facc15"

    else:
        color = "#ef4444"

    issue_text = "<br>".join(issues)

    st.markdown(
    f"""
<div class="health-card">

<h2 style="text-align:center;">
🩺 AI HEALTH SCORE
</h2>

<div class="health-score">
{score}
</div>

<div class="progress">

<div
class="progress-bar"
style="
width:{score}%;
background:{color};
">
</div>

</div>

<div
class="health-status"
style="color:{color};">

{status}

</div>

<div class="health-issue">

{"<br>".join(issues)}

</div>

</div>
""",
    unsafe_allow_html=True
)
st.subheader("📌 AI System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Models Trained",
        len(model_history)
    )

with col2:
    st.metric(
        "Production Model",
        model_info["latest_model"]
    )

with col3:
    st.metric(
        "Total Predictions",
        stats["total_predictions"]
    )

with col4:
    st.metric(
        "AI Health",
        f"{health['health_score']}%"
    )

st.divider()
# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🛡️ SentinelML")

st.sidebar.caption("AI Reliability Platform")
st.sidebar.markdown("---")

st.sidebar.subheader("Deployment Overview")

st.sidebar.write("**Model:** Fraud Detection")
st.sidebar.write(
    f"**Version:** {model_info['latest_model']}"
)
st.sidebar.write("**Framework:** FastAPI")
st.sidebar.write("**Dashboard:** Streamlit")
st.sidebar.write("**Database:** PostgreSQL")

st.sidebar.markdown("---")

st.sidebar.subheader("Infrastructure")

if stats:
    st.sidebar.success("🟢 API Online")
else:
    st.sidebar.error("🔴 API Offline")

st.sidebar.success("🟢 Database Connected")
st.sidebar.success("🟢 Model Loaded")
st.sidebar.success("🟢 MLflow Connected")
st.sidebar.success("🟢 n8n Automation")
st.sidebar.success("🟢 Docker Running")

st.sidebar.markdown("---")

st.sidebar.subheader("Engineer")

st.sidebar.write("Karunya G. K.")

st.sidebar.caption(
    "AI Engineer • MLOps • Production ML"
)
# -----------------------------
# Generate Prediction
# -----------------------------

col1, col2 = st.columns([1, 4])

with col1:

    if st.button(
        "▶ Generate Prediction",
        width="stretch"
    ):

        response = requests.get(
    f"{API_URL}/predict"
)

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction generated successfully!")

        

            prediction = result["prediction"]
            actual = result["actual"]

            pred_col1, pred_col2 = st.columns(2)

            with pred_col1:
                st.metric(
                    "Model Prediction",
                    "🚨 Fraud" if prediction == 1 else "✅ Normal"
                )

            with pred_col2:
                st.metric(
                    "Actual Class",
                    "🚨 Fraud" if actual == 1 else "✅ Normal"
                )

        else:

            st.error(
                "Prediction request failed."
            )

with col2:

    st.info(
        "Click the button to generate a new fraud prediction."
    )
# -----------------------------
# Production Model
# -----------------------------

st.subheader("🚀 Production Model")

if model_info:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Model Version",
            model_info["latest_model"]
        )

    with col2:
        st.metric(
            "Algorithm",
            model_info["algorithm"]
        )

    with col3:
        st.metric(
            "Dataset Size",
            model_info["dataset_size"]
        )

    col4, col5, col6, col7 = st.columns(4)

    with col4:
        st.metric(
            "Accuracy",
            f"{model_info['accuracy']}%"
        )

    with col5:
        st.metric(
            "Precision",
            f"{model_info['precision']}%"
        )

    with col6:
        st.metric(
            "Recall",
            f"{model_info['recall']}%"
        )

    with col7:
        st.metric(
            "F1 Score",
            f"{model_info['f1_score']}%"
        )

    st.info(
        f"Last Trained: {model_info['trained_at']}"
    )

else:
    st.error("Could not load production model information.")

st.divider()
st.divider()

# -----------------------------
# System Health
# -----------------------------

st.subheader("🟢 System Health")

health_col1, health_col2, health_col3, health_col4 = st.columns(4)

with health_col1:

    if stats:
        st.metric("API Status", "🟢 Online")
    else:
        st.metric("API Status", "🔴 Offline")

with health_col2:
    st.metric("Database", "🟢 Connected")

with health_col3:
    st.metric("Model", "🟢 Loaded")

with health_col4:
    st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))

st.divider()

# -----------------------------
# Data Drift Monitoring
# -----------------------------

st.subheader("📈 Data Drift Monitoring")


if drift:

    drift_col1, drift_col2, drift_col3 = st.columns(3)

    with drift_col1:
        if drift["drift_detected"]:
            st.error("🔴 Drift Detected")
        else:
            st.success("🟢 No Drift")

    with drift_col2:
        st.metric(
            "Drifted Features",
            len(drift["drifted_features"])
        )

    with drift_col3:
        st.metric(
            "Total Features",
            drift["total_features"]
        )

    if drift["drift_detected"]:
        st.warning(
            "Drift detected in:\n\n"
            + ", ".join(drift["drifted_features"])
        )
    else:
        st.success("No feature drift detected.")

else:
    st.error("Could not load drift information.")

st.divider()

# -----------------------------
# Active Alerts
# -----------------------------

st.subheader("🚨 Active Alerts")

if drift:

    if drift["drift_detected"]:

        st.error(
            "🔴 HIGH PRIORITY\n\n"
            "Data Drift Detected\n\n"
            "Recommended Action: Retrain Production Model"
        )

        if drift["drifted_features"]:

            st.write("### Affected Features")

            for feature in drift["drifted_features"]:
                st.write(f"• {feature}")

    else:

        st.success(
            "🟢 No Active Alerts\n\n"
            "System operating normally."
        )

else:

    st.warning(
        "⚠️ Unable to determine system alert status."
    )

st.divider()

# -----------------------------
# Statistics
# -----------------------------

if stats:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Predictions",
            stats["total_predictions"]
        )

    with col2:
        st.metric(
            "Fraud Predictions",
            stats["fraud_predictions"]
        )

    with col3:
        st.metric(
            "Normal Predictions",
            stats["normal_predictions"]
        )

    st.divider()

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "Fraud Rate",
            f"{stats['fraud_rate']}%"
        )

    with col5:
        st.metric(
            "Model Version",
            stats["model_version"]
        )

else:
    st.error("Could not connect to FastAPI.")
    st.stop()

# -----------------------------
# Model Performance
# -----------------------------

st.divider()

st.subheader("🤖 Model Performance")


if metrics:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Accuracy",
            f"{metrics['accuracy']}%"
        )

    with col2:
        st.metric(
            "Precision",
            f"{metrics['precision']}%"
        )

    with col3:
        st.metric(
            "Recall",
            f"{metrics['recall']}%"
        )

    with col4:
        st.metric(
            "F1 Score",
            f"{metrics['f1_score']}%"
        )

else:
    st.error("Could not load model metrics.")

# -----------------------------
# Prediction History
# -----------------------------

st.divider()

st.subheader("📋 Recent Predictions")



if history:

    df = pd.DataFrame(history)

    st.dataframe(df, width="stretch")

else:
    st.error("Could not load prediction history.")

# -----------------------------
# Prediction Distribution
# -----------------------------

st.divider()

st.subheader("📊 Prediction Distribution")

chart_data = pd.DataFrame(
    {
        "Prediction": ["Normal", "Fraud"],
        "Count": [
            stats["normal_predictions"],
            stats["fraud_predictions"]
        ]
    }
)

fig = px.pie(
    chart_data,
    names="Prediction",
    values="Count",
    hole=0.55,
    title="Prediction Distribution"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    showlegend=True
)

st.plotly_chart(fig, width="stretch")

# -----------------------------
# Prediction Trend
# -----------------------------

st.divider()

st.subheader("📈 Prediction Trend")


if trend:

    trend_df = pd.DataFrame(trend)

    if not trend_df.empty:

        fig = px.line(
            trend_df,
            x="created_at",
            y="prediction_number",
            markers=True,
            title="Prediction Trend"
        )

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Prediction Number"
        )

        st.plotly_chart(fig, width="stretch")

    else:
        st.info("No prediction data available.")

else:
    st.error("Could not load prediction trend.")

# -----------------------------
# Confusion Matrix
# -----------------------------

st.divider()

st.subheader("📊 Confusion Matrix")


if metrics:

    confusion_matrix = [
        [
            metrics["true_negative"],
            metrics["false_positive"]
        ],
        [
            metrics["false_negative"],
            metrics["true_positive"]
        ]
    ]

    fig, ax = plt.subplots(figsize=(7,6))

    sns.heatmap(
        confusion_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Normal", "Fraud"],
        yticklabels=["Normal", "Fraud"],
        ax=ax
    )

    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    plt.tight_layout()

    st.pyplot(fig)

else:
    st.error("Could not load confusion matrix.")

# -----------------------------
# Model Registry
# -----------------------------

st.divider()

st.subheader("📚 Model Registry")

if model_history:

    history_df = pd.DataFrame(model_history)

    search = st.text_input(
        "🔍 Search Model",
        placeholder="Example: model_v10"
    )

    if search:

        history_df = history_df[
            history_df["model"]
            .str.contains(search, case=False)
        ]

    st.dataframe(
        history_df,
        width="stretch",
        hide_index=True
)

else:

    st.error(
        "Could not load model registry."
    )

st.divider()

st.divider()

st.subheader("🤖 Model Management")

if st.button("🔄 Retrain Production Model"):

    start = time.time()

    with st.spinner("🔄 Retraining production model..."):
        result = fetch_api("auto-retrain")

    elapsed = round(time.time() - start, 2)

    if result:

        st.success("🎉 Retraining Completed!")

        st.info(f"⏱ Training Time: {elapsed} seconds")

        st.subheader("📋 Retraining Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Status",
                result["status"]
            )

        with col2:
            st.metric(
                "Training Time",
                f"{elapsed}s"
            )

        if "drift" in result:

            drift = result["drift"]

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Drift Detected",
                    "Yes" if drift["drift_detected"] else "No"
                )

            with col2:
                st.metric(
                    "Severity",
                    drift.get("severity", "Unknown")
                )

            if drift["drift_detected"]:

                st.warning("⚠️ Drift detected in the following features:")

                for feature in drift["drifted_features"]:
                    st.write(f"• {feature}")

                st.info(
                    f"Recommendation: {drift.get('recommendation', 'No recommendation available')}"
                )

        if "output" in result:

            with st.expander("📜 Retraining Logs"):
                st.code(result["output"])

    else:

        st.error("❌ Retraining failed.")