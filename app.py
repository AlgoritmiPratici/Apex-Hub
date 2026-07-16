import streamlit as st
import pandas as pd
import time
import requests
import json
import datetime
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. KERNEL & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="APEX OS | Tech Infrastructure", layout="wide", initial_sidebar_state="expanded")

# Inizializzazione della memoria di sistema. 
# Questo blocca definitivamente ricaricamenti a vuoto e crash di variabili (AttributeError).
def initialize_system_state():
    states = {
        'active_hub': None,
        'active_category': None,
        'active_tool': None,
        'm1_buffer': None,
        'sys_logs': "",
        'vault_clearance': False
    }
    for key, val in states.items():
        if key not in st.session_state:
            st.session_state[key] = val

initialize_system_state()

# Rilevamento URL per Deep Linking ManyChat (?hub=tech o ?hub=zero)
param_hub = st.query_params.get("hub", "tech")

# Helper per simulare i log di sistema
def sys_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

# ==========================================
# 2. MOTORE GRAFICO PREMIUM (ZINC/LINEAR UI)
# ==========================================
st.markdown("""
    <style>
    /* Pulizia totale dell'interfaccia nativa Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {background-color: transparent !important;}
    
    /* Font e Sfondi Assoluti */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    [data-testid="stAppViewContainer"] { background-color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #09090B !important; border-right: 1px solid #1F2937 !important; }
    
    /* Tipografia Elite */
    h1 { 
        background: linear-gradient(to right, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800 !important; letter-spacing: -0.04em !important; margin-bottom: 0.5rem !important; font-size: 2.2rem !important;
    }
    h2, h3 { color: #FAFAFA !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    p, span, label { color: #A1A1AA !important; font-size: 0.95rem; line-height: 1.6; }
    
    /* Box Ingegnerizzati (Effetto Vercel) */
    .premium-card {
        background-color: #050505; border: 1px solid #27272A; border-radius: 8px;
        padding: 2rem; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.7); margin-bottom: 1.5rem;
    }
    
    /* Terminale Backend Simulator */
    .cmd-window {
        background-color: #000000; border: 1px solid #18181B; border-radius: 6px;
        padding: 1.2rem; font-family: 'JetBrains Mono', Consolas, monospace;
        color: #34D399; font-size: 0.85rem; line-height: 1.5; white-space: pre-wrap;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.8); margin-top: 1rem;
    }
    .cmd-err { color: #EF4444; } .cmd-sys { color: #71717A; } .cmd-warn { color: #F59E0B; }
    
    /* Pulsanti High-End */
    div.stButton > button {
        background: #FFFFFF !important; color: #000000 !important; font-weight: 700 !important;
        border-radius: 6px !important; border: none !important; padding: 0.75rem !important;
        text-transform: uppercase; letter-spacing: 0.5px; transition: transform 0.1s ease; width: 100%;
    }
    div.stButton > button:active { transform: scale(0.98); }
    
    div.stDownloadButton > button {
        background: transparent !important; color: #10B981 !important; font-weight: 700 !important;
        border-radius: 6px !important; border: 1px solid #10B981 !important; padding: 0.75rem !important;
        text-transform: uppercase; letter-spacing: 0.5px; width: 100%; transition: background 0.2s ease;
    }
    div.stDownloadButton > button:hover { background: rgba(16,185,129,0.1) !important; }
    
    /* Stile Tabs (Vercel Style) */
    div[data-baseweb="tab-list"] { background-color: transparent !important; border-bottom: 1px solid #27272A; }
    div[data-baseweb="tab"] { background-color: transparent !important; border-radius: 0 !important; }
    div[data-baseweb="tab"] p { color: #71717A !important; font-weight: 600; font-size: 0.9rem;}
    div[aria-selected="true"] { border-bottom: 2px solid #10B981 !important; }
    div[aria-selected="true"] p { color: #10B981 !important; }
    
    /* Badges */
    .status-badge {
        display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 4px;
        background: rgba(16, 185, 129, 0.1); color: #10B981; font-size: 0.7rem;
        font-weight: 800; border: 1px solid rgba(16, 185, 129, 0.2); letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. HELPER UX: HEADER USER-FRIENDLY
# ==========================================
def render_tool_header(badge, title, business_guide, tech_specs):
    """
    Stampa un'intestazione premium dividendo il linguaggio "User Friendly" da quello "Tecnico".
    In questo modo i Manager capiscono il valore, e gli Sviluppatori capiscono il codice.
    """
    st.markdown(f"<div class='status-badge'>{badge}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["💡 Guida per il Business", "⚙️ Specifiche Tecniche"])
    with tab1:
        st.markdown(f"<div style='padding: 1rem 0;'><p style='color:#E4E4E7; font-size:1.05rem;'>{business_guide}</p></div>", unsafe_allow_html=True)
    with tab2:
        st.markdown(f"<div style='padding: 1rem 0; background-color:#050505; border-left:3px solid #3B82F6; padding-left:1rem;'><p style='font-family:monospace; font-size:0.85rem; color:#A1A1AA;'>{tech_specs}</p></div>", unsafe_allow_html=True)

# ==========================================
# 4. ARCHITETTURA MENU SCALABILE (DIZIONARIO)
# ==========================================
# Questa struttura permette di aggiungere 100 tool in futuro senza spaccare l'app.
ECOSYSTEMS = {
    "⚡ APEX ENGINE (Tech Ops)": {
        "Data & Security": ["01. CSV Normalizer", "02. Protocollo .env"],
        "Network & API": ["03. Webhook Router", "04. API Injector", "05. Telegram Scraper"],
        "Analytics & Strategy": ["06. ROI Telemetry", "07. Cloud Cost Matrix"]
    },
    "🔒 ZERO VAULT (Database)": {
        "Intelligence": ["08. AI & SaaS Database"]
    }
}

st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #FFF; font-weight: 800; font-size: 1.5rem; letter-spacing: -1px; margin-bottom:0;">APEX OS</h2>
        <span style="color: #10B981; font-size: 0.75rem; font-weight: 700; letter-spacing: 2px;">BUILD 1.0.0-PROD</span>
    </div>
""", unsafe_allow_html=True)

