import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# ==========================================
# 1. CONFIGURAZIONE E ROUTING INVISIBILE
# ==========================================
st.set_page_config(
    page_title="APEX Global Infrastructure", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# Estrazione dinamica del brand. Se l'utente arriva da RisorsaZero, NON DEVE VEDERE AlgoritmiPratici.
query_params = st.query_params
target_brand = query_params.get("target", "AlgoritmiPratici")

# ==========================================
# 2. INIEZIONE CSS MICRO-ESTETICA (PREMIUM)
# ==========================================
st.markdown("""
    <style>
    /* Rimozione Branding Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div.stDeployButton {visibility: hidden;}
    
    /* Tipografia e Spaziature Premium */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Titoli Massicci e Puliti */
    h1 { font-weight: 800 !important; letter-spacing: -0.05em; margin-bottom: 1.5rem !important; }
    h2, h3 { font-weight: 700 !important; letter-spacing: -0.03em; }
    .highlight { color: #10B981 !important; font-weight: 700; }
    
    /* Card Glassmorphism */
    .card {
        background: rgba(17, 22, 34, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 1.8rem;
        border-radius: 8px;
        border: 1px solid rgba(226, 232, 240, 0.05);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Pulsanti Ingegnerizzati */
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: #0A0D14 !important;
        font-weight: 800 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.6rem 0 !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);
    }
    
    /* Fix Blocchi Codice per renderli asettici */
    div[data-testid="stCodeBlock"] {
        border-radius: 6px;
        border: 1px solid rgba(226, 232, 240, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. ROUTING ISOLATO (EVITA LA CONTAMINAZIONE)
# ==========================================
# Sezione: AlgoritmiPratici
if target_brand == "AlgoritmiPratici":
    st.sidebar.markdown("<div style='color: #10B981; font-weight:800; font-size:1.2rem; text-align:center;'>APEX CORE</div>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    modulo = st.sidebar.radio("MODULI OPERATIVI:", [
        "01. Normalizzazione CSV", "02. Blindatura .env", "03. Estrattore Telegram", 
        "04. Matrice Cloud", "05. Dashboard Analitica", "06. Webhook Router", "07. Iniezione CRM"
    ])
    
    if modulo == "01. Normalizzazione CSV":
        st.title("⚙️ Normalizzazione Dataset CSV")
        st.markdown("<div class='card'>Innestare il database grezzo. Gli algoritmi elimineranno le ridondanze in <b>3 millisecondi</b>.</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Carica File (.csv)", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file, sep=None, engine='python').drop_duplicates()
            if 'Email' in df.columns:
                df['Email'] = df['Email'].astype(str).str.lower().str.strip()
                df = df[~df['Email'].isin(['nan', 'none', '', 'null'])].dropna(subset=['Email'])
            st.success("Validazione completata.")
            st.dataframe(df.head(3), use_container_width=True)
            st.download_button("📥 Scarica Dataset Validato", df.to_csv(index=False).encode('utf-8'), "apex_output.csv", "text/csv")
        st.markdown("### Codice Sorgente")
        st.code("import pandas as pd\ndef clean(file):\n    return pd.read_csv(file).drop_duplicates()", language="python")

    elif modulo == "05. Dashboard Analitica":
        st.title("📊 Centro di Controllo")
        col1, col2 = st.columns(2)
        col1.metric("MRR Ecosistema", "€ 42.500", "+12.4%")
        col2.metric("Latenza Endpoint", "4.2 ms", "-0.8 ms", delta_color="inverse")
        df_chart = pd.DataFrame({'Dipartimento': ['Sales', 'Marketing', 'IT'], 'Cassa YTD': [85000, -22000, 45000]})
        fig = px.bar(df_chart, x='Dipartimento', y='Cassa YTD', color='Cassa YTD', color_continuous_scale=['#EF4444', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.title("Infrastruttura Offline")
        st.info("I moduli selezionati sono in fase di aggiornamento crittografico. Riprovare a breve.")

# Sezione: SintesiMentale
elif target_brand == "SintesiMentale":
    st.sidebar.markdown("<div style='color: #A855F7; font-weight:800; font-size:1.2rem; text-align:center;'>SINTESIMENTALE</div>", unsafe_allow_html=True)
    st.title("🧠 Protocolli di Ottimizzazione Neurale")
    st.markdown("<div class='card'><h3>La Bibbia Faceless dell'Asset Empire</h3>La risorsa strategica definitiva per l'edificazione e lo scaling di un impero multimediale.<br><br><a href='https://tuo-link-gumroad.com'><button style='background:#A855F7; color:white; width:100%; padding:0.8rem; border:none; font-weight:bold; border-radius:4px;'>🔓 SBLOCCA L'EBOOK SU GUMROAD</button></a></div>", unsafe_allow_html=True)

# Sezione: MetodoEstetico
elif target_brand == "MetodoEstetico":
    st.sidebar.markdown("<div style='color: #F97316; font-weight:800; font-size:1.2rem; text-align:center;'>METODOESTETICO</div>", unsafe_allow_html=True)
    st.title("🎨 Ingegneria dell'Ordine Visivo")
    st.markdown("<div class='card'><h3>Digital Executive Planner</h3>Il framework minimalistico per il tracciamento scientifico del tempo e delle abitudini.<br><br><a href='https://tuo-link-gumroad.com'><button style='background:#F97316; color:white; width:100%; padding:0.8rem; border:none; font-weight:bold; border-radius:4px;'>📥 SCARICA IL PLANNER SU GUMROAD</button></a></div>", unsafe_allow_html=True)

# Sezione: RisorsaZero
elif target_brand == "RisorsaZero":
    st.sidebar.markdown("<div style='color: #3B82F6; font-weight:800; font-size:1.2rem; text-align:center;'>RISORSAZERO</div>", unsafe_allow_html=True)
    st.title("📁 Database Segreto di Internet")
    st.markdown("### ⚡ AI Toolkit Privato (50 Tool Gratuiti Selezionati)")
    df_toolkit = pd.DataFrame({"Categoria": ["Prompting", "Sintesi Vocale", "Video"], "Strumento": ["Gemini Advanced", "ElevenLabs", "CapCut Pro"], "Bypass": ["Free Tier", "10k Caratteri", "Export 4K"]})
    st.dataframe(df_toolkit, use_container_width=True, hide_index=True)
    st.download_button("📥 Esporta Archivio Completo (.csv)", df_toolkit.to_csv(index=False).encode('utf-8'), "risorsazero_toolkit.csv", "text/csv")
