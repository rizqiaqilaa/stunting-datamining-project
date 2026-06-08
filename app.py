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

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a1628 0%, #0d2137 50%, #0a1628 100%);
}
[data-testid="stSidebar"] {
    background: #061020 !important;
    border-right: 1px solid #1a3a5c;
}
[data-testid="stSidebar"] * { color: #c8dff0 !important; }

.main-title {
    font-size: 2.8rem; font-weight: 800;
    background: linear-gradient(135deg, #38ef7d, #11998e, #38a1ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -1px; margin-bottom: 0;
}
.main-sub {
    color: #5a8fa8; font-size: 0.95rem;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 2rem;
}
.metric-card {
    background: linear-gradient(135deg, #0d2137, #112840);
    border: 1px solid #1a3a5c; border-radius: 16px;
    padding: 1.2rem 1.5rem; text-align: center;
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

st.markdown('<p class="main-title">🗺️ StuntGraph</p>', unsafe_allow_html=True)
st.markdown('<p class="main-sub">// Graph-Based Spatio-Temporal Analysis of Stunting in Indonesia</p>', unsafe_allow_html=True)


# Quick stats
import pickle, os
try:
    with open("datmin_results/dashboard_data.pkl", "rb") as f:
        data = pickle.load(f)

    df_final = data['df_final']
    df_prov  = data['df_prov']

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
        avg = df_final['Stunting'].mean()
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val">{avg:.1f}%</div>
            <div class="metric-lbl">Rata-rata Stunting</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        high = (df_prov['Risiko'] == 'High Risk').sum()
        st.markdown(f"""<div class="metric-card">
            <div class="metric-val" style="color:#ef4444;">{high}</div>
            <div class="metric-lbl">Provinsi High Risk</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 About")
    st.markdown("""
    This dashboard presents a spatiotemporal analysis of socioeconomic factors affecting the prevalence of stunting 
    in Indonesia’s 34 provinces from **2021 to 2024** using:
    
    | Methods | Functions |
    |--------|--------|
    | **PCA** | Dimension reduction & identification of dominant factors |
    | **Multiple Linear Regression** | Analysis of the influence of socioeconomic factors |
    | **Spatial Network** | Construction of interprovincial networks |
    | **Community Detection (Louvain)** | Detection of stunting communities |
    | **K-Means Clustering** | Risk level classification |
    """)

except FileNotFoundError:
    st.error("File `datmin_results/dashboard_data.pkl` not found!")
    st.info("Make sure the `.pkl` file is in the `datmin_results/` folder")
