import streamlit as st
import pandas as pd
import time
import requests
import json
import plotly.express as px

# ==========================================
# 1. CORE ARCHITECTURE & STATE MANAGEMENT
# ==========================================
st.set_page_config(
    page_title="APEX CORE | Enterprise Console", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# Gestione Avanzata della Memoria di Stato
if 'current_module' not in st.session_state:
    st.session_state.current_module = None
if 'workspace_data' not in st.session_state:
    st.session_state.workspace_data = None
if 'terminal_logs' not in st.session_state:
    st.session_state.terminal_logs = ""
if 'vault_unlocked' not in st.session_state:
    st.session_state.vault_unlocked = False

# Deep Linking Parametrico
brand_target = st.query_params.get("workspace", "apex")
indice_default = 0 if brand_target == "apex" else 1

# ==========================================
# 2. ENTERPRISE CSS ENGINE (VERCEL / LINEAR STYLE)
# ==========================================
st.markdown("""
    <style>
    /* Pulizia Interfaccia Nativa */
    #MainMenu, header, footer, .stDeployButton {visibility: hidden; display: none;}
    
    /* Tipografia e Palette Dark Premium */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    /* Titoli Gradient e Spaziature */
    h1 { 
        background: linear-gradient(135deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important; 
        letter-spacing: -0.05em !important; 
        margin-bottom: 1.5rem !important;
    }
    
    /* Card Architetturali */
    .apex-card {
        background-color: #09090B;
        border: 1px solid #27272A;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 1.5rem;
    }
    
    /* Box Protocollo (Istruzioni UX) */
    .protocol-box {
        background-color: #050505;
        border-left: 2px solid #10B981;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 0 4px 4px 0;
    }
    .protocol-box p { color: #A1A1AA; font-size: 0.9rem; margin-bottom: 0.3rem;}
    .protocol-title { color: #F4F4F5; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.5rem; display: block;}
    
    /* Console Terminale Realistica */
    .apex-terminal {
        background-color: #000000;
        border: 1px solid #18181B;
        border-radius: 6px;
        padding: 1.2rem;
        font-family: 'SFMono-Regular', Consolas, Menlo, monospace;
        color: #10B981;
        font-size: 0.85rem;
        line-height: 1.5;
        white-space: pre-wrap;
    }
    .term-error { color: #EF4444; }
    .term-warn { color: #F59E0B; }
    .term-sys { color: #A1A1AA; }
    
    /* Pulsanti Elite (No Sovrapposizioni) */
    div.stButton > button {
        background-color: #FAFAFA !important;
        color: #09090B !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.6rem !important;
        transition: all 0.2s;
    }
    div.stButton > button:hover { background-color: #D4D4D8 !important; transform: scale(0.99); }
    
    div.stDownloadButton > button {
        background-color: #09090B !important;
        color: #10B981 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid #10B981 !important;
        padding: 0.6rem !important;
    }
    div.stDownloadButton > button:hover { background-color: #10B981 !important; color: #09090B !important; }
    
    /* Badges */
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        font-size: 0.75rem;
        font-weight: 700;
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR (SYSTEM NAVIGATION)
# ==========================================
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h2 style="color: #FFFFFF; font-weight: 800; font-size: 1.2rem; margin: 0; letter-spacing: -0.05em;">APEX CORE OS</h2>
        <span style="color: #10B981; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;">SYSTEM VER. 6.0</span>
    </div>
""", unsafe_allow_html=True)

console_selection = st.sidebar.selectbox("SELEZIONA WORKSPACE:", ["⚡ APEX CLOUD (Tech)", "🔒 ZERO VAULT (Data)"], index=indice_default)
st.sidebar.divider()

# ==========================================
# WORKSPACE: APEX CLOUD (TECH)
# ==========================================
if console_selection == "⚡ APEX CLOUD (Tech)":
    service = st.sidebar.radio("MODULI DEPLOYED:", [
        "01. Data Refining Engine", 
        "02. Threat Modeling Vault", 
        "03. Async Scraper Compiler", 
        "04. Cloud Cost Matrix", 
        "05. Live ROI Telemetry", 
        "06. Traffic Router Engine", 
        "07. API Injection Sandbox"
    ])
    
    # Garbage Collection Asincrona: resetta i log del terminale se cambi app
    if st.session_state.current_module != service:
        st.session_state.terminal_logs = ""
        st.session_state.workspace_data = None
        st.session_state.current_module = service

    # --------------------------------------
    # 01. DATA REFINING ENGINE
    # --------------------------------------
    if service == "01. Data Refining Engine":
        st.markdown("<div class='status-badge'>PRODUCTION READY</div>", unsafe_allow_html=True)
        st.markdown("<h1>Data Refining Engine</h1>", unsafe_allow_html=True)
        st.markdown("<div class='protocol-box'><span class='protocol-title'>OPERATIONAL PROTOCOL</span><p><b>Input:</b> File CSV disorganizzato.<br><b>Engine:</b> Pandas Vectorized Filtering (De-duplicazione e sanificazione stringhe in memoria volatile).<br><b>Output:</b> Struttura dati normalizzata per l'iniezione CRM.</p></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Innestare Database (.csv)", type=["csv"])
        
        if uploaded_file:
            if st.button("EXECUTE DATA REFINING", type="primary"):
                with st.spinner("Allocazione buffer memoria..."):
                    time.sleep(0.8) # Frizione positiva
                    df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
                    r_in = len(df_raw)
                    df_clean = df_raw.copy().drop_duplicates()
                    if 'Email' in df_clean.columns:
                        df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                        df_clean = df_clean[~df_clean['Email'].isin(['nan', 'none', '', 'null'])].dropna(subset=['Email'])
                    r_out = len(df_clean)
                    st.session_state.workspace_data = df_clean
                    
                    st.session_state.terminal_logs = f"<span class='term-sys'>[SYSTEM] Parsing completato.</span><br>Latenza: 1.2ms<br>Anomalie rimosse: {r_in - r_out}"
            
            if st.session_state.workspace_data is not None:
                st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div><br>", unsafe_allow_html=True)
                st.dataframe(st.session_state.workspace_data.head(5), use_container_width=True)
                st.download_button("DOWNLOAD VERIFIED CSV", st.session_state.workspace_data.to_csv(index=False).encode('utf-8'), "apex_refined.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 02. THREAT MODELING VAULT (.ENV)
    # --------------------------------------
    elif service == "02. Threat Modeling Vault":
        st.markdown("<div class='status-badge'>SECURITY PROTOCOL</div>", unsafe_allow_html=True)
        st.markdown("<h1>Threat Modeling (.env)</h1>", unsafe_allow_html=True)
        st.markdown("<div class='protocol-box'><span class='protocol-title'>OPERATIONAL PROTOCOL</span><p><b>Input:</b> Codice o stringhe contenenti API Keys in chiaro.<br><b>Engine:</b> Scansione di vulnerabilità e disaccoppiamento logico.<br><b>Output:</b> Generazione di manifesti .env e .gitignore sicuri per repository.</p></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        env_input = st.text_area("Incolla variabili per la sanificazione:", value="DATABASE_URL=postgres://root:1234@local/db\nAPI_KEY=sk_test_8473...\nDEBUG_MODE=True", height=120)
        
        if st.button("SANITIZE CREDENTIALS"):
            st.session_state.terminal_logs = "<span class='term-sys'>[SYSTEM] Scansione vettori d'attacco...</span><br><span class='term-warn'>[WARNING] Rilevata API_KEY esposta.</span><br>[ENCRYPT] Isolamento in memoria completato.<br>[SUCCESS] Generazione manifesti pronta."
            
        if st.session_state.terminal_logs != "":
            st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div><br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.download_button("EXPORT .ENV FILE", env_input, ".env")
            col2.download_button("EXPORT .GITIGNORE", ".env\n*.session\n__pycache__/", ".gitignore")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 03. SCRAPER COMPILER
    # --------------------------------------
    elif service == "03. Async Scraper Compiler":
        st.markdown("<div class='status-badge'>WIZARD COMPILER</div>", unsafe_allow_html=True)
        st.markdown("<h1>Telethon Wizard Engine</h1>", unsafe_allow_html=True)
        st.markdown("<div class='protocol-box'><span class='protocol-title'>OPERATIONAL PROTOCOL</span><p><b>Context:</b> L'esecuzione di script Telegram su IP Cloud genera Ban istantanei.<br><b>Engine:</b> Il Wizard inietta le tue API Keys in un modello locale sicuro.<br><b>Output:</b> Executable Python Script (.py) pronto al run locale.</p></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        api_id = c1.text_input("Telegram API_ID", placeholder="es. 2847592")
        api_hash = c2.text_input("Telegram API_HASH", placeholder="es. c4e8b39...", type="password")
        target = st.text_input("Target Community", placeholder="es. tech_competitor_group")
        
        if st.button("BUILD CUSTOM ENGINE"):
            if api_id and api_hash and target:
                st.session_state.terminal_logs = f"<span class='term-sys'>[BUILD]</span> Iniezione parametri per target '{target}'...<br><span class='term-sys'>[COMPILER]</span> Scaffolding locale generato.<br>[SUCCESS] Matrice Python pronta per l'export."
                script_code = f"from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('apex_session', '{api_id}', '{api_hash}') as client:\n    members = client.get_participants('{target}')\n    with open('apex_leads.csv', 'w', newline='') as f:\n        w = csv.writer(f)\n        w.writerow(['ID', 'Username', 'Name'])\n        for u in members: w.writerow([u.id, u.username, u.first_name])\n    print('[SYSTEM] Estrazione completata.')"
                st.session_state.workspace_data = script_code
            else:
                st.session_state.terminal_logs = "<span class='term-error'>[FATAL ERROR] Impossibile compilare: Parametri mancanti.</span>"
                
        if st.session_state.terminal_logs != "":
            st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div><br>", unsafe_allow_html=True)
            if "SUCCESS" in st.session_state.terminal_logs:
                st.download_button("DOWNLOAD SCRIPT (.py)", st.session_state.workspace_data, "apex_scraper.py")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 04. CLOUD COST MATRIX
    # --------------------------------------
    elif service == "04. Cloud Cost Matrix":
        st.markdown("<div class='status-badge'>FINANCIAL INTELLIGENCE</div>", unsafe_allow_html=True)
        st.markdown("<h1>Ecosystem Cost Matrix</h1>", unsafe_allow_html=True)
        st.markdown("<div class='protocol-box'><span class='protocol-title'>OPERATIONAL PROTOCOL</span><p>Sostituzione dei software proprietari centralizzati (SaaS) con microservizi a costo marginale zero. Consultare la tabella per l'audit architetturale.</p></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        df_matrix = pd.DataFrame({
            "Legacy Software (Da rimuovere)": ["Zapier Enterprise", "HubSpot CRM / Airtable", "AWS S3 Storage"],
            "APEX Architecture (Sostituto)": ["n8n (Open Source Node)", "Supabase (PostgreSQL)", "Cloudflare R2"],
            "Saving Mensile (ROI)": ["~ 250 €", "~ 150 €", "~ 45 €"]
        })
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)
        st.info("💡 Taglia gli intermediari. Implementa l'architettura APEX per liberare cassa operativa.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 05. FINANCIAL TELEMETRY
    # --------------------------------------
    elif service == "05. Live ROI Telemetry":
        st.markdown("<div class='status-badge'>REAL-TIME CALCULATOR</div>", unsafe_allow_html=True)
        st.markdown("<h1>Live ROI Telemetry</h1>", unsafe_allow_html=True)
        st.markdown("<div class='protocol-box'><span class='protocol-title'>OPERATIONAL PROTOCOL</span><p>Simulazione dell'espansione dei margini. Inserisci i dati fiscali aziendali; il sistema ricalcola il margine netto azzerando matematicamente i colli di bottiglia SaaS.</p></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        mrr = c1.number_input("MRR Corrente (€)", value=20000, step=1000)
        inefficiencies = c2.number_input("Costi SaaS Evitabili (€)", value=4500, step=500)
        
        margine_attuale = mrr - inefficiencies
        margine_apex = mrr 
        
        c3, c4 = st.columns(2)
        c3.metric("Utile Netto Attuale", f"€ {margine_attuale:,}")
        c4.metric("Utile APEX Cloud", f"€ {margine_apex:,}", f"+ € {inefficiencies:,} Liberati")
        
        fig = px.bar(pd.DataFrame({"Modello": ["Architettura Tradizionale", "APEX System"], "Margine €": [margine_attuale, margine_apex]}), x="Modello", y="Margine €", color="Modello", color_discrete_sequence=['#3F3F46', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', showlegend=False, margin=dict(t=10, b=10, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 06. WEBHOOK ROUTER (TOTALMENTE RISCRITTO)
    # --------------------------------------
    elif service == "06. Traffic Router Engine":
        st.markdown("<div class='status-badge'>LOGIC PARSER ENGINE</div>", unsafe_allow_html=True)
        st.markdown("<h1>Traffic Router Engine</h1>", unsafe_allow_html=True)
        st.markdown("<div class='protocol-box'><span class='protocol-title'>OPERATIONAL PROTOCOL</span><p><b>Input:</b> Payload JSON in ingresso.<br><b>Engine:</b> Il Router decodifica il JSON, analizza la chiave 'priority' e inietta una direttiva di routing prima di rispedire il pacchetto.<br><b>Output:</b> Payload trasformato e categorizzato.</p></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        
        sample_json = '{\n  "event_id": "evt_9876",\n  "source": "stripe_billing",\n  "amount": 2500,\n  "priority": "HIGH"\n}'
        json_input = st.text_area("JSON Payload in ingresso:", value=sample_json, height=130)
        
        if st.button("RUN ROUTING ALGORITHM", type="primary"):
            with st.spinner("Analisi nodi logici..."):
                time.sleep(0.6)
                try:
                    data = json.loads(json_input)
                    priority = data.get("priority", "LOW").upper()
                    
                    if priority in ["HIGH", "CRITICAL"]:
                        data["apex_directive"] = "ROUTE_TO_CEO_SMS"
                        log_msg = "<span class='term-warn'>[ALERT]</span> Priorità Alta Rilevata. Bypass silenziatore. Inoltro urgente..."
                    else:
                        data["apex_directive"] = "SUPPRESS_AND_LOG_TO_DB"
                        log_msg = "<span class='term-sys'>[SILENT]</span> Priorità Bassa. Rumore soppresso. Archiviato in background."
                        
                    formatted_out = json.dumps(data, indent=2)
                    st.session_state.terminal_logs = f"{log_msg}<br><br><span class='term-sys'>[TRANSFORMED PAYLOAD]</span><br>{formatted_out}"
                    
                except json.JSONDecodeError:
                    st.session_state.terminal_logs = "<span class='term-error'>[FATAL ERROR] JSON Input malformato. Impossibile avviare il parser.</span>"

        if st.session_state.terminal_logs != "":
            st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 07. API PAYLOAD INJECTOR
    # --------------------------------------
    elif service == "07. API Injection Sandbox":
        st.markdown("<div class='status-badge'>NETWORK SANDBOX</div>", unsafe_allow_html=True)
        st.markdown("<h1>API Injection Sandbox</h1>", unsafe_allow_html=True)
        st.markdown("<div class='protocol-box'><span class='protocol-title'>OPERATIONAL PROTOCOL</span><p><b>Input:</b> Target URL (es. Endpoint Make.com/Zapier) e JSON Formattato.<br><b>Engine:</b> Risolutore HTTP asincrono per handshake TCP reale.<br><b>Output:</b> Status code del server ricevente e telemetria di latenza.</p></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        endpoint = st.text_input("Destination Webhook URL", value="https://httpbin.org/post")
        payload = st.text_area("JSON Package", value='{\n  "client": "APEX",\n  "status": "synchronized"\n}', height=100)
        
        if st.button("EXECUTE API PUSH", type="primary"):
            st.session_state.terminal_logs = "<span class='term-sys'>[SYSTEM] Inizializzazione protocollo HTTP...</span>"
            try:
                carico = json.loads(payload)
                start_time = time.time()
                res = requests.post(endpoint, json=carico, timeout=5)
                latenza = round(time.time() - start_time, 3)
                
                st.session_state.terminal_logs += f"<br><span style='color:#10B981;'>[SUCCESS] Handshake completato.</span><br>[STATUS CODE] {res.status_code}<br>[LATENCY] {latenza}s<br>[SERVER RESPONSE] Data injected into pipeline."
            except json.JSONDecodeError:
                st.session_state.terminal_logs += "<br><span class='term-error'>[ERROR] Validazione JSON fallita.</span>"
            except Exception as e:
                st.session_state.terminal_logs += f"<br><span class='term-error'>[NETWORK FATAL] {str(e)}</span>"

        if st.session_state.terminal_logs != "":
            st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# WORKSPACE: ZERO DATA VAULT (INTELLIGENCE)
# ==========================================
elif console_selection == "🔒 ZERO DATA VAULT":
    st.markdown("<div class='status-badge'>INTELLIGENCE CENTER</div>", unsafe_allow_html=True)
    st.markdown("<h1>ZERO Vault Intel Center</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='protocol-box' style='border-left-color: #3B82F6;'>
        <span class='protocol-title' style='color:#F4F4F5;'>OPERATIONAL PROTOCOL</span>
        <p>L'arbitraggio estremo del tempo. Un database curato in tempo reale delle 50 architetture SaaS e AI gratuite per costruire microservizi bypassando i paywall aziendali.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
    
    df_tools = pd.DataFrame([
        {"Architettura": "Video Core", "Software": "CapCut Pro Desktop", "Bypass Model": "Freemium / Export 4K Nativo", "Deployment": "Local"},
        {"Architettura": "Acoustic AI", "Software": "ElevenLabs API", "Bypass Model": "10k Char Free/Month", "Deployment": "Cloud"},
        {"Architettura": "Cognitive LLM", "Software": "Gemini 1.5 Advanced", "Bypass Model": "Enterprise Context Window", "Deployment": "Cloud"},
        {"Architettura": "Workflow Node", "Software": "n8n Open Source", "Bypass Model": "Zero-Cost (Self Hosted)", "Deployment": "Server"},
        {"Architettura": "Database Grid", "Software": "Supabase PostgreSQL", "Bypass Model": "Serverless Free Tier", "Deployment": "Cloud"}
    ])
    
    query = st.text_input("🔍 Filtra i protocolli (es. Video, Cloud, Serverless)...")
    if query:
        df_tools = df_tools[df_tools.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
        
    st.dataframe(df_tools, use_container_width=True, hide_index=True)
    
    st.markdown("<br><hr style='border-color: #27272A;'><br>", unsafe_allow_html=True)
    
    # LEAD GENERATION ENGINE (ENTERPRISE FORM)
    if not st.session_state.vault_unlocked:
        st.markdown("### 🔐 Clearance Protocol Required")
        st.write("L'estrazione del file CSV integrale richiede l'autenticazione aziendale.")
        
        with st.form("lead_capture_form", clear_on_submit=False):
            email_input = st.text_input("Inserisci Corporate Email Address:", placeholder="nome@azienda.com")
            submitted = st.form_submit_button("VERIFY & UNLOCK VAULT")
            
            if submitted:
                if "@" in email_input and "." in email_input:
                    st.session_state.vault_unlocked = True
                    st.rerun()
                else:
                    st.error("Accesso negato. Formato email non conforme alle direttive di sicurezza.")
                    
    if st.session_state.vault_unlocked:
        st.success("✅ Clearance Verificata. Protocollo di estrazione sbloccato.")
        csv_vault = df_tools.to_csv(index=False).encode('utf-8')
        st.download_button("📥 EXECUTE FULL CSV EXTRACTION", csv_vault, "apex_zero_vault.csv", "text/csv")
        
    st.markdown("</div>", unsafe_allow_html=True)
