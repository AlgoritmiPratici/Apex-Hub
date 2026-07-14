import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# 1. CONFIGURAZIONE ARCHITETTURALE & RESPONSIVE
st.set_page_config(
    page_title="APEX Global Infrastructure Hub", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# 2. INIEZIONE CSS ENTERPRISE (Risoluzione Contrasti e Testo Nero)
st.markdown("""
    <style>
    /* Pulizia Interfaccia Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div.stDeployButton {visibility: hidden;}
    
    /* Configurazione Palette Colori Scuro Globale */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0B0E14 !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Correzione Radicale Testo Tabelle e Dataframe (Risoluzione Bug Immagine 1) */
    div[data-testid="stTable"] table, div[data-testid="stDataFrame"] table {
        color: #E2E8F0 !important;
        background-color: #151A23 !important;
    }
    div[data-testid="stTable"] td, div[data-testid="stTable"] th, div[data-testid="stDataFrame"] td {
        color: #E2E8F0 !important;
        border-bottom: 1px solid #232A38 !important;
    }
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #E2E8F0 !important;
    }
    
    /* Sidebar Layout */
    [data-testid="stSidebar"] {
        background-color: #121620 !important;
        border-right: 1px solid #232A38 !important;
    }
    
    /* Elementi di Navigazione */
    .sidebar-title {
        color: #10B981 !important;
        font-weight: 700;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    /* Evidenziazioni */
    .highlight { color: #10B981 !important; font-weight: bold; }
    .brand-orange { color: #F97316 !important; font-weight: bold; }
    .brand-purple { color: #A855F7 !important; font-weight: bold; }
    .brand-blue { color: #3B82F6 !important; font-weight: bold; }
    
    /* Pulsanti Full-Width Ingegnerizzati */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #10B981 !important;
        color: #0B0E14 !important;
        font-weight: 700 !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        width: 100% !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #34D399 !important;
        transform: translateY(-1px);
    }
    
    /* Card Contenitore */
    .card {
        background-color: #151A23;
        padding: 1.5rem;
        border-radius: 6px;
        border: 1px solid #232A38;
        margin-bottom: 1rem;
    }
    
    /* Badge Status */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        font-size: 0.8rem;
        font-weight: bold;
        border: 1px solid #10B981;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. ARCHITETTURA SIDEBAR MULTI-ASSET
# ==========================================
st.sidebar.markdown("<div class='sidebar-title'>APEX MATRIX PLATFORM</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; color: #64748B; font-size: 0.75rem; margin-bottom: 1.5rem;'>Ecosistema Unificato Multi-Asset</div>", unsafe_allow_html=True)

# Selezione dell'Asset Principale
asset_selezionato = st.sidebar.selectbox("SELEZIONA BRAND NETWORK:", [
    "📌 ASSET 00: AlgoritmiPratici",
    "🧠 ASSET 01: SintesiMentale",
    "🎨 ASSET 02: MetodoEstetico",
    "📁 ASSET 03: RisorsaZero"
])

st.sidebar.markdown("---")

# ==========================================
# FLOW LOGICO: ALGORITMIPRATICI (AUTOMATION)
# ==========================================
if asset_selezionato == "📌 ASSET 00: AlgoritmiPratici":
    modulo = st.sidebar.radio("MODULI SETTIMANA 1:", [
        "01. Normalizzazione CSV", 
        "02. Blindatura .env", 
        "03. Estrattore Telegram", 
        "04. Stack Cloud Invariato", 
        "05. Dashboard Analitica", 
        "06. Webhook Router", 
        "07. Bridge API CRM"
    ])
    
    if modulo == "01. Normalizzazione CSV":
        st.markdown("<div class='status-badge'>ENGINE ONLINE</div>", unsafe_allow_html=True)
        st.title("⚙️ Normalizzazione Data-Dump")
        st.markdown("Elimina le ridondanze dei fogli di calcolo. Formatta le stringhe per l'iniezione CRM in <span class='highlight'>tempo reale</span>.", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Innestare Database Grezzo (.csv)", type=["csv"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded_file is not None:
            df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
            df_clean = df_raw.copy().drop_duplicates()
            if 'Email' in df_clean.columns:
                df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                df_clean = df_clean[~df_clean['Email'].isin(['nan', 'none', '', 'null'])].dropna(subset=['Email'])
            st.success("Validazione completata.")
            st.markdown("#### Preview Dataset Strutturato")
            st.dataframe(df_clean.head(5), use_container_width=True)
            csv_pulito = df_clean.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Scarica Database Validato", data=csv_pulito, file_name="apex_clean.csv", mime="text/csv")

    elif modulo == "05. Dashboard Analitica":
        st.markdown("<div class='status-badge'>REVENUE CORE</div>", unsafe_allow_html=True)
        st.title("📊 Centro di Controllo Direzionale")
        col1, col2 = st.columns(2)
        col1.metric(label="MRR Ecosistema", value="€ 42.500", delta="+12.4%")
        col2.metric(label="Latenza Endpoint", value="4.2 ms", delta="-0.8 ms", delta_color="inverse")
        
        df_chart = pd.DataFrame({'Dipartimento': ['Sales', 'Marketing', 'IT Infrastructure'], 'Cassa YTD': [85000, -22000, 45000]})
        fig = px.bar(df_chart, x='Dipartimento', y='Cassa YTD', color='Cassa YTD', color_continuous_scale=['#EF4444', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.title("Sorgenti dell'Infrastruttura")
        st.info("Utilizza il menu laterale per navigare tra gli altri script pronti al download forniti da AlgoritmiPratici.")

# ==========================================
# FLOW LOGICO: SINTESIMENTALE (EBOOK HUB)
# ==========================================
elif asset_selezionato == "🧠 ASSET 01: SintesiMentale":
    st.sidebar.markdown("<div style='color: #A855F7; font-weight: bold; text-align: center;'>Ambiente eBook Premium</div>", unsafe_allow_html=True)
    st.title("🧠 SintesiMentale: Manuali Asimmetrici")
    st.markdown("Istruzioni d'élite per la manipolazione logica delle informazioni e l'ottimizzazione neurale.")
    
    st.markdown("""
    <div class='card'>
    <h3>📚 Volume Primario: La Bibbia Faceless dell'Asset Empire</h3>
    La guida universale per la capitalizzazione sistematica delle piattaforme digitali senza l'esposizione del volto. Contenuto ad alto RPM finanziario.
    <br><br>
    <a href="https://gumroad.com" target="_blank" style="text-decoration: none;">
        <button style="background-color: #A855F7; color: white; width: 100%; padding: 0.6rem; border: none; font-weight: bold; border-radius: 4px; cursor: pointer;">
            🔓 SBLOCCA L'EBOOK COMPLETO SU GUMROAD
        </button>
    </a>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FLOW LOGICO: METODOESTETICO (PLANNER HUB)
# ==========================================
elif asset_selezionato == "🎨 ASSET 02: MetodoEstetico":
    st.sidebar.markdown("<div style='color: #F97316; font-weight: bold; text-align: center;'>Sistemi Visivi & Printable</div>", unsafe_allow_html=True)
    st.title("🎨 MetodoEstetico: Produttività ed Ingegneria Visiva")
    st.markdown("Strumenti visivi standardizzati per l'azzeramento del caos operativo e la gestione scientifica del tempo.")
    
    st.markdown("""
    <div class='card'>
    <h3>📅 Digital Executive Planner PDF</h3>
    Il framework di journaling, habit-tracking e pianificazione finanziaria ad alta conversione d'impulso. Layout minimalistico antracite.
    <br><br>
    <a href="https://gumroad.com" target="_blank" style="text-decoration: none;">
        <button style="background-color: #F97316; color: white; width: 100%; padding: 0.6rem; border: none; font-weight: bold; border-radius: 4px; cursor: pointer;">
            📥 SCARICA IL PLANNER MATRICE SU GUMROAD
        </button>
    </a>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FLOW LOGICO: RISORSAZERO (CURATED LISTS)
# ==========================================
elif asset_selezionato == "📁 ASSET 03: RisorsaZero":
    st.sidebar.markdown("<div style='color: #3B82F6; font-weight: bold; text-align: center;'>Arbitraggio del Tempo</div>", unsafe_allow_html=True)
    st.title("📁 RisorsaZero: Database Segreto di Internet")
    st.markdown("Elenchi curati di risorse indisponibili per risparmiare centine di ore di ricerca manuale.")
    
    # Integrazione Diretta dell'AI Toolkit (Evitiamo Notion!)
    st.markdown("### ⚡ AI Toolkit Privato (50 Tool Gratuiti Selezionati)")
    
    data_toolkit = {
        "Categoria": ["Ingegneria Prompt", "Sintesi Vocale", "Generazione Video", "Automazione API", "Storage Object"],
        "Nome Strumento": ["Gemini Pro Advanced", "ElevenLabs Core", "CapCut Desktop Engine", "n8n Open Source", "Cloudflare R2 Storage"],
        "Bypass Finanziario": ["Free Tier Attivo", "10k Caratteri Mese", "Export 4K Gratuito", "Illimitato Self-Hosted", "10GB Gratis Zero Friction"]
    }
    df_toolkit = pd.DataFrame(data_toolkit)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.dataframe(df_toolkit, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    csv_toolkit = df_toolkit.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Esporta l'intero Archivio (.csv)", data=csv_toolkit, file_name="risorsazero_ai_toolkit.csv", mime="text/csv")

# Footer asettico e costante
st.sidebar.markdown("<div style='font-size: 0.7rem; color: #475569; text-align: center; margin-top: 5rem;'>APEX NETWORK PLATFORM © 2026</div>", unsafe_allow_html=True)
