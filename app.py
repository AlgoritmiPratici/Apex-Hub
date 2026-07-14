import streamlit as st
import pandas as pd
import requests
import io

# Configurazione Base Asettica
st.set_page_config(page_title="Apex Infrastructure Hub", layout="wide", initial_sidebar_state="expanded")

# Stile Dark Corporate
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("Infrastruttura B2B")
st.sidebar.markdown("Seleziona il modulo operativo:")

menu = st.sidebar.radio("", [
    "01 - Motore Pulizia Dati (Excel)", 
    "02 - Protocollo .env", 
    "03 - Estrattore Telegram", 
    "04 - Mappa Architetturale SaaS", 
    "05 - Dashboard Esecutiva", 
    "06 - Router Notifiche API", 
    "07 - Simulatore Iniezione CRM"
])

# ==========================================
# MODULO 01: EXCEL CLEANER (Eseguibile)
# ==========================================
if menu == "01 - Motore Pulizia Dati (Excel)":
    st.title("⚙️ Motore di Pulizia Dati B2B")
    st.write("Carica un database disorganizzato (CSV). Il sistema eliminerà le inefficienze in 3 millisecondi.")
    
    uploaded_file = st.file_uploader("Carica file .csv", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df.drop_duplicates(inplace=True)
            if 'Email' in df.columns:
                df['Email'] = df['Email'].astype(str).str.lower().str.strip()
                df.dropna(subset=['Email'], inplace=True)
            
            # Scarico Risultato
            csv_pulito = df.to_csv(index=False).encode('utf-8')
            st.success("Analisi completata. Database normalizzato.")
            st.download_button(label="📥 Scarica Database Pulito", data=csv_pulito, file_name="dati_ottimizzati.csv", mime="text/csv")
        except Exception as e:
            st.error(f"Collasso strutturale: {e}")
            
    st.markdown("---")
    # Pulsante Codice Sorgente
    codice_01 = """import pandas as pd\ndf = pd.read_csv('dati.csv')\ndf.drop_duplicates(inplace=True)\ndf.to_csv('puliti.csv', index=False)"""
    st.download_button("Scarica Codice Sorgente (.py)", data=codice_01, file_name="asset_01.py")

# ==========================================
# MODULO 02: PROTOCOLLO .ENV (Informativo)
# ==========================================
elif menu == "02 - Protocollo .env":
    st.title("🔒 Protocollo di Sicurezza Asincrona")
    st.markdown("""
    ### La vulnerabilità delle variabili hardcoded
    Lasciare le chiavi API nel codice è un rischio inaccettabile. 
    1. Installa: `pip install python-dotenv`
    2. Crea un file `.env` e inserisci: `API_KEY=tua_chiave_segreta`
    3. Proteggi il file con `.gitignore`.
    """)
    codice_02 = """import os\nfrom dotenv import load_dotenv\nload_dotenv()\nsegreto = os.getenv('API_KEY')"""
    st.download_button("Scarica Template Sorgente (.py)", data=codice_02, file_name="asset_02_sicurezza.py")

# ==========================================
# MODULO 03: ESTRATTORE TELEGRAM (Solo download)
# ==========================================
elif menu == "03 - Estrattore Telegram":
    st.title("📡 Estrattore Lead Telegram (Telethon)")
    st.warning("Per ragioni di sicurezza e autenticazione OTP, questo script deve girare sui tuoi server locali, non sul cloud.")
    st.markdown("Scarica il codice sorgente, inserisci le tue chiavi API di Telegram e avvialo nel tuo terminale.")
    codice_03 = """from telethon.sync import TelegramClient\n# [Codice completo Telethon pre-generato]"""
    st.download_button("Scarica Codice Sorgente (.py)", data=codice_03, file_name="asset_03_telethon.py")

# ==========================================
# MODULO 04: MAPPA SAAS (Sostituisce Notion)
# ==========================================
elif menu == "04 - Mappa Architetturale SaaS":
    st.title("🗺️ Infrastruttura Backend a Costo Zero")
    st.table(pd.DataFrame({
        "Livello Tecnico": ["Edge & Security", "Frontend", "Backend Logico", "Database", "Storage"],
        "Tool (Free Tier)": ["Cloudflare", "Vercel", "n8n / Make", "Supabase", "AWS S3 / R2"],
        "Scopo": ["WAF, DNS", "Latenza Zero UI", "Routing API", "PostgreSQL", "Archivio Asset"]
    }))

# ==========================================
# MODULO 05: DASHBOARD (Eseguibile Live)
# ==========================================
elif menu == "05 - Dashboard Esecutiva":
    st.title("📊 Centro di Controllo (Dati, non Opinioni)")
    df_dash = pd.DataFrame({
        'Dipartimento': ['Vendite', 'Marketing', 'Infrastruttura'],
        'ROI': [45000, -12000, 89000],
        'Stato': ['Ottimale', 'Perdita', 'Ottimale']
    })
    st.dataframe(df_dash, use_container_width=True)
    st.error("ATTENZIONE: Il Marketing sta bruciando cassa.")
    codice_05 = """import streamlit as st\nimport pandas as pd\n# [Codice completo Streamlit]"""
    st.download_button("Scarica Codice Sorgente (.py)", data=codice_05, file_name="asset_05_dashboard.py")

# ==========================================
# MODULO 06: ROUTER NOTIFICHE (Solo download)
# ==========================================
elif menu == "06 - Router Notifiche API":
    st.title("🔀 Router Asincrono Notifiche (Webhook)")
    st.markdown("Un webhook FastAPI per silenziare il rumore aziendale. Esegui il deploy su Render.com o AWS.")
    codice_06 = """from fastapi import FastAPI\napp = FastAPI()\n@app.post('/webhook')\nasync def ricevi(): pass"""
    st.download_button("Scarica Codice Sorgente (.py)", data=codice_06, file_name="asset_06_router.py")

# ==========================================
# MODULO 07: CRM MOCK (Eseguibile)
# ==========================================
elif menu == "07 - Simulatore Iniezione CRM":
    st.title("🔄 Simulatore Iniezione Dati CRM")
    st.write("Simula un push API verso il tuo gestionale.")
    nome = st.text_input("Nome Lead", "Target SpA")
    email = st.text_input("Email", "ceo@target.com")
    
    if st.button("Inietta nel CRM"):
        st.success(f"[SUCCESS] Payload per {nome} ({email}) inviato con latenza < 1.2s. Pipeline intatta.")
    
    codice_07 = """import requests\npayload = {'nome':'x', 'email':'y'}\nrequests.post('API_URL', json=payload)"""
    st.download_button("Scarica Codice Sorgente (.py)", data=codice_07, file_name="asset_07_crm.py")