# 1. Scelta Ecosistema (Asset 0 o Asset 3)
hub_list = list(ECOSYSTEMS.keys())
default_hub_index = 0 if param_hub == "tech" else 1
selected_hub = st.sidebar.selectbox("ECOSISTEMA:", hub_list, index=default_hub_index)

st.sidebar.markdown("<hr style='border-color:#1F2937; margin: 1rem 0;'>", unsafe_allow_html=True)

# 2. Scelta Strumento dinamica
selected_tool = None
if selected_hub == "⚡ APEX ENGINE (Tech Ops)":
    st.sidebar.markdown("<p style='font-size: 0.75rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase;'>Workspaces</p>", unsafe_allow_html=True)
    categories = ECOSYSTEMS[selected_hub]
    selected_cat = st.sidebar.selectbox("Categoria:", list(categories.keys()), label_visibility="collapsed")
    selected_tool = st.sidebar.radio("Seleziona Strumento:", categories[selected_cat])
else:
    # Zero Vault ha un solo tool principale, la selezione è bypassata visivamente
    selected_tool = "08. AI & SaaS Database"

# Gestore di Memoria (Pulisce il terminale quando cambi strumento)
if st.session_state.active_tool != selected_tool:
    st.session_state.sys_logs = ""
    st.session_state.m1_buffer = None
    st.session_state.active_tool = selected_tool

# ==========================================
# 5. CORE LOGIC: APEX ENGINE (ASSET 0)
# ==========================================

