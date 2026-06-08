import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

st.set_page_config(page_title="Spatial Network - StuntGraph", page_icon="🗺️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&display=swap');
* { font-family: 'Sora', sans-serif; }
[data-testid="stAppViewContainer"] { background: #0a1628; }
[data-testid="stSidebar"] { background: #061020 !important; border-right: 1px solid #1a3a5c; }
[data-testid="stSidebar"] * { color: #c8dff0 !important; }
.section-title {
    font-size: 1.1rem; font-weight: 700; color: #ffc107;
    border-left: 3px solid #ffc107; padding-left: 12px; margin: 2rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🗺️ Spatial Network Construction")

@st.cache_resource
def load_data():
    with open("datmin_results/dashboard_data.pkl", "rb") as f:
        return pickle.load(f)

data = load_data()
G                    = data['G']
adj_matrix           = data['adj_matrix']
adj_matrix_df        = data['adj_matrix_df']
degree_centrality_df = data['degree_centrality_df']
nodes                = data['nodes']
gdf_spatial          = data['gdf_spatial']

# ── SECTION 1: Graph Stats
st.markdown('<div class="section-title">📊 Graph Statistics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
stats = [
    ("Nodes (Provinsi)", G.number_of_nodes(), "#38ef7d"),
    ("Edges (Koneksi)", G.number_of_edges(), "#38a1ff"),
    ("Avg Degree", f"{np.mean([d for _, d in G.degree()]):.2f}", "#ffc107"),
    ("Density", f"{nx.density(G):.3f}", "#ef4444"),
]
for col, (label, val, color) in zip([col1,col2,col3,col4], stats):
    with col:
        st.markdown(f"""<div style="background:#0d2137; border:1px solid #1a3a5c; border-radius:12px; padding:1rem; text-align:center;">
        <div style="font-size:1.8rem; font-weight:800; color:{color};">{val}</div>
        <div style="font-size:0.75rem; color:#5a8fa8; text-transform:uppercase; letter-spacing:1px;">{label}</div>
        </div>""", unsafe_allow_html=True)

# SECTION 2: Adjacency Matrix
st.markdown('<div class="section-title">🔲 Adjacency Matrix Heatmap</div>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor('#0d2137'); ax.set_facecolor('#0d2137')
sns.heatmap(
    adj_matrix, ax=ax,
    cmap=sns.light_palette("#ffc107", as_cmap=True),
    linewidths=0.3, linecolor='#0a1628',
    cbar_kws={'shrink': 0.7}
)
ax.set_title('Adjacency Matrix — Spatial Weights', color='white', fontsize=12, fontweight='bold')
ax.tick_params(colors='white', labelsize=7)
plt.tight_layout(); st.pyplot(fig)

# ── SECTION 3: Degree Centrality
st.markdown('<div class="section-title">📈 Degree Centrality per Province</div>', unsafe_allow_html=True)

df_deg = degree_centrality_df.sort_values('Degree_Centrality', ascending=True)

fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor('#0d2137'); ax.set_facecolor('#0d2137')
colors_bar = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(df_deg)))
ax.barh(df_deg['Provinsi'], df_deg['Degree_Centrality'], color=colors_bar, edgecolor='none')
ax.set_title('Degree Centrality - Strategic Hubs of the Province', color='white', fontsize=12, fontweight='bold')
ax.set_xlabel('Degree Centrality', color='#5a8fa8')
ax.tick_params(colors='white', labelsize=8); ax.spines[:].set_color('#1a3a5c')
for i, (prov, val) in enumerate(zip(df_deg['Provinsi'], df_deg['Degree_Centrality'])):
    ax.text(val + 0.001, i, f'{val:.3f}', va='center', color='white', fontsize=7)
plt.tight_layout(); st.pyplot(fig)

st.markdown("""
<div style="background:#0d2137; border:1px solid #1a3a5c; border-radius:12px; padding:1rem 1.5rem; margin:1rem 0;">
<b style="color:#ffc107;">💡 Insight:</b>
<ul style="color:#c8dff0; margin-top:8px;">
<li>The provinces with the highest degree centrality are <b>regional strategic hubs</b></li>
<li>East Kalimantan and Bengkulu have the most connections to neighboring provinces</li>
<li>Isolated provinces (low degree) require special attention in policy interventions</li>
</ul>
</div>
""", unsafe_allow_html=True)
