import streamlit as st

st.set_page_config(
    page_title="StuntGraph Dashboard",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Sora', sans-serif; }

[data-testid="stSidebar"] {
    background: #061020 !important;
    border-right: 1px solid #1a3a5c;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0;
    letter-spacing: -2px;
}
.main-sub {
    color: #64748b;
    font-size: 1rem;
    font-family: 'JetBrains Mono', monospace;
    margin-top: -8px;
    margin-bottom: 2rem;
}
.metric-card {
    background: linear-gradient(135deg, #0d2137, #112840);
    border: 1px solid #1a3a5c;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(56,239,125,0.15);
}
.metric-val { font-size: 2rem; font-weight: 800; color: #38ef7d; }
.metric-lbl { font-size: 0.75rem; color: #5a8fa8; letter-spacing: 1px; text-transform: uppercase; }
.section-title {
    font-size: 1.1rem; font-weight: 700; color: #38ef7d;
    border-left: 3px solid #38ef7d; padding-left: 12px;
    margin: 2rem 0 1rem 0; letter-spacing: 0.5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
🗺️ StuntGraph
</div>
<div class="main-sub">
Graph-Based Spatio-Temporal Analysis of Stunting in Indonesia
</div>
""", unsafe_allow_html=True)

# Quick stats
import pickle, os
try:
    with open("datmin_results_new/dashboard_data.pkl", "rb") as f:
        data = pickle.load(f)

    df_final = data['df_final']
    df_prov  = data['df_prov']

    st.sidebar.markdown("### 📅 Select the Year")
    selected_year = st.sidebar.radio("",
            sorted(df_final["Tahun"].unique()),
            horizontal=True)

    df_year = df_final[
        df_final["Tahun"] == selected_year
    ]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">34</div>
            <div class="metric-lbl">Provinsi</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">136</div>
            <div class="metric-lbl">Observasi</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        avg = df_year['Stunting'].mean()
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{avg:.1f}%</div>
            <div class="metric-lbl">Average Stunting</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        high = (df_prov['Risiko'] == 'High Risk').sum()
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val" style="color:#ef4444;">{high}</div>
            <div class="metric-lbl">Provinsi High Risk</div>
        </div>""", unsafe_allow_html=True)

    import plotly.express as px
    colA, colB = st.columns(2)

    with colA:
        trend = (
            df_final.groupby("Tahun")["Stunting"]
            .mean()
            .reset_index()
        )
        fig = px.line(
            trend,
            x="Tahun",
            y="Stunting",
            markers=True,
            title="Average Stunting Trend"
        )
        st.plotly_chart(fig, use_container_width=True)

    with colB:
        risk_count = (
            df_prov["Risiko"]
            .value_counts()
            .reset_index()
        )
        risk_count.columns = ["Risk", "Count"]
        fig2 = px.pie(
            risk_count,
            names="Risk",
            values="Count",
            title="Risk Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("## 🔍 Key Insights")
    st.info(f"""
        Average stunting prevalence in {selected_year}
        is {avg:.2f}% across 34 provinces.
        """)

    st.markdown("---")
    st.markdown("### 📋 About")
    st.markdown("""
        This dashboard presents a spatio-temporal analysis of socioeconomic factors affecting stunting prevalence
        across Indonesia's 34 provinces from **2021 to 2024** using the following methods:

        | Methods | Functions |
        |-----------|-----------|
        | **PCA** | Dimensionality reduction and identification of dominant factors |
        | **Multiple Linear Regression** | Analysis of the influence of socioeconomic factors |
        | **Spatial Network Construction** | Construction of interprovincial networks |
        | **Community Detection (Louvain)** | Identification of spatial communities |
        | **K-Means Clustering** | Classification of provinces into low-, medium-, and high-risk groups |
        """)

except FileNotFoundError:
    st.error("File `datmin_results_new/dashboard_data.pkl` not found!")
    st.info("Make sure the `.pkl` file is in the `datmin_results_new/` folder")
