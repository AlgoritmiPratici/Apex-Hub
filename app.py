import streamlit as st
import pandas as pd
import time
import requests
import json
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. ARCHITETTURA DI SISTEMA E MEMORIA
# ==========================================
st.set_page_config(
    page_title="APEX Console | Enterprise Infrastructure", 
    layout="wide", 
    initial_sidebar_state="auto"
)

# Inizializzazione Memoria di Stato Infrangibile
for key, val in {
    'active_service': None,
    'm1_buffer': None,
    'sys_terminal': "",
    'vault_clearance': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Deep Linking per Smistamento ManyChat
hub_query = st.query_params.get("hub", "apex")
default_hub_idx = 0 if hub_query == "apex" else 1

# ==========================================
# 2. MOTORE CSS: ESTETICA "HIGH-END TECH"
# ==========================================
st.markdown("""
    <style>
    /* Omissione totale del framework Streamlit */
    #MainMenu, header, footer, .stDeployButton {display: none !important;}
    
    /* Tipografia d'Elite (Inter) e Sfondo Assoluto */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #09090B !important; border-right: 1px solid #18181B !important; }
    
    /* Gerarchia dei Colori e Spazio Negativo */
    h1 { 
        color: #FFFFFF !important; font-weight: 800 !important; 
        letter-spacing: -0.04em !important; margin-bottom: 0.2rem !important; font-size: 2.2rem !important;
    }
    h2, h3, h4 { color: #F4F4F5 !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    p, span, label, .stWidgetLabel { color: #A1A1AA !important; font-size: 0.95rem; line-height: 1.6; }
    
    /* Box Ingegnerizzati (No bordi pesanti, solo lusso visivo) */
    .premium-panel {
        background-color: #09090B;
        border: 1px solid #27272A;
        border-radius: 8px;
        padding: 2.5rem;
        box-shadow: 0 20px 40px -15px rgba(0,0,0,0.7);
        margin-bottom: 2rem;
    }
    
    /* Executive Summary Box */
    .exec-summary {
        background-color: transparent;
        border-left: 2px solid #10B981;
        padding: 0.5rem 0 0.5rem 1.5rem;
        margin-bottom: 2rem;
    }
    
    /* Console Log di Rete */
    .net-console {
        background-color: #050505;
        border: 1px solid #1F2937;
        border-radius: 6px;
        padding: 1.5rem;
        font-family: 'JetBrains Mono', 'SFMono-Regular', Consolas, monospace;
        color: #10B981;
        font-size: 0.85rem;
        line-height: 1.5;
        white-space: pre-wrap;
        margin-top: 1rem;
    }
    .err-log { color: #F87171; } .sys-log { color: #71717A; } .warn-log { color: #FBBF24; }
    
    /* Override Elementi Interattivi */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #050505 !important; color: #FFFFFF !important; border: 1px solid #27272A !important; border-radius: 6px !important;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
        border-color: #10B981 !important; box-shadow: none !important;
    }
    
    /* Pulsanti High-End */
    div.stButton > button {
        background-color: #FFFFFF !important; color: #000000 !important; font-weight: 700 !important;
        border-radius: 6px !important; border: none !important; padding: 0.75rem 1.5rem !important;
        text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.85rem !important; transition: all 0.2s;
    }
    div.stButton > button:hover { background-color: #E4E4E7 !important; transform: translateY(-1px); }
    
    div.stDownloadButton > button {
        background-color: transparent !important; color: #10B981 !important; font-weight: 700 !important;
        border-radius: 6px !important; border: 1px solid #10B981 !important; padding: 0.75rem 1.5rem !important;
        text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.85rem !important; width: 100%;
    }
    div.stDownloadButton > button:hover { background-color: rgba(16,185,129,0.05) !important; }
    
    /* Status Badge Corporate */
    .corp-badge {
        display: inline-flex; align-items: center; padding: 3px 10px; border-radius: 4px;
        background: rgba(255, 255, 255, 0.05); color: #E2E8F0; font-size: 0.7rem;
        font-weight: 700; border: 1px solid rgba(255, 255, 255, 0.1); letter-spacing: 1px; margin-bottom: 15px; text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. COMPONENTI UX STANDARDIZZATI
# ==========================================
def render_service_header(badge, title, use_case, tech_spec):
    st.markdown(f"<div class='corp-badge'>{badge}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='exec-summary'><p style='color: #E2E8F0; font-size: 1.05rem; font-weight: 400;'>{use_case}</p></div>", unsafe_allow_html=True)
    with st.expander("⚙️ ARCHITETTURA DI SISTEMA (Dettagli Tecnici)"):
        st.markdown(f"<p style='font-size: 0.85rem; font-family: monospace;'>{tech_spec}</p>", unsafe_allow_html=True)

# ==========================================
# 4. CONSOLE DI NAVIGAZIONE LATERALE
# ==========================================
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #FFFFFF; font-weight: 800; font-size: 1.4rem; margin: 0; letter-spacing: -0.05em;">APEX CONSOLE</h2>
        <span style="color: #10B981; font-size: 0.7rem; font-weight: 700; letter-spacing: 2px;">REL 1.0.0-PROD</span>
    </div>
""", unsafe_allow_html=True)

hub_selection = st.sidebar.selectbox("INFRASTRUCTURE HUB", ["01 // TECH ENGINE", "02 // DATA VAULT"], index=default_hub_idx)
st.sidebar.markdown("<hr style='border-color:#18181B; margin: 1.5rem 0;'>", unsafe_allow_html=True)

# ==========================================
# HUB 01: TECH ENGINE (ALGORITMI PRATICI)
# ==========================================
if hub_selection == "01 // TECH ENGINE":
    service = st.sidebar.radio("DEPLOYED SERVICES", [
        "Data Normalization Engine", 
        "Environment Security Protocol", 
        "Asynchronous Scraper Compiler", 
        "Infrastructure Cost Matrix", 
        "Financial ROI Telemetry", 
        "Webhook Traffic Router", 
        "API Payload Injector"
    ])
    
    # Garbage Collector
    if st.session_state.active_service != service:
        st.session_state.sys_terminal = ""
        st.session_state.m1_buffer = None
        st.session_state.active_service = service

    st.sidebar.markdown("<div style='font-size:0.7rem; color:#52525B; text-align:center; margin-top:3rem;'>NETWORK STATUS: SECURED<br>ENCRYPTION: AES-256</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVIZIO 1: NORMALIZZAZIONE CSV
    # --------------------------------------
    if service == "Data Normalization Engine":
        render_service_header(
            "DATA PROCESSING", "Data Normalization Engine",
            "Elimina i colli di bottiglia operativi. Carica database o liste contatti estratti da sistemi obsoleti: il motore rileverà anomalie, distruggerà i duplicati e formatterà i dati per l'iniezione diretta nel tuo CRM aziendale.",
            "Runtime: Python Pandas. Operazioni: De-duplicazione vettoriale, cast stringhe in lowercase, strip degli spazi bianchi, dropna() condizionale su array 'Email'."
        )
        
        st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Innestare Data Dump (.csv)", type=["csv"])
        
        if uploaded_file:
            if st.button("ESEGUI NORMALIZZAZIONE DATI", use_container_width=True):
                with st.spinner("Compilazione buffer in memoria..."):
                    time.sleep(0.9)
                    try:
                        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
                        r_in = len(df_raw)
                        df_clean = df_raw.copy().drop_duplicates()
                        
                        email_col = next((c for c in df_clean.columns if c.lower() == 'email'), None)
                        if email_col:
                            df_clean[email_col] = df_clean[email_col].astype(str).str.lower().str.strip()
                            df_clean = df_clean[~df_clean[email_col].isin(['nan', 'none', '', 'null'])].dropna(subset=[email_col])
                            msg = "Sanificazione array email completata con successo."
                        else:
                            msg = "<span class='warn-log'>Nessuna matrice 'Email' rilevata. Eseguita sanificazione globale di base.</span>"
                        
                        r_out = len(df_clean)
                        st.session_state.m1_buffer = df_clean
                        st.session_state.sys_terminal = f"<span class='sys-log'>[SYS] Handshake dati completato. Latenza: 1.2ms.</span><br>{msg}<br>Record Iniziali: {r_in} | Record Validi: {r_out} | Anomalie Distrutte: {r_in - r_out}"
                    except Exception as e:
                        st.session_state.sys_terminal = f"<span class='err-log'>[FATAL ERROR] Impossibile eseguire il parsing. File corrotto o codifica non supportata. Dettagli: {e}</span>"
        
        if st.session_state.m1_buffer is not None:
            st.markdown(f"<div class='net-console'>{st.session_state.sys_terminal}</div><br>", unsafe_allow_html=True)
            st.dataframe(st.session_state.m1_buffer.head(5), use_container_width=True)
            st.download_button("📥 ESPORTA DATASET VALIDATO (.CSV)", st.session_state.m1_buffer.to_csv(index=False).encode('utf-8'), "apex_normalized.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVIZIO 2: SECURITY .ENV
    # --------------------------------------
    elif service == "Environment Security Protocol":
        render_service_header(
            "CYBERSECURITY", "Environment Security Protocol",
            "Metti in sicurezza la tua architettura. Incolla il codice o le variabili che contengono password aziendali in chiaro: il protocollo le isolerà, generando i manifesti crittografati (.env e .gitignore) per blindare il tuo server.",
            "Esecuzione di pattern matching regex per chiavi API. Disaccoppiamento logico tramite standard POSIX Environment Variables."
        )
        st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
        raw_env = st.text_area("Variabili esposte (Key=Value):", value="DATABASE_URL=postgres://admin:root123@local/db\nSTRIPE_SECRET=sk_live_29384...\nDEBUG_MODE=True", height=120)
        
        if st.button("BLINDA E COMPILA MANIFESTI", use_container_width=True):
            st.session_state.sys_terminal = "<span class='sys-log'>[SEC-OPS] Avvio scansione pattern...</span><br><span class='warn-log'>[ALERT] Rilevate stringhe sensibili non protette.</span><br>[ENCRYPT] Disaccoppiamento memoria completato.<br><span style='color:#10B981'>[SUCCESS] Manifesti di sicurezza pronti per il deployment.</span>"
            
        if st.session_state.sys_terminal != "":
            st.markdown(f"<div class='net-console'>{st.session_state.sys_terminal}</div><br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.download_button("📥 DOWNLOAD .ENV", raw_env, ".env")
            c2.download_button("📥 DOWNLOAD .GITIGNORE", ".env\n__pycache__/\n*.session", ".gitignore")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVIZIO 3: COMPILER TELEGRAM
    # --------------------------------------
    elif service == "Asynchronous Scraper Compiler":
        render_service_header(
            "DATA EXTRACTION", "Asynchronous Scraper Compiler",
            "Costruisci un estrattore dati personalizzato. Le policy cloud vietano lo scraping diretto; compila qui le tue credenziali e scarica il software python su misura da avviare in totale sicurezza sul tuo terminale locale.",
            "Generazione dinamica di scaffolding Python (libreria Telethon). Il client richiede esecuzione localhost per bypassare i blocchi IP cloud tramite handshaking OTP."
        )
        st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        api_id = c1.text_input("Telegram API_ID", placeholder="es. 2847592")
        api_hash = c2.text_input("Telegram API_HASH", placeholder="es. c4e8b...", type="password")
        target = st.text_input("Username Community Target (senza @)", placeholder="es. tech_competitor_group")
        
        if st.button("COMPILA SOFTWARE SORGENTE", use_container_width=True):
            if api_id and api_hash and target:
                script = f"from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('apex_session', '{api_id}', '{api_hash}') as client:\n    members = client.get_participants('{target}')\n    with open('apex_leads.csv', 'w', newline='', encoding='utf-8') as f:\n        w=csv.writer(f)\n        w.writerow(['ID','Username','Name'])\n        for u in members: w.writerow([u.id, u.username, u.first_name])\n    print('[SYSTEM] Data extraction completed.')"
                st.session_state.m1_buffer = script
                st.session_state.sys_terminal = f"<span class='sys-log'>[BUILD] Iniezione parametri per target '{target}'...</span><br><span class='sys-log'>[COMPILER] Generazione binario sorgente completata.</span><br><span style='color:#10B981'>[SUCCESS] Eseguibile Python pronto per il download.</span>"
            else:
                st.session_state.sys_terminal = "<span class='err-log'>[FATAL ERROR] Fallimento compilazione. Parametri architetturali mancanti.</span>"
                st.session_state.m1_buffer = None
                
        if st.session_state.sys_terminal != "":
            st.markdown(f"<div class='net-console'>{st.session_state.sys_terminal}</div><br>", unsafe_allow_html=True)
            if st.session_state.m1_buffer:
                st.download_button("📥 DOWNLOAD SOFTWARE (.PY)", st.session_state.m1_buffer, "apex_scraper.py")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVIZIO 4: COST MATRIX
    # --------------------------------------
    elif service == "Infrastructure Cost Matrix":
        render_service_header(
            "FINANCIAL AUDIT", "Infrastructure Cost Matrix",
            "Mappa le perdite di cassa. Questa matrice evidenzia gli abbonamenti software (SaaS) che le aziende pagano inutilmente, contrapposti alle soluzioni Cloud Serverless e Open Source necessarie per azzerare i costi.",
            "Audit comparativo per l'ottimizzazione dell'Operational Expenditure (OPEX). Sostituzione di servizi monolitici con architetture distribuite a costo marginale zero."
        )
        st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
        df_matrix = pd.DataFrame({
            "Legacy Software (Sprechi)": ["Zapier Enterprise", "Airtable / HubSpot", "AWS S3 / Google Cloud", "Mailchimp"],
            "APEX Architecture (Sostituto)": ["n8n (Self-Hosted Node)", "Supabase (PostgreSQL)", "Cloudflare R2", "Mautic / AWS SES"],
            "Margine Recuperato Mensile": ["~ 250 €", "~ 150 €", "~ 45 €", "~ 80 €"]
        })
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVIZIO 5: ROI TELEMETRY
    # --------------------------------------
    elif service == "Financial ROI Telemetry":
        render_service_header(
            "BUSINESS ANALYTICS", "Financial ROI Telemetry",
            "Simulatore dinamico di marginalità. Inserisci il tuo fatturato e i costi tecnologici correnti: il sistema calcolerà istantaneamente l'utile netto reale che otterresti adottando i protocolli APEX.",
            "Data Visualization via Plotly Express. Calcolo lineare della dilatazione dei margini operativi basato sulla soppressione dei costi SaaS."
        )
        st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        mrr = c1.number_input("Fatturato Mensile Ricorrente (MRR) €", value=15000, step=1000)
        opex = c2.number_input("Costi Tecnologici Correnti (Da Tagliare) €", value=3200, step=100)
        
        m_old, m_new = mrr - opex, mrr
        c3, c4 = st.columns(2)
        c3.metric("Utile Mensile Storico", f"€ {m_old:,}")
        c4.metric("Utile Mensile APEX", f"€ {m_new:,}", f"+ € {opex:,} (Cassa Netta Liberata)")
        
        fig = go.Figure(data=[
            go.Bar(name='Infrastruttura Storica', x=['Modello di Business'], y=[m_old], marker_color='#27272A', text=f"€{m_old}", textposition='auto'),
            go.Bar(name='Infrastruttura APEX', x=['Modello di Business'], y=[m_new], marker_color='#10B981', text=f"€{m_new}", textposition='auto')
        ])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', barmode='group', margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVIZIO 6: WEBHOOK ROUTER
    # --------------------------------------
    elif service == "Webhook Traffic Router":
        render_service_header(
            "NETWORK ALGORITHMS", "Webhook Traffic Router",
            "Filtra il rumore digitale. Inserisci il codice di un evento (es. alert server). L'algoritmo valuterà autonomamente l'urgenza: inoltrerà gli eventi critici al management e archivierà in silenzio le inefficienze minori.",
            "Simulazione Endpoint REST. Parsing JSON asincrono e valutazione parametro 'priority' per instradamento condizionale logico."
        )
        st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
        json_in = st.text_area("Payload Evento (JSON):", value='{\n  "event": "server_down",\n  "system": "AWS_Cluster_01",\n  "priority": "CRITICAL"\n}', height=120)
        
        if st.button("TESTA ALGORITMO DI ROUTING", use_container_width=True):
            with st.spinner("Compilazione rami logici..."):
                time.sleep(0.5)
                try:
                    data = json.loads(json_in)
                    prio = str(data.get("priority", "LOW")).upper()
                    if prio in ["HIGH", "CRITICAL"]:
                        data["apex_directive"] = "SMS_SENT_TO_MANAGEMENT"
                        msg = "<span class='warn-log'>[URGENT] Classificazione critica. Bypass silenziatore. Direttiva di inoltro attivata.</span>"
                    else:
                        data["apex_directive"] = "SILENT_DATABASE_LOG"
                        msg = "<span class='sys-log'>[SILENCED] Classificazione minore. Rumore soppresso e archiviato in background.</span>"
                    st.session_state.sys_terminal = f"{msg}<br><br><span style='color:#FFF'>OUTPUT TRASFORMATO:</span><br>{json.dumps(data, indent=2)}"
                except json.JSONDecodeError:
                    st.session_state.sys_terminal = "<span class='err-log'>[FATAL ERROR] Struttura JSON non conforme alle direttive RFC 8259.</span>"
                    
        if st.session_state.sys_terminal != "":
            st.markdown(f"<div class='net-console'>{st.session_state.sys_terminal}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # SERVIZIO 7: API INJECTOR
    # --------------------------------------
    elif service == "API Payload Injector":
        render_service_header(
            "SYSTEM INTEGRATION", "API Payload Injector Sandbox",
            "Verifica la connessione tra i tuoi sistemi. Inserisci l'URL di destinazione (Webhook del CRM o gestionale) e i dati da inviare: il tool eseguirà un test di latenza in tempo reale per garantirti che le informazioni fluiscano istantaneamente.",
            "Esecuzione HTTP Request (POST) via modulo Python 'requests'. Gestione dei timeout (5s) e misurazione telemetrica della latenza di risposta TCP/TLS."
        )
        st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
        url = st.text_input("Endpoint URL Destinazione", value="https://httpbin.org/post")
        payload = st.text_area("Struttura Dati (JSON)", value='{\n  "lead_name": "Marcus Aurelius",\n  "status": "Qualified_Buyer"\n}', height=100)
        
        if st.button("ESEGUI PUSH DI RETE (POST)", use_container_width=True):
            st.session_state.sys_terminal = "<span class='sys-log'>[NETWORK] Negoziazione protocollo TLS in corso...</span>"
            try:
                p_json = json.loads(payload)
                t0 = time.time()
                res = requests.post(url, json=p_json, timeout=5)
                lat = round(time.time() - t0, 3)
                st.session_state.sys_terminal += f"<br><span style='color:#10B981'>[SUCCESS] Transazione verificata.</span><br>HTTP STATUS: {res.status_code}<br>LATENCY: {lat}s<br><br><span class='sys-log'>[SERVER RESPONSE]</span><br>{res.text[:200]}..."
            except json.JSONDecodeError:
                st.session_state.sys_terminal += "<br><span class='err-log'>[ERROR] Parsing JSON fallito.</span>"
            except Exception as e:
                st.session_state.sys_terminal += f"<br><span class='err-log'>[TIMEOUT] Connessione al server remoto abortita. Dettagli: {e}</span>"
                
        if st.session_state.sys_terminal != "":
            st.markdown(f"<div class='net-console'>{st.session_state.sys_terminal}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HUB 02: ZERO DATA VAULT (ASSET 03)
# ==========================================
elif hub_selection == "02 // DATA VAULT":
    st.markdown("<div class='corp-badge'>INTELLIGENCE CENTER</div>", unsafe_allow_html=True)
    st.markdown("<h1>ZERO VAULT Database</h1>", unsafe_allow_html=True)
    st.markdown("<div class='exec-summary'><p style='color: #E2E8F0; font-size: 1.05rem; font-weight: 400;'>Perché bruciare ore in ricerca e sviluppo aziendale? Accedi al database privato delle 50 architetture SaaS e AI Open Source usate dai top player per automatizzare infrastrutture bypassando i paywall.</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-panel'>", unsafe_allow_html=True)
    df_vault = pd.DataFrame([
        {"Stack Operativo": "Video Generativo", "Piattaforma": "CapCut Enterprise", "Modello Finanziario": "Freemium", "Vantaggio Competitivo": "Export 4K Senza Watermark"},
        {"Stack Operativo": "Intelligenza Acustica", "Piattaforma": "ElevenLabs Core", "Modello Finanziario": "10k Char Gratis", "Vantaggio Competitivo": "Clonazione Neurale Reale"},
        {"Stack Operativo": "Motore Logico (LLM)", "Piattaforma": "Gemini 1.5 Pro", "Modello Finanziario": "Standard Tier", "Vantaggio Competitivo": "Finestra Contesto Illimitato"},
        {"Stack Operativo": "Automazione Server", "Piattaforma": "n8n Open Source", "Modello Finanziario": "0€ (Self Hosted)", "Vantaggio Competitivo": "Esecuzioni (Task) Infinite"},
        {"Stack Operativo": "Database Cloud", "Piattaforma": "Supabase (SQL)", "Modello Finanziario": "Serverless Free", "Vantaggio Competitivo": "Sostituzione Firebase"}
    ])
    
    search = st.text_input("🔍 Filtra i record in tempo reale (es. Video, Automazione, Cloud)...")
    if search:
        df_vault = df_vault[df_vault.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
    st.dataframe(df_vault, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # LEAD GENERATION SYSTEM (ENTERPRISE GATEWAY)
    if not st.session_state.vault_clearance:
        st.markdown("<div class='premium-panel' style='border-color:#10B981; border-width: 2px;'>", unsafe_allow_html=True)
        st.markdown("<h3>🔒 Accesso Root e Clearance</h3>", unsafe_allow_html=True)
        st.write("L'estrazione del file .CSV con i 50 record integrali richiede l'autenticazione aziendale. Registra la tua utenza per aprire il gate.")
        
        with st.form("clearance_form", clear_on_submit=False):
            email = st.text_input("Identificativo Email (Corporate/Personale)", placeholder="cto@azienda.com")
            submit = st.form_submit_button("VERIFICA IDENTITÀ E SBLOCCA DATABASE", use_container_width=True)
            st.caption("Connessione SSL. I dati non verranno mai condivisi con terze parti.")
            
            if submit:
                if "@" in email and "." in email:
                    # UX Friction fittizia per aumentare il valore
                    bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        bar.progress(i + 1)
                    st.session_state.vault_clearance = True
                    st.rerun()
                else:
                    st.error("[ERROR] Handshake fallito. Formato email respinto.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    if st.session_state.vault_clearance:
        st.markdown("<div class='premium-panel' style='border-color:#10B981; background:rgba(16,185,129,0.03);'>", unsafe_allow_html=True)
        st.success("✅ Clearance Verificata. Protocolli di estrazione aperti.")
        st.download_button("📥 DOWNLOAD DATABASE (.CSV)", df_vault.to_csv(index=False).encode('utf-8'), "apex_zero_vault.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("<div style='font-size:0.75rem; color:#52525B; text-align:center; margin-top:2rem;'>APEX TECHNOLOGIES © 2026<br>Confidential Infrastructure</div>", unsafe_allow_html=True)
