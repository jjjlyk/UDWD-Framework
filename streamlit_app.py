# ── UDWD FRAMEWORK — STREAMLIT DASHBOARD ─────────────────────────────────
# Standalone results dashboard for DGG_UDWD_Pipeline.ipynb.
# All values are the FINAL results from the notebook — nothing is recomputed.
#
# Run locally:  streamlit run streamlit_app.py

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="UDWD Framework",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Palette ──────────────────────────────────────────────────────────────
INK      = "#1F2A37"
MUTED    = "#6B7280"
ACCENT   = "#2A9D8F"   # valuable / positive
CAT = {
    "Exact Duplicates":     "#B23A48",
    "Near-Duplicates":      "#E26D5A",
    "Dark Data":            "#6C5B7B",
    "Near-Zero Content":    "#F2A65A",
    "Broadcast Redundancy": "#3D7EA6",
    "Valuable":             ACCENT,
}

st.markdown(f"""
<style>
.block-container {{ max-width: 1180px; padding-top: 2.2rem; padding-bottom: 3rem; }}
h1, h2, h3, h4 {{ color: {INK}; letter-spacing: -0.01em; }}

.hero {{ padding: 0.4rem 0 1.4rem 0; border-bottom: 1px solid #E5E7EB; margin-bottom: 1.6rem; }}
.hero .eyebrow {{ font-size: 0.78rem; font-weight: 700; letter-spacing: 0.12em;
                  text-transform: uppercase; color: {ACCENT}; margin-bottom: 0.5rem; }}
.hero h1 {{ font-size: clamp(1.7rem, 3.4vw, 2.5rem); line-height: 1.15; margin: 0 0 0.5rem 0; padding: 0; }}
.hero .sub {{ font-size: clamp(1rem, 1.6vw, 1.2rem); color: {MUTED}; margin: 0; }}

.kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
         gap: 0.8rem; margin: 0.4rem 0 1.8rem 0; }}
.kpi {{ background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px;
        padding: 1rem 1.1rem; box-shadow: 0 1px 2px rgba(16,24,40,0.04); }}
.kpi .num {{ font-size: 1.55rem; font-weight: 800; color: {INK}; line-height: 1.1; }}
.kpi .lbl {{ font-size: 0.82rem; color: {MUTED}; margin-top: 0.3rem; }}
.kpi.accent {{ box-shadow: inset 0 3px 0 {ACCENT}, 0 1px 2px rgba(16,24,40,0.04); }}

.card {{ background: #F8FAFB; border: 1px solid #E5E7EB; border-radius: 12px;
         padding: 1.2rem 1.4rem; margin-bottom: 1rem; color: #374151; line-height: 1.65; }}
.card p {{ margin: 0 0 0.7rem 0; }}
.card p:last-child {{ margin-bottom: 0; }}

.steps {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 0.8rem; }}
.step {{ background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1rem; }}
.step .n {{ display: inline-block; width: 1.7rem; height: 1.7rem; line-height: 1.7rem; text-align: center;
            border-radius: 50%; background: {ACCENT}; color: white; font-weight: 700; font-size: 0.85rem; }}
.step .t {{ font-weight: 700; color: {INK}; margin: 0.55rem 0 0.25rem 0; }}
.step .d {{ font-size: 0.86rem; color: {MUTED}; line-height: 1.5; }}

.tax {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 0.8rem; }}
.tax .item {{ background: #FFFFFF; border: 1px solid #E5E7EB; border-left-width: 5px;
              border-radius: 10px; padding: 0.85rem 1rem; }}
.tax .name {{ font-weight: 700; color: {INK}; }}
.tax .rule {{ font-size: 0.86rem; color: {MUTED}; margin-top: 0.2rem; }}

.note {{ font-size: 0.85rem; color: {MUTED}; border-left: 3px solid #D1D5DB;
         padding: 0.2rem 0 0.2rem 0.8rem; margin: 0.6rem 0; }}
.footer {{ text-align: center; font-size: 0.8rem; color: {MUTED};
           border-top: 1px solid #E5E7EB; margin-top: 2.5rem; padding-top: 1rem; }}

.stTabs [data-baseweb="tab-list"] {{ gap: 0.25rem; flex-wrap: wrap; }}
.stTabs [data-baseweb="tab"] {{ padding: 0.5rem 0.9rem; }}
div[data-testid="stMetric"] {{ background: #FFFFFF; border: 1px solid #E5E7EB;
                               border-radius: 10px; padding: 0.7rem 0.9rem; }}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────
def kpi_row(items):
    cards = "".join(
        f'<div class="kpi{" accent" if accent else ""}"><div class="num">{num}</div>'
        f'<div class="lbl">{lbl}</div></div>'
        for num, lbl, accent in items
    )
    st.markdown(f'<div class="kpis">{cards}</div>', unsafe_allow_html=True)


def note(text):
    st.markdown(f'<div class="note">{text}</div>', unsafe_allow_html=True)


def style(fig, height=380, **kw):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(family="Inter, Segoe UI, sans-serif", size=13, color=INK),
        showlegend=False,
        **kw,
    )
    return fig


def show(fig):
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# ── Charts ───────────────────────────────────────────────────────────────
def waste_chart():
    cats   = ["Exact Duplicates", "Near-Duplicates", "Dark Data",
              "Near-Zero Content", "Broadcast Redundancy", "Valuable"]
    counts = [266537, 54074, 81164, 6339, 6890, 99128]
    pcts   = ["51.5%", "10.5%", "15.7%", "1.2%", "1.3%", "19.2%"]
    fig = go.Figure(go.Bar(
        x=counts[::-1], y=cats[::-1], orientation="h",
        marker_color=[CAT[c] for c in cats[::-1]],
        text=[f"{v:,}  ·  {p}" for v, p in zip(counts[::-1], pcts[::-1])],
        textposition="outside", cliponaxis=False,
        hovertemplate="%{y}: %{x:,} emails<extra></extra>",
    ))
    fig.update_xaxes(title="Number of emails", range=[0, 330000], tickformat=",")
    return style(fig, height=360)


def storage_chart():
    stages = ["Original corpus", "After exact dedup", "After near-dup dedup", "Reclaimable waste"]
    sizes  = [1355.35, 647.60, 483.60, 1013.51]
    colors = ["#94A3B8", "#5FB3A9", ACCENT, CAT["Exact Duplicates"]]
    fig = go.Figure(go.Bar(
        x=stages, y=sizes, marker_color=colors, width=0.55,
        text=[f"{v:,.2f} MB" for v in sizes], textposition="outside", cliponaxis=False,
        hovertemplate="%{x}: %{y:,.2f} MB<extra></extra>",
    ))
    fig.update_yaxes(title="Storage (MB)", range=[0, 1550])
    return style(fig, height=380)


def confusion(cm, colorscale, title):
    labels = [[f"<b>{v:,}</b>" for v in row] for row in cm]
    fig = go.Figure(go.Heatmap(
        z=cm, x=["Predicted valuable", "Predicted waste"], y=["Actual valuable", "Actual waste"],
        text=labels, texttemplate="%{text}", textfont=dict(size=18),
        colorscale=colorscale, showscale=False, xgap=3, ygap=3,
        hovertemplate="%{y} / %{x}: %{z:,}<extra></extra>",
    ))
    fig.update_yaxes(autorange="reversed")
    return style(fig, height=330, title=dict(text=title, font=dict(size=14)))


def shap_chart():
    feats = ["content_length", "file_size_kb", "tfidf_subject", "email_age_days", "recipient_volume"]
    vals  = [0.0862, 0.0415, 0.0220, 0.0135, 0.0085]
    ranks = [1, 2, 3, 4, 11]
    colors = ["#8E5BB5" if f.startswith("tfidf") else "#3D7EA6" for f in feats]
    fig = go.Figure(go.Bar(
        x=vals[::-1], y=[f"#{r}  {f}" for r, f in zip(ranks[::-1], feats[::-1])],
        orientation="h", marker_color=colors[::-1],
        text=[f"{v:.4f}" for v in vals[::-1]], textposition="outside", cliponaxis=False,
        hovertemplate="%{y}: %{x:.4f}<extra></extra>",
    ))
    fig.update_xaxes(title="Mean |SHAP| value", range=[0, 0.1])
    return style(fig, height=320)


# ── Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="eyebrow">UDWD Framework</div>
  <h1>Detecting and Visualizing Digital Waste in Corporate Email Communications</h1>
  <p class="sub">A Machine Learning Approach for Estimating Energy Savings and CO₂ Reduction</p>
</div>
""", unsafe_allow_html=True)

