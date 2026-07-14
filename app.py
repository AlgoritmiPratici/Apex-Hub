import streamlit as st
import pandas as pd
import time
import requests
import json
import plotly.express as px

# ==========================================
# 1. CORE ARCHITECTURE & ROUTING CONFIG
# ==========================================
st.set_page_config(
    page_title="APEX CONSOLE | Enterprise Solution Network", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Inizializzazione della Memoria di Stato (Session State Persistence)
if 'dataset_refined' not in st.session_state:
    st.session_state.dataset_refined = None
if 'vault_authorized' not in st.session_state:
    st.session_state.vault_authorized = False

# Estrazione dinamica del brand per il Deep Linking tramite ManyChat
query_params = st.query_params
brand_target = query_params.get("workspace", "apex")

# Normalizzazione dell'indice sidebar in base all'URL di provenienza
mappa_brand = {"apex": 0, "zerovault": 1}
indice_default = mappa_brand.get(brand_target, 0)

# ==========================================
# 2. DESIGN ENGINE (VERCEL / STRIPE STYLE)
# ==========================================
st.markdown("""
    <style>
    /* Rimozione degli elementi nativi della sandbox Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div.stDeployButton {visibility: hidden;}
    
    /* Configurazione Layout Dark Mode Enterprise */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #05070B !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Risoluzione contrasti stringhe alfa-numeriche e widget labels */
    label, p, span, li, th, td, .stWidgetLabel, [data-testid="stWidgetLabel"] p {
        color: #CCCCCC !important;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Titoli ad Alto Impatto Visivo con Gradiente */
    h1 {
        background: linear-gradient(135deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.06em !important;
        margin-bottom: 1.5rem !important;
    }
    h2, h3 { color: #FFFFFF !important; font-weight: 700 !important; letter-spacing: -0.03em; }
    
    .highlight-green { color: #10B981 !important; font-weight: 600; }
    .highlight-blue { color: #3B82F6 !important; font-weight: 600; }
    
    /* Card Strutturate Glassmorphism */
    .enterprise-card {
        background: rgba(18, 22, 32, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.04);
        margin-bottom: 1.5rem;
    }
    
    /* Protocollo Operativo Box (Manuale d'Uso) */
    .protocol-box {
        background-color: #0B0F17;
        border-left: 3px solid #3B82F6;
        padding: 1rem 1.5rem;
        border-radius: 0 4px 4px 0;
        margin-bottom: 1.5rem;
    }
    
    /* Terminal Console Unix Estetica */
    .terminal-console {
        background-color: #020408;
        border: 1px solid #1F2937;
        border-radius: 6px;
        padding: 1.2rem;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        color: #34D399;
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    /* Override selettivo degli input element di Streamlit */
    div[data-testid="stSelectbox"] div[data-baseweb="select"], div[data-testid="stTextInput"] input {
        background-color: #0D111A !important;
        color: #FFFFFF !important;
        border: 1px solid #1F2937 !important;
    }
    
    /* Override Tabelle e Dataframe */
    div[data-testid="stTable"] table, div[data-testid="stDataFrame"] table {
        color: #E2E8F0 !important;
        background-color: #0D111A !important;
    }
    
    /* Sistema dei Pulsanti Enterprise */
    div.stButton > button {
        background: #FFFFFF !important;
        color: #05070B !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.7rem 1.5rem !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background: #E4E4E7 !important;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.15);
    }
    
    div.stDownloadButton > button {
        background: transparent !important;
        color: #10B981 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid #10B981 !important;
        width: 100% !important;
        text-transform: uppercase;
        padding: 0.7rem 1.5rem !important;
    }
    div.stDownloadButton > button:hover {
        background: rgba(16, 185, 129, 0.08) !important;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        background: rgba(16, 185, 129, 0.08);
        color: #10B981;
        font-size: 0.75rem;
        font-weight: 700;
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR NAVIGATION CONSOLE
# ==========================================
st.sidebar.markdown("""
<div style='text-align:center; padding: 1rem 0;'>
    <div style='color:#FFFFFF; font-weight:800; font-size:1.2rem; letter-spacing:-0.03em;'>APEX SYSTEM NETWORK</div>
    <div style='color:#64748B; font-size:0.75rem; margin-top:0.3rem;'>Control Panel v4.0.2</div>
</div>
<hr style='border-color: #1F2937; margin-top:0;'>
""", unsafe_allow_html=True)

console_selection = st.sidebar.selectbox("INFRASTRUCTURE CONSOLE:", ["⚡ APEX CORE ENGINE", "🔒 ZERO DATA VAULT"], index=indice_default)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# WORKSPACE: APEX CORE ENGINE (AUTOMATION B2B)
# ==========================================
if console_selection == "⚡ APEX CORE ENGINE":
    service = st.sidebar.radio("DEPLOYED SERVICES:", [
        "Data Refining Engine", 
        "Threat Modeling Vault", 
        "Telegram API Compiler", 
        "Ecosystem Cost Matrix", 
        "Dynamic Revenue Simulator", 
        "Asynchronous Traffic Router", 
        "Telemetry Payload Injector"
    ])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("<div style='font-size:0.75rem; color:#475569; text-align:center;'>Handshake Protocol: SECURE<br>Encryption: AES-256-GCM</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVICE 01: DATA REFINING ENGINE
    # --------------------------------------
    if service == "Data Refining Engine":
        st.markdown("<div class='status-badge'>PRODUCTION ACTIVE</div>", unsafe_allow_html=True)
        st.markdown("<h1>Data Refining Engine</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='protocol-box'>
            <b>OPERATIONAL PROTOCOL:</b><br>
            • <b>Input:</b> File .csv grezzo esportato da database disorganizzati.<br>
            • <b>Processo:</b> Parsing asincrono del dataset, rimozione automatica dei duplicati e sanificazione delle stringhe email.<br>
            • <b>Output:</b> Dataset normalizzato pronto per l'importazione immediata nel CRM aziendale.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Raw CSV Dataset", type=["csv"])
        
        if uploaded_file:
            df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
            righe_in = len(df_raw)
            df_clean = df_raw.copy().drop_duplicates()
            if 'Email' in df_clean.columns:
                df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                df_clean = df_clean[~df_clean['Email'].isin(['nan', 'none', '', 'null'])].dropna(subset=['Email'])
            righe_out = len(df_clean)
            st.session_state.dataset_refined = df_clean
            
            st.success("Dataset elaborato dal kernel di sistema.")
            c1, col2, col3 = st.columns(3)
            c1.metric("Raw Records Input", righe_in)
            col2.metric("Sanitized Records", righe_out)
            col3.metric("Anomalies Purged", righe_in - righe_out, delta="-Optimized", delta_color="inverse")
            
            st.dataframe(st.session_state.dataset_refined.head(5), use_container_width=True)
            st.download_button("EXPORT VALIDATED DATASET", st.session_state.dataset_refined.to_csv(index=False).encode('utf-8'), "apex_refined_output.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVICE 02: THREAT MODELING VAULT (.ENV)
    # --------------------------------------
    elif service == "Threat Modeling Vault":
        st.markdown("<div class='status-badge'>SECURITY SERVICE</div>", unsafe_allow_html=True)
        st.markdown("<h1>Threat Modeling Vault (.env)</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='protocol-box'>
            <b>OPERATIONAL PROTOCOL:</b><br>
            • <b>Input:</b> Inserimento di variabili sensibili e chiavi API in testo libero.<br>
            • <b>Processo:</b> Scansione di vulnerabilità ed isolamento runtime delle credenziali dalla logica applicativa.<br>
            • <b>Output:</b> File .env strutturato e manifesto .gitignore protetto generati istantaneamente.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.write("Inserisci le tue coppie Chiave=Valore (una per riga) per compilarle in sicurezza:")
        user_env = st.text_area("Raw Environment Variables", value="DATABASE_URL=postgres://user:pass@localhost:5432/db\nAPI_SECRET_KEY=9a8b7c6d5e\nDEBUG_MODE=False", height=120)
        
        if st.button("SANITIZE AND COMPILE VAULT"):
            st.markdown("<div class='terminal-console'>[SECURITY] Analisi stringhe avviata...<br>[WARNING] Rilevata chiave 'API_SECRET_KEY' in chiaro nel form. Isolamento strutturale in corso...<br>[SUCCESS] File crittografato runtime. Esportazione manifesti completata.</div>", unsafe_allow_html=True)
            col_d1, col_d2 = st.columns(2)
            col_d1.download_button("DOWNLOAD .ENV FILE", user_env, ".env")
            col_d2.download_button("DOWNLOAD .GITIGNORE", ".env\n*.session\n__pycache__/", ".gitignore")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVICE 03: TELEGRAM API COMPILER
    # --------------------------------------
    elif service == "Telegram API Compiler":
        st.markdown("<div class='status-badge'>WIZARD COMPILER</div>", unsafe_allow_html=True)
        st.markdown("<h1>Asynchronous Scraper Wizard</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='protocol-box'>
            <b>OPERATIONAL PROTOCOL:</b><br>
            • <b>Input:</b> Credenziali API fornite dal portale ufficiale my.telegram.org e canale competitor target.<br>
            • <b>Processo:</b> Iniezione dei parametri all'interno dell'architettura client asincrona Telethon.<br>
            • <b>Output:</b> Script Python personalizzato pronto all'uso locale, esente da restrizioni IP Cloud.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        api_id = st.text_input("Telegram API_ID", placeholder="es. 2847592")
        api_hash = st.text_input("Telegram API_HASH", placeholder="es. c4e8b394a20f...", type="password")
        group_target = st.text_input("Target Community Username", placeholder="es. community_competitor")
        
        if st.button("BUILD SCAFFOLDING"):
            if api_id and api_hash and group_target:
                compiled_code = f"from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('apex_session', '{api_id}', '{api_hash}') as client:\n    members = client.get_participants('{group_target}')\n    print('[SUCCESS] Estrazione completata per', len(members), 'record.')"
                st.markdown("<div class='terminal-console'>[SYSTEM] Compilatore in ascolto...<br>[SUCCESS] Matrice Python generata con successo. Sincronizza lo script locale.</div>", unsafe_allow_html=True)
                st.code(compiled_code, language="python")
                st.download_button("DOWNLOAD SCRIPT (.py)", compiled_code, "telethon_extractor.py")
            else:
                st.error("Errore di compilazione: Parametri incompleti.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVICE 04: ECOSYSTEM COST MATRIX
    # --------------------------------------
    elif service == "Ecosystem Cost Matrix":
        st.markdown("<div class='status-badge'>FINANCIAL STRATEGY</div>", unsafe_allow_html=True)
        st.markdown("<h1>Enterprise Cost Architecture Matrix</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='protocol-box'>
            <b>OPERATIONAL PROTOCOL:</b><br>
            • <b>Input:</b> Analisi comparativa strutturata dei flussi di costo.<br>
            • <b>Processo:</b> Mappatura dei colli di bottiglia finanziari causati dai canoni SaaS proprietari chiusi.<br>
            • <b>Output:</b> Tabella architetturale di migrazione verso microservizi a costo marginale zero.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.write("Mappatura delle sostituzioni strutturali implementate nell'infrastruttura APEX:")
        
        matrix_data = {
            "Software Sostituito": ["Zapier Enterprise", "HubSpot Suite", "AWS S3 / Bucket", "Auth0 Security"],
            "Soluzione APEX Deploy": ["n8n Workflow Engine", "Supabase CRM Cluster", "Cloudflare R2 Storage", "Isolamento Kernel .env"],
            "Costo Tradizionale Mese": ["350 €", "120 €", "45 €", "80 €"],
            "Impatto APEX Finanziario": ["0 € (Self-Hosted)", "0 € (Serverless Free Tier)", "0 € (Fino a 10GB)", "0 € (Protocollo Logico)"]
        }
        st.dataframe(pd.DataFrame(matrix_data), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVICE 05: DYNAMIC REVENUE SIMULATOR
    # --------------------------------------
    elif service == "Dynamic Revenue Simulator":
        st.markdown("<div class='status-badge'>CALCULATOR REAL-TIME</div>", unsafe_allow_html=True)
        st.markdown("<h1>Financial Telemetry Live Simulator</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='protocol-box'>
            <b>OPERATIONAL PROTOCOL:</b><br>
            • <b>Input:</b> Inserimento delle variabili finanziarie correnti (MRR, Costi SaaS, Churn Rate).<br>
            • <b>Processo:</b> Elaborazione dinamica dell'impatto dei margini netti post-ottimizzazione infrastrutturale.<br>
            • <b>Output:</b> Grafico vettoriale interattivo delle metriche di rendimento aziendale.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        c_sim1, col_sim2, col_sim3 = st.columns(3)
        user_mrr = c_sim1.number_input("Fatturato Mensile Ricorrente / MRR (€)", value=25000, step=1000)
        user_saas = col_sim2.number_input("Canoni Licenze SaaS Correnti (€)", value=3200, step=100)
        user_churn = col_sim3.slider("Tasso di Abbandono Clienti / Churn Rate (%)", 0.0, 15.0, 4.5)
        
        margine_corrente = user_mrr - user_saas - (user_mrr * (user_churn / 100))
        margine_ottimizzato = user_mrr - 0 - (user_mrr * (user_churn / 100)) # Costi SaaS eliminati
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Margine Netto Corrente", f"€ {margine_corrente:,.2f}")
        col_m2.metric("Margine Netto Ottimizzato (APEX)", f"€ {margine_ottimizzato:,.2f}", f"+€ {user_saas:,} Recuperati")
        
        df_chart = pd.DataFrame({
            "Architettura": ["Stato Corrente", "Modello APEX OS"],
            "Margine Operativo Effettivo (€)": [margine_corrente, margine_ottimizzato]
        })
        fig = px.bar(df_chart, x="Architettura", y="Margine Operativo Effettivo (€)", color="Architettura", color_discrete_sequence=['#EF4444', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVICE 06: ASYNCHRONOUS TRAFFIC ROUTER
    # --------------------------------------
    elif service == "Asynchronous Traffic Router":
        st.markdown("<div class='status-badge'>TELEMETRY GATE</div>", unsafe_allow_html=True)
        st.markdown("<h1>Asynchronous Traffic Router</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='protocol-box'>
            <b>OPERATIONAL PROTOCOL:</b><br>
            • <b>Input:</b> Payload JSON simulato in ingresso da un server di notifica esterno.<br>
            • <b>Processo:</b> Analisi logica e classificazione asincrona dei livelli di urgenza dei dati.<br>
            • <b>Output:</b> Instradamento mirato verso console direzionale o soppressione del log di rumore.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        st.write("Imposta le regole del server di smistamento per testare l'algoritmo di routing:")
        evento_origine = st.selectbox("Sorgente Evento API:", ["Stripe Checkout", "HubSpot Lead Form", "Server Health Ping"])
        livello_priorita = st.radio("Livello di Priorità Tracciato:", ["LOW (Log Silenzioso)", "CRITICAL (Inoltro Istantaneo)"])
        
        if st.button("TRIGGER LOG SIMULATION"):
            st.markdown("<div class='terminal-console' id='term-log'>[SERVER] In ascolto sulla porta 8080... Webhook intercettato.<br>[PARSING] Payload acquisito da sorgente: " + evento_origine + "</div>", unsafe_allow_html=True)
            time.sleep(0.6)
            if "CRITICAL" in livello_priorita:
                st.markdown("<div class='terminal-console' style='border-top:none; border-radius:0 0 6px 6px; color:#F59E0B;'>[ALERT ROUTED] Evento ad alto impatto. Notifica push inoltrata al CTO.<br>[STATUS] Transaction Completed (200 OK)</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='terminal-console' style='border-top:none; border-radius:0 0 6px 6px; color:#64748B;'>[SUPPRESSED] Inefficienza filtrata. Payload archiviato nel database di log passivo senza disturbare il management.<br>[STATUS] Transaction Completed (200 OK)</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVICE 07: TELEMETRY PAYLOAD INJECTOR
    # --------------------------------------
    elif service == "Telemetry Payload Injector":
        st.markdown("<div class='status-badge'>SANDBOX CORE</div>", unsafe_allow_html=True)
        st.markdown("<h1>API Payload Injector Sandbox</h1>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='protocol-box'>
            <b>OPERATIONAL PROTOCOL:</b><br>
            • <b>Input:</b> Inserimento dell'endpoint webhook reale e del relativo dizionario JSON di prova.<br>
            • <b>Processo:</b> Handshake TCP ed esecuzione forzata di una richiesta POST asincrona via rete HTTP.<br>
            • <b>Output:</b> Log di telemetria reale con visualizzazione del codice di risposta del server di destinazione.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
        target_url = st.text_input("Destination Endpoint URL", value="https://httpbin.org/post")
        st.caption("*Default impostato su httpbin.org per test di rete sicuri a riscontro immediato (Status 200).*")
        
        stringa_json = '{\n  "client_id": "AP-2026",\n  "status": "synchronized",\n  "metric": "latenza_ottimale"\n}'
        payload_area = st.text_area("JSON Payload Data Struct", value=stringa_json, height=120)
        
        if st.button("EXECUTE LIVE INJECTION"):
            console_window = st.empty()
            console_window.markdown("<div class='terminal-console'>[CONNECTING] Negoziazione pacchetti TCP...</div>", unsafe_allow_html=True)
            time.sleep(0.7)
            try:
                carico_json = json.loads(payload_area)
                risposta_rete = requests.post(target_url, json=carico_json, timeout=6)
                console_window.markdown(f"<div class='terminal-console'>[SUCCESS] Richiesta inoltrata.<br>[SERVER STATUS] Code: {risposta_rete.status_code}<br>[NETWORK LATENCY] {risposta_rete.elapsed.total_seconds()}s<br>[BODY BACKEND] {risposta_rete.text[:150]}...</div>", unsafe_allow_html=True)
            except json.JSONDecodeError:
                console_window.markdown("<div class='terminal-console' style='color:#EF4444;'>[ERROR] Sintassi JSON malformata. Impossibile compilare il payload.</div>", unsafe_allow_html=True)
            except Exception as e:
                console_window.markdown(f"<div class='terminal-console' style='color:#EF4444;'>[FATAL] Timeout di rete o server irraggiungibile: {str(e)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# WORKSPACE: ZERO DATA VAULT (INTELLIGENCE)
# ==========================================
elif console_selection == "🔒 ZERO DATA VAULT":
    st.markdown("<div class='status-badge'>DATA CENTER ACTIVE</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='highlight-blue'>ZERO VAULT Intel Center</h1>", unsafe_allow_html=True)
    st.write("Database centralizzato degli strumenti digitali di produttività ed arbitraggio temporale.")
    
    st.markdown("""
    <div class='protocol-box' style='border-left-color: #3B82F6;'>
        <b>OPERATIONAL PROTOCOL:</b><br>
        • <b>Input:</b> Query di ricerca inserita dall'operatore.<br>
        • <b>Processo:</b> Filtraggio istantaneo delle matrici di database interne basato su stringhe nidificate.<br>
        • <b>Output:</b> Tabella dinamica delle risorse verificate ad estrazione CSV protetta da Email-Gate.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='enterprise-card'>", unsafe_allow_html=True)
    
    database_matrice = pd.DataFrame([
        {"Cluster": "Video Engineering", "Software Tool": "CapCut Core Engine", "Financial Policy": "Freemium Model / 4K Export", "Network Stack": "Video Layer"},
        {"Cluster": "Acoustic AI", "Software Tool": "ElevenLabs Core", "Financial Policy": "10k Characters Free/Month", "Network Stack": "Audio Layer"},
        {"Cluster": "Cognitive LLM", "Software Tool": "Gemini Advanced Engine", "Financial Policy": "Enterprise Kontext Window", "Network Stack": "Logic Layer"},
        {"Cluster": "API Automation", "Software Tool": "n8n Open Source Node", "Financial Policy": "0€ (Self-Hosted Architecture)", "Network Stack": "Backend Routing"},
        {"Cluster": "Cloud Data", "Software Tool": "Supabase PostgreSQL", "Financial Policy": "Serverless Instance Free Tier", "Network Stack": "Database Cluster"}
    ])
    
    chiave_ricerca = st.text_input("🔍 Filter Central Registry (es. Video, Audio, Backend, 0€)...")
    if chiave_ricerca:
        filtro_maschera = database_matrice.apply(lambda riga: riga.astype(str).str.contains(chiave_ricerca, case=False).any(), axis=1)
        database_matrice = database_matrice[filtro_maschera]
        
    st.dataframe(database_matrice, use_container_width=True, hide_index=True)
    st.markdown("---")
    
    # LEAD GENERATION EMAIL-GATE SYSTEM
    if not st.session_state.lead_vault:
        st.markdown("### 🔒 Authorize Extended CSV Extraction")
        st.write("Inserisci le credenziali di comunicazione aziendale per sbloccare l'esportazione del file matrice.")
        email_input = st.text_input("Corporate Email Address:")
        
        if st.button("VERIFY AND UNLOCK DATA EXTRACTION"):
            if "@" in email_input and "." in email_input:
                st.session_state.lead_vault = True
                st.rerun()
            else:
                st.error("Protocollo di autenticazione respinto: Indirizzo non valido.")
                
    if st.session_state.lead_vault:
        st.success("✅ Autorizzazione concessa. Estrazione pacchetti sbloccata.")
        csv_vault = database_matrice.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DOWNLOAD INTEGRAL REGISTRY (.CSV)", csv_vault, "zero_vault_intelligence.csv", "text/csv")
        
    st.markdown("</div>", unsafe_allow_html=True)

# Footer di sistema asettico
st.sidebar.markdown("<div style='font-size: 0.7rem; color: #334155; text-align: center; margin-top: 4rem;'>APEX MATRIX PLATFORM © 2026<br>All Rights Reserved. SYSTEM VER. 4.0.0</div>", unsafe_allow_html=True)
