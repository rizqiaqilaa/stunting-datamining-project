import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

st.set_page_config(page_title="Community & Clustering - StuntGraph", page_icon="🔍", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&display=swap');
* { font-family: 'Sora', sans-serif; }
.section-title {
    font-size: 1.1rem; font-weight: 700; color: #a855f7;
    border-left: 3px solid #a855f7; padding-left: 12px; margin: 2rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🔍 Community Detection and K-Means Clustering")

@st.cache_resource
def load_data():
    with open("datmin_results_new/dashboard_data.pkl", "rb") as f:
        return pickle.load(f)

data = load_data()
df_comm_profile  = data['df_comm_profile']
df_prov          = data['df_prov']
cluster_per_prov = data['cluster_per_prov']
gdf_spatial      = data['gdf_spatial']
gdf_viz          = data['gdf_viz']
stunting_avg     = data['stunting_avg']

# SECTION 1: Community Detection
st.markdown('<div class="section-title">🌐 Community Detection — Louvain Algorithm</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    # Peta community
    try:
        fig, ax = plt.subplots(figsize=(10, 7))
        gdf_spatial.plot(column='community', cmap='tab20', ax=ax,
                        edgecolor='white', linewidth=0.5, legend=True)
        ax.set_title('Community Detection Map - Louvain Algorithm', color='white', fontsize=11, fontweight='bold')
        ax.axis('off')
        plt.tight_layout(); st.pyplot(fig)
    except Exception as e:
        st.warning(f"The map cannot be displayed: {e}")

with col2:
    st.markdown("**Average Stunting Rate by Community**")
    fig, ax = plt.subplots(figsize=(5, 6))
    colors_comm = plt.cm.tab20(np.linspace(0, 1, len(df_comm_profile)))
    ax.bar(df_comm_profile['community'].astype(str), df_comm_profile['Stunting'],
           color=colors_comm, edgecolor='none')
    ax.axhline(df_comm_profile['Stunting'].mean(), color='#ffc107', lw=1.5,
               linestyle='--', label='Rata-rata')
    ax.set_xlabel('ID Komunitas', color='#5a8fa8')
    ax.set_ylabel('Avg Stunting (%)', color='#5a8fa8')
    ax.set_title('Stunting by Community', color='black', fontsize=10, fontweight='bold')
    ax.tick_params(colors='black', labelsize=8); ax.spines[:].set_color('#1a3a5c')
    ax.legend(facecolor='#0d2137', fontsize=8)
    plt.tight_layout(); st.pyplot(fig)

    # Modularity info
    st.markdown("""
    <div style="background:#0d2137; border:1px solid #a855f7; border-radius:10px; padding:1rem; margin-top:1rem;">
    <p style="color:#5a8fa8; font-size:0.75rem; margin:0;">MODULARITY SCORE</p>
    <p style="color:#a855f7; font-size:2rem; font-weight:800; margin:0;">0.7490</p>
    <p style="color:#c8dff0; font-size:0.8rem; margin-top:4px;">Strong community structure ✅</p>
    </div>
    """, unsafe_allow_html=True)

# SECTION 2: K-Means Clustering
st.markdown('<div class="section-title">🎯 K-Means Clustering - Stunting Risk Groups</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    try:
        fig, ax = plt.subplots(figsize=(10, 7))
        color_map = {'High Risk': '#ef4444', 'Medium Risk': '#ffc107', 'Low Risk': '#22c55e'}
        gdf_viz['plot_color'] = gdf_viz['Risiko'].map(color_map).fillna('#888888')
        gdf_viz.plot(color=gdf_viz['plot_color'], ax=ax, edgecolor='white', linewidth=0.5)
        patches = [mpatches.Patch(color=v, label=k) for k, v in color_map.items()]
        ax.legend(handles=patches, loc='lower left', fontsize=9,
                 facecolor='#0d2137', title='Risk Group',
                 title_fontsize=9)
        ax.set_title('K-Means Cluster Map - Stunting Risk by Province (K=3)',
                    color='black', fontsize=11, fontweight='bold')
        ax.axis('off')
        plt.tight_layout(); st.pyplot(fig)
    except Exception as e:
        st.warning(f"Peta can't displayed: {e}")

with col2:
    st.markdown("**Cluster Distribution**")

    risk_counts = df_prov['Risiko'].value_counts()
    colors_risk = ['#ef4444', '#ffc107', '#22c55e']

    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(
        risk_counts.values, labels=risk_counts.index,
        colors=colors_risk[:len(risk_counts)],
        autopct='%1.0f%%', startangle=90,
        textprops={'color': 'black', 'fontsize': 9}
    )
    for at in autotexts: at.set_color('white')
    ax.set_title('Risk Distribution', color='black', fontsize=10, fontweight='bold')
    plt.tight_layout(); st.pyplot(fig)

    # Silhouette score
    st.markdown("""
        <div style="background:#0d2137; border:1px solid #22c55e; border-radius:10px; padding:1rem; margin-top:1rem;">
        <p style="color:#5a8fa8; font-size:0.75rem; margin:0;">SILHOUETTE SCORE</p>
        <p style="color:#22c55e; font-size:2rem; font-weight:800; margin:0;">0.2025</p>
        <p style="color:#c8dff0; font-size:0.8rem; margin-top:4px;">
        No strong cluster structure (< 0.25)
        </p>
        <p style="color:#c8dff0; font-size:0.75rem; margin-top:8px;">
        Compared with the previous model, greater overlap among provinces reduced inter-cluster separation, reflecting the continuous nature of socioeconomic characteristics.
        </p>
        </div>
        """, unsafe_allow_html=True)

# SECTION 3: Province List per Cluster
st.markdown('<div class="section-title">📋 List of Provinces by Cluster</div>', unsafe_allow_html=True)

tab_high, tab_med, tab_low = st.tabs(["🔴 High Risk", "🟡 Medium Risk", "🟢 Low Risk"])

with tab_high:
    high = cluster_per_prov[cluster_per_prov['Risiko'] == 'High Risk'][['Provinsi','Cluster']]
    st.dataframe(high.reset_index(drop=True), use_container_width=True)

with tab_med:
    med = cluster_per_prov[cluster_per_prov['Risiko'] == 'Medium Risk'][['Provinsi','Cluster']]
    st.dataframe(med.reset_index(drop=True), use_container_width=True)

with tab_low:
    low = cluster_per_prov[cluster_per_prov['Risiko'] == 'Low Risk'][['Provinsi','Cluster']]
    st.dataframe(low.reset_index(drop=True), use_container_width=True)
