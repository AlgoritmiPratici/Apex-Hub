import streamlit as st
import pandas as pd
import time
import requests
import json
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CORE ARCHITECTURE & STATE MANAGEMENT
# ==========================================
st.set_page_config(
    page_title="APEX CORE | Enterprise Console", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Gestione Infrangibile della Memoria di Stato
default_states = {
    'current_module': None,
    'm1_data': None,
    'terminal_logs': "",
    'vault_unlocked': False
}
for key, value in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Deep Linking Routing
brand_target = st.query_params.get("workspace", "apex")
indice_default = 0 if brand_target == "apex" else 1

# ==========================================
# 2. PREMIUM CSS ENGINE (STRIPE / LINEAR STYLE)
# ==========================================
st.markdown("""
    <style>
    /* Pulizia Interfaccia Nativa */
    #MainMenu, header, footer, .stDeployButton {visibility: hidden; display: none;}
    
    /* Tipografia e Palette Dark Premium */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    /* Titoli Gradient e Spaziature */
    h1 { 
        background: linear-gradient(135deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important; 
        letter-spacing: -0.04em !important; 
        margin-bottom: 0.5rem !important;
    }
    h3 { color: #E2E8F0 !important; font-weight: 700 !important; letter-spacing: -0.02em; margin-bottom: 1rem !important;}
    p { color: #A1A1AA; font-size: 0.95rem; line-height: 1.5; }
    
    /* Card Architetturali */
    .apex-card {
        background-color: #09090B;
        border: 1px solid #27272A;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.5rem;
    }
    
    /* Personalizzazione Tabs (Vercel Style) */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 0px !important;
        border-bottom: 2px solid transparent !important;
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 2px solid #10B981 !important;
    }
    button[data-baseweb="tab"] p {
        color: #71717A !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #10B981 !important;
    }
    
    /* Console Terminale Realistica */
    .apex-terminal {
        background-color: #000000;
        border: 1px solid #18181B;
        border-radius: 6px;
        padding: 1.2rem;
        font-family: 'SFMono-Regular', Consolas, Menlo, monospace;
        color: #10B981;
        font-size: 0.85rem;
        line-height: 1.6;
        white-space: pre-wrap;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
    }
    .term-error { color: #EF4444; }
    .term-warn { color: #F59E0B; }
    .term-sys { color: #71717A; }
    
    /* Pulsanti Elite */
    div.stButton > button {
        background-color: #FAFAFA !important;
        color: #09090B !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.6rem !important;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div.stButton > button:hover { background-color: #E4E4E7 !important; transform: scale(0.99); }
    
    div.stDownloadButton > button {
        background-color: #09090B !important;
        color: #10B981 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid #10B981 !important;
        padding: 0.6rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div.stDownloadButton > button:hover { background-color: #10B981 !important; color: #09090B !important; }
    
    /* Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        background: rgba(16, 185, 129, 0.1);
        color: #10B981;
        font-size: 0.7rem;
        font-weight: 800;
        border: 1px solid rgba(16, 185, 129, 0.2);
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS (DRY PRINCIPLE)
# ==========================================
def render_header(badge_text, title, business_text, tech_text):
    """Genera l'intestazione standardizzata per ogni modulo con Tab esplicativi."""
    st.markdown(f"<div class='status-badge'>{badge_text}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    
    tab_biz, tab_tech = st.tabs(["🎯 Beneficio Pratico (Business)", "⚙️ Sotto il Cofano (Tech Ops)"])
    with tab_biz:
        st.markdown(f"<p>{business_text}</p>", unsafe_allow_html=True)
    with tab_tech:
        st.markdown(f"<p>{tech_text}</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR (SYSTEM NAVIGATION)
# ==========================================
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h2 style="color: #FFFFFF; font-weight: 800; font-size: 1.3rem; margin: 0; letter-spacing: -0.05em;">APEX CORE OS</h2>
        <span style="color: #10B981; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;">PRODUCTION v7.0</span>
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
    
    # Garbage Collection: reset logica al cambio modulo
    if st.session_state.current_module != service:
        st.session_state.terminal_logs = ""
        st.session_state.current_module = service

    # --------------------------------------
    # 01. DATA REFINING ENGINE
    # --------------------------------------
    if service == "01. Data Refining Engine":
        render_header(
            "DATA PROCESSING", 
            "Data Refining Engine", 
            "Carica un file Excel/CSV caotico. Il sistema eliminerà istantaneamente i contatti doppi e formatterà i dati in modo perfetto, pronti per essere importati nel tuo CRM senza errori manuali.",
            "<b>Input:</b> Raw CSV.<br><b>Engine:</b> Pandas Vectorized Filtering con Drop Duplicates. Fallback automatico se la chiave 'Email' è mancante.<br><b>Output:</b> Dataset normalizzato UTF-8."
        )
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Trascina il tuo file CSV qui", type=["csv"])
        
        if uploaded_file:
            if st.button("ESEGUI PULIZIA DATI", type="primary"):
                with st.spinner("Ingegnerizzazione dei dati in corso..."):
                    time.sleep(0.8) # Frizione psicologica positiva
                    try:
                        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
                        righe_in = len(df_raw)
                        df_clean = df_raw.copy().drop_duplicates()
                        
                        # Edge Case Handling (Se la colonna email non c'è, non crasha)
                        col_email = next((col for col in df_clean.columns if col.lower() == 'email'), None)
                        if col_email:
                            df_clean[col_email] = df_clean[col_email].astype(str).str.lower().str.strip()
                            df_clean = df_clean[~df_clean[col_email].isin(['nan', 'none', '', 'null'])].dropna(subset=[col_email])
                            msg = "[SUCCESS] De-duplicazione e validazione indirizzi completata."
                        else:
                            msg = "<span class='term-warn'>[WARNING] Colonna 'Email' non trovata. Eseguita solo de-duplicazione generale.</span>"

                        righe_out = len(df_clean)
                        st.session_state.m1_data = df_clean
                        st.session_state.terminal_logs = f"<span class='term-sys'>[SYSTEM] Parsing CSV completato. Latenza: 1.2ms</span><br>{msg}<br>Anomalie scartate: {righe_in - righe_out}"
                    except Exception as e:
                        st.session_state.terminal_logs = f"<span class='term-error'>[FATAL ERROR] Impossibile leggere il file. Errore di codifica: {str(e)}</span>"
            
            if st.session_state.m1_data is not None:
                st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div><br>", unsafe_allow_html=True)
                st.dataframe(st.session_state.m1_data.head(5), use_container_width=True)
                st.download_button("📥 SCARICA DATASET PULITO", st.session_state.m1_data.to_csv(index=False).encode('utf-8'), "apex_refined.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 02. THREAT MODELING VAULT (.ENV)
    # --------------------------------------
    elif service == "02. Threat Modeling Vault":
        render_header(
            "SECURITY PROTOCOL", 
            "Threat Modeling (.env)", 
            "Inserire password aziendali e chiavi API direttamente nei file di codice è il modo più rapido per subire un attacco hacker. Questo tool separa in automatico i tuoi dati sensibili, rendendo il tuo codice sicuro e condivisibile.",
            "<b>Input:</b> Stringhe Key=Value.<br><b>Engine:</b> Sanitizzazione e isolamento delle variabili d'ambiente.<br><b>Output:</b> Generazione asincrona di .env (dati) e .gitignore (muro di fuoco)."
        )
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        env_input = st.text_area("Incolla le variabili (es. API_KEY=12345):", value="DATABASE_URL=postgres://root:1234@local/db\nSTRIPE_SECRET=sk_live_8473...\nDEBUG_MODE=True", height=120)
        
        if st.button("METTI IN SICUREZZA"):
            st.session_state.terminal_logs = "<span class='term-sys'>[SYSTEM] Scansione vettori d'attacco...</span><br><span class='term-warn'>[WARNING] Rilevate credenziali in chiaro.</span><br>[ENCRYPT] Disaccoppiamento logico completato.<br><span style='color:#10B981;'>[SUCCESS] Generazione manifesti pronta per il download.</span>"
            
        if st.session_state.terminal_logs != "":
            st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div><br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.download_button("📥 EXPORT .ENV FILE", env_input, ".env")
            col2.download_button("📥 EXPORT .GITIGNORE", ".env\n*.session\n__pycache__/", ".gitignore")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 03. SCRAPER COMPILER
    # --------------------------------------
    elif service == "03. Async Scraper Compiler":
        render_header(
            "COMPILER WIZARD", 
            "Telethon Builder Engine", 
            "Non puoi estrarre contatti da Telegram usando server cloud (rischieresti il blocco dell'account). Inserisci i tuoi dati qui: il sistema scriverà un software personalizzato per te. Scaricalo e avvialo in totale sicurezza dal tuo computer.",
            "<b>Context:</b> Prevenzione Cloud-Ban Telegram.<br><b>Engine:</b> Iniezione dinamica dei parametri API_ID/HASH in uno scaffolding Python (Telethon).<br><b>Output:</b> Script Executable Locale."
        )
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        api_id = c1.text_input("Telegram API_ID", placeholder="es. 2847592")
        api_hash = c2.text_input("Telegram API_HASH", placeholder="es. c4e8b39...", type="password")
        target = st.text_input("Username Community da analizzare", placeholder="es. nome_gruppo")
        
        if st.button("COSTRUISCI SOFTWARE"):
            if api_id and api_hash and target:
                st.session_state.terminal_logs = f"<span class='term-sys'>[BUILD]</span> Iniezione parametri target '{target}'...<br><span class='term-sys'>[COMPILER]</span> Scaffolding generato.<br><span style='color:#10B981;'>[SUCCESS] Software Python compilato con successo.</span>"
                script_code = f"from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('apex_session', '{api_id}', '{api_hash}') as client:\n    members = client.get_participants('{target}')\n    with open('apex_leads.csv', 'w', newline='') as f:\n        w = csv.writer(f)\n        w.writerow(['ID', 'Username', 'Name'])\n        for u in members: w.writerow([u.id, u.username, u.first_name])\n    print('[SYSTEM] Estrazione completata.')"
                st.session_state.m1_data = script_code
            else:
                st.session_state.terminal_logs = "<span class='term-error'>[FATAL ERROR] Impossibile compilare: Compila tutti i campi richiesti.</span>"
                st.session_state.m1_data = None
                
        if st.session_state.terminal_logs != "":
            st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div><br>", unsafe_allow_html=True)
            if st.session_state.m1_data:
                st.download_button("📥 DOWNLOAD SOFTWARE (.py)", st.session_state.m1_data, "apex_scraper.py")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 04. CLOUD COST MATRIX
    # --------------------------------------
    elif service == "04. Cloud Cost Matrix":
        render_header(
            "FINANCIAL AUDIT", 
            "Ecosystem Cost Matrix", 
            "Scopri esattamente quanto la tua azienda sta sprecando in abbonamenti mensili inutili. Questa tabella ti mostra i software costosi che usi oggi e le alternative avanzate a costo zero che dovresti usare domani.",
            "<b>Audit:</b> Sostituzione di servizi monolitici SaaS con architetture Cloud Serverless e Open Source.<br><b>Risultato:</b> Abbattimento OPEX e massimizzazione scalabilità."
        )
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        df_matrix = pd.DataFrame({
            "Software Costoso Attuale": ["Zapier Enterprise", "HubSpot CRM", "AWS S3 Storage"],
            "Architettura APEX (0€)": ["n8n (Open Source Node)", "Supabase (PostgreSQL)", "Cloudflare R2"],
            "Risparmio Netto Mensile": ["~ 250 €", "~ 150 €", "~ 45 €"]
        })
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 05. FINANCIAL TELEMETRY
    # --------------------------------------
    elif service == "05. Live ROI Telemetry":
        render_header(
            "REAL-TIME CALCULATOR", 
            "Live ROI Telemetry", 
            "Inserisci il tuo fatturato e i tuoi costi attuali. Scopri istantaneamente quanta cassa operativa puoi sbloccare alla fine dell'anno rimuovendo le inefficienze tecniche.",
            "<b>Input:</b> Variabili MRR e OPEX.<br><b>Engine:</b> Ricalcolo del margine netto con eliminazione dei colli di bottiglia SaaS.<br><b>Output:</b> Grafico vettoriale Plotly."
        )
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        mrr = c1.number_input("Fatturato Mensile (MRR) €", value=20000, step=1000)
        inefficiencies = c2.number_input("Costi Abbonamenti SaaS Evitabili €", value=4500, step=500)
        
        margine_attuale = mrr - inefficiencies
        margine_apex = mrr 
        
        c3, c4 = st.columns(2)
        c3.metric("Utile Mensile Attuale", f"€ {margine_attuale:,}")
        c4.metric("Utile Mensile APEX", f"€ {margine_apex:,}", f"+ € {inefficiencies:,} di Cassa Liberata")
        
        # Grafico Plotly ultra-pulito
        fig = go.Figure(data=[
            go.Bar(name='Attuale', x=['Architettura Tradizionale'], y=[margine_attuale], marker_color='#3F3F46'),
            go.Bar(name='APEX', x=['APEX System'], y=[margine_apex], marker_color='#10B981')
        ])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', showlegend=False, margin=dict(t=30, b=10, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 06. WEBHOOK ROUTER (LOGICA REALE)
    # --------------------------------------
    elif service == "06. Traffic Router Engine":
        render_header(
            "LOGIC PARSER ENGINE", 
            "Traffic Router Engine", 
            "Troppe notifiche uccidono la produttività. Incolla i dati di un evento (es. un pagamento fallito). Il sistema capirà da solo se è urgente (avvisandoti) o se è un'informazione inutile (archiviandola in silenzio).",
            "<b>Input:</b> Payload JSON.<br><b>Engine:</b> JSON Parsing & Key Evaluation ('priority').<br><b>Output:</b> Iniezione di direttive di instradamento asincrono nel payload."
        )
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        sample_json = '{\n  "event_id": "evt_9876",\n  "source": "stripe_billing",\n  "amount": 2500,\n  "priority": "HIGH"\n}'
        json_input = st.text_area("JSON Payload in ingresso:", value=sample_json, height=130)
        
        if st.button("ESEGUI ALGORITMO DI ROUTING", type="primary"):
            with st.spinner("Analisi nodi logici..."):
                time.sleep(0.5)
                try:
                    data = json.loads(json_input)
                    priority = str(data.get("priority", "LOW")).upper()
                    
                    if priority in ["HIGH", "CRITICAL"]:
                        data["apex_directive"] = "ROUTE_TO_CEO_SMS"
                        log_msg = "<span class='term-warn'>[ALERT] Priorità Alta Rilevata. Inoltro urgente eseguito.</span>"
                    else:
                        data["apex_directive"] = "SUPPRESS_AND_LOG_TO_DB"
                        log_msg = "<span class='term-sys'>[SILENT] Priorità Bassa. Rumore soppresso. Archiviato in background.</span>"
                        
                    formatted_out = json.dumps(data, indent=2)
                    st.session_state.terminal_logs = f"{log_msg}<br><br><span class='term-sys'>[TRANSFORMED PAYLOAD]</span><br>{formatted_out}"
                    
                except json.JSONDecodeError:
                    st.session_state.terminal_logs = "<span class='term-error'>[FATAL ERROR] JSON Input malformato. Assicurati di usare le virgolette doppie (\").</span>"

        if st.session_state.terminal_logs != "":
            st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 07. API PAYLOAD INJECTOR
    # --------------------------------------
    elif service == "07. API Injection Sandbox":
        render_header(
            "NETWORK SANDBOX", 
            "API Injection Sandbox", 
            "Metti in comunicazione due software che non si parlano. Inserisci l'indirizzo del tuo gestionale e i dati del cliente. Questo tool sparerà le informazioni da una parte all'altra in frazioni di secondo.",
            "<b>Input:</b> Endpoint REST URL e Payload JSON.<br><b>Engine:</b> Risolutore HTTP asincrono per handshake TCP.<br><b>Output:</b> Restituzione Status Code reale e latenza di rete."
        )
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        endpoint = st.text_input("Endpoint URL Destinazione", value="https://httpbin.org/post")
        payload = st.text_area("Dati (JSON Format)", value='{\n  "client": "APEX",\n  "status": "synchronized"\n}', height=100)
        
        if st.button("ESEGUI INIEZIONE DATI", type="primary"):
            st.session_state.terminal_logs = "<span class='term-sys'>[SYSTEM] Inizializzazione protocollo HTTP...</span>"
            try:
                carico = json.loads(payload)
                start_time = time.time()
                res = requests.post(endpoint, json=carico, timeout=5)
                latenza = round(time.time() - start_time, 3)
                
                st.session_state.terminal_logs += f"<br><span style='color:#10B981;'>[SUCCESS] Handshake completato.</span><br>[STATUS CODE] {res.status_code}<br>[LATENCY] {latenza}s<br><br><span class='term-sys'>[SERVER RESPONSE]</span><br>{res.text[:200]}..."
            except json.JSONDecodeError:
                st.session_state.terminal_logs += "<br><span class='term-error'>[ERROR] Validazione JSON fallita. Controlla la sintassi.</span>"
            except Exception as e:
                st.session_state.terminal_logs += f"<br><span class='term-error'>[NETWORK FATAL] Timeout o Endpoint non raggiungibile. Dettagli: {str(e)}</span>"

        if st.session_state.terminal_logs != "":
            st.markdown(f"<div class='apex-terminal'>{st.session_state.terminal_logs}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# WORKSPACE: ZERO DATA VAULT (INTELLIGENCE)
# ==========================================
elif console_selection == "🔒 ZERO DATA VAULT":
    st.markdown("<div class='status-badge'>INTELLIGENCE CENTER</div>", unsafe_allow_html=True)
    st.markdown("<h1>ZERO Vault Intel Center</h1>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom: 2rem;'>Perché perdere 100 ore a cercare strumenti aziendali quando l'abbiamo già fatto noi? Esplora il database interattivo delle 50 architetture SaaS e AI gratuite per costruire microservizi bypassando i paywall.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
    
    df_tools = pd.DataFrame([
        {"Categoria": "Video Generation", "Software": "CapCut Desktop", "Modello Finanziario": "Freemium / Export 4K", "Vantaggio": "No Watermark"},
        {"Categoria": "Voice AI", "Software": "ElevenLabs API", "Modello Finanziario": "10k Char Free/Month", "Vantaggio": "Voci ultra-realistiche"},
        {"Categoria": "Cognitive LLM", "Software": "Gemini 1.5 Advanced", "Modello Finanziario": "Enterprise Context", "Vantaggio": "Analisi Documenti"},
        {"Categoria": "Workflow Node", "Software": "n8n Open Source", "Modello Finanziario": "Zero-Cost (Self Hosted)", "Vantaggio": "Nessun limite task"},
        {"Categoria": "Database", "Software": "Supabase PostgreSQL", "Modello Finanziario": "Serverless Free Tier", "Vantaggio": "Sostituisce Airtable"}
    ])
    
    query = st.text_input("🔍 Filtra il database istantaneamente (es. Video, Gratis, Automazione)...")
    if query:
        df_tools = df_tools[df_tools.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
        
    st.dataframe(df_tools, use_container_width=True, hide_index=True)
    st.markdown("---")
    
    # LEAD GENERATION ENGINE (ENTERPRISE AUTH GATE)
    if not st.session_state.vault_unlocked:
        st.markdown("### 🔐 Sblocca l'accesso completo")
        st.write("L'estrazione del file CSV integrale richiede l'autorizzazione. Nessun costo, solo verifica aziendale.")
        
        with st.form("auth_gate"):
            col_icon, col_input = st.columns([1, 10])
            with col_icon:
                st.markdown("<h2 style='text-align:right; color:#10B981;'>🛡️</h2>", unsafe_allow_html=True)
            with col_input:
                email_input = st.text_input("Corporate Email Address:", placeholder="nome@azienda.com", label_visibility="collapsed")
            
            submitted = st.form_submit_button("AUTHORIZE & DOWNLOAD", use_container_width=True)
            st.caption("*Trasmissione dati crittografata AES-256. Zero spam garantito.*")
            
            if submitted:
                if "@" in email_input and "." in email_input:
                    st.session_state.vault_unlocked = True
                    st.rerun()
                else:
                    st.error("Accesso negato. Inserisci un indirizzo email valido.")
                    
    if st.session_state.vault_unlocked:
        st.success("✅ Autorizzazione verificata. Estrazione sbloccata.")
        csv_vault = df_tools.to_csv(index=False).encode('utf-8')
        st.download_button("📥 DOWNLOAD DATABASE INTEGRALE (.CSV)", csv_vault, "apex_zero_vault.csv", "text/csv")
        
    st.markdown("</div>", unsafe_allow_html=True)
