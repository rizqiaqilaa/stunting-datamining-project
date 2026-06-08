import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="PCA & Regression - StuntGraph", page_icon="📐", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&display=swap');
* { font-family: 'Sora', sans-serif; }
[data-testid="stAppViewContainer"] { background: #0a1628; }
[data-testid="stSidebar"] { background: #061020 !important; border-right: 1px solid #1a3a5c; }
[data-testid="stSidebar"] * { color: #c8dff0 !important; }
.section-title {
    font-size: 1.1rem; font-weight: 700; color: #38a1ff;
    border-left: 3px solid #38a1ff; padding-left: 12px; margin: 2rem 0 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 📐 PCA and Multiple Linear Regression")

@st.cache_resource
def load_data():
    with open("datmin_results/dashboard_data.pkl", "rb") as f:
        return pickle.load(f)

data     = load_data()
pca      = data['pca']
pca_df   = data['pca_df']
loadings = data['loadings']
X_pca    = data['X_pca']
y_test   = data['y_test']
y_pred   = data['y_pred']
df_final = data['df_final']
feature_cols = data['feature_cols']

# SECTION 1: Scree Plot
st.markdown('<div class="section-title">📉 Scree Plot PCA</div>', unsafe_allow_html=True)

explained = pca.explained_variance_ratio_
cumulative = np.cumsum(explained)

fig, ax = plt.subplots(figsize=(9, 4))
fig.patch.set_facecolor('#0d2137'); ax.set_facecolor('#0d2137')
x = np.arange(1, len(explained)+1)
ax.bar(x, explained, color='#38a1ff', alpha=0.7, label='Individual', edgecolor='none')
ax2 = ax.twinx()
ax2.plot(x, cumulative, color='#38ef7d', lw=2, marker='o', markersize=7, markerfacecolor='white', label='Cumulative')
ax2.axhline(0.8, color='#ffc107', lw=1.5, linestyle='--', alpha=0.7)
ax2.set_ylabel('Cumulative Variance', color='#38ef7d')
ax2.tick_params(colors='#38ef7d')
ax.set_xlabel('Principal Component', color='#5a8fa8')
ax.set_ylabel('Explained Variance Ratio', color='#38a1ff')
ax.set_title('Scree Plot PCA', color='white', fontsize=12, fontweight='bold')
ax.tick_params(colors='white'); ax.spines[:].set_color('#1a3a5c')
ax2.spines[:].set_color('#1a3a5c')
for xi, yi in zip(x, explained):
    ax.text(xi, yi + 0.005, f'{yi:.2f}', ha='center', color='white', fontsize=9)
plt.tight_layout(); st.pyplot(fig)

# SECTION 2: PCA Biplot / Scatter
st.markdown('<div class="section-title">🔵 PCA Scatter Plot</div>', unsafe_allow_html=True)

stunting_vals = pca_df['Stunting'].values
norm = (stunting_vals - stunting_vals.min()) / (stunting_vals.max() - stunting_vals.min())

fig, ax = plt.subplots(figsize=(9, 6))
fig.patch.set_facecolor('#0d2137'); ax.set_facecolor('#0d2137')
sc = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=norm, cmap='RdYlGn_r', s=60, alpha=0.8, edgecolors='none')
cb = plt.colorbar(sc, ax=ax)
cb.set_label('Stunting Level', color='white')
cb.ax.yaxis.set_tick_params(color='white')
plt.setp(cb.ax.yaxis.get_ticklabels(), color='white')
ax.set_xlabel('PC1', color='#5a8fa8'); ax.set_ylabel('PC2', color='#5a8fa8')
ax.set_title('PCA — PC1 vs PC2 (warna = level stunting)', color='white', fontsize=12, fontweight='bold')
ax.tick_params(colors='white'); ax.spines[:].set_color('#1a3a5c')
plt.tight_layout(); st.pyplot(fig)

# SECTION 3: Feature Loadings
st.markdown('<div class="section-title">📊 Feature Loadings (PC1 & PC2)</div>', unsafe_allow_html=True)

load_arr = loadings[['PC1','PC2']].values
features = list(loadings.index)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for idx, (ax, pc, color) in enumerate(zip(axes, ['PC1','PC2'], ['#38a1ff','#38ef7d'])):
    fig.patch.set_facecolor('#0d2137'); ax.set_facecolor('#0d2137')
    vals = loadings[pc].values
    colors_bar = [color if v >= 0 else '#ef4444' for v in vals]
    ax.barh(features, vals, color=colors_bar, edgecolor='none')
    ax.axvline(0, color='white', lw=0.8, alpha=0.5)
    ax.set_title(f'Loadings {pc}', color='white', fontsize=11, fontweight='bold')
    ax.tick_params(colors='white', labelsize=9); ax.spines[:].set_color('#1a3a5c')
plt.tight_layout(); st.pyplot(fig)

# SECTION 4: Regression
st.markdown('<div class="section-title">📈 Multiple Linear Regression — Actual vs Predicted</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('#0d2137'); ax.set_facecolor('#0d2137')
    ax.scatter(y_test, y_pred, color='#38a1ff', alpha=0.6, s=50, edgecolors='none')
    mn, mx = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
    ax.plot([mn, mx], [mn, mx], 'r--', lw=1.5, alpha=0.7, label='Perfect fit')
    ax.set_xlabel('Actual Stunting', color='#5a8fa8')
    ax.set_ylabel('Predicted Stunting', color='#5a8fa8')
    ax.set_title('Actual vs Predicted', color='white', fontsize=12, fontweight='bold')
    ax.tick_params(colors='white'); ax.spines[:].set_color('#1a3a5c')
    ax.legend(labelcolor='white', facecolor='#0d2137')
    plt.tight_layout(); st.pyplot(fig)

with col2:
    from sklearn.metrics import mean_squared_error, r2_score
    r2   = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    st.markdown(f"""
    <div style="background:#0d2137; border:1px solid #1a3a5c; border-radius:12px; padding:1.2rem;">
    <p style="color:#5a8fa8; font-size:0.8rem; margin:0;">MODEL PERFORMANCE</p>
    <hr style="border-color:#1a3a5c; margin:8px 0;">
    <p style="color:#c8dff0; margin:6px 0;">R² Score</p>
    <p style="color:#38a1ff; font-size:1.8rem; font-weight:800; margin:0;">{r2:.3f}</p>
    <hr style="border-color:#1a3a5c; margin:8px 0;">
    <p style="color:#c8dff0; margin:6px 0;">RMSE</p>
    <p style="color:#ffc107; font-size:1.8rem; font-weight:800; margin:0;">{rmse:.2f}</p>
    <hr style="border-color:#1a3a5c; margin:8px 0;">
    <p style="color:#c8dff0; font-size:0.82rem;">Poverty and sanitation are significant predictors (p &lt; 0.05)</p>
    </div>
    """, unsafe_allow_html=True)
