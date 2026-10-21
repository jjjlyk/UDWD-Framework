# ── UDWD THESIS DEFENSE DEMO — STREAMLIT VERSION ─────────────────────────
# Standalone port of the Gradio dashboard (last cell of DGG_UDWD_Pipeline.ipynb).
# All values are the FINAL results from the notebook — nothing is recomputed.
#
# Run locally:  streamlit run streamlit_app.py

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import streamlit as st

st.set_page_config(page_title="UDWD Thesis Demo", page_icon="📧", layout="wide")

st.markdown("""
<style>
.stat-box { background:#f0f4f8; border-radius:10px; padding:14px 10px;
            text-align:center; border:1px solid #d1dce8; height:100%; }
.stat-num { font-size:1.45em; font-weight:800; color:#1a5276; line-height:1.1; }
.stat-lbl { font-size:0.80em; color:#555; margin-top:4px; }
</style>
""", unsafe_allow_html=True)


def stat_box(num, lbl):
    st.markdown(f'<div class="stat-box"><div class="stat-num">{num}</div>'
                f'<div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)


def show(fig):
    st.pyplot(fig, width='stretch')
    plt.close(fig)


def make_waste_chart():
    labels = ['Exact\nDuplicates', 'Near\nDuplicates', 'Dark\nData',
              'Near-Zero\nContent', 'Broadcast\nRedundancy', 'Valuable']
    values = [266537, 54074, 81164, 6339, 6890, 99128]
    colors = ['#c0392b','#e74c3c','#e67e22','#f39c12','#d35400','#27ae60']
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.bar(labels, values, color=colors, edgecolor='white', linewidth=0.8)
    ax.set_title('Email Classification Results — UDWD Framework', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel('Number of Emails', fontsize=10)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1500,
                f'{val:,}', ha='center', va='bottom', fontsize=8.5, fontweight='bold')
    ax.set_ylim(0, max(values) * 1.15)
    ax.spines[['top','right']].set_visible(False)
    fig.tight_layout()
    return fig

def make_storage_chart():
    stages = ['Original\nCorpus','After Exact\nDedup','After Near-Dup\nDedup','Reclaimable\nWaste Storage']
    sizes  = [1355.35, 647.60, 483.60, 1013.51]
    colors = ['#2980b9','#27ae60','#27ae60','#c0392b']
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(stages, sizes, color=colors, edgecolor='white', linewidth=0.8, width=0.5)
    ax.set_title('Storage Across Pipeline Stages', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel('Storage (MB)', fontsize=10)
    for bar, val in zip(bars, sizes):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 12,
                f'{val:.2f} MB', ha='center', va='bottom', fontsize=9, fontweight='bold')
    ax.set_ylim(0, 1600)
    ax.spines[['top','right']].set_visible(False)
    fig.tight_layout()
    return fig

def make_rf_cm():
    cm = np.array([[13566, 1304],[1191, 12968]])
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt=',d', cmap='Blues', ax=ax,
                xticklabels=['Pred Valuable','Pred Waste'],
                yticklabels=['Actual Valuable','Actual Waste'],
                linewidths=0.5, cbar=False, annot_kws={'size':13,'weight':'bold'})
    ax.set_title('Random Forest — Confusion Matrix\n(Test Set, n = 29,029)', fontsize=11, fontweight='bold')
    fig.tight_layout()
    return fig

def make_if_cm():
    cm = np.array([[3848, 11022],[11025, 3134]])
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt=',d', cmap='Oranges', ax=ax,
                xticklabels=['Pred Valuable','Pred Waste'],
                yticklabels=['Actual Valuable','Actual Waste'],
                linewidths=0.5, cbar=False, annot_kws={'size':13,'weight':'bold'})
    ax.set_title('Isolation Forest — Confusion Matrix\n(Test Set, n = 29,029)', fontsize=11, fontweight='bold')
    fig.tight_layout()
    return fig

