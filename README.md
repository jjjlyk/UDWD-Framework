# UDWD Framework

**Detecting and Visualizing Digital Waste in Corporate Email Communications**
*A Machine Learning Approach for Estimating Energy Savings and CO₂ Reduction*

<!-- TODO: replace with your Streamlit app URL -->
**Live dashboard:** https://udwd-framework.streamlit.app/

---

## Overview

Corporate email systems accumulate large amounts of **digital waste**: duplicated messages, near-identical forwards, mass broadcasts, and short, aging messages nobody revisits. This data still has to be stored, backed up, and powered, yet it is rarely measured.

The **Unstructured Data Waste Detection (UDWD) Framework** is a pipeline that detects, categorizes, and visualizes digital waste in email, then translates the reclaimable storage into energy and CO₂ estimates. It is applied to the [Enron Email Corpus](https://www.cs.cmu.edu/~enron/) (517,401 emails, ~150 mailboxes, 1999–2002).

## Key results

| Metric | Value |
|---|---|
| Emails analyzed | 517,401 |
| Classified as digital waste | 415,004 (80.2%) |
| Reclaimable storage | 1,013.51 MB of 1,355.35 MB |
| **Storage reduction** | **74.78%** |
| Random Forest F1 (held-out test set) | 0.9122 |
| Random Forest F1 (10-fold CV, training set) | 0.9510 ± 0.0016 |
| Estimated energy saved | 0.002027 kWh / year |
| Estimated CO₂ reduced | 0.000472 kg / year |

## How it works

1. **Parse:** extract body, sender, recipients, date, and thread headers from each email.
2. **Deduplicate:** flag exact copies (SHA-256) and near-copies (MinHash LSH, Jaccard ≥ 0.85).
3. **Label:** apply the waste taxonomy below, in priority order.
4. **Learn:** train a supervised Random Forest and an unsupervised Isolation Forest on 5,000 TF-IDF features + 4 metadata features (70 / 15 / 15 stratified split).
5. **Explain:** rank feature influence with SHAP on 1,000 stratified test records.
6. **Estimate:** convert waste storage to energy and CO₂ (`MB × 0.000002 kWh/MB/yr × 0.233 kg CO₂/kWh`).

### Waste taxonomy

| Category | Rule | Emails |
|---|---|---|
| Exact Duplicates | Identical SHA-256 hash of the raw body | 266,537 |
| Near-Duplicates | MinHash LSH Jaccard similarity ≥ 0.85 | 54,074 |
| Near-Zero Content | ≤ 5 words after cleaning | 6,339 |
| Dark Data | Older than 365 days **and** ≤ 50 words | 81,164 |
| Broadcast Redundancy | ≥ 10 recipients **and** TF-IDF similarity ≥ 0.70 | 6,890 |
| Valuable | None of the above | 99,128 |

## Repository contents

| File | Description |
|---|---|
| `DGG_UDWD_Pipeline.ipynb` | Full pipeline notebook (Google Colab) with final outputs |
| `streamlit_app.py` | Results dashboard (uses the notebook's final values; no recomputation) |
| `requirements.txt` | Dependencies for the dashboard |
| `.streamlit/config.toml` | Dashboard theme |

## Running the dashboard locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open http://localhost:8501.

## Reproducing the pipeline

The notebook is designed for **Google Colab**. It expects the Enron corpus tarball (`enron_mail_20150507.tar.gz`, from https://www.cs.cmu.edu/~enron/) in Google Drive at `MyDrive/Thesis/`. Full execution is compute-heavy (parsing, LSH, pairwise similarity, 10-fold CV, SHAP) and can take several hours.

Main libraries: scikit-learn, pandas, NumPy, datasketch, NLTK, SHAP, matplotlib, seaborn.

## License

Released under the [MIT License](LICENSE).
