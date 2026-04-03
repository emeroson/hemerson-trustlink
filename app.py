"""
╔═════════════════════════════════════════════════════════════════════════════════╗
║                                                                                 ║
║                  🛡️  HEMERSON TRUSTLINK v4.0  🛡️                             ║
║                                                                                 ║
║              DÉTECTION INTELLIGENTE DE FRAUDE FINANCIÈRE                       ║
║                     Machine Learning • IA • Temps Réel                         ║
║                                                                                 ║
║                   Auteur: Anoh Amon Francklin Hemerson                         ║
║                              © 2026 - Premium                                  ║
║                                                                                 ║
╚═════════════════════════════════════════════════════════════════════════════════╝

APPLICATION:
- Analyse 30 caractéristiques par transaction
- Détection fraude instantanée (< 1 seconde)
- Machine Learning certifié et optimisé
- Interface professionnelle moderne

INSTRUCTIONS POUR L'UTILISATEUR:
Si vous voyez du code HTML s'afficher directement au lieu d'être rendu,
redémarrez Streamlit avec Ctrl+C puis relancez avec: streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# ═════════════════════════════════════════════════════════════════════════════════
# ⚙️  CONFIGURATION PAGE
# ═════════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🛡️ Hemerson TrustLink - Détection Fraude IA Premium",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "🛡️ Hemerson TrustLink v4.0 - Auteur: Anoh Amon Francklin Hemerson"}
)

# ═════════════════════════════════════════════════════════════════════════════════
# 🔌 CHARGEMENT DES RESSOURCES
# ═════════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def charger_modele():
    try:
        modele = joblib.load("model.pkl")
        scaler = joblib.load("scaler.pkl")
        return modele, scaler
    except FileNotFoundError:
        st.error("❌ ERREUR: Modèles ML non trouvés!")
        return None, None

modele, scaler = charger_modele()

if "historique" not in st.session_state:
    st.session_state.historique = []

# ═════════════════════════════════════════════════════════════════════════════════
# 🎨 STYLING CSS EXPERT - CONTRASTE MAXIMAL ULTRA
# ═════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600&display=swap');

:root {
    --bg-primary: #0a0e27;
    --bg-secondary: #050812;
    --bg-card: #111b3d;
    --bg-card-hover: #192551;
    --bg-accent: #0f1436;
    --border-primary: #2a3f5f;
    --border-secondary: #3a4f6f;
    --text-primary: #ffffff;
    --text-secondary: #e0e7ff;
    --text-muted: #a0aec0;
    --text-subtle: #7c8db5;
    --accent-blue: #4f7bff;
    --accent-blue-light: #6b8aff;
    --accent-red: #ff4757;
    --accent-red-light: #ff6b7a;
    --accent-green: #2ed573;
    --accent-green-light: #4ade80;
    --accent-orange: #ffa502;
    --accent-orange-light: #ffb74d;
    --shadow-primary: rgba(0, 0, 0, 0.4);
    --shadow-accent: rgba(79, 123, 255, 0.2);
    --gradient-primary: linear-gradient(135deg, #0a0e27 0%, #050812 50%, #0f1436 100%);
    --gradient-card: linear-gradient(135deg, #111b3d 0%, #192551 100%);
    --gradient-accent: linear-gradient(135deg, #4f7bff 0%, #00d4ff 100%);
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body, [class*="css"], .stApp {
    font-family: 'Poppins', sans-serif !important;
    background: var(--gradient-primary) !important;
    color: var(--text-primary) !important;
    line-height: 1.6 !important;
    font-weight: 400 !important;
}

.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1900px !important;
    margin: 0 auto !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
}

#MainMenu, footer, header {
    display: none !important;
}

/* SIDEBAR ENHANCED */
[data-testid="stSidebar"] {
    background: var(--gradient-card) !important;
    border-right: 3px solid var(--border-primary) !important;
    box-shadow: 4px 0 20px var(--shadow-primary) !important;
}

[data-testid="stSidebar"] > div > div:first-child {
    padding-top: 2rem !important;
}

/* TABS ULTRA CONTRAST */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 4px solid var(--border-primary) !important;
    gap: 2rem !important;
    padding-bottom: 0.5rem !important;
    margin-bottom: 2rem !important;
}

[data-testid="stTabs"] [role="tab"] {
    color: var(--text-muted) !important;
    font-weight: 800 !important;
    font-size: 17px !important;
    padding: 1.5rem 2rem !important;
    border-bottom: 4px solid transparent !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

[data-testid="stTabs"] [role="tab"]:hover {
    color: var(--text-secondary) !important;
    background: rgba(79, 123, 255, 0.05) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--accent-blue) !important;
    border-bottom-color: var(--accent-blue) !important;
    box-shadow: 0 6px 16px var(--shadow-accent) !important;
    background: rgba(79, 123, 255, 0.08) !important;
}

/* INPUTS ULTRA VISIBLE */
.stNumberInput input, .stTextInput input, .stSelectbox select {
    background: var(--bg-card) !important;
    border: 3px solid var(--border-primary) !important;
    color: var(--text-primary) !important;
    border-radius: 12px !important;
    padding: 1.2rem 1rem !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    font-family: 'Poppins', sans-serif !important;
    transition: all 0.3s ease !important;
}

.stNumberInput input::placeholder, .stTextInput input::placeholder {
    color: var(--text-muted) !important;
    font-weight: 500 !important;
}

.stNumberInput input:focus, .stTextInput input:focus, .stSelectbox select:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 4px rgba(79, 123, 255, 0.15) !important;
    outline: none !important;
    background: var(--bg-card-hover) !important;
}

.stNumberInput label, .stTextInput label, .stSelectbox label {
    color: var(--text-secondary) !important;
    font-weight: 900 !important;
    font-size: 15px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-bottom: 0.8rem !important;
}

/* BUTTONS PREMIUM */
.stButton > button {
    background: var(--gradient-accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1rem 2.5rem !important;
    font-weight: 900 !important;
    font-size: 16px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 6px 20px rgba(79, 123, 255, 0.4) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(79, 123, 255, 0.6) !important;
}

.stButton > button:active {
    transform: translateY(-1px) !important;
}

/* METRICS ENHANCED */
[data-testid="stMetric"] {
    background: var(--gradient-card) !important;
    border: 3px solid var(--border-primary) !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    box-shadow: 0 8px 24px var(--shadow-primary) !important;
    transition: transform 0.3s ease !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 12px 32px var(--shadow-primary) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 14px !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-size: 3rem !important;
    font-weight: 900 !important;
    line-height: 1.1 !important;
    margin: 0.5rem 0 !important;
}

/* ALERTS IMPROVED */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left: 6px solid var(--accent-blue) !important;
    background: rgba(79, 123, 255, 0.08) !important;
    color: var(--text-primary) !important;
    padding: 1.8rem !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    box-shadow: 0 4px 12px var(--shadow-primary) !important;
}

/* DATA FRAMES ENHANCED */
[data-testid="stDataFrame"] {
    border: 3px solid var(--border-primary) !important;
    border-radius: 12px !important;
    box-shadow: 0 6px 20px var(--shadow-primary) !important;
}

[data-testid="stDataFrame"] th {
    background: var(--gradient-card) !important;
    color: var(--text-primary) !important;
    font-weight: 900 !important;
    padding: 1.2rem !important;
    font-size: 15px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

[data-testid="stDataFrame"] td {
    color: var(--text-secondary) !important;
    padding: 1rem !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    border-bottom: 1px solid var(--border-primary) !important;
}

/* SCROLLBARS */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: 6px;
}

::-webkit-scrollbar-thumb {
    background: var(--border-primary);
    border-radius: 6px;
    border: 2px solid var(--bg-secondary);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-blue);
}

/* CUSTOM CLASSES ULTRA */
.card-premium {
    background: var(--gradient-card);
    border: 3px solid var(--border-primary);
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 2.5rem;
    box-shadow: 0 10px 32px var(--shadow-primary);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-premium:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px var(--shadow-primary);
}

.card-title {
    font-size: 22px;
    font-weight: 900;
    color: var(--text-primary);
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    line-height: 1.3;
}

.card-subtitle {
    font-size: 16px;
    color: var(--text-muted);
    font-weight: 700;
    line-height: 1.6;
}

.badge-premium {
    display: inline-block;
    padding: 0.8rem 1.5rem;
    border-radius: 30px;
    font-size: 14px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: 3px solid;
    transition: all 0.3s ease;
}

.badge-premium:hover {
    transform: scale(1.05);
}

.badge-success {
    background: rgba(46, 213, 115, 0.1);
    color: var(--accent-green);
    border-color: var(--accent-green);
}

.badge-danger {
    background: rgba(255, 71, 87, 0.1);
    color: var(--accent-red);
    border-color: var(--accent-red);
}

.badge-warning {
    background: rgba(255, 165, 2, 0.1);
    color: var(--accent-orange);
    border-color: var(--accent-orange);
}

.badge-info {
    background: rgba(79, 123, 255, 0.1);
    color: var(--accent-blue);
    border-color: var(--accent-blue);
}

.stat-box {
    background: var(--gradient-card);
    border: 3px solid var(--border-primary);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 8px 24px var(--shadow-primary);
    transition: all 0.3s ease;
}

.stat-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px var(--shadow-primary);
}

.stat-label {
    font-size: 13px;
    color: var(--text-muted);
    text-transform: uppercase;
    font-weight: 900;
    letter-spacing: 1.5px;
    margin-bottom: 1rem;
}

.stat-value {
    font-size: 2.8rem;
    font-weight: 900;
    color: var(--text-primary);
    line-height: 1.1;
}

.progress-bar-premium {
    width: 100%;
    height: 12px;
    background: var(--bg-card-hover);
    border-radius: 6px;
    overflow: hidden;
    margin: 2rem 0;
    border: 2px solid var(--border-primary);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}

.progress-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.3) 50%, transparent 100%);
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.progress-success {
    background: var(--gradient-accent);
}

.progress-danger {
    background: linear-gradient(90deg, #ff4757, #ff6b7a);
}

.progress-warning {
    background: linear-gradient(90deg, #ffa502, #ffb74d);
}

.verdict-box-premium {
    border-radius: 16px;
    padding: 3rem;
    border: 4px solid;
    margin-bottom: 2.5rem;
    background: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    box-shadow: 0 12px 40px var(--shadow-primary);
}

.verdict-danger {
    border-color: var(--accent-red);
    background: linear-gradient(135deg, rgba(255, 71, 87, 0.08) 0%, rgba(255, 71, 87, 0.02) 100%);
}

.verdict-warning {
    border-color: var(--accent-orange);
    background: linear-gradient(135deg, rgba(255, 165, 2, 0.08) 0%, rgba(255, 165, 2, 0.02) 100%);
}

.verdict-success {
    border-color: var(--accent-green);
    background: linear-gradient(135deg, rgba(46, 213, 115, 0.08) 0%, rgba(46, 213, 115, 0.02) 100%);
}

.section-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--border-secondary), transparent);
    margin: 3rem 0;
    border-radius: 1px;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.animate-in {
    animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.animate-pulse {
    animation: pulse 2s infinite;
}

.title-primary {
    font-size: 56px;
    font-weight: 900;
    color: var(--text-primary);
    line-height: 1.2;
    text-transform: uppercase;
    letter-spacing: -0.02em;
    text-shadow: 0 4px 20px rgba(79, 123, 255, 0.3);
}

.title-secondary {
    font-size: 28px;
    font-weight: 900;
    color: var(--accent-blue);
    margin-top: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    text-shadow: 0 2px 10px rgba(79, 123, 255, 0.2);
}

.subtitle {
    font-size: 17px;
    color: var(--text-secondary);
    font-weight: 700;
    line-height: 1.8;
    margin-top: 1.5rem;
}

/* RESPONSIVE DESIGN */
@media (max-width: 1200px) {
    .main .block-container {
        padding: 1.5rem 2rem !important;
    }

    .title-primary {
        font-size: 48px;
    }

    .card-premium {
        padding: 2rem;
    }
}

@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 1.5rem !important;
    }

    [data-testid="stTabs"] [role="tab"] {
        padding: 1rem 1.5rem !important;
        font-size: 15px !important;
    }

    .title-primary {
        font-size: 36px;
    }

    .card-premium {
        padding: 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════════
# 📊 SIDEBAR - BRANDING PREMIUM
# ═════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    components.html("""
    <div style="text-align: center; padding: 3rem 2rem; border-bottom: 4px solid #3a4f6f; margin-bottom: 3rem; position: relative;">
        <div style="position: relative; z-index: 1; font-family: 'Poppins', sans-serif;">
            <div style="font-size: 64px; margin-bottom: 1.5rem; filter: drop-shadow(0 0 12px rgba(79, 123, 255, 0.4));">🛡️</div>
            <h1 style="font-size: 36px; font-weight: 900; margin: 0; color: #ffffff; text-transform: uppercase; letter-spacing: -0.02em; line-height: 1.1;">
                HEMERSON
            </h1>
            <h2 style="font-size: 28px; font-weight: 900; margin: 0.5rem 0 0; background: linear-gradient(135deg, #4f7bff 0%, #00d4ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-transform: uppercase; letter-spacing: 0.08em; line-height: 1.1;">
                TRUSTLINK
            </h2>
            <p style="font-size: 14px; color: #a0aec0; margin: 1.5rem 0 0; text-transform: uppercase; letter-spacing: 1px; font-weight: 800; line-height: 1.4;">
                🧠 DÉTECTION FRAUDE IA<br><span style="color: #4f7bff;">MACHINE LEARNING</span>
            </p>
        </div>
    </div>
    """, height=280)
    
    st.markdown("### 📈 STATISTIQUES SESSION")
    
    total = len(st.session_state.historique)
    fraudes = sum(1 for h in st.session_state.historique if h["verdict"] == "FRAUDE")
    suspects = sum(1 for h in st.session_state.historique if h["verdict"] == "SUSPECT")
    saines = total - fraudes - suspects
    
    col1, col2 = st.columns(2)
    col1.metric("📊 TOTAL", total)
    col2.metric("🚨 FRAUDES", fraudes)
    col1.metric("⚠️ SUSPECTS", suspects)
    col2.metric("✅ SAINES", saines)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    if total > 0:
        taux = round(fraudes / total * 100, 1)
        couleur = "🔴" if taux > 20 else "🟠" if taux > 5 else "🟢"
        st.markdown(f"""
        <div class="card-premium">
            <div class="stat-label">🎯 TAUX GLOBAL</div>
            <div style="font-size: 36px; font-weight: 900; color: #ffffff; margin: 1rem 0;">{couleur} {taux}%</div>
            <div class="progress-bar-premium">
                <div class="progress-fill progress-danger" style="width: {min(taux, 100)}%;"></div>
            </div>
            <div style="font-size: 12px; color: #a0aec0; margin-top: 1rem;">
                {total} TRANSACTION(S) ANALYSÉE(S)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&display=swap" rel="stylesheet">
    <div style="font-family:'Poppins',sans-serif; padding:1.3rem 1.1rem; background:rgba(8,12,32,0.8); border:1.5px solid #2a3f5f; border-left:4px solid #4f7bff; border-radius:10px;">
        <div style="margin-bottom:0.9rem;">
            <div style="font-size:10px; color:#7c8db5; text-transform:uppercase; letter-spacing:1.5px; font-weight:700; margin-bottom:0.3rem;">👨‍💻 Auteur &amp; Développeur</div>
            <div style="font-size:13.5px; color:#ffffff; font-weight:800;">Anoh Amon Francklin Hemerson</div>
        </div>
        <div style="height:1px; background:rgba(58,79,111,0.5); margin:0.7rem 0;"></div>
        <div style="margin-bottom:0.9rem;">
            <div style="font-size:10px; color:#7c8db5; text-transform:uppercase; letter-spacing:1.5px; font-weight:700; margin-bottom:0.3rem;">👨‍💼 Superviseur</div>
            <div style="font-size:13.5px; color:#4f7bff; font-weight:800;">M. AKPOSSO DIDIER MARTIAL</div>
        </div>
        <div style="height:1px; background:rgba(58,79,111,0.5); margin:0.7rem 0;"></div>
        <div style="font-size:10px; color:#5a6a85; text-transform:uppercase; letter-spacing:1px; font-weight:600; text-align:center;">
            © 2026 • Premium &nbsp;•&nbsp; <span style="color:#2ed573;">IA Avancée</span>
        </div>
    </div>
    """, height=175)

# ═════════════════════════════════════════════════════════════════════════════════
# 🎯 HEADER PRINCIPAL - ULTRA VISIBLE & ENCADRÉ
# ═════════════════════════════════════════════════════════════════════════════════
components.html("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&display=swap" rel="stylesheet">
<div style="
    font-family: 'Poppins', sans-serif;
    background: linear-gradient(135deg, #0d1530 0%, #111b3d 60%, #0a1228 100%);
    border: 3px solid #2a3f6f;
    border-radius: 18px;
    padding: 2.6rem 3rem 2.2rem;
    text-align: center;
    box-shadow: 0 0 0 1px rgba(79,123,255,0.12), 0 12px 40px rgba(0,0,0,0.55);
    position: relative;
    overflow: hidden;
">
    <!-- coins décoratifs -->
    <div style="position:absolute;top:0;left:0;width:28px;height:28px;border-top:3px solid #4f7bff;border-left:3px solid #4f7bff;border-radius:4px 0 0 0;"></div>
    <div style="position:absolute;top:0;right:0;width:28px;height:28px;border-top:3px solid #4f7bff;border-right:3px solid #4f7bff;border-radius:0 4px 0 0;"></div>
    <div style="position:absolute;bottom:0;left:0;width:28px;height:28px;border-bottom:3px solid #4f7bff;border-left:3px solid #4f7bff;border-radius:0 0 0 4px;"></div>
    <div style="position:absolute;bottom:0;right:0;width:28px;height:28px;border-bottom:3px solid #4f7bff;border-right:3px solid #4f7bff;border-radius:0 0 4px 0;"></div>

    <div style="font-size:42px; margin-bottom:0.9rem; filter:drop-shadow(0 0 14px rgba(79,123,255,0.5));">🛡️</div>

    <!-- Nom de l'app : blanc, grand, encadré -->
    <div style="display:inline-block; border:2px solid rgba(255,255,255,0.18); border-radius:10px; padding:0.5rem 2rem; margin-bottom:1.1rem; background:rgba(255,255,255,0.04);">
        <h1 style="font-size:34px; font-weight:900; color:#ffffff; margin:0; text-transform:uppercase; letter-spacing:0.05em; text-shadow:0 2px 16px rgba(79,123,255,0.35);">
            HEMERSON TRUSTLINK
        </h1>
    </div>

    <!-- Sous-titre EN ROUGE -->
    <p style="font-size:16px; font-weight:800; color:#ff4757; margin:0 0 0.8rem; text-transform:uppercase; letter-spacing:0.07em; text-shadow:0 0 20px rgba(255,71,87,0.4);">
        🧠 Détection Intelligente de Fraude Financière
    </p>

    <!-- Ligne déco rouge -->
    <div style="width:90px; height:3px; background:linear-gradient(90deg,#ff4757,#ff8c94); margin:0 auto 0.9rem; border-radius:2px;"></div>

    <!-- Descriptif -->
    <p style="font-size:12.5px; color:#a0aec0; font-weight:600; margin:0; letter-spacing:0.03em; line-height:1.8;">
        Machine Learning Avancé &nbsp;•&nbsp; Analyse Temps Réel &nbsp;•&nbsp; 30 Caractéristiques &nbsp;•&nbsp;
        <span style="color:#2ed573; font-weight:700;">Score IA Certifié</span>
    </p>
</div>
""", height=295)