kpi_row([
    ("517,401",     "Emails analyzed",                False),
    ("80.2%",       "Classified as digital waste",    False),
    ("74.78%",      "Storage reduction",              True),
    ("1,013.51 MB", "Reclaimable storage",            False),
    ("0.9122",      "Random Forest F1 (test set)",    False),
])

tabs = st.tabs([
    "Overview", "Waste Classification", "Storage Reduction",
    "Model Performance", "Feature Importance", "Content Clusters", "Environmental Impact",
])

# ── Overview ─────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("### Abstract")
    st.markdown("""
<div class="card">
<p>Corporate email systems quietly accumulate large amounts of <b>digital waste</b>: duplicated messages,
near-identical forwards, mass broadcasts, and short, aging messages nobody revisits. This data still has to be
stored, backed up, and powered, which costs organizations money and contributes to carbon emissions,
yet it is rarely measured.</p>
<p>This study proposes the <b>Unstructured Data Waste Detection (UDWD) Framework</b>, a pipeline that detects,
categorizes, and visualizes digital waste in email. Applied to the <b>Enron Email Corpus</b> (517,401 emails from
roughly 150 mailboxes, 1999–2002), the framework combines SHA-256 exact and MinHash LSH near-duplicate detection with a
rule-based waste taxonomy, then trains a supervised <b>Random Forest</b> and an unsupervised <b>Isolation Forest</b>
on TF-IDF content features and email metadata. <b>SHAP</b> analysis explains which email attributes drive waste
predictions, and the reclaimable storage is converted into energy and CO₂ estimates.</p>
<p>The framework classified <b>80.2%</b> of the corpus as waste, representing <b>1,013.51 MB (74.78%)</b> of
reclaimable storage. The Random Forest achieved an <b>F1-score of 0.9122</b> on the held-out test set
(0.9510 in 10-fold cross-validation), and content length emerged as the strongest predictor of waste.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("### How the framework works")
    st.markdown("""
<div class="steps">
  <div class="step"><span class="n">1</span><div class="t">Parse</div>
    <div class="d">Read every email's body, sender, recipients, date, and thread headers.</div></div>
  <div class="step"><span class="n">2</span><div class="t">Deduplicate</div>
    <div class="d">Flag exact copies (SHA-256 hash) and near-copies (MinHash LSH, similarity ≥ 0.85).</div></div>
  <div class="step"><span class="n">3</span><div class="t">Label</div>
    <div class="d">Apply the waste taxonomy rules below to every remaining email.</div></div>
  <div class="step"><span class="n">4</span><div class="t">Learn</div>
    <div class="d">Train Random Forest and Isolation Forest on 5,000 TF-IDF + 4 metadata features.</div></div>
  <div class="step"><span class="n">5</span><div class="t">Explain</div>
    <div class="d">Use SHAP to rank which email attributes most influence predictions.</div></div>
  <div class="step"><span class="n">6</span><div class="t">Estimate</div>
    <div class="d">Convert reclaimable storage into yearly energy (kWh) and CO₂ savings.</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### Waste taxonomy")
    st.markdown(f"""
<div class="tax">
  <div class="item" style="border-left-color:{CAT['Exact Duplicates']}"><div class="name">Exact Duplicates</div>
    <div class="rule">Byte-for-byte identical message bodies (same SHA-256 hash).</div></div>
  <div class="item" style="border-left-color:{CAT['Near-Duplicates']}"><div class="name">Near-Duplicates</div>
    <div class="rule">Forwarded or lightly edited copies (Jaccard similarity ≥ 0.85).</div></div>
  <div class="item" style="border-left-color:{CAT['Near-Zero Content']}"><div class="name">Near-Zero Content</div>
    <div class="rule">Five words or fewer after cleaning.</div></div>
  <div class="item" style="border-left-color:{CAT['Dark Data']}"><div class="name">Dark Data</div>
    <div class="rule">Older than 365 days and 50 words or fewer.</div></div>
  <div class="item" style="border-left-color:{CAT['Broadcast Redundancy']}"><div class="name">Broadcast Redundancy</div>
    <div class="rule">Sent to 10+ recipients with content similarity ≥ 0.70.</div></div>
  <div class="item" style="border-left-color:{CAT['Valuable']}"><div class="name">Valuable</div>
    <div class="rule">Meets none of the conditions above; retained.</div></div>
</div>
""", unsafe_allow_html=True)
    note("Labels are applied in priority order: the first rule an email matches determines its category.")

# ── Waste Classification ─────────────────────────────────────────────────
with tabs[1]:
    st.markdown("### Email classification results")
    st.markdown("Two deduplication passes followed by rule-based taxonomy labeling classified "
                "**415,004 emails (80.2%)** as digital waste.")
    show(waste_chart())
    st.dataframe(
        pd.DataFrame({
            "Category":    ["Exact Duplicates", "Near-Duplicates", "Dark Data", "Near-Zero Content",
                            "Broadcast Redundancy", "Total Waste", "Valuable"],
            "Emails":      ["266,537", "54,074", "81,164", "6,339", "6,890", "415,004", "99,128"],
            "% of corpus": ["51.5%", "10.5%", "15.7%", "1.2%", "1.3%", "80.2%", "19.2%"],
            "Storage":     ["707.79 MB", "163.93 MB", "—", "—", "—", "1,013.51 MB", "—"],
        }),
        hide_index=True, width="stretch",
    )

# ── Storage Reduction ────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("### Storage across pipeline stages")
    st.markdown("Deduplication alone shrinks the corpus from **1,355.35 MB** to **483.60 MB** "
                "(64.32% baseline reduction). Including every waste category, **1,013.51 MB (74.78%)** "
                "is reclaimable.")
    show(storage_chart())
    st.dataframe(
        pd.DataFrame({
            "Stage":     ["Original corpus", "After exact dedup", "After near-dup dedup", "All waste categories"],
            "Storage":   ["1,355.35 MB", "647.60 MB", "483.60 MB", "1,013.51 MB reclaimable"],
            "Reduction": ["—", "−52.2%", "−64.3% cumulative", "−74.78% total"],
        }),
        hide_index=True, width="stretch",
    )

# ── Model Performance ────────────────────────────────────────────────────
with tabs[3]:
    st.markdown("### Random Forest: supervised classification")
    st.caption("Held-out test set, n = 29,029 · 10-fold cross-validation on training set only, n = 135,459")
    left, right = st.columns([1, 1], gap="large")
    with left:
        show(confusion([[13566, 1304], [1191, 12968]],
                       [[0, "#E8F4F2"], [1, ACCENT]], "Confusion matrix (test set)"))
    with right:
        st.markdown("**Test set**")
        c1, c2 = st.columns(2)
        c1.metric("Precision", "0.9086")
        c2.metric("Recall", "0.9159")
        c1.metric("F1-score", "0.9122")
        c2.metric("Accuracy", "0.9141")
        st.markdown("**10-fold cross-validation**")
        c1, c2, c3 = st.columns(3)
        c1.metric("F1-score", "0.9510", "± 0.0016", delta_color="off")
        c2.metric("Precision", "0.9803")
        c3.metric("Recall", "0.9234")

    st.divider()
    st.markdown("### Isolation Forest: unsupervised anomaly detection")
    left, right = st.columns([1, 1], gap="large")
    with left:
        show(confusion([[3848, 11022], [11025, 3134]],
                       [[0, "#FDF0E6"], [1, "#E8743B"]], "Confusion matrix (test set)"))
    with right:
        st.markdown("**Test set**")
        c1, c2 = st.columns(2)
        c1.metric("Precision", "0.2214")
        c2.metric("Recall", "0.2213")
        c1.metric("F1-score", "0.2214")
        c2.metric("Accuracy", "0.2405")
        note("Isolation Forest is designed for contamination below 0.10. It was set to <b>0.488</b> to match "
             "the empirical waste ratio, so its low F1 reflects operating outside its intended regime, "
             "not a like-for-like comparison with Random Forest.")

# ── Feature Importance ───────────────────────────────────────────────────
with tabs[4]:
    st.markdown("### Which email attributes best predict digital waste?")
    st.markdown("SHAP values computed on a stratified sample of **1,000 test records**. "
                "Content length dominates; email age ranks 4th; recipient volume ranks 11th overall.")
    show(shap_chart())
    st.markdown(
        '<span style="color:#3D7EA6">■</span> Metadata feature &nbsp;&nbsp; '
        '<span style="color:#8E5BB5">■</span> TF-IDF content feature',
        unsafe_allow_html=True,
    )

# ── Content Clusters ─────────────────────────────────────────────────────
with tabs[5]:
    st.markdown("### K-Means content clustering")
    st.markdown("Emails grouped by topic (k = 5, TF-IDF reduced with 50-component SVD). Waste rate ranges from "
                "**7.4%** to **66.1%**, a **58.7-point spread**, showing that word patterns help distinguish "
                "waste from valuable content.")
    st.dataframe(
        pd.DataFrame({
            "Cluster":      ["Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4", "Cluster 5"],
            "Total emails": [43769, 137002, 4289, 1692, 6769],
            "Waste emails": [14270, 76257, 2836, 125, 905],
            "Waste rate":   [0.326, 0.557, 0.661, 0.074, 0.134],
            "Profile":      ["Lower waste", "Mixed", "High waste", "Lowest waste", "Low waste"],
        }),
        hide_index=True, width="stretch",
        column_config={
            "Total emails": st.column_config.NumberColumn(format="localized"),
            "Waste emails": st.column_config.NumberColumn(format="localized"),
            "Waste rate":   st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1),
        },
    )
    note("Waste labels are overlaid on the clusters for observation only; they were not used to form them.")

# ── Environmental Impact ─────────────────────────────────────────────────
with tabs[6]:
    st.markdown("### Energy and carbon reduction estimates")
    kpi_row([
        ("74.78%",         "Storage reduction (primary metric)", True),
        ("1,013.51 MB",    "Reclaimable storage",                False),
        ("0.002027 kWh",   "Energy saved per year",              False),
        ("0.000472 kg",    "CO₂ reduced per year",               False),
    ])
    st.markdown("""
<div class="card">
<p><b>Formula:</b> waste storage (MB) × 0.000002 kWh/MB/year × 0.233 kg CO₂/kWh</p>
<p>These are proportional indicators at research scale. The <b>74.78% storage reduction rate</b> and the reusable
UDWD framework are the primary contributions. For a corpus 10× larger, the estimate grows to
<b>0.02025 kWh/year</b> and <b>0.004716 kg CO₂/year</b>.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">Dataset: Enron Email Corpus (CMU/FERC release) · 517,401 emails · ~150 mailboxes · 1999–2002</div>
""", unsafe_allow_html=True)
