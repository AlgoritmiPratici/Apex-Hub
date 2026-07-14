import streamlit as st
import pandas as pd
import time
import requests
import plotly.express as px

# ==========================================
# 1. CONFIGURAZIONE E ROUTING
# ==========================================
st.set_page_config(
    page_title="APEX & ZERO HUB", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# Routing tramite URL (es: ?hub=tech oppure ?hub=zero)
hub_richiesto = st.query_params.get("hub", "tech")
index_default = 0 if hub_richiesto == "tech" else 1

# ==========================================
# 2. INIEZIONE CSS MINIMALE (PULIZIA)
# ==========================================
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div.stDeployButton {visibility: hidden;}
    
    .highlight { color: #10B981; font-weight: bold; }
    .card { background-color: #111622; padding: 1.5rem; border-radius: 8px; border: 1px solid #222C3A; margin-bottom: 1rem; }
    
    div.stButton > button {
        background-color: #10B981 !important; color: #0A0D14 !important; font-weight: bold !important; width: 100% !important;
    }
    div.stDownloadButton > button {
        background-color: #1E293B !important; color: #E2E8F0 !important; font-weight: bold !important; width: 100% !important; border: 1px solid #334155 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. NAVIGAZIONE SIDEBAR
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: #E2E8F0;'>MODULI ESECUTIVI</h2>", unsafe_allow_html=True)
scelta_hub = st.sidebar.radio("Seleziona Ecosistema:", ["📌 Asset 00: AlgoritmiPratici", "📁 Asset 03: RisorsaZero"], index=index_default)
st.sidebar.markdown("---")

# ==========================================
# ECOSISTEMA: ALGORITMIPRATICI (ASSET 00)
# ==========================================
if scelta_hub == "📌 Asset 00: AlgoritmiPratici":
    modulo = st.sidebar.selectbox("Strumenti Tech B2B:", [
        "01. Normalizzazione CSV", "02. Sicurezza .env", "03. Estrattore Telegram", 
        "04. Matrice Cloud", "05. Dashboard Live", "06. Webhook Router", "07. Sync CRM"
    ])
    
    if modulo == "01. Normalizzazione CSV":
        st.title("⚙️ Motore di Normalizzazione Dataset")
        st.markdown("Pulisci i tuoi fogli di calcolo in millisecondi.")
        uploaded_file = st.file_uploader("Carica il tuo file CSV grezzo", type=["csv"])
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
            df_clean = df.drop_duplicates()
            if 'Email' in df_clean.columns:
                df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                df_clean = df_clean.dropna(subset=['Email'])
            
            st.success("✅ Dataset ottimizzato.")
            st.dataframe(df_clean.head(5), use_container_width=True)
            st.download_button("📥 Scarica CSV Pulito", df_clean.to_csv(index=False).encode('utf-8'), "dati_puliti.csv", "text/csv")

    elif modulo == "02. Sicurezza .env":
        st.title("🔒 Protocollo .env")
        st.markdown("Isola le credenziali dal codice sorgente.")
        st.code("import os\nfrom dotenv import load_dotenv\nload_dotenv()\nAPI_KEY = os.getenv('API_KEY')", language="python")

    elif modulo == "03. Estrattore Telegram":
        st.title("📡 Scraper API Telegram")
        st.markdown("Estrazione lead asincrona via Telethon (Esecuzione in locale richiesta per OTP).")
        st.code("from telethon.sync import TelegramClient\n# Usa le credenziali da my.telegram.org\nwith TelegramClient('session', API_ID, API_HASH) as client:\n    pass", language="python")

    elif modulo == "04. Matrice Cloud":
        st.title("🗺️ Stack Backend a Costo Zero")
        df_stack = pd.DataFrame({"Livello": ["WAF/DNS", "UI", "Automazione", "Database"], "Tool": ["Cloudflare", "Streamlit", "n8n", "Supabase"]})
        st.table(df_stack)

    elif modulo == "05. Dashboard Live":
        st.title("📊 Financial Core")
        col1, col2 = st.columns(2)
        col1.metric("Revenue", "€ 42.500", "+12.4%")
        col2.metric("Latenza", "4.2 ms", "-0.8 ms", delta_color="inverse")
        df_chart = pd.DataFrame({'Reparto': ['Sales', 'Marketing', 'IT'], 'Cassa': [85000, -22000, 45000]})
        fig = px.bar(df_chart, x='Reparto', y='Cassa', color='Cassa', color_continuous_scale=['#EF4444', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig, use_container_width=True)

    elif modulo == "06. Webhook Router":
        st.title("🔀 Router Notifiche API")
        st.code("from fastapi import FastAPI\napp = FastAPI()\n@app.post('/webhook')\nasync def route(req: dict): return {'status': 'ok'}", language="python")

    elif modulo == "07. Sync CRM":
        st.title("🔄 Test Iniezione CRM")
        st.markdown("Simula l'invio asincrono di dati verso un endpoint.")
        if st.button("Simula Push Dati"):
            with st.spinner("Connessione API..."):
                time.sleep(1)
                st.success("Payload inviato con latenza < 1.2s.")

# ==========================================
# ECOSISTEMA: RISORSAZERO (ASSET 03)
# ==========================================
elif scelta_hub == "📁 Asset 03: RisorsaZero":
    st.title("⚡ AI Toolkit Database (Top 50)")
    st.markdown("Perché perdere 100 ore a cercare tool quando l'abbiamo già fatto noi? Filtra, copia o scarica l'archivio.")
    
    # Dati simulati del tuo database (puoi espanderlo qui o leggere da un file locale in futuro)
    dati_ai = [
        {"Categoria": "Generazione Video", "Tool": "CapCut Pro", "Modello Finanziario": "Freemium", "Link": "capcut.com"},
        {"Categoria": "Sintesi Vocale", "Tool": "ElevenLabs", "Modello Finanziario": "10k Caratteri Gratis", "Link": "elevenlabs.io"},
        {"Categoria": "Prompting", "Tool": "Gemini Advanced", "Modello Finanziario": "Abbonamento / Free Tier", "Link": "gemini.google.com"},
        {"Categoria": "Automazione", "Tool": "n8n", "Modello Finanziario": "Open Source / 0€", "Link": "n8n.io"},
        {"Categoria": "Database", "Tool": "Supabase", "Modello Finanziario": "Serverless Free Tier", "Link": "supabase.com"}
    ]
    df_tools = pd.DataFrame(dati_ai)
    
    # Motore di ricerca interno
    ricerca = st.text_input("🔍 Cerca per categoria, tool o modello (es: Video, Gratis, Open Source)...")
    
    if ricerca:
        # Filtra il dataframe basato sulla ricerca in qualsiasi colonna
        mask = df_tools.apply(lambda row: row.astype(str).str.contains(ricerca, case=False).any(), axis=1)
        df_filtrato = df_tools[mask]
    else:
        df_filtrato = df_tools
        
    st.dataframe(df_filtrato, use_container_width=True, hide_index=True)
    
    # Export del file pulito
    csv_tools = df_tools.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Scarica Database Integrale (.csv)", data=csv_tools, file_name="risorsazero_toolkit.csv", mime="text/csv")
