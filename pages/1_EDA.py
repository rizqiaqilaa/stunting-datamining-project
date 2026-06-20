import streamlit as st
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import geopandas as gpd

st.set_page_config(page_title="EDA - StuntGraph", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&display=swap');
* { font-family: 'Sora', sans-serif; }
        
.section-title{
    font-size:1.1rem;
    font-weight:700;
    color:#16a34a;
    border-left:3px solid #16a34a;
    padding-left:12px;
    margin:2rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 📊 Exploratory Data Analysis")

@st.cache_resource
def load_data():
    with open("datmin_results_new/dashboard_data.pkl", "rb") as f:
        return pickle.load(f)

data = load_data()
df_final   = data['df_final']
correlation = data['correlation']
stunting_avg = data['stunting_avg']

# ── SECTION 1: Trend
st.markdown('<div class="section-title">📈 Prevalence Trends of Stunting, 2021-2024</div>', unsafe_allow_html=True)

trend = df_final.groupby('Tahun')['Stunting'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(trend['Tahun'], trend['Stunting'], color='#38ef7d', lw=2.5, marker='o', markersize=8, markerfacecolor='white')
ax.fill_between(trend['Tahun'], trend['Stunting'], alpha=0.15, color='#38ef7d')
for x, y in zip(trend['Tahun'], trend['Stunting']):
    ax.annotate(f'{y:.1f}%', (x, y), textcoords="offset points", xytext=(0, 12), color='white', fontsize=10, ha='center')
ax.set_title('Average Annual National Prevalence of Stunting', color='black', fontsize=13, fontweight='bold')
ax.set_xlabel('Tahun', color='black'); ax.set_ylabel('Stunting (%)', color='#5a8fa8')
ax.tick_params(colors='black'); ax.spines[:].set_color('#1a3a5c')
ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
plt.tight_layout()
st.pyplot(fig)

# SECTION 2: Correlation Heatmap
st.markdown('<div class="section-title">🔗 Correlation Heatmap</div>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(8, 6))
mask = np.zeros_like(correlation, dtype=bool)
mask[np.triu_indices_from(mask, k=1)] = True
sns.heatmap(
    correlation, annot=True, fmt='.2f', cmap='coolwarm',
    center=0, ax=ax, linewidths=0.5, linecolor='#1a3a5c',
    annot_kws={'size': 9, 'color': 'black'},
    cbar_kws={'shrink': 0.8}
)
ax.set_title('Correlation Matrix - Stunting and Socioeconomic Factors', color='black', fontsize=12, fontweight='bold')
ax.tick_params(colors='black', labelsize=9)
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
<div style="background:#f8fafc; border:1px solid #d1d5db; border-radius:12px; padding:1rem 1.5rem; margin:1rem 0;">
<b style="color:#38ef7d;">💡 Insight:</b>
<ul style="color:black; margin-top:8px;">
<li>Poverty is <b>positively</b> correlated with stunting (r = 0.43)</li>
<li>Sanitation, education, and clean water are <b>negatively</b> correlated with stunting</li>
<li>Provinces with better sanitation and education tend to have lower rates of stunting</li>
</ul>
</div>
""", unsafe_allow_html=True)

# SECTION 3: Top & Bottom Provinces
st.markdown('<div class="section-title">Top 10 & Bottom 10 Provinces</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    top10 = stunting_avg.nlargest(10, 'Stunting_avg')
    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.barh(top10['Provinsi'], top10['Stunting_avg'], color='#ef4444', edgecolor='none')
    ax.set_title('Top 10 Highest Stunting Rates', color='black', fontsize=11, fontweight='bold')
    ax.tick_params(colors='black', labelsize=8); ax.spines[:].set_color('#1a3a5c')
    ax.set_xlabel('Avg Stunting (%)', color='black')
    for bar, val in zip(bars, top10['Stunting_avg']):
        ax.text(val + 0.2, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', color='black', fontsize=8)
    plt.tight_layout(); st.pyplot(fig)

with col2:
    bot10 = stunting_avg.nsmallest(10, 'Stunting_avg')
    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.barh(bot10['Provinsi'], bot10['Stunting_avg'], color='#38ef7d', edgecolor='none')
    ax.set_title('Top 10 Lowest Rates of Stunting', color='black', fontsize=11, fontweight='bold')
    ax.tick_params(colors='black', labelsize=8); ax.spines[:].set_color('#1a3a5c')
    ax.set_xlabel('Avg Stunting (%)', color='black')
    for bar, val in zip(bars, bot10['Stunting_avg']):
        ax.text(val + 0.1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', color='black', fontsize=8)
    plt.tight_layout(); st.pyplot(fig)

# SECTION 4: Raw Data
st.markdown('<div class="section-title">📋 Complete Data</div>', unsafe_allow_html=True)
tahun_filter = st.selectbox("Filter by Year:", ['All'] + sorted(df_final['Tahun'].unique().tolist()))
df_show = df_final if tahun_filter == 'All' else df_final[df_final['Tahun'] == tahun_filter]
st.dataframe(df_show.reset_index(drop=True), use_container_width=True, height=300)
