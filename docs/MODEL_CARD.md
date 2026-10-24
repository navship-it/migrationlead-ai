# Model card: synthetic conversion demonstration
## Intended use
Portfolio demonstration of a supervised classification workflow. Not approved for real lead scoring. The rules module, separately, illustrates a possible operational queue.
## Target and timing
Paid within 30 days of arrival; features restricted to the first 48h. No payment, final-status or later interactions enter features. Leads already paid before scoring must be excluded from a real open-lead queue; this simplified generator does not simulate payment timestamps.
## Data generation
5,000 fictional records, NumPy seed 42. A logistic outcome process combines recorded engagement, response time, referral source and normally distributed unobserved variation, then samples Bernoulli outcomes. This intentionally makes some predictors informative. Model quality primarily measures recovery of designed relationships. It cannot validate generalisation to Immatrix.
## Training and evaluation
One-hot categorical variables, standardised numeric variables and logistic regression. Train on records whose arrival +32 days precedes 2025-10-01; test arrivals from that date through year-end. This conservative embargo ensures all training labels have matured at test start. Outcomes assumed fully observed by 2026-02-02. Preprocessing fitted only on training records; no test tuning. No hyperparameter search. No saved model pickle required; the app retrains the synthetic experiment when first opened.
## Metrics
Precision and conversion capture in the top 20%, average precision and Brier score. Compare rules and newest-first on the same holdout. Brier score is an aggregate probability-error measure, not proof of calibration. Calibration plots, uncertainty intervals, repeated time windows and segment-level evaluation remain future work for real data.
## Limitations and safeguards
Simulation does not include realistic missingness, cohort shifts, detailed activities, payment timestamps or duplicates. Inputs are validated but validation does not establish timestamp provenance. No causal conclusions, fairness certification or revenue claims. Keep human review and a service floor; otherwise prioritisation can create feedback loops by making low-ranked leads receive less attention. Track overrides and follow-up exposure. Do not transfer learned synthetic probabilities to client files.
