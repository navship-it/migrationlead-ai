# MigrationLead AI
### Excel-first lead prioritisation for a small immigration consultancy
**Author: Navya Ravindran | Business Analysis · CRM Analytics · Applied ML**

Independent portfolio demonstration prepared for discussion with Immatrix. No affiliation, endorsement, access to company records, or measured company outcomes. All included records are fictional.

## The problem
A small team tracking enquiries in Excel needs a consistent follow-up queue, visibility into missed responses, and a way to evaluate future ML without buying a new CRM.

## The solution
1. **Use today:** transparent rule-based priorities and an Excel-compatible follow-up export.
2. **Explore for later:** logistic regression trained on 5,000 synthetic enquiries, evaluated against rules and newest-first ranking.
3. **Prove before investing:** a small live pilot, agreed service minimums and measured conversion outcomes.

This is decision support for commercial follow-up, not visa eligibility or approval prediction. No paid AI API, GPU or CRM subscription is required by this prototype. Hosting, security and ongoing support are separate production decisions.

## Run locally (Python 3.11 recommended)
Download/extract this repository and open a terminal in its folder.
```bash
python -m venv .venv
```
Activate on macOS/Linux:
```bash
source .venv/bin/activate
```
Activate on Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```
Then:
```bash
python -m pip install -r requirements.txt
python core.py
python -m unittest discover -s tests -v
python -m streamlit run app.py
```
Open the local address printed by Streamlit. The app has a follow-up queue, experimental ML lab and business case. A synthetic sample loads automatically. For Excel files, use **Save As → CSV UTF-8**; native .xlsx uploads are not supported.

## Repository map
- `app.py`: interactive Streamlit demonstration
- `core.py`: input validation, business rules, synthetic generator and ML experiment
- `data/sample_leads.csv`: 100 fictional 48-hour lead snapshots
- `data/lead_template.csv`: empty schema for anonymised CSV preparation
- `data/synthetic_history.csv`: reproducible simulation, not client evidence
- `reports/model_metrics.json`: actual computed simulation metrics
- `reports/synthetic_test_predictions.csv`: held-out predictions
- `docs/CLIENT_PROPOSAL.md`: client-facing proposal and pilot scope
- `docs/DEMO_SCRIPT.md`: a five-minute presentation walkthrough
- `docs/DATA_DICTIONARY.md`: schema, scoring timing and rules
- `docs/MODEL_CARD.md`: assumptions, evaluation and limitations
- `docs/GITHUB_SETUP.md`: beginner-friendly publishing guide

## Reproduced simulation results
The held-out period contains 1,277 leads with 172 conversions. The highest-ranked 256 leads include:

| Ranking approach | Conversions in top 256 | Precision | Share of all conversions captured |
|---|---:|---:|---:|
| Simulated ML | 70 | 27.3% | 40.7% |
| Business rules | 57 | 22.3% | 33.1% |
| Newest first | 37 | 14.5% | 21.5% |

These comparisons describe an artificial dataset whose relationships were designed by the author. They do not establish real predictive accuracy, additional revenue or causal conversion uplift. Newest-first is only one baseline; a real pilot must also measure the existing consultant workflow. Results may vary slightly across dependency versions.

## Architecture
Excel CSV → validation → explainable rules → consultant queue → CSV export.
Separately: synthetic history → time-based training/test split → ML evaluation report.
The synthetic ML model never scores uploaded business files. Export includes only lead ID, priority, score and action. Uploads are processed in app memory and are not intentionally written to disk; this is not a production security guarantee.

## Responsible first implementation
Keep the workbook as the source of truth. Review all leads within an agreed service window. Limit access; use pseudonymous IDs; do not upload passports, contact details or customer records to GitHub. Real data belongs in an approved private environment. A production version needs access control, audit logging, data retention arrangements, robust ingestion and an agreed owner.

## Portfolio positioning
Completed: reproducible synthetic data, functioning prioritisation code, interactive app source, model evaluation, tests and pilot documentation.
Not claimed: a live Immatrix engagement, production deployment, visa-domain expertise, or actual business uplift.