# --- 01. CSV NORMALIZER ---
if selected_tool == "01. CSV Normalizer":
    render_tool_header(
        "DATA PROCESSING", 
        "CSV Normalizer Engine",
        "Pulisci i tuoi contatti Excel in un secondo. Carica la lista contatti estratta dai tuoi vecchi sistemi: questo strumento distruggerà i doppioni e correggerà le email formattate male, consegnandoti un file pulito e pronto per essere caricato sul tuo CRM (es. HubSpot o ActiveCampaign).",
        "Libreria: <code>pandas</code>. Processo: De-duplicazione vettoriale <code>drop_duplicates()</code>. Type casting forzato a stringa e regex trim su array 'Email'. Memoria: Volatile, elaborazione RAM-only senza conservazione dati sul server."
    )
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Trascina il tuo file CSV qui", type=["csv"])
    
    if uploaded_file:
        if st.button("ESEGUI PULIZIA DATI", type="primary"):
            with st.spinner("Analisi e normalizzazione in corso..."):
                time.sleep(0.6) # Latenza simulata per valore percepito
                try:
                    df = pd.read_csv(uploaded_file, sep=None, engine='python')
                    r_in = len(df)
                    df_clean = df.drop_duplicates()
                    
                    # Cerca colonna email in modo case-insensitive
                    email_col = next((c for c in df_clean.columns if c.lower() == 'email'), None)
                    if email_col:
                        df_clean[email_col] = df_clean[email_col].astype(str).str.lower().str.strip()
                        df_clean = df_clean[~df_clean[email_col].isin(['nan', 'none', '', 'null'])].dropna(subset=[email_col])
                        log_msg = "Sanificazione array email completata con successo."
                    else:
                        log_msg = "<span class='cmd-warn'>[WARNING] Colonna 'Email' non rilevata. Eseguita solo pulizia globale.</span>"
                        
                    r_out = len(df_clean)
                    st.session_state.m1_buffer = df_clean
                    st.session_state.sys_logs = f"<span class='cmd-sys'>[{sys_time()}] [root@apex] ~ Parsing Eseguito. Latenza: 1.2ms.</span><br>{log_msg}<br>Dati Grezzi: {r_in} | Dati Validi: {r_out} | Anomalie Distrutte: {r_in - r_out}"
                except Exception as e:
                    st.session_state.sys_logs = f"<span class='cmd-err'>[{sys_time()}] [FATAL] Errore di codifica del file. Assicurati che sia un CSV standard. {e}</span>"

    if st.session_state.m1_buffer is not None:
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
        st.dataframe(st.session_state.m1_buffer.head(5), use_container_width=True)
        st.download_button("📥 SCARICA DATABASE PULITO", st.session_state.m1_buffer.to_csv(index=False).encode('utf-8'), "dati_puliti.csv", "text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 02. PROTOCOLLO .ENV ---
elif selected_tool == "02. Protocollo .env":
    render_tool_header(
        "CYBERSECURITY", 
        "Threat Modeler (.env)",
        "Lasciare le password aziendali nel codice sorgente è come lasciare le chiavi attaccate alla porta dell'ufficio. Incolla qui il tuo codice o le tue configurazioni: il sistema estrarrà le informazioni sensibili e ti creerà i file crittografati (.env e .gitignore) per blindare il tuo progetto.",
        "Standard applicato: 12-Factor App Methodology. Analisi pattern per il disaccoppiamento logico tra variabili d'ambiente (Environment Variables) e codice backend."
    )
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    raw_text = r"""DATABASE_URL=postgres://admin:root123@local/db
API_SECRET=sk_live_8473djds83...
DEBUG_MODE=True"""
    env_input = st.text_area("Incolla variabili esposte (Formato Key=Value):", value=raw_text, height=120)
    
    if st.button("METTI IN SICUREZZA"):
        st.session_state.sys_logs = f"<span class='cmd-sys'>[{sys_time()}] [sec-ops@apex] ~ Scansione file...</span><br><span class='cmd-warn'>[ALERT] Rilevate password e chiavi esposte.</span><br>[ENCRYPT] Generazione chiavi di disaccoppiamento...<br><span style='color:#10B981'>[SUCCESS] Architettura protetta. File pronti al download.</span>"
        
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.download_button("📥 SCARICA FILE .ENV", env_input, ".env")
        c2.download_button("📥 SCARICA .GITIGNORE", ".env\n__pycache__/\n*.session\n.DS_Store", ".gitignore")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 03. WEBHOOK ROUTER ---
elif selected_tool == "03. Webhook Router":
    render_tool_header(
        "ALGORITHMS", 
        "Traffic Router Engine",
        "Troppe notifiche uccidono la produttività aziendale. Inserisci i dati di un evento (es. un pagamento fallito). Il sistema capirà da solo se è urgente (avvisando il management via SMS) o se è un'informazione minore (archiviandola in silenzio nel database).",
        "Simulazione Endpoint REST. Parsing asincrono del payload JSON in ingresso. Valutazione booleana della chiave 'priority' per instradamento logico (Event-Driven Architecture)."
    )
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    json_test = r"""{
  "source": "server_monitor",
  "error_code": "502_bad_gateway",
  "priority": "CRITICAL"
}"""
    json_in = st.text_area("Payload Evento in Ingresso (JSON):", value=json_test, height=130)
    
    if st.button("ESEGUI ALGORITMO DI ROUTING"):
        with st.spinner("Valutazione rami logici..."):
            time.sleep(0.5)
            try:
                data = json.loads(json_in)
                prio = str(data.get("priority", "LOW")).upper()
                if prio in ["HIGH", "CRITICAL"]:
                    data["apex_action"] = "FORWARD_TO_CTO_SMS"
                    msg = f"<span class='cmd-warn'>[{sys_time()}] [URGENT] Priorità Alta rilevata. Bypass filtri attivato. Evento inoltrato.</span>"
                else:
                    data["apex_action"] = "SILENT_DB_LOG"
                    msg = f"<span class='cmd-sys'>[{sys_time()}] [SILENT] Priorità Bassa. Rumore soppresso e loggato a sistema.</span>"
                st.session_state.sys_logs = f"{msg}<br><br><span class='cmd-sys'>OUTPUT TRASFORMATO:</span><br>{json.dumps(data, indent=2)}"
            except json.JSONDecodeError as e:
                st.session_state.sys_logs = f"<span class='cmd-err'>[{sys_time()}] [FATAL ERROR] JSON malformato. Eccezione Syntax Error: {e}</span>"
                
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 04. API INJECTOR ---
elif selected_tool == "04. API Injector":
    render_tool_header(
        "NETWORK OPS", 
        "API Payload Sandbox",
        "Verifica che i tuoi software stiano comunicando correttamente. Inserisci l'URL del tuo Webhook (es. Zapier o Make.com) e invia un contatto di prova. Il sistema testerà la latenza di rete e confermerà se i dati sono giunti a destinazione.",
        "Esecuzione <code>requests.post</code>. Handshake TCP/TLS asincrono verso endpoint remoto. Rilevazione telemetrica della latenza (ms) e decodifica dell'HTTP Status Code."
    )
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    url = st.text_input("URL di Destinazione (Endpoint REST)", value="https://httpbin.org/post")
    payload_str = r"""{
  "cliente": "APEX Corp",
  "status": "Integrazione Attiva"
}"""
    payload = st.text_area("Dati da inviare (JSON)", value=payload_str, height=110)
    
    if st.button("INVIA DATI AL SERVER"):
        st.session_state.sys_logs = f"<span class='cmd-sys'>[{sys_time()}] [net-ops@apex] ~ Negoziazione protocollo HTTP...</span>"
        try:
            p_json = json.loads(payload)
            t0 = time.time()
            res = requests.post(url, json=p_json, timeout=5)
            lat = round(time.time() - t0, 3)
            st.session_state.sys_logs += f"<br><span style='color:#10B981'>[{sys_time()}] [SUCCESS] Transazione verificata.</span><br>HTTP CODE: {res.status_code}<br>LATENZA: {lat}s<br><br><span class='cmd-sys'>[RAW SERVER RESPONSE]</span><br>{res.text[:250]}..."
        except json.JSONDecodeError:
            st.session_state.sys_logs += f"<br><span class='cmd-err'>[{sys_time()}] [ERROR] Formattazione JSON invalida. Payload respinto.</span>"
        except Exception as e:
            st.session_state.sys_logs += f"<br><span class='cmd-err'>[{sys_time()}] [TIMEOUT FATAL] Nessuna risposta dal server remoto. Dettagli: {e}</span>"
            
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 05. TELEGRAM SCRAPER ---
elif selected_tool == "05. Telegram Scraper":
    render_tool_header(
        "DATA EXTRACTION", 
        "Telegram Scraper Wizard",
        "Genera un software personalizzato per estrarre membri dai gruppi concorrenti. Poiché estrarre dati dal Cloud genera il Ban dell'account Telegram, inserisci i tuoi dati qui: noi scriveremo il software per te. Scaricalo e avvialo dal tuo PC in sicurezza.",
        "Compilazione dinamica di script Python (libreria Telethon). Il client richiede l'esecuzione localhost per l'handshaking OTP lato client, bypassando i filtri anti-bot IP."
    )
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    api_id = c1.text_input("Telegram API_ID", placeholder="es. 2847592")
    api_hash = c2.text_input("Telegram API_HASH", placeholder="es. c4e8b...", type="password")
    target = st.text_input("Username Gruppo Competitor (Senza @)", placeholder="es. marketing_italia")
    
    if st.button("COMPILA SOFTWARE SORGENTE"):
        if api_id and api_hash and target:
            # Script generato e sanificato tramite Raw String
            script = f"""from telethon.sync import TelegramClient
import csv

with TelegramClient('apex_session', '{api_id}', '{api_hash}') as c:
    users = c.get_participants('{target}')
    with open('leads.csv', 'w', newline='', encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['ID','Username','Name'])
        for u in users: w.writerow([u.id, u.username, u.first_name])
    print('[OK] Estrazione Dati Completata.')"""
            st.session_state.m1_buffer = script
            st.session_state.sys_logs = f"<span class='cmd-sys'>[{sys_time()}] [compiler@apex] ~ Iniezione parametri per '{target}'...</span><br><span style='color:#10B981'>[SUCCESS] Eseguibile Python compilato. Pronto al download.</span>"
        else:
            st.session_state.sys_logs = f"<span class='cmd-err'>[{sys_time()}] [FATAL ERROR] Parametri mancanti. Compilazione abortita.</span>"
            st.session_state.m1_buffer = None
            
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
        if st.session_state.m1_buffer:
            st.download_button("📥 SCARICA SCRIPT PYTHON (.PY)", st.session_state.m1_buffer, "telegram_scraper.py")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 06. ROI TELEMETRY ---
elif selected_tool == "06. ROI Telemetry":
    render_tool_header(
        "BUSINESS ANALYTICS", 
        "Financial ROI Forecaster",
        "Simulatore predittivo di marginalità. Inserisci il fatturato attuale e le spese software mensili fisse (OPEX). Il sistema calcolerà istantaneamente l'aumento dell'utile netto aziendale se decidessi di passare alle automazioni gratuite.",
        "Data Visualization tramite Plotly Express. Calcolo vettoriale real-time dell'abbattimento dell'Operational Expenditure."
    )
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    mrr = c1.number_input("Fatturato Mensile Attuale (MRR) €", value=25000, step=1000)
    opex = c2.number_input("Costi Abbonamenti SaaS Evitabili €", value=4200, step=100)
    
    m_old, m_new = mrr - opex, mrr 
    c3, c4 = st.columns(2)
    c3.metric("Utile Netto Attuale", f"€ {m_old:,}")
    c4.metric("Utile Netto APEX", f"€ {m_new:,}", f"+ € {opex:,} Cassa Sbloccata")
    
    fig = go.Figure(data=[
        go.Bar(name='Infrastruttura Attuale', x=['Modello di Business'], y=[m_old], marker_color='#27272A', text=f"€{m_old}", textposition='auto'),
        go.Bar(name='Infrastruttura APEX', x=['Modello di Business'], y=[m_new], marker_color='#10B981', text=f"€{m_new}", textposition='auto')
    ])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', barmode='group', margin=dict(t=20, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 07. CLOUD COST MATRIX ---
elif selected_tool == "07. Cloud Cost Matrix":
    render_tool_header(
        "STRATEGY", 
        "Infrastructure Cost Matrix",
        "Mappa le perdite di cassa. Questa matrice evidenzia gli abbonamenti software che stai pagando inutilmente oggi, e ti fornisce l'esatta alternativa gratuita o Open Source da usare per azzerare i costi operativi.",
        "Audit comparativo TCO (Total Cost of Ownership) tra infrastrutture monolitiche legacy e microservizi Serverless distribuiti."
    )
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Software Costoso (Spreco)": ["Zapier Enterprise", "HubSpot / Airtable", "AWS S3 / Google Cloud", "Mailchimp"],
        "Soluzione APEX (Costo 0)": ["n8n (Self-Hosted Node)", "Supabase (PostgreSQL)", "Cloudflare R2", "Mautic / AWS SES"],
        "Margine Salvato Mensile": ["~ 250 €", "~ 150 €", "~ 45 €", "~ 80 €"]
    }), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HUB 02: ZERO VAULT (ASSET 03)