def make_shap_chart():
    features  = ['content_length','file_size_kb','tfidf_subject','email_age_days','recipient_volume']
    shap_vals = [0.0862, 0.0415, 0.0220, 0.0135, 0.0085]
    colors = ['#8e44ad' if f.startswith('tfidf') else '#2980b9' for f in features]
    fig, ax = plt.subplots(figsize=(7, 3.5))
    bars = ax.barh(features[::-1], shap_vals[::-1], color=colors[::-1], edgecolor='white', linewidth=0.5)
    ax.set_title('SHAP Feature Importance — Top Confirmed Features\n(n = 1,000 stratified test sample)',
                 fontsize=11, fontweight='bold')
    ax.set_xlabel('Mean |SHAP| Value', fontsize=9)
    for bar, val in zip(bars, shap_vals[::-1]):
        ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2, f'{val:.4f}', va='center', fontsize=9)
    ax.set_xlim(0, 0.105)
    ax.spines[['top','right']].set_visible(False)
    ax.legend(handles=[mpatches.Patch(color='#2980b9', label='Metadata'),
                       mpatches.Patch(color='#8e44ad', label='TF-IDF')], fontsize=8, loc='lower right')
    fig.tight_layout()
    return fig

def make_cluster_chart():
    data = [['Cluster 1','43,769','14,270','32.6%','Lower waste'],
            ['Cluster 2','137,002','76,257','55.7%','Mixed'],
            ['Cluster 3','4,289','2,836','66.1%','High waste'],
            ['Cluster 4','1,692','125','7.4%','Lowest waste'],
            ['Cluster 5','6,769','905','13.4%','Low waste']]
    cols = ['Cluster','Total Emails','Waste Emails','Waste Rate','Label']
    row_colors = ['#fadbd8','#fdebd0','#f9ebea','#d5f5e3','#d6eaf8']
    fig, ax = plt.subplots(figsize=(8, 2.8))
    ax.axis('off')
    tbl = ax.table(cellText=data, colLabels=cols, cellLoc='center', loc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.6)
    for j in range(len(cols)):
        tbl[0,j].set_facecolor('#2c3e50')
        tbl[0,j].set_text_props(color='white', fontweight='bold')
    for i, color in enumerate(row_colors):
        for j in range(len(cols)):
            tbl[i+1,j].set_facecolor(color)
    ax.set_title('K-Means Content Clustering (k=5, TF-IDF + SVD 50 components)',
                 fontsize=11, fontweight='bold', pad=10)
    fig.tight_layout()
    return fig


# ── Header ───────────────────────────────────────────────────────────────
st.markdown("""
# 📧 UDWD Framework — Thesis Defense Demo
### Detecting and Visualizing Digital Waste in Corporate Email Communications
**Dizon · Gaa · Go** &nbsp;|&nbsp; Mapúa University, B.S. Computer Science &nbsp;|&nbsp; Adviser: Geldof B. Resuello
""")
st.divider()

st.markdown("## 📊 Key Results at a Glance")
for col, (num, lbl) in zip(st.columns(6), [
    ('517,401',          'Emails Analyzed'),
    ('80.2%',            'Total Waste Rate'),
    ('74.78%',           'Storage Reduction'),
    ('1,013.51 MB',      'Reclaimable Storage'),
    ('0.002027 kWh',     'Energy Saved / Year'),
    ('0.000472 kg CO₂',  'Reduced / Year'),
]):
    with col:
        stat_box(num, lbl)
st.divider()

tab_waste, tab_storage, tab_models, tab_shap, tab_clusters, tab_env = st.tabs([
    "📂 Waste Classification", "💾 Storage Reduction", "🤖 Model Performance",
    "🔍 SHAP Importance", "🗂️ Content Clusters", "🌱 Environmental Impact",
])

with tab_waste:
    st.markdown("""
### Deduplication + Taxonomy Labeling Results
Two deduplication passes (SHA-256 exact + MinHash LSH near-duplicate) followed by
rule-based UDWD taxonomy labeling. **415,004 emails (80.2%)** classified as digital waste.
""")
    show(make_waste_chart())
    st.markdown("""
| Category | Count | % of Corpus | Storage |
|---|---|---|---|
| Exact Duplicates | 266,537 | 51.5% | 707.79 MB |
| Near-Duplicates | 54,074 | 10.5% | 163.93 MB |
| Dark Data | 81,164 | 15.7% | — |
| Near-Zero Content | 6,339 | 1.2% | — |
| Broadcast Redundancy | 6,890 | 1.3% | — |
| **Total Waste** | **415,004** | **80.2%** | **1,013.51 MB** |
| Valuable | 99,128 | 19.2% | — |
""")

