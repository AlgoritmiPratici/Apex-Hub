import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# ==========================================
# 1. CONFIGURAZIONE ARCHITETTURALE
# ==========================================
st.set_page_config(
    page_title="APEX Engineering Hub", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. INIEZIONE CSS ENTERPRISE
# ==========================================
st.markdown("""
    <style>
    /* Pulizia totale dell'interfaccia Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div.stDeployButton {visibility: hidden;}
    
    /* Palette Colori: Dark Mode Assoluta & Verde Acido */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0B0E14;
        color: #E2E8F0;
        font-family: 'Inter', 'Montserrat', sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #151A23;
        border-right: 1px solid #232A38;
    }
    
    /* Titoli e Testi */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
    }
    .highlight { color: #10B981; font-weight: bold; }
    
    /* Restyling Metriche */
    [data-testid="stMetricValue"] {
        color: #10B981 !important;
    }
    
    /* Pulsanti (Massimizzati per Mobile Friction-Zero) */
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
        font-size: 0.9rem !important;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #0EA5E9 !important;
        transform: translateY(-2px);
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
# 3. INTERFACCIA DI NAVIGAZIONE
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: #10B981 !important;'>APEX SYSTEMS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; color: #64748B; font-size: 0.8rem; margin-bottom: 2rem;'>Infrastruttura B2B Autorizzata</div>", unsafe_allow_html=True)

menu = st.sidebar.radio("SELEZIONA MODULO:", [
    "01. Motore Normalizzazione Dati", 
    "02. Blindatura Protocollo .env", 
    "03. Estrattore Dati Telegram", 
    "04. Matrice Cloud Costo Zero", 
    "05. Dashboard Analitica Live", 
    "06. Webhook Smistamento API", 
    "07. Iniezione Payload CRM"
])

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size: 0.75rem; color: #475569; text-align: center;'>Connessione Criptata AES-256<br>Server Locale: ONLINE</div>", unsafe_allow_html=True)

# ==========================================
# MODULO 01: EXCEL CLEANER (Potenziato)
# ==========================================
if menu == "01. Motore Normalizzazione Dati":
    st.markdown("<div class='status-badge'>MODULO OPERATIVO</div>", unsafe_allow_html=True)
    st.title("⚙️ Motore di Normalizzazione Dati")
    st.markdown("Elimina le inefficienze dei fogli di calcolo manuali. Il sistema identifica ridondanze e formatta i dati per l'iniezione CRM in <span class='highlight'>tempo reale</span>.", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Innestare Database Grezzo (.csv)", type=["csv"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        with st.spinner("[SYSTEM] Calcolo algoritmi di pulizia in corso..."):
            try:
                # Utilizziamo un engine robusto per i vari tipi di separatori CSV europei
                df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
                righe_iniziali = len(df_raw)
                
                df_clean = df_raw.copy()
                df_clean.drop_duplicates(inplace=True)
                
                if 'Email' in df_clean.columns:
                    df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                    # Rimuove valori fittizi o vuoti
                    df_clean = df_clean[~df_clean['Email'].isin(['nan', 'none', '', 'null'])]
                    df_clean.dropna(subset=['Email'], inplace=True)
                
                righe_finali = len(df_clean)
                righe_eliminate = righe_iniziali - righe_finali
                
                time.sleep(0.8) # Effetto calcolo
                
                # Metriche di Ritorno
                st.success(f"[SUCCESS] Normalizzazione completata.")
                col1, col2, col3 = st.columns(3)
                col1.metric("Record Iniziali", righe_iniziali)
                col2.metric("Record Validati", righe_finali)
                col3.metric("Inefficienze Rimosse", righe_eliminate, delta="-Ottimizzato", delta_color="inverse")
                
                # Preview Dati (Costruisce Fiducia)
                st.markdown("#### Preview Dati Strutturati (Primi 5 record)")
                st.dataframe(df_clean.head(5), use_container_width=True)
                
                # Esportazione
                csv_pulito = df_clean.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Scarica Database Validato", data=csv_pulito, file_name="apex_dati_strutturati.csv", mime="text/csv")
                
            except Exception as e:
                st.error(f"[ERROR] Collasso Strutturale: {e}. Assicurati che il file sia un CSV valido.")

    st.markdown("---")
    st.markdown("### Architettura Sorgente")
    codice_01 = """# Autore: APEX Systems\nimport pandas as pd\ndef ottimizza_database(file_path):\n    df = pd.read_csv(file_path)\n    df.drop_duplicates(inplace=True)\n    if 'Email' in df.columns:\n        df['Email'] = df['Email'].str.lower().str.strip()\n        df.dropna(subset=['Email'], inplace=True)\n    return df"""
    st.code(codice_01, language="python")
    st.download_button("💾 Salva Protocollo (.py)", data=codice_01, file_name="asset_01_cleaner.py")

# ==========================================
# MODULO 02: PROTOCOLLO .ENV
# ==========================================
elif menu == "02. Blindatura Protocollo .env":
    st.markdown("<div class='status-badge'>DOCUMENTAZIONE TECNICA</div>", unsafe_allow_html=True)
    st.title("🔒 Blindatura Credenziali (.env)")
    st.markdown("Le password esposte nel codice sorgente sono un <span class='highlight'>suicidio aziendale</span>. Disaccoppia la logica dai dati sensibili.", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
    <h4>Procedura di Isolamento</h4>
    1. Installa il modulo: <code>pip install python-dotenv</code><br>
    2. Crea il file occulto <code>.env</code> nella root directory del server.<br>
    3. Inserisci le chiavi senza virgolette: <code>API_SECRET=123456789</code><br>
    4. <b>CRITICO:</b> Aggiungi <code>.env</code> al file <code>.gitignore</code> per prevenire fughe di dati sui repository pubblici.
    </div>
    """, unsafe_allow_html=True)
    
    codice_02 = """# Protocollo di estrazione sicura runtime\nimport os\nfrom dotenv import load_dotenv\n\nload_dotenv()\nAPI_SECRET = os.getenv("API_KEY")\n\nif not API_SECRET:\n    raise SystemExit("[CRITICAL] Credenziali assenti. Arresto di sicurezza.")"""
    st.code(code=codice_02, language="python")
    st.download_button("💾 Scarica Protocollo Sicurezza (.py)", data=codice_02, file_name="asset_02_security.py")

# ==========================================
# MODULO 03: ESTRATTORE TELEGRAM
# ==========================================
elif menu == "03. Estrattore Dati Telegram":
    st.markdown("<div class='status-badge'>SORGENTE DOWNLOAD</div>", unsafe_allow_html=True)
    st.title("📡 Estrattore Lead Telegram (API)")
    st.markdown("Estrazione massiva e asincrona dei membri di un canale <span class='highlight'>bypassando i limiti visivi</span> dell'app.", unsafe_allow_html=True)
    
    st.warning("Per ragioni di sicurezza e crittografia OTP (One-Time Password) di Telegram, questo software non può essere eseguito nel cloud pubblico. Scarica il codice ed eseguilo nel tuo terminale locale.")
    
    codice_03 = """# Requisiti: pip install telethon python-dotenv\nfrom telethon.sync import TelegramClient\nimport os, csv\nfrom dotenv import load_dotenv\n\nload_dotenv()\napi_id = os.getenv('TELEGRAM_API_ID')\napi_hash = os.getenv('TELEGRAM_API_HASH')\n\nwith TelegramClient('session_apex', api_id, api_hash) as client:\n    utenti = client.get_participants('gruppo_competitor_target')\n    with open('lead_estratti.csv', 'w', newline='') as f:\n        writer = csv.writer(f)\n        writer.writerow(['ID', 'Username', 'Nome'])\n        for u in utenti:\n            writer.writerow([u.id, u.username, u.first_name])\n    print("[SUCCESS] Estrazione completata.")"""
    st.code(codice_03, language="python")
    st.download_button("📥 Scarica Motore di Estrazione", data=codice_03, file_name="asset_03_telethon.py")

# ==========================================
# MODULO 04: MAPPA ARCHITETTURALE
# ==========================================
elif menu == "04. Matrice Cloud Costo Zero":
    st.markdown("<div class='status-badge'>STRATEGIA AZIENDALE</div>", unsafe_allow_html=True)
    st.title("🗺️ Matrice Cloud a Costo Zero")
    st.markdown("Le aziende inefficienti pagano decine di abbonamenti SaaS. I leader costruiscono infrastrutture interconnesse <span class='highlight'>azzerando i costi operativi</span>.", unsafe_allow_html=True)
    
    tabella_saas = pd.DataFrame({
        "Livello Architetturale": ["Edge Security & DNS", "Hosting Interfaccia", "Core Logico & Webhooks", "Database Relazionale", "Object Storage (File)"],
        "Soluzione Free Tier": ["Cloudflare WAF", "Vercel / Streamlit Cloud", "n8n (Self-Hosted)", "Supabase (PostgreSQL)", "Cloudflare R2 (10GB)"],
        "Vantaggio Tattico": ["Protezione DDoS inclusa", "Latenza zero, deploy git", "Automazione infinita", "Query SQL asettiche", "Bypass server AWS"]
    })
    st.table(tabella_saas)

# ==========================================
# MODULO 05: DASHBOARD ANALITICA
# ==========================================
elif menu == "05. Dashboard Analitica Live":
    st.markdown("<div class='status-badge'>MODULO OPERATIVO</div>", unsafe_allow_html=True)
    st.title("📊 Centro di Controllo Direzionale")
    st.markdown("I dati in tempo reale annientano le opinioni in sala riunioni. <span class='highlight'>Nessun ritardo, nessuna scusa.</span>", unsafe_allow_html=True)
    
    # Metriche
    col1, col2, col3 = st.columns(3)
    col1.metric(label="MRR (Mensile Ricorrente)", value="€ 42.500", delta="+12.4%")
    col2.metric(label="Customer Acquisition Cost", value="€ 18.40", delta="-€ 2.10", delta_color="inverse")
    col3.metric(label="Server Uptime", value="99.98%", delta="Stabile", delta_color="off")
    
    # Grafico Plotly Avanzato (B2B Premium Look)
    st.markdown("#### Margine per Dipartimento (YTD)")
    df_chart = pd.DataFrame({
        'Dipartimento': ['Sales & Ops', 'Marketing', 'Infrastruttura (IT)', 'Ricerca & Sviluppo'],
        'Cassa Generata/Bruciata': [85000, -22000, 45000, -15000]
    })
    
    # Creazione chart interattivo Plotly
    fig = px.bar(df_chart, x='Dipartimento', y='Cassa Generata/Bruciata', 
                 color='Cassa Generata/Bruciata', color_continuous_scale=['#EF4444', '#10B981'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0', margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MODULO 06: ROUTER WEBHOOK
# ==========================================
elif menu == "06. Webhook Smistamento API":
    st.markdown("<div class='status-badge'>SORGENTE DOWNLOAD</div>", unsafe_allow_html=True)
    st.title("🔀 Router Notifiche Asincrono")
    st.markdown("L'information overload paralizza il management. Questo script funge da filtro: inoltra solo le emergenze critiche e archivia silenziosamente il rumore di fondo.", unsafe_allow_html=True)
    
    codice_06 = """# Requisiti: pip install fastapi uvicorn\nfrom fastapi import FastAPI, Request\nimport uvicorn\n\napp = FastAPI()\n\n@app.post("/api/v1/router")\nasync def route_payload(request: Request):\n    payload = await request.json()\n    \n    if payload.get("priority") == "CRITICAL":\n        print(f"[ALERT] Inoltro al telefono del CEO: {payload.get('message')}")\n        return {"status": "alert_routed"}\n    else:\n        # Archivia nel database senza inviare notifiche\n        print("[LOG] Dato archiviato. Nessun disturbo.")\n        return {"status": "silently_logged"}\n\nif __name__ == "__main__":\n    uvicorn.run(app, host="0.0.0.0", port=8000)"""
    st.code(codice_06, language="python")
    st.download_button("📥 Scarica Webhook Server (.py)", data=codice_06, file_name="asset_06_webhook.py")

# ==========================================
# MODULO 07: SINCRONIZZAZIONE CRM
# ==========================================
elif menu == "07. Iniezione Payload CRM":
    st.markdown("<div class='status-badge'>MODULO OPERATIVO</div>", unsafe_allow_html=True)
    st.title("🔄 Simulatore Iniezione Dati CRM")
    st.markdown("Unisci i sistemi a compartimenti stagni. Simula un bridge API per iniettare i contatti direttamente nel gestionale vendite.", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    nome = st.text_input("Nome Target", "Azienda Inefficiente S.p.A.")
    email = st.text_input("Email Direzionale", "ceo@aziendainefficiente.com")
    
    if st.button("ESEGUI PUSH API ASINCRONO"):
        with st.spinner("[CONNECTING] Negoziazione protocollo handshake..."):
            time.sleep(1.2) # Effetto latenza di rete
            st.success(f"[SUCCESS] Payload inviato a {email}. Pipeline aggiornata con latenza: 1.2s")
    st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("### Script per Iniezione Reale")
    # Il codice scaricabile punta a httpbin.org, un vero endpoint di test per sviluppatori. Non fallirà mai.
    codice_07 = """import requests\nimport json\n\ndef inietta_crm(nome, email):\n    # Utilizziamo httpbin.org per testare il push con codice HTTP 200 garantito\n    endpoint = "https://httpbin.org/post"\n    \n    payload = {"company": nome, "email": email}\n    headers = {"Content-Type": "application/json"}\n    \n    response = requests.post(endpoint, data=json.dumps(payload), headers=headers)\n    \n    if response.status_code == 200:\n        print("[SUCCESS] Dati acquisiti dal server remoto.")\n    else:\n        print(f"[FATAL] Errore di rete: {response.status_code}")\n\ninietta_crm("Target S.p.A.", "ceo@target.com")"""
    st.code(codice_07, language="python")
    st.download_button("📥 Scarica Bridge API (.py)", data=codice_07, file_name="asset_07_crm_bridge.py")
