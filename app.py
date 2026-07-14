import streamlit as st
import pandas as pd
import time
import plotly.express as px

# ==========================================
# 1. CONFIGURAZIONE ARCHITETTURALE
# ==========================================
# DEVE essere la prima riga del codice.
st.set_page_config(
    page_title="APEX & ZERO HUB", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# Inizializzazione della Memoria di Stato (Session State) per evitare reset anomali
if 'dati_puliti' not in st.session_state:
    st.session_state.dati_puliti = None
if 'lead_acquisito' not in st.session_state:
    st.session_state.lead_acquisito = False

# Rimozione SOLO del watermark di Streamlit. Manteniamo l'header per il mobile.
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. ROUTING E NAVIGAZIONE
# ==========================================
hub_richiesto = st.query_params.get("hub", "tech")
index_default = 0 if hub_richiesto == "tech" else 1

st.sidebar.markdown("<h3 style='text-align: center; color: #10B981;'>MODULI ESECUTIVI</h3>", unsafe_allow_html=True)
scelta_hub = st.sidebar.radio("SELEZIONA ECOSISTEMA:", ["📌 Asset 00: AlgoritmiPratici", "📁 Asset 03: RisorsaZero"], index=index_default)
st.sidebar.markdown("---")

# ==========================================
# ECOSISTEMA: ALGORITMIPRATICI (ASSET 00)
# ==========================================
if scelta_hub == "📌 Asset 00: AlgoritmiPratici":
    modulo = st.sidebar.selectbox("PIPELINE OPERATIVA:", [
        "01. Normalizzazione CSV", "02. Sicurezza .env", "03. Estrattore Telegram", 
        "04. Matrice Cloud", "05. Dashboard Live", "06. Webhook Router", "07. Sync CRM"
    ])
    
    if modulo == "01. Normalizzazione CSV":
        st.title("⚙️ Motore di Normalizzazione Dataset")
        st.write("Inserisci il dump dei dati grezzi. Algoritmo di pulizia e de-duplicazione asincrona in tempo reale.")
        
        uploaded_file = st.file_uploader("Innestare file .csv", type=["csv"])
        
        if uploaded_file:
            # Calcolo e storaggio nello stato per evitare reset
            df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
            df_clean = df_raw.copy().drop_duplicates()
            if 'Email' in df_clean.columns:
                df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                df_clean = df_clean[~df_clean['Email'].isin(['nan', 'none', '', 'null'])].dropna(subset=['Email'])
            
            st.session_state.dati_puliti = df_clean
            
        if st.session_state.dati_puliti is not None:
            st.success("✅ Struttura validata e ottimizzata.")
            st.dataframe(st.session_state.dati_puliti.head(5), use_container_width=True)
            
            csv_export = st.session_state.dati_puliti.to_csv(index=False).encode('utf-8')
            st.download_button("📥 SCARICA DATASET PULITO", csv_export, "apex_dati_puliti.csv", "text/csv", type="primary")
            
        st.markdown("---")
        st.markdown("**Codice Sorgente dell'Algoritmo:**")
        st.code("import pandas as pd\ndef clean(file):\n    df = pd.read_csv(file).drop_duplicates()\n    return df.dropna(subset=['Email'])", language="python")

    elif modulo == "02. Sicurezza .env":
        st.title("🔒 Protocollo .env")
        st.markdown("Isola le credenziali dal codice sorgente per prevenire data breach aziendali.")
        st.code("import os\nfrom dotenv import load_dotenv\n\nload_dotenv()\nAPI_KEY = os.getenv('API_KEY')\nif not API_KEY:\n    raise SystemExit('Credenziali assenti.')", language="python")

    elif modulo == "03. Estrattore Telegram":
        st.title("📡 Scraper API Telegram")
        st.markdown("Estrazione lead in background via Telethon (Esecuzione in locale richiesta per OTP).")
        st.code("from telethon.sync import TelegramClient\n# Usa le credenziali da my.telegram.org\nwith TelegramClient('session', API_ID, API_HASH) as client:\n    utenti = client.get_participants('target_group')", language="python")

    elif modulo == "04. Matrice Cloud":
        st.title("🗺️ Stack Backend a Costo Zero")
        df_stack = pd.DataFrame({"Livello Architetturale": ["WAF/DNS", "Hosting UI", "Automazione", "Database"], "Soluzione Zero-Cost": ["Cloudflare", "Streamlit Cloud", "n8n Self-Hosted", "Supabase Serverless"]})
        st.table(df_stack)

    elif modulo == "05. Dashboard Live":
        st.title("📊 Financial Core Dashboard")
        col1, col2 = st.columns(2)
        col1.metric("Revenue Ecosistema", "€ 42.500", "+12.4%")
        col2.metric("Latenza Endpoint", "4.2 ms", "-0.8 ms", delta_color="inverse")
        df_chart = pd.DataFrame({'Reparto': ['Sales', 'Marketing', 'Infrastruttura IT'], 'Cassa Operativa': [85000, -22000, 45000]})
        fig = px.bar(df_chart, x='Reparto', y='Cassa Operativa', color='Cassa Operativa', color_continuous_scale=['#EF4444', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig, use_container_width=True)

    elif modulo == "06. Webhook Router":
        st.title("🔀 Router Notifiche API")
        st.markdown("Filtro asincrono per eliminare il rumore operativo e inoltrare solo i payload critici.")
        st.code("from fastapi import FastAPI\napp = FastAPI()\n@app.post('/webhook')\nasync def route(req: dict):\n    return {'status': '200 OK'}", language="python")

    elif modulo == "07. Sync CRM":
        st.title("🔄 Iniezione CRM Asincrona")
        st.markdown("Simula il push di dati verso un endpoint REST esterno.")
        if st.button("ESEGUI PUSH DATI", type="primary"):
            with st.spinner("Negoziazione protocollo di rete..."):
                time.sleep(1)
                st.success("Payload inviato con successo. Latenza: 0.9s.")

# ==========================================
# ECOSISTEMA: RISORSAZERO (ASSET 03)
# ==========================================
elif scelta_hub == "📁 Asset 03: RisorsaZero":
    st.title("⚡ Database AI Toolkit (Top 50)")
    st.write("Filtra il database in tempo reale. Inserisci la tua email per sbloccare il download dell'intero archivio CSV.")
    
    dati_ai = [
        {"Categoria": "Video Generation", "Tool": "CapCut Pro", "Costo": "Freemium", "Vantaggio": "Export 4K"},
        {"Categoria": "Sintesi Vocale", "Tool": "ElevenLabs", "Costo": "Gratis 10k/Mese", "Vantaggio": "Voci ultra-realistiche"},
        {"Categoria": "Prompting", "Tool": "Gemini Advanced", "Costo": "Abbonamento", "Vantaggio": "Finestra di contesto enorme"},
        {"Categoria": "Automazione API", "Tool": "n8n", "Costo": "0€ (Self Hosted)", "Vantaggio": "Nessun limite di task"},
        {"Categoria": "Database SQL", "Tool": "Supabase", "Costo": "Free Tier", "Vantaggio": "Sostituisce Firebase"}
    ]
    df_tools = pd.DataFrame(dati_ai)
    
    # Ricerca Live
    ricerca = st.text_input("🔍 Cerca per categoria, nome o costo (es: Video, Gratis)...")
    if ricerca:
        mask = df_tools.apply(lambda row: row.astype(str).str.contains(ricerca, case=False).any(), axis=1)
        df_filtrato = df_tools[mask]
    else:
        df_filtrato = df_tools
        
    st.dataframe(df_filtrato, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # LEAD GENERATION GATE (Il vero valore dell'Asset 03)
    if not st.session_state.lead_acquisito:
        st.markdown("### 🔓 Sblocca l'esportazione")
        st.write("Ottieni il file .csv completo per integrarlo nei tuoi flussi di lavoro.")
        email_lead = st.text_input("Inserisci la tua email aziendale/principale:")
        
        if st.button("Sblocca Download", type="primary"):
            if "@" in email_lead and "." in email_lead:
                # In una versione futura, qui invierai l'email al tuo CRM (Make.com/n8n)
                st.session_state.lead_acquisito = True
                st.rerun()
            else:
                st.error("Inserisci un indirizzo email valido.")
    
    if st.session_state.lead_acquisito:
        st.success("Accesso sbloccato. Salva il file qui sotto.")
        csv_tools = df_tools.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 SCARICA DATABASE (.csv)", data=csv_tools, file_name="risorsazero_toolkit.csv", mime="text/csv", type="primary")