with tab_storage:
    st.markdown("""
### Pipeline Storage Impact
From **1,355.35 MB** → **483.60 MB** after deduplication (64.32% baseline reduction).
Total reclaimable waste storage: **1,013.51 MB (74.78%)**.
""")
    show(make_storage_chart())
    st.markdown("""
| Stage | Storage | Reduction |
|---|---|---|
| Original corpus | 1,355.35 MB | — |
| After exact dedup | 647.60 MB | −52.2% |
| After near-dup dedup | 483.60 MB | −64.3% cumulative |
| All waste categories | 1,013.51 MB reclaimable | **−74.78% total** |
""")

with tab_models:
    st.markdown("### Random Forest — Supervised Classification")
    left, right = st.columns(2)
    with left:
        st.caption("RF Confusion Matrix")
        show(make_rf_cm())
    with right:
        st.markdown("""
**Test Set** (n = 29,029)

| Metric | Value |
|---|---|
| Precision | 0.9086 |
| Recall | 0.9159 |
| F1-Score | 0.9122 |
| Accuracy | 0.9141 |
| TP / TN | 12,968 / 13,566 |
| FP / FN | 1,304 / 1,191 |

**10-Fold CV** (training only, n = 135,459)

| Metric | Value |
|---|---|
| F1-Score | 0.9510 ± 0.0016 |
| Precision | 0.9803 |
| Recall | 0.9234 |
| Fold spread | 0.0052 |
""")
    st.divider()
    st.markdown("### Isolation Forest — Unsupervised Anomaly Detection")
    left, right = st.columns(2)
    with left:
        st.caption("IF Confusion Matrix")
        show(make_if_cm())
    with right:
        st.markdown("""
**Test Set** (n = 29,029)

| Metric | Value |
|---|---|
| Precision | 0.2214 |
| Recall | 0.2213 |
| F1-Score | 0.2214 |
| Accuracy | 0.2405 |
| TP / TN | 3,134 / 3,848 |
| FP / FN | 11,022 / 11,025 |

> IF is designed for contamination < 0.10.
> Forced to **0.488** to match the empirical waste ratio —
> low F1 reflects operating outside its intended regime,
> not a like-for-like comparison with RF.
""")

with tab_shap:
    st.markdown("""
### RQ2: Which email attributes best predict digital waste?
SHAP values on a stratified sample of **1,000 test records**.
Content-length features dominate; email age ranks 4th; recipient volume ranks 11th.
""")
    show(make_shap_chart())
    st.markdown("""
| Rank | Feature | Mean \\|SHAP\\| | Type |
|---|---|---|---|
| 1 | content_length | 0.0862 | Metadata |
| 2 | file_size_kb | 0.0415 | Metadata |
| 3 | tfidf_subject | 0.0220 | TF-IDF |
| 4 | email_age_days | 0.0135 | Metadata |
| 11 | recipient_volume | 0.0085 | Metadata |
""")

with tab_clusters:
    st.markdown("""
### K-Means Clustering (k=5, TF-IDF + SVD 50 components)
Waste rate ranges from **7.4%** (Cluster 4) to **66.1%** (Cluster 3) —
a **58.7 pp spread** confirming word patterns distinguish waste from valuable content.
""")
    show(make_cluster_chart())

with tab_env:
    st.markdown("### Energy and Carbon Reduction Estimates")
    for col, (num, lbl) in zip(st.columns(4), [
        ('74.78%',              'Storage Reduction<br><small>Primary contribution metric</small>'),
        ('1,013.51 MB',         'Reclaimable Storage'),
        ('0.002027 kWh/yr',     'Energy Savings'),
        ('0.000472 kg CO₂/yr',  'CO₂ Reduction'),
    ]):
        with col:
            stat_box(num, lbl)
    st.divider()
    st.markdown("""
**Formula:** Waste storage (MB) × 0.000002 kWh/MB/yr × 0.233 kg CO₂/kWh

> These are proportional indicators at research scale. The **74.78% storage reduction rate**
> and the reusable UDWD framework are the primary contributions.

**Extrapolation:** 10× larger corpus → **0.02025 kWh/yr**, **0.004716 kg CO₂/yr**
""")

st.divider()
st.markdown("""
<center><small>
UDWD Framework · Dizon, Gaa, Go · Mapúa University · 2026<br>
Dataset: Enron Email Corpus (CMU/FERC) · 517,401 emails · ~150 mailboxes · 1999–2002
</small></center>
""", unsafe_allow_html=True)
