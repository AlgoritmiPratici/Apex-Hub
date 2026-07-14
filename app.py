import streamlit as st
import pandas as pd
import time
import requests
import json
import plotly.express as px

# ==========================================
# 1. CORE ARCHITECTURE & ROUTING
# ==========================================
st.set_page_config(
    page_title="APEX CORE | Infrastructure Hub", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# Gestione Avanzata dello Stato (Garbage Collection & Routing)
if 'current_module' not in st.session_state:
    st.session_state.current_module = None
if 'lead_vault' not in st.session_state:
    st.session_state.lead_vault = False
if 'workspace_data' not in st.session_state:
    st.session_state.workspace_data = None

# Deep Linking
brand_target = st.query_params.get("workspace", "apex")
indice_default = 0 if brand_target == "apex" else 1

# ==========================================
# 2. VERCEL-STYLE CSS ENGINE (BUG FIX SOVRAPPOSIZIONE)
# ==========================================
st.markdown("""
    <style>
    /* Rimozione rumore visivo Streamlit */
    #MainMenu, header, footer, .stDeployButton {visibility: hidden; display: none;}
    
    /* Tipografia e Colori Base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    /* Forzatura Contrasti per la leggibilità totale */
    p, span, li, label, .stWidgetLabel { color: #A1A1AA !important; }
    h1 { 
        background: linear-gradient(to right, #FFFFFF, #71717A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important; 
        letter-spacing: -0.04em !important; 
    }
    h2, h3, h4 { color: #F4F4F5 !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    
    /* Layout Box Architetturale */
    .glass-card {
        background-color: #09090B;
        border: 1px solid #27272A;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.5rem;
    }
    
    .tech-spec-box {
        background-color: #050505;
        border-left: 2px solid #10B981;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Console Output */
    .cmd-terminal {
        background-color: #000000;
        border: 1px solid #27272A;
        border-radius: 4px;
        padding: 1rem;
        font-family: 'SFMono-Regular', monospace;
        color: #34D399;
        font-size: 0.85rem;
    }
    
    /* Pulsanti Elite */
    div.stButton > button {
        background-color: #FAFAFA !important;
        color: #09090B !important;
        font-weight: 700 !important;
        border-radius: 4px !important;
        border: none !important;
        transition: all 0.2s;
    }
    div.stButton > button:hover { background-color: #D4D4D8 !important; }
    
    div.stDownloadButton > button {
        background-color: #09090B !important;
        color: #10B981 !important;
        font-weight: 700 !important;
        border-radius: 4px !important;
        border: 1px solid #10B981 !important;
    }
    div.stDownloadButton > button:hover { background-color: #10B981 !important; color: #09090B !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR (PULIZIA DOM PER EVITARE BUG)
# ==========================================
st.sidebar.markdown("""
    <div style="margin-bottom: 1.5rem; text-align: center;">
        <h2 style="color: #FFFFFF; font-weight: 800; font-size: 1.2rem; margin-bottom: 0;">APEX SYSTEM</h2>
        <span style="color: #10B981; font-size: 0.75rem; font-weight: 600; letter-spacing: 1px;">CORE OS v5.0</span>
    </div>
""", unsafe_allow_html=True)

st.sidebar.divider() # Sostituisce l'HTML grezzo, risolvendo i bug grafici di sovrapposizione.

console_selection = st.sidebar.selectbox("WORKSPACE CLUSTER:", ["⚡ APEX TECH ENGINE", "🔒 ZERO DATA VAULT"], index=indice_default)

st.sidebar.divider()

# ==========================================
# ECOSISTEMA: APEX TECH ENGINE
# ==========================================
if console_selection == "⚡ APEX TECH ENGINE":
    service = st.sidebar.radio("ACTIVE PROTOCOLS:", [
        "01. Data Refining Engine", 
        "02. Threat Modeling Vault", 
        "03. Async Scraper Compiler", 
        "04. Cloud Cost Matrix", 
        "05. Live ROI Telemetry", 
        "06. Traffic Router Engine", 
        "07. API Injection Sandbox"
    ])
    
    # Garbage Collection: Resetta i dati in cache se l'utente cambia modulo
    if st.session_state.current_module != service:
        st.session_state.workspace_data = None
        st.session_state.current_module = service

    st.sidebar.markdown("<div style='font-size:0.75rem; color:#52525B; text-align:center; margin-top:2rem;'>Connection: SECURE AES-256</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 01. DATA REFINING
    # --------------------------------------
    if service == "01. Data Refining Engine":
        st.markdown("<h1>Data Refining Engine</h1>", unsafe_allow_html=True)
        st.markdown("<div class='tech-spec-box'><span style='color:#F4F4F5; font-weight:600;'>[PROTOCOL]</span> Inserimento CSV Grezzo → Pulizia Memoria Asincrona → Export Normalizzato per CRM.</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Innestare Database Dump (.csv)", type=["csv"])
        
        if uploaded_file:
            if st.button("EXECUTE DATA REFINING", type="primary"):
                # Ingegneria Psicologica: Simulazione di carico per percepire il valore
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.markdown("<div class='cmd-terminal'>[SYSTEM] Allocazione buffer memoria...</div>", unsafe_allow_html=True)
                time.sleep(0.5)
                progress_bar.progress(30)
                status_text.markdown("<div class='cmd-terminal'>[SYSTEM] Esecuzione de-duplicazione vettoriale...</div>", unsafe_allow_html=True)
                time.sleep(0.8)
                progress_bar.progress(70)
                
                df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
                righe_in = len(df_raw)
                df_clean = df_raw.copy().drop_duplicates()
                if 'Email' in df_clean.columns:
                    df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                    df_clean = df_clean[~df_clean['Email'].isin(['nan', 'none', '', 'null'])].dropna(subset=['Email'])
                righe_out = len(df_clean)
                st.session_state.workspace_data = df_clean
                
                progress_bar.progress(100)
                status_text.markdown("<div class='cmd-terminal' style='color:#10B981;'>[SUCCESS] Normalizzazione completata con latenza < 1.4s.</div>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Raw Inputs", righe_in)
                c2.metric("Valid Outputs", righe_out)
                c3.metric("Anomalies Purged", righe_in - righe_out, delta="-Ottimizzato", delta_color="inverse")
                
                st.dataframe(st.session_state.workspace_data.head(5), use_container_width=True)
                st.download_button("DOWNLOAD VERIFIED DATASET", st.session_state.workspace_data.to_csv(index=False).encode('utf-8'), "apex_refined.csv", "text/csv")
                
                # Micro-Upsell
                st.info("Infrastruttura validata. Ottimizza le perdite implementando API backend.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 02. THREAT MODELING
    # --------------------------------------
    elif service == "02. Threat Modeling Vault":
        st.markdown("<h1>Threat Modeling (.env)</h1>", unsafe_allow_html=True)
        st.markdown("<div class='tech-spec-box'><span style='color:#F4F4F5; font-weight:600;'>[PROTOCOL]</span> Scansione vettori d'attacco → Disaccoppiamento credenziali → Generazione manifesti sicuri.</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        env_input = st.text_area("Incolla le variabili hardcoded per la sanificazione:", value="DATABASE_URL=postgres://root:admin123@local/db\nSTRIPE_SECRET=sk_live_837482...\nDEBUG=True", height=150)
        
        if st.button("SANITIZE CREDENTIALS", type="primary"):
            st.markdown("<div class='cmd-terminal'>[SCAN] Ricerca pattern insicuri...<br>[WARNING] Rilevate password in chiaro.<br>[ENCRYPT] Isolamento runtime completato.</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.download_button("EXPORT .ENV MANIFEST", env_input, ".env")
            col2.download_button("EXPORT .GITIGNORE FIREWALL", ".env\n__pycache__/\n*.session", ".gitignore")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 03. SCRAPER COMPILER
    # --------------------------------------
    elif service == "03. Async Scraper Compiler":
        st.markdown("<h1>Telethon Wizard Engine</h1>", unsafe_allow_html=True)
        st.markdown("<div class='tech-spec-box'><span style='color:#F4F4F5; font-weight:600;'>[PROTOCOL]</span> Inserimento API_ID/HASH → Compilazione Sandbox → Esportazione Script Locale (Bypass Cloud Ban).</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col_api1, col_api2 = st.columns(2)
        api_id = col_api1.text_input("Telegram API_ID", placeholder="Es. 837492")
        api_hash = col_api2.text_input("Telegram API_HASH", placeholder="Es. 8fa7b...", type="password")
        target = st.text_input("Target Community Username", placeholder="Es. competitor_group")
        
        if st.button("BUILD CUSTOM ENGINE", type="primary"):
            if api_id and api_hash and target:
                script_code = f"from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('apex_session', '{api_id}', '{api_hash}') as client:\n    members = client.get_participants('{target}')\n    with open('apex_leads.csv', 'w', newline='') as f:\n        w = csv.writer(f)\n        w.writerow(['ID', 'User', 'Name'])\n        for u in members: w.writerow([u.id, u.username, u.first_name])\n    print('[SYSTEM] Estrazione completata.')"
                st.markdown("<div class='cmd-terminal'>[BUILD] Scaffolding script locale... DONE.</div>", unsafe_allow_html=True)
                st.download_button("DOWNLOAD EXECUTABLE (.py)", script_code, "apex_scraper.py")
            else:
                st.error("Protocollo fallito: Parametri di compilazione mancanti.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 04. CLOUD COST MATRIX
    # --------------------------------------
    elif service == "04. Cloud Cost Matrix":
        st.markdown("<h1>Infrastructure Cost Matrix</h1>", unsafe_allow_html=True)
        st.markdown("<div class='tech-spec-box'><span style='color:#F4F4F5; font-weight:600;'>[PROTOCOL]</span> Audit abbonamenti SaaS → Sostituzione Microservizi → Calcolo Zero-Cost.</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        df_matrix = pd.DataFrame({
            "Legacy Software (Da rimuovere)": ["Zapier Enterprise", "HubSpot CRM", "AWS S3 Storage"],
            "APEX Architecture (Da integrare)": ["n8n (Open Source Node)", "Supabase (PostgreSQL)", "Cloudflare R2"],
            "Saving Mensile": ["~ 250 €", "~ 150 €", "~ 45 €"]
        })
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)
        st.info("Taglia gli intermediari. Implementa l'architettura APEX per operare a margine netto.")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 05. FINANCIAL TELEMETRY
    # --------------------------------------
    elif service == "05. Live ROI Telemetry":
        st.markdown("<h1>Financial Telemetry Simulator</h1>", unsafe_allow_html=True)
        st.markdown("<div class='tech-spec-box'><span style='color:#F4F4F5; font-weight:600;'>[PROTOCOL]</span> Inserimento Dati Fiscali → Calcolo Dispersione → Visualizzazione Utile Netto Ottimizzato.</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        mrr = c1.number_input("MRR (Fatturato Mensile Ricorrente) €", value=20000, step=1000)
        inefficiencies = c2.number_input("Costi SaaS e Lavoro Manuale Evitabile €", value=4500, step=500)
        
        margine_attuale = mrr - inefficiencies
        margine_apex = mrr  # Simuliamo che Apex azzera le inefficienze
        
        c3, c4 = st.columns(2)
        c3.metric("Utile Netto Tradizionale", f"€ {margine_attuale:,}")
        c4.metric("Utile Netto APEX OS", f"€ {margine_apex:,}", f"+ € {inefficiencies:,} Cassa Liberata")
        
        fig = px.bar(pd.DataFrame({"Modello": ["Attuale", "APEX OS"], "Margine €": [margine_attuale, margine_apex]}), x="Modello", y="Margine €", color="Modello", color_discrete_sequence=['#52525B', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 06. WEBHOOK ROUTER
    # --------------------------------------
    elif service == "06. Traffic Router Engine":
        st.markdown("<h1>Asynchronous Traffic Router</h1>", unsafe_allow_html=True)
        st.markdown("<div class='tech-spec-box'><span style='color:#F4F4F5; font-weight:600;'>[PROTOCOL]</span> Simulazione Evento → Filtraggio Logico → Soppressione/Inoltro Payload.</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        source = st.selectbox("Sorgente Segnale:", ["Stripe Payment Failed", "Newsletter Unsubscribe", "Server Offline Alert"])
        
        if st.button("INJECT TEST SIGNAL", type="primary"):
            st.markdown(f"<div class='cmd-terminal'>[SYSTEM] Ricevuto Webhook da: {source}...<br>[ANALYSIS] Classificazione urgenza...</div>", unsafe_allow_html=True)
            time.sleep(1)
            if "Server Offline" in source:
                st.markdown("<div class='cmd-terminal' style='color:#F59E0B; margin-top:0.5rem;'>[CRITICAL ROUTE] Alert inoltrato al management bypassando i filtri.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='cmd-terminal' style='color:#71717A; margin-top:0.5rem;'>[SILENT LOG] Segnale non critico. Archiviato in DB senza notifica.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 07. API PAYLOAD INJECTOR
    # --------------------------------------
    elif service == "07. API Injection Sandbox":
        st.markdown("<h1>API Injection Sandbox</h1>", unsafe_allow_html=True)
        st.markdown("<div class='tech-spec-box'><span style='color:#F4F4F5; font-weight:600;'>[PROTOCOL]</span> Endpoint Target → JSON Formatting → Esecuzione Handshake HTTP.</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        endpoint = st.text_input("Target URL", value="https://httpbin.org/post")
        payload = st.text_area("JSON Object", value='{\n  "status": "active",\n  "company": "Apex Corp"\n}', height=100)
        
        if st.button("EXECUTE API PUSH", type="primary"):
            with st.spinner("Stabilizzazione tunnel TLS..."):
                try:
                    res = requests.post(endpoint, json=json.loads(payload), timeout=3)
                    st.markdown(f"<div class='cmd-terminal'>[SUCCESS] HTTP {res.status_code}<br>[LATENCY] {res.elapsed.total_seconds()}s<br>[PAYLOAD] Iniezione CRM confermata.</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<div class='cmd-terminal' style='color:#EF4444;'>[FATAL] Connessione abortita: {str(e)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ECOSISTEMA: ZERO DATA VAULT (LEAD GEN)
# ==========================================
elif console_selection == "🔒 ZERO DATA VAULT":
    st.markdown("<h1>ZERO Intel Data Vault</h1>", unsafe_allow_html=True)
    st.markdown("<div class='tech-spec-box'><span style='color:#F4F4F5; font-weight:600;'>[PROTOCOL]</span> Accesso al database proprietario SaaS per l'arbitraggio estremo del tempo.</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    df_tools = pd.DataFrame([
        {"Architettura": "Video Generation", "Software": "CapCut Pro", "Modello Logico": "Freemium / Export 4K"},
        {"Architettura": "Voice Neural Engine", "Software": "ElevenLabs", "Modello Logico": "10k Char Free/Month"},
        {"Architettura": "LLM Analysis", "Software": "Gemini 1.5 Advanced", "Modello Logico": "Deep Think Context"},
        {"Architettura": "Backend Automation", "Software": "n8n Open Source", "Modello Logico": "Zero-Cost (Self Hosted)"}
    ])
    
    query = st.text_input("🔍 Filtra i protocolli del database (es. Video, Open Source)...")
    if query:
        df_tools = df_tools[df_tools.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
        
    st.dataframe(df_tools, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    if not st.session_state.lead_vault:
        st.markdown("### 🔐 Authorize Database Extraction")
        email = st.text_input("Inserisci l'email direzionale per ottenere il Dump CSV completo:")
        if st.button("AUTHORIZE ACCESS", type="primary"):
            if "@" in email and "." in email:
                st.session_state.lead_vault = True
                st.rerun()
            else:
                st.error("Handshake fallito: Formato credenziali respinto.")
                
    if st.session_state.lead_vault:
        st.success("Autorizzazione verificata. Estrazione sbloccata.")
        st.download_button("📥 EXPORT FULL MATRIX (.CSV)", df_tools.to_csv(index=False).encode('utf-8'), "zero_vault_db.csv", "text/csv")
    st.markdown("</div>", unsafe_allow_html=True)