# ═════════════════════════════════════════════════════════════════════════════════
# 📑 ONGLETS PRINCIPAUX
# ═════════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "🔍 ANALYSER TRANSACTION",
    "📋 HISTORIQUE",
    "📊 TABLEAU DE BORD"
])

# ╔═════════════════════════════════════════════════════════════════════════════╗
# ║ ONGLET 1 - ANALYSE TRANSACTION                                              ║
# ╚═════════════════════════════════════════════════════════════════════════════╝
with tab1:
    st.markdown("""
    <div class="card-premium animate-in">
        <div class="card-title">💳 DONNÉES DE LA TRANSACTION</div>
        <div class="card-subtitle">Renseignez les paramètres pour analyse instantanée</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        montant = st.number_input("💸 MONTANT (FCFA)", min_value=0.0, format="%.2f", value=5000.0)
    with col2:
        horodatage = st.number_input("⏱️ HORODATAGE (secondes)", min_value=0.0, value=43200.0)
    with col3:
        libelle = st.text_input("📝 DESCRIPTION TRANSACTION", placeholder="Ex: Achat en ligne")
    
    st.markdown("""
    <div class="card-premium animate-in">
        <div class="card-title">🧬 VECTEURS D'ANALYSE (V1-V28)</div>
        <div class="card-subtitle">Composantes PCA • Laissez à 0.0 par défaut ou remplissez avec vos données</div>
    </div>
    """, unsafe_allow_html=True)
    
    vecteurs = []
    _, *inner_cols, _ = st.columns([0.5] + [1]*7 + [0.5])
    for i in range(1, 29):
        with inner_cols[(i - 1) % 7]:
            v = st.number_input(f"V{i}", value=0.0, key=f"v{i}")
            vecteurs.append(v)
    
    st.markdown("")
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        analyser = st.button("🔍 ANALYSER", use_container_width=True, type="primary")
    with col_info:
        st.caption("✅ ANALYSÉ SÉCURISÉ | ⚡ INSTANTANÉ | 💾 SAUVEGARDÉ | 🆓 100% GRATUIT")
    
    if analyser and modele is not None:
        with st.spinner("🔄 ANALYSE EN COURS..."):
            time.sleep(0.4)
            
            entree = np.array([horodatage] + vecteurs + [montant]).reshape(1, -1)
            entree_scaled = scaler.transform(entree)
            proba = modele.predict_proba(entree_scaled)[0][1]
            score = proba * 100
            pred = modele.predict(entree_scaled)[0]
            ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            lbl = libelle.strip() if libelle.strip() else f"TRANSACTION #{len(st.session_state.historique)+1}"
            
            if score > 75:
                verdict = "FRAUDE"
                couleur = "danger"
                icone = "🚨"
                conseil = "⛔ TRANSACTION À BLOQUER IMMÉDIATEMENT"
                badge_class = "danger"
            elif score > 50:
                verdict = "SUSPECT"
                couleur = "warning"
                icone = "⚠️"
                conseil = "🔍 VÉRIFICATION MANUELLE RECOMMANDÉE"
                badge_class = "warning"
            else:
                verdict = "SAINE"
                couleur = "success"
                icone = "✅"
                conseil = "✔️ TRANSACTION APPROUVÉE - PROFIL NORMAL"
                badge_class = "success"
            
            st.session_state.historique.append({
                "id": len(st.session_state.historique) + 1,
                "date": ts,
                "libelle": lbl,
                "montant": montant,
                "verdict": verdict,
                "score": round(score, 2),
                "prediction": int(pred),
            })
            
            st.success(f"✅ ANALYSE #{len(st.session_state.historique)} COMPLÉTÉE AVEC SUCCÈS")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_res, col_det = st.columns([1.2, 1])
            
            with col_res:
                # Determine progress class
                if couleur == 'success':
                    progress_class = 'success'
                elif couleur == 'danger':
                    progress_class = 'danger'
                else:
                    progress_class = 'warning'
                
                st.markdown(f"""
                <div class="verdict-box-premium verdict-{couleur} animate-in">
                    <div style="margin-bottom: 2rem;">
                        <span class="badge-premium badge-{badge_class}">{icone} {verdict}</span>
                    </div>
                    <div style="font-size: 56px; font-weight: 900; color: var(--text-primary); margin-bottom: 2rem; line-height: 1; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);">
                        {score:.1f}%
                    </div>
                    <div style="font-size: 18px; color: var(--text-secondary); margin-bottom: 2.5rem; line-height: 1.8; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">
                        {conseil}
                    </div>
                    <div class="progress-bar-premium">
                        <div class="progress-fill progress-{progress_class}" style="width: {min(score, 100)}%;"></div>
                <div style="margin-top: 2rem; display: flex; justify-content: space-between; font-size: 13px; color: var(--text-muted); font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px;">
                    <span>🔴 RISQUE FAIBLE (0%)</span>
                    <span>🟡 MODÉRÉ (50%)</span>
                    <span>🟢 MAXIMUM (100%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with col_det:
                st.markdown(f"""
                <div class="card-premium">
                    <div class="card-title">📊 DÉTAILS COMPLETS</div>
                    <div style="font-size: 14px; line-height: 2.2; color: #e0e7ff;">
                        <div><strong style="color: #ffffff;">MONTANT:</strong> {montant:,.0f} FCFA</div>
                        <div><strong style="color: #ffffff;">PRÉDICTION:</strong> {"FRAUDE" if pred == 1 else "LÉGITIME"}</div>
                        <div><strong style="color: #ffffff;">CONFIANCE:</strong> {abs(score - 50) * 2:.0f}%</div>
                        <div><strong style="color: #ffffff;">HORODATAGE:</strong> {ts}</div>
                        <div><strong style="color: #ffffff;">DESCRIPTION:</strong> {lbl}</div>
                        <div><strong style="color: #ffffff;">ID ANALYSE:</strong> #{len(st.session_state.historique)}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ╔═════════════════════════════════════════════════════════════════════════════╗
# ║ ONGLET 2 - HISTORIQUE                                                       ║
# ╚═════════════════════════════════════════════════════════════════════════════╝
with tab2:
    if not st.session_state.historique:
        components.html("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&display=swap" rel="stylesheet">
        <div style="text-align:center;padding:3.2rem 2rem;background:linear-gradient(135deg,#111b3d,#0d1530);border:2px dashed #3a4f6f;border-radius:16px;box-shadow:0 8px 28px rgba(0,0,0,0.3);font-family:'Poppins',sans-serif;">
            <div style="font-size:52px;margin-bottom:1rem;filter:drop-shadow(0 0 10px rgba(79,123,255,0.3));">📋</div>
            <h3 style="color:#ffffff;margin:0 0 0.8rem;font-size:22px;font-weight:900;text-transform:uppercase;letter-spacing:1px;">AUCUNE ANALYSE<br>EFFECTUÉE</h3>
            <p style="color:#a0aec0;margin:0 auto;font-size:14px;font-weight:600;line-height:1.7;max-width:420px;">
                Lancez votre première analyse dans l'onglet <strong style="color:#4f7bff;">ANALYSER TRANSACTION</strong> pour voir vos résultats ici
            </p>
            <div style="margin:1.3rem auto 0;width:60px;height:3px;background:linear-gradient(90deg,#4f7bff,#00d4ff);border-radius:2px;"></div>
        </div>
        """, height=270)
    else:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown("### 📊 HISTORIQUE COMPLET DES ANALYSES")
        with col2:
            if st.button("📥 EXPORTER CSV", use_container_width=True):
                df = pd.DataFrame(st.session_state.historique)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("", csv, "trustlink_export.csv", "text/csv", use_container_width=True)
        with col3:
            if st.button("🗑️ RÉINITIALISER", use_container_width=True):
                st.session_state.historique = []
                st.rerun()
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        for item in reversed(st.session_state.historique):
            verdict = item["verdict"]
            score = item["score"]
            badge_type = "success" if verdict == "SAINE" else "danger" if verdict == "FRAUDE" else "warning"
            
            # Determine progress class for history
            if badge_type == 'success':
                hist_progress_class = 'success'
            elif badge_type == 'danger':
                hist_progress_class = 'danger'
            else:
                hist_progress_class = 'warning'
            
            st.markdown(f"""
            <div style="background: var(--gradient-card); border: 3px solid var(--border-primary); border-radius: 14px; padding: 2rem; margin-bottom: 1.5rem; box-shadow: 0 6px 20px var(--shadow-primary);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 2rem;">
                    <div style="flex: 1; min-width: 300px;">
                        <div style="font-weight: 900; color: var(--text-primary); margin-bottom: 0.8rem; font-size: 18px; text-transform: uppercase; letter-spacing: 0.5px;">#{item['id']} - {item['libelle']}</div>
                        <div style="font-size: 14px; color: var(--text-muted); font-weight: 700;">{item['date']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 0.8rem; text-transform: uppercase; font-weight: 800; letter-spacing: 0.8px;">MONTANT</div>
                        <div style="font-weight: 900; color: var(--text-primary); font-size: 18px;">{item['montant']:,.0f} FCFA</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 0.8rem; text-transform: uppercase; font-weight: 800; letter-spacing: 0.8px;">SCORE RISQUE</div>
                        <div style="font-weight: 900; color: var(--text-primary); font-size: 18px;">{score:.1f}%</div>
                    </div>
                    <div>
                        <span class="badge-premium badge-{badge_type}">{verdict}</span>
                    </div>
                </div>
                <div class="progress-bar-premium" style="margin-top: 1.5rem;">
                    <div class="progress-fill progress-{hist_progress_class}" style="width: {min(score, 100)}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ╔═════════════════════════════════════════════════════════════════════════════╗
# ║ ONGLET 3 - TABLEAU DE BORD                                                  ║
# ╚═════════════════════════════════════════════════════════════════════════════╝
with tab3:
    if not st.session_state.historique:
        components.html("""
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&display=swap" rel="stylesheet">
        <div style="text-align:center;padding:3.2rem 2rem;background:linear-gradient(135deg,#111b3d,#0d1530);border:2px dashed #3a4f6f;border-radius:16px;box-shadow:0 8px 28px rgba(0,0,0,0.3);font-family:'Poppins',sans-serif;">
            <div style="font-size:52px;margin-bottom:1rem;filter:drop-shadow(0 0 10px rgba(79,123,255,0.3));">📊</div>
            <h3 style="color:#ffffff;margin:0 0 0.8rem;font-size:22px;font-weight:900;text-transform:uppercase;letter-spacing:1px;">AUCUNE DONNÉE<br>DISPONIBLE</h3>
            <p style="color:#a0aec0;margin:0 auto;font-size:14px;font-weight:600;line-height:1.7;max-width:500px;">
                Effectuez des analyses pour voir les statistiques détaillées,<br>graphiques interactifs et indicateurs de performance
            </p>
            <div style="margin:1.3rem auto 0;width:60px;height:3px;background:linear-gradient(90deg,#4f7bff,#00d4ff);border-radius:2px;"></div>
        </div>
        """, height=270)
    else:
        df = pd.DataFrame(st.session_state.historique)
        total = len(df)
        fraudes = len(df[df.verdict == "FRAUDE"])
        suspects = len(df[df.verdict == "SUSPECT"])
        saines = len(df[df.verdict == "SAINE"])
        score_moy = df["score"].mean()
        montant_total = df["montant"].sum()
        taux_fraude = fraudes / total * 100

        # ── ALERTE DYNAMIQUE ─────────────────────────────────────────────
        if taux_fraude > 30:
            st.error(f"🚨 ALERTE CRITIQUE — Taux de fraude : **{taux_fraude:.1f}%** ({fraudes}/{total} transactions)")
        elif taux_fraude > 10:
            st.warning(f"⚠️ VIGILANCE — Taux de fraude modéré : **{taux_fraude:.1f}%** ({fraudes}/{total} transactions)")
        else:
            st.success(f"✅ SITUATION NORMALE — Taux de fraude : **{taux_fraude:.1f}%** ({fraudes}/{total} transactions)")

        # ── KPI ───────────────────────────────────────────────────────────
        st.markdown("### 📈 KPI — INDICATEURS CLÉS DE PERFORMANCE")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="stat-box"><div class="stat-label">📊 Total Analyses</div><div class="stat-value">{total}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-box"><div class="stat-label" style="color:#ff4757;">🚨 Fraudes</div><div class="stat-value" style="color:#ff4757;">{fraudes}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="stat-box"><div class="stat-label" style="color:#ffa502;">⚠️ Suspects</div><div class="stat-value" style="color:#ffa502;">{suspects}</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="stat-box"><div class="stat-label" style="color:#2ed573;">✅ Saines</div><div class="stat-value" style="color:#2ed573;">{saines}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ── STYLE COMMUN GRAPHIQUES ───────────────────────────────────────
        BG   = "rgba(10,14,39,0.97)"
        PLOT = "rgba(5,9,28,0.97)"
        FONT = dict(color="#ffffff", size=14, family="Poppins")
        AXIS = dict(tickfont=dict(color="#ffffff", size=13), title_font=dict(color="#ffffff", size=14),
                    gridcolor="rgba(79,123,255,0.15)", linecolor="#3a4f6f", zerolinecolor="#3a4f6f")
        MARGIN = dict(t=55, b=55, l=55, r=45)

        # ── LIGNE 1 : Barres + Donut ──────────────────────────────────────
        st.markdown("### 📊 RÉPARTITION DES VERDICTS")
        col1, col2 = st.columns(2)

        with col1:
            fig = go.Figure(go.Bar(
                x=["✅ SAINES", "⚠️ SUSPECTS", "🚨 FRAUDES"], y=[saines, suspects, fraudes],
                marker=dict(color=["#2ed573","#ffa502","#ff4757"], line=dict(color="#0a0e27", width=2)),
                text=[f"<b>{saines}</b>",f"<b>{suspects}</b>",f"<b>{fraudes}</b>"],
                textposition="outside", textfont=dict(size=15, color="#ffffff"),
                hovertemplate="<b>%{x}</b><br>Nombre : %{y}<extra></extra>",
            ))
            fig.update_layout(
                title=dict(text="Transactions par verdict", font=dict(color="#ffffff",size=16), x=0.5, xanchor="center"),
                height=400, paper_bgcolor=BG, plot_bgcolor=PLOT, font=FONT, margin=MARGIN,
                xaxis=dict(showgrid=False, tickfont=dict(color="#ffffff",size=14), linecolor="#3a4f6f"),
                yaxis=dict(title="Nombre", **AXIS),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with col2:
            fig = go.Figure(go.Pie(
                labels=["✅ SAINES","⚠️ SUSPECTS","🚨 FRAUDES"], values=[saines, suspects, fraudes],
                marker=dict(colors=["#2ed573","#ffa502","#ff4757"], line=dict(color="#0a0e27",width=3)),
                hole=0.44, textfont=dict(size=14, color="#ffffff"), textinfo="label+percent",
                pull=[0, 0.04, 0.09],
                hovertemplate="<b>%{label}</b><br>Nombre : %{value}<br>Part : %{percent}<extra></extra>",
            ))
            fig.update_layout(
                title=dict(text="Distribution globale", font=dict(color="#ffffff",size=16), x=0.5, xanchor="center"),
                height=400, paper_bgcolor=BG, font=FONT, margin=MARGIN,
                legend=dict(font=dict(color="#ffffff",size=13), bgcolor="rgba(17,27,61,0.85)", bordercolor="#3a4f6f", borderwidth=1),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ── LIGNE 2 : Évolution scores + Jauge risque ─────────────────────
        st.markdown("### 📈 ÉVOLUTION DU SCORE DE RISQUE & NIVEAU GLOBAL")
        col1, col2 = st.columns([2, 1])

        with col1:
            ids    = [e["id"]    for e in st.session_state.historique]
            scores = [e["score"] for e in st.session_state.historique]
            pts_col = ["#ff4757" if s>75 else "#ffa502" if s>50 else "#2ed573" for s in scores]
            fig = go.Figure()
            fig.add_hrect(y0=75, y1=110, fillcolor="rgba(255,71,87,0.05)", line_width=0)
            fig.add_hrect(y0=50, y1=75,  fillcolor="rgba(255,165,2,0.04)", line_width=0)
            fig.add_trace(go.Scatter(
                x=ids, y=scores, mode="lines+markers", name="Score de risque",
                line=dict(color="#4f7bff", width=3),
                marker=dict(size=11, color=pts_col, line=dict(color="#ffffff", width=2)),
                fill="tozeroy", fillcolor="rgba(79,123,255,0.07)",
                hovertemplate="<b>Analyse #%{x}</b><br>Score : %{y:.1f}%<extra></extra>",
            ))
            fig.add_hline(y=75, line_dash="dash", line_color="#ff4757", line_width=2,
                annotation=dict(text="🚨 SEUIL FRAUDE 75%", font=dict(color="#ff4757",size=13), bgcolor="rgba(255,71,87,0.15)", bordercolor="#ff4757"))
            fig.add_hline(y=50, line_dash="dash", line_color="#ffa502", line_width=2,
                annotation=dict(text="⚠️ SEUIL SUSPECT 50%", font=dict(color="#ffa502",size=13), bgcolor="rgba(255,165,2,0.15)", bordercolor="#ffa502"))
            fig.update_layout(
                title=dict(text="Évolution temporelle des scores", font=dict(color="#ffffff",size=16), x=0.5, xanchor="center"),
                height=400, paper_bgcolor=BG, plot_bgcolor=PLOT, font=FONT, margin=MARGIN,
                xaxis=dict(title="N° Analyse", **AXIS), yaxis=dict(title="Score (%)", range=[0,112], **AXIS),
                hovermode="x unified",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with col2:
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=score_moy,
                delta=dict(reference=50, increasing=dict(color="#ff4757"), decreasing=dict(color="#2ed573"), font=dict(size=14,color="#ffffff")),
                number=dict(suffix="%", font=dict(size=40, color="#ffffff")),
                title=dict(text="SCORE MOYEN<br>GLOBAL", font=dict(size=14, color="#ffffff")),
                gauge=dict(
                    axis=dict(range=[0,100], tickwidth=2, tickcolor="#ffffff", tickfont=dict(color="#ffffff",size=12)),
                    bar=dict(color="#4f7bff", thickness=0.28),
                    bgcolor="rgba(0,0,0,0)", borderwidth=0,
                    steps=[
                        dict(range=[0,50],  color="rgba(46,213,115,0.18)"),
                        dict(range=[50,75], color="rgba(255,165,2,0.18)"),
                        dict(range=[75,100],color="rgba(255,71,87,0.18)"),
                    ],
                    threshold=dict(line=dict(color="#ff4757",width=4), thickness=0.85, value=75),
                ),
            ))
            fig.update_layout(height=400, paper_bgcolor=BG, font=FONT, margin=dict(t=55,b=25,l=20,r=20))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ── LIGNE 3 : Volume financier + Distribution scores ───────────────
        st.markdown("### 💰 ANALYSE FINANCIÈRE & DISTRIBUTION")
        col1, col2 = st.columns(2)

        with col1:
            mv = df.groupby("verdict")["montant"].sum().reset_index()
            cmap = {"SAINE":"#2ed573","SUSPECT":"#ffa502","FRAUDE":"#ff4757"}
            fig = go.Figure(go.Bar(
                x=mv["verdict"], y=mv["montant"],
                marker=dict(color=[cmap.get(v,"#4f7bff") for v in mv["verdict"]], line=dict(width=2,color="#0a0e27")),
                text=[f"{v:,.0f} F" for v in mv["montant"]], textposition="outside",
                textfont=dict(color="#ffffff", size=12),
                hovertemplate="<b>%{x}</b><br>Volume : %{y:,.0f} FCFA<extra></extra>",
            ))
            fig.update_layout(
                title=dict(text="Volume financier par verdict (FCFA)", font=dict(color="#ffffff",size=16), x=0.5, xanchor="center"),
                height=360, paper_bgcolor=BG, plot_bgcolor=PLOT, font=FONT, margin=MARGIN,
                xaxis=dict(showgrid=False, tickfont=dict(color="#ffffff",size=14), linecolor="#3a4f6f"),
                yaxis=dict(title="Montant (FCFA)", **AXIS),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with col2:
            fig = go.Figure(go.Box(
                y=df["score"], name="Scores", boxmean="sd",
                marker=dict(color="#4f7bff", size=8),
                line=dict(color="#4f7bff", width=2),
                fillcolor="rgba(79,123,255,0.15)",
                hovertemplate="Score : %{y:.1f}%<extra></extra>",
            ))
            fig.update_layout(
                title=dict(text="Distribution des scores de risque", font=dict(color="#ffffff",size=16), x=0.5, xanchor="center"),
                height=360, paper_bgcolor=BG, plot_bgcolor=PLOT, font=FONT, margin=MARGIN,
                yaxis=dict(title="Score (%)", range=[0,105], **AXIS),
                xaxis=dict(tickfont=dict(color="#ffffff")),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # ── STATS AVANCÉES ────────────────────────────────────────────────
        st.markdown("### 🔬 STATISTIQUES AVANCÉES")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="card-premium">
                <div class="card-title">💰 ANALYSE DES MONTANTS</div>
                <div style="font-size:15px;line-height:2.5;color:#e0e7ff;">
                    <div><span style="color:#a0aec0;">VOLUME TOTAL :</span> <span style="color:#fff;font-weight:800;">{montant_total:,.0f} FCFA</span></div>
                    <div><span style="color:#a0aec0;">MONTANT MOYEN :</span> <span style="color:#fff;font-weight:800;">{montant_total/total:,.0f} FCFA</span></div>
                    <div><span style="color:#a0aec0;">À RISQUE :</span> <span style="color:#ff4757;font-weight:800;">{df[df.verdict != 'SAINE'].montant.sum():,.0f} FCFA</span></div>
                    <div><span style="color:#a0aec0;">MONTANT MIN :</span> <span style="color:#fff;font-weight:800;">{df.montant.min():,.0f} FCFA</span></div>
                    <div><span style="color:#a0aec0;">MONTANT MAX :</span> <span style="color:#fff;font-weight:800;">{df.montant.max():,.0f} FCFA</span></div>
                </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="card-premium">
                <div class="card-title">🎯 MÉTRIQUES CLÉS</div>
                <div style="font-size:15px;line-height:2.5;color:#e0e7ff;">
                    <div><span style="color:#a0aec0;">SCORE MOYEN :</span> <span style="color:#fff;font-weight:800;">{score_moy:.1f}%</span></div>
                    <div><span style="color:#a0aec0;">TAUX FRAUDE :</span> <span style="color:#ff4757;font-weight:800;">{taux_fraude:.1f}%</span></div>
                    <div><span style="color:#a0aec0;">SCORE MIN :</span> <span style="color:#fff;font-weight:800;">{df.score.min():.1f}%</span></div>
                    <div><span style="color:#a0aec0;">SCORE MAX :</span> <span style="color:#fff;font-weight:800;">{df.score.max():.1f}%</span></div>
                    <div><span style="color:#a0aec0;">ÉCART-TYPE :</span> <span style="color:#4f7bff;font-weight:800;">{df.score.std():.1f}%</span></div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📋 VUE DÉTAILLÉE COMPLÈTE")
        df_view = df[["id","date","libelle","montant","verdict","score"]].copy()
        df_view.columns = ["ID","DATE","DESCRIPTION","MONTANT (FCFA)","VERDICT","SCORE (%)"]
        st.dataframe(df_view, use_container_width=True, hide_index=True)