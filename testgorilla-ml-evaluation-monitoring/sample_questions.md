ML Model Evaluation & Monitoring — Sample Assessment

Five scenario-based questions designed to assess practical ML engineering judgment across model evaluation, data drift, model promotion, production diagnosis, and explainability.

Skills Assessed

Model evaluation and metric selection
Data drift detection and interpretation
Model promotion and evaluation gates
Production performance diagnosis
SHAP-based model explainability

Question 1 — Choosing the Right Evaluation Metric

Scenario

You are evaluating a binary fraud-detection model. Fraud represents only 1% of all transactions.

Two candidate models produce:

Model A: Accuracy 99.2%, Precision 18%, Recall 82%, F1 30%
Model B: Accuracy 99.6%, Precision 72%, Recall 41%, F1 52%

The business states that missing fraudulent transactions is significantly more costly than reviewing legitimate transactions manually.

Which model is the better candidate for deployment?

A. Model B, because it has higher accuracy and F1
B. Model A, because its substantially higher recall better reflects the stated business cost
C. Model B, because precision is always more important than recall in fraud detection
D. Either model, because accuracy above 99% makes the difference negligible

Correct answer: B

Skill tested: Metric selection and business-aware model evaluation

Why: The question tests whether the candidate can select evaluation criteria based on business consequences rather than relying on accuracy alone.

Question 2 — Detecting Meaningful Data Drift

Scenario

A machine learning model has been stable in production for three months. Its validation performance was:

Precision: 91%
Recall: 88%
F1: 89%

A weekly monitoring report now shows that the distribution of several input features has changed substantially.

There is not yet enough newly labeled production data to calculate a reliable production F1 score.

What is the most appropriate next action?

A. Immediately retrain the model using the new production data
B. Ignore the drift because production F1 cannot yet be calculated
C. Investigate the drifted features and determine whether the changes could affect model behavior before deciding on retraining
D. Automatically roll back to the previous model

Correct answer: C

Skill tested: Data drift interpretation and production monitoring judgment

Why: Detecting drift is a signal for investigation, not by itself a reason to automatically retrain or roll back a model.

Question 3 — Safe Model Promotion

Scenario

A newly trained candidate model achieves an overall F1 score of 0.94, compared with 0.91 for the current production model.

Before promotion, evaluation shows:

Candidate recall on a critical minority class: 0.61
Current production recall on that class: 0.84
The deployment policy requires at least 0.75 recall for every critical class.

What should the ML engineer do?

A. Promote the candidate because its overall F1 score is higher
B. Promote the candidate and monitor its minority-class recall after deployment
C. Reject the candidate because it fails the required recall threshold for a critical class
D. Choose the candidate because overall F1 is always more important than class-level metrics

Correct answer: C

Skill tested: Model evaluation gates and safe production model promotion

Why: A model should not be promoted solely because its overall metric improves. A deployment gate for a critical class must also be satisfied.

Question 4 — Diagnosing Production Model Degradation

Scenario

A classification model has been running in production for six weeks.

Monitoring shows:

Prediction latency: unchanged
Infrastructure health: normal
Input volume: normal
Feature distributions: moderately changed
Precision: decreased from 93% to 86%
Recall: decreased from 90% to 89%
The largest precision drop occurs for one particular customer segment.

What should the ML engineer investigate first?

A. Increase the model's inference hardware
B. Retrain the model immediately using all available production data
C. Perform segment-level error analysis to determine whether the data or feature shift is causing the degradation
D. Increase the classification threshold without further investigation

Correct answer: C

Skill tested: Production model diagnosis and failure-slice analysis

Why: A production performance drop should first be diagnosed at the relevant slices and data/features before changing the model, infrastructure, or decision threshold.

Question 5 — Interpreting SHAP Explanations

Scenario

An ML model predicts whether a transaction should be flagged for review.

For one individual prediction, the SHAP explanation shows:

transaction_amount: +1.8
merchant_risk_score: +1.2
account_age: −0.7
transaction_count_24h: −0.2

The model's baseline output is 0.25.

Which interpretation is correct?

A. transaction_amount decreases the prediction because its SHAP value is positive
B. transaction_amount has the strongest contribution pushing this prediction in the positive direction relative to the model's baseline
C. account_age is the most important feature globally because its SHAP value is negative
D. SHAP values represent feature correlation and therefore cannot indicate a feature's contribution to an individual prediction

Correct answer: B

Skill tested: Local model explainability and SHAP interpretation

Why: SHAP values explain how individual features contribute to a specific prediction relative to the model's baseline. A positive value indicates a contribution in the positive direction, while a negative value pushes the prediction in the opposite direction.