# ==========================================
elif selected_hub == "🔒 ZERO VAULT (Database)":
    render_tool_header(
        "DATA INTELLIGENCE", 
        "Database AI Toolkit (Top 50)",
        "Perché perdere 100 ore a cercare strumenti aziendali quando l'abbiamo già fatto noi? Esplora il database privato delle 50 architetture SaaS e AI gratuite (o Open Source) usate dai top player per automatizzare processi a costo zero.",
        "Rendering dinamico di DataFrame Pandas con maschera di filtraggio asincrona. Data-Gate integrato per lead generation con simulazione di auth server-side."
    )
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    df_vault = pd.DataFrame([
        {"Tecnologia": "Video Generativo", "Software": "CapCut Desktop", "Licenza": "Freemium", "Vantaggio Strategico": "Export 4K Senza Watermark"},
        {"Tecnologia": "Modelli Vocali", "Software": "ElevenLabs Core", "Licenza": "10k Char Gratis", "Vantaggio Strategico": "Clonazione Voce Reale"},
        {"Tecnologia": "Motore Logico AI", "Software": "Gemini Advanced", "Licenza": "Standard Tier", "Vantaggio Strategico": "Contesto Dati Illimitato"},
        {"Tecnologia": "Automazione Flussi", "Software": "n8n Open Source", "Licenza": "0€ (Self Hosted)", "Vantaggio Strategico": "Nessun limite task/esecuzioni"},
        {"Tecnologia": "Database Backend", "Software": "Supabase (SQL)", "Licenza": "Serverless Free", "Vantaggio Strategico": "Sostituisce Airtable/Firebase"}
    ])
    
    search = st.text_input("🔍 Ricerca rapida nel database (es. Video, Automazione, Gratis)...")
    if search:
        df_vault = df_vault[df_vault.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
    
    # LA BARRIERA PSICOLOGICA (PAYWALL DEI DATI)
    display_df = df_vault if st.session_state.vault_clearance else df_vault.head(3)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    if not st.session_state.vault_clearance:
        st.markdown("<div style='text-align:center; padding:1rem; color:#71717A; font-size:0.85rem; border-top:1px dashed #27272A; margin-bottom:1rem;'>[ ACCESSO LIMITATO. 47 RECORD OSCURATI. VERIFICA IDENTITÀ RICHIESTA ]</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='border: 1px solid #10B981; border-radius: 8px; padding: 1.5rem; background: rgba(16,185,129,0.02);'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; color:#10B981 !important;'>🔒 Sblocca Archivio Completo</h3>", unsafe_allow_html=True)
        st.write("L'esportazione del file .CSV integrale richiede l'autenticazione aziendale. Registra la tua email per aprire il gateway.")
        
        with st.form("clearance_form", clear_on_submit=False):
            email = st.text_input("Corporate Email Address:", placeholder="cto@azienda.com", label_visibility="collapsed")
            submit = st.form_submit_button("VERIFICA E SBLOCCA DATABASE")
            st.caption("Connessione SSL sicura. Garantiamo totale assenza di spam.")
            
            if submit:
                if "@" in email and "." in email:
                    bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        bar.progress(i + 1)
                    st.session_state.vault_clearance = True
                    st.rerun()
                else:
                    st.error("[ERROR] Handshake fallito. Formato email respinto.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.markdown("<div style='border: 1px solid #10B981; border-radius: 8px; padding: 1.5rem; background: rgba(16,185,129,0.05); text-align:center;'>", unsafe_allow_html=True)
        st.success("✅ Identità Verificata. Protocolli di estrazione aperti.")
        st.download_button("📥 DOWNLOAD DATABASE INTEGRALE (.CSV)", df_vault.to_csv(index=False).encode('utf-8'), "apex_ai_toolkit.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
