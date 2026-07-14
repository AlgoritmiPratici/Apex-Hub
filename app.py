import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# ==========================================
# 1. CONFIGURAZIONE & GESTIONE PARAMETRI URL
# ==========================================
st.set_page_config(
    page_title="APEX Global Infrastructure Network", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# Estrazione dinamica del brand dall'URL per eliminare la frizione utente
# Esempio d'uso: ...streamlit.app/?target=SintesiMentale
query_params = st.query_params
target_iniziale = query_params.get("target", "📌 ASSET 00: AlgoritmiPratici")

# Normalizzazione indici per selectbox
mappa_target = {
    "AlgoritmiPratici": 0,
    "SintesiMentale": 1,
    "MetodoEstetico": 2,
    "RisorsaZero": 3
}
indice_default = mappa_target.get(target_iniziale, 0)

# ==========================================
# 2. INIEZIONE CSS ENTERPRISE (CONTRATO RIGOROSO)
# ==========================================
st.markdown("""
    <style>
    /* Reset Totale UI Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div.stDeployButton {visibility: hidden;}
    
    /* Configurazione Palette Cromatica Rigida */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0A0D14 !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* RISOLUZIONE CRITICITÀ TESTI SCURI (FORZATURA GLOBALE) */
    label, p, span, li, th, td, .stWidgetLabel, [data-testid="stWidgetLabel"] p {
        color: #E2E8F0 !important;
        font-weight: 500;
    }
    
    /* Overwrite Input Elements */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #141923 !important;
        color: #FFFFFF !important;
        border: 1px solid #222C3A !important;
    }
    
    div[data-testid="stTable"] table, div[data-testid="stDataFrame"] table {
        color: #E2E8F0 !important;
        background-color: #111622 !important;
    }
    
    /* Barra Laterale */
    [data-testid="stSidebar"] {
        background-color: #111622 !important;
        border-right: 1px solid #222C3A !important;
    }
    
    /* Tipografia d'Elite */
    h1, h2, h3, h4 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: -0.04em;
    }
    .highlight { color: #10B981 !important; font-weight: 600; }
    
    /* Pulsanti ad Alta Conversione */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #10B981 !important;
        color: #0A0D14 !important;
        font-weight: 700 !important;
        border-radius: 4px !important;
        border: none !important;
        padding: 0.7rem 1.4rem !important;
        width: 100% !important;
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #34D399 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
    }
    
    .card {
        background-color: #141923;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #222C3A;
        margin-bottom: 1.2rem;
    }
    
    .status-online {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        font-size: 0.75rem;
        font-weight: bold;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. STRUTTURA LATERALE (SIDEBAR)
# ==========================================
st.sidebar.markdown("<div style='color: #10B981; font-weight:700; font-size:1.1rem; text-align:center;'>APEX CORE ENGINE</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

lista_brand = [
    "📌 ASSET 00: AlgoritmiPratici",
    "🧠 ASSET 01: SintesiMentale",
    "🎨 ASSET 02: MetodoEstetico",
    "📁 ASSET 03: RisorsaZero"
]

asset_selezionato = st.sidebar.selectbox("BRAND NETWORK DEPLOYED:", lista_brand, index=indice_default)
st.sidebar.markdown("---")

# ==========================================
# BRAND FLOW: ALGORITMIPRATICI (AUTOMATION B2B)
# ==========================================
if asset_selezionato == "📌 ASSET 00: AlgoritmiPratici":
    modulo = st.sidebar.radio("FUNNEL OPERATIVO S1:", [
        "01. Normalizzazione CSV", 
        "02. Blindatura Protocollo .env", 
        "03. Estrattore Client Telegram", 
        "04. Stack Cloud Architetturale", 
        "05. Dashboard Analitica Live", 
        "06. Webhook Router Endpoint", 
        "07. Bridge API CRM Pipeline"
    ])
    
    if modulo == "01. Normalizzazione CSV":
        st.markdown("<div class='status-online'>CORE SCRIPT OPERATIVO</div>", unsafe_allow_html=True)
        st.title("⚙️ Normalizzazione Dataset CSV")
        st.markdown("Eliminazione istantanea delle inefficienze causate dall'inserimento dati manuale.", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Innestare Database Grezzo (.csv)", type=["csv"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        if uploaded_file is not None:
            df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
            df_clean = df_raw.copy().drop_duplicates()
            if 'Email' in df_clean.columns:
                df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                df_clean = df_clean[~df_clean['Email'].isin(['nan', 'none', '', 'null'])].dropna(subset=['Email'])
            st.success("Analisi eseguita. Record normalizzati.")
            st.dataframe(df_clean.head(5), use_container_width=True)
            csv_pulito = df_clean.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Scarica Report Validato", data=csv_pulito, file_name="apex_output_clean.csv", mime="text/csv")
            
        st.markdown("### Codice Sorgente")
        codice_01 = "import pandas as pd\ndef clean(file):\n    return pd.read_csv(file).drop_duplicates()"
        st.code(codice_01, language="python")

    elif modulo == "02. Blindatura Protocollo .env":
        st.title("🔒 Blindatura Credenziali e Variabili Runtime")
        st.markdown("Protezione delle chiavi API aziendali tramite disaccoppiamento logico.")
        st.markdown("<div class='card'><h4>Standard Esecutivo</h4>1. Installa: python-dotenv<br>2. Isola le chiavi in un file occulto .env<br>3. Mura gli accessi inserendo il file nel tuo .gitignore</div>", unsafe_allow_html=True)
        codice_02 = "import os\nfrom dotenv import load_dotenv\nload_dotenv()\nkey = os.getenv('API_KEY')"
        st.code(codice_02, language="python")
        st.download_button("💾 Scarica Modulo Privato (.py)", data=codice_02, file_name="asset_02_env.py")

    elif modulo == "03. Estrattore Client Telegram":
        st.title("📡 Scraper Asincrono API Telegram")
        st.markdown("Estrazione lead in background dai canali dei competitor bypassando le limitazioni visive dell'applicazione.")
        st.warning("Per vincoli crittografici e protocolli OTP di sicurezza, questo applicativo richiede l'esecuzione in un kernel locale.")
        codice_03 = "from telethon.sync import TelegramClient\n# Inserire API_ID e API_HASH estratti da my.telegram.org\nclient = TelegramClient('session', api_id, api_hash)"
        st.code(codice_03, language="python")
        st.download_button("📥 Scarica Codice di Estrazione", data=codice_03, file_name="asset_03_telegram.py")

    elif modulo == "04. Stack Cloud Architetturale":
        st.title("🗺️ Mappa dei Microservizi a Costo Zero")
        st.markdown("Sostituzione sistematica dei software proprietari e centralizzazione dei flussi dati aziendali.")
        df_saas = pd.DataFrame({
            "Livello Architetturale": ["Edge & DNS", "Hosting UI", "Core Webhooks", "Database Relazionale", "Object Storage"],
            "Infrastruttura": ["Cloudflare WAF", "Vercel / Streamlit", "n8n Open Source", "Supabase PostgreSQL", "Cloudflare R2"],
            "Costo di Mantenimento": ["0€ - Free Tier", "0€ - Free Tier", "0€ - Self Hosted", "0€ - Serverless Tier", "0€ - Fino a 10GB"]
        })
        st.table(df_saas)

    elif modulo == "05. Dashboard Analitica Live":
        st.title("📊 Centro di Controllo Direzionale")
        st.markdown("Le metriche oggettive distruggono le giustificazioni in sala riunioni.")
        col1, col2 = st.columns(2)
        col1.metric(label="MRR Global Network", value="€ 42.500", delta="+12.4%")
        col2.metric(label="Server Response Latenza", value="4.2 ms", delta="-0.8 ms", delta_color="inverse")
        
        df_chart = pd.DataFrame({'Dipartimento': ['Sales', 'Marketing', 'Infrastructure'], 'Cassa': [85000, -22000, 45000]})
        fig = px.bar(df_chart, x='Dipartimento', y='Cassa', color='Cassa', color_continuous_scale=['#EF4444', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig, use_container_width=True)

    elif modulo == "06. Webhook Router Endpoint":
        st.title("🔀 Router Asincrono delle Notifiche")
        st.markdown("Filtro logico dei payload esterni: isolamento delle urgenze critiche e archiviazione passiva dei log.")
        codice_06 = "from fastapi import FastAPI\napp = FastAPI()\n@app.post('/webhook')\nasync def route(req: dict):\n    return {'status': 'processed'}"
        st.code(codice_06, language="python")
        st.download_button("📥 Scarica Webhook Server", data=codice_06, file_name="asset_06_webhook.py")

    elif modulo == "07. Bridge API CRM Pipeline":
        st.title("🔄 Iniezione Automatica Lead CRM")
        st.markdown("Interconnessione asincrona tra database isolati. Eliminazione dell'inserimento manuale.")
        nome = st.text_input("Ragione Sociale", "Inefficienza Corp S.p.A.")
        email = st.text_input("Email Decision Maker", "cto@inefficienza.com")
        if st.button("Forza Push Dati"):
            with st.spinner("[CONNECTING] Sincronizzazione in corso..."):
                time.sleep(1)
                st.success(f"Payload per {email} iniettato nella pipeline di vendita.")
        codice_07 = "import requests\nres = requests.post('https://httpbin.org/post', json={'email': 'target'})"
        st.code(codice_07, language="python")
        st.download_button("📥 Scarica Bridge API", data=codice_07, file_name="asset_07_bridge.py")

# ==========================================
# BRAND FLOW: SINTESIMENTALE
# ==========================================
elif asset_selezionato == "🧠 ASSET 01: SintesiMentale":
    st.title("🧠 SintesiMentale: Protocolli di Ottimizzazione Neurale")
    st.markdown("Sintesi asimmetriche ad alto valore informativo per l'arbitraggio dei mercati digitali.")
    st.markdown("""
    <div class='card'>
    <h3>📚 La Bibbia Faceless dell'Asset Empire (Manuale Completo)</h3>
    La risorsa strategica definitiva per l'edificazione, la gestione passiva e lo scaling finanziario di un impero multimediale faceless nel biennio 2026-2030.
    <br><br>
    <a href="https://gumroad.com" target="_blank" style="text-decoration: none;">
        <button style="background-color: #10B981; color: #0A0D14; width: 100%; padding: 0.8rem; border: none; font-weight: bold; border-radius: 4px; cursor: pointer; text-transform: uppercase;">
            🔓 SBLOCCA L'EBOOK PREMIUM SU GUMROAD
        </button>
    </a>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# BRAND FLOW: METODOESTETICO
# ==========================================
elif asset_selezionato == "🎨 ASSET 02: MetodoEstetico":
    st.title("🎨 MetodoEstetico: Ingegneria dell'Ordine Visivo")
    st.markdown("Sistemi organizzativi visivi standardizzati per l'azzeramento del caos operativo e del rumore mentale.")
    st.markdown("""
    <div class='card'>
    <h3>📅 Digital Executive Planner (Formato PDF Printable)</h3>
    Il framework minimalistico grigio antracite strutturato per il tracciamento scientifico del tempo, delle abitudini ad alto rendimento e del budget di capitale.
    <br><br>
    <a href="https://gumroad.com" target="_blank" style="text-decoration: none;">
        <button style="background-color: #10B981; color: #0A0D14; width: 100%; padding: 0.8rem; border: none; font-weight: bold; border-radius: 4px; cursor: pointer; text-transform: uppercase;">
            📥 SCARICA IL PLANNER MATRICE SU GUMROAD
        </button>
    </a>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# BRAND FLOW: RISORSAZERO
# ==========================================
elif asset_selezionato == "📁 ASSET 03: RisorsaZero":
    st.title("📁 RisorsaZero: Database degli Strumenti di Internet")
    st.markdown("Archivi strutturati di risorse occultate. Massimizzazione dell'efficienza temporale tramite la fruizione immediata di tool validati.")
    
    st.markdown("### ⚡ AI Toolkit Privato (50 Tool Gratuiti Selezionati)")
    data_toolkit = {
        "Categoria Architetturale": ["Ingegneria Prompt", "Sintesi Vocale", "Generazione Video", "Automazione API", "Storage Object"],
        "Nome Strumento Unificato": ["Gemini Pro Advanced", "ElevenLabs Core Server", "CapCut Engine Desktop", "n8n Open Source Instance", "Cloudflare R2 Systems"],
        "Bypass Barriera Finanziaria": ["Free Tier Attivo", "10k Caratteri / Mese", "Export 4K Gratuito", "Illimitato Self-Hosted", "10GB Gratuite Zero Friction"]
    }
    df_toolkit = pd.DataFrame(data_toolkit)
    st.dataframe(df_toolkit, use_container_width=True, hide_index=True)
    
    csv_toolkit = df_toolkit.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Esporta l'intero Database (.csv)", data=csv_toolkit, file_name="risorsazero_toolkit.csv", mime="text/csv")
