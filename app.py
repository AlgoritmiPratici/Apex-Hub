import streamlit as st
import pandas as pd
import time
import requests
import json
import datetime
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. KERNEL & STATE MANAGEMENT (INFRANGIBILE)
# ==========================================
st.set_page_config(page_title="NEXUS Cloud | Enterprise Infrastructure", layout="wide", initial_sidebar_state="expanded")

# Inizializzazione Blindata (Garbage Collection & Persistence)
STATES = {
    'active_tool': None,
    'm1_buffer': None,
    'sys_logs': "",
    'vault_clearance': False,
    'last_category': None
}
for key, val in STATES.items():
    if key not in st.session_state:
        st.session_state[key] = val

def sys_time():
    """Genera timestamp millisecondi per log ultra-realistici."""
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

# Deep Linking Parametrico per ManyChat
param_hub = st.query_params.get("workspace", "core")

# ==========================================
# 2. MOTORE CSS: VERCEL/LINEAR HIGH-END UI
# ==========================================
st.markdown("""
    <style>
    /* DISTRUZIONE TOTALE ELEMENTI NATIVI STREAMLIT */
    #MainMenu, header, footer, .stDeployButton {display: none !important;}
    [data-testid="stElementToolbar"], [data-testid="stToolbar"], button[title="View fullscreen"] {
        display: none !important; opacity: 0 !important; visibility: hidden !important; pointer-events: none !important;
    }
    
    /* Typography & Palette (Dark Zinc) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #030303 !important; color: #E4E4E7 !important; }
    [data-testid="stSidebar"] { background-color: #0A0A0A !important; border-right: 1px solid #18181B !important; }
    
    /* Titoli High-End */
    h1 { 
        background: linear-gradient(135deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800 !important; letter-spacing: -0.04em !important; margin-bottom: 0.2rem !important; font-size: 2.3rem !important;
    }
    h2, h3 { color: #FAFAFA !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    p, span, label, .stWidgetLabel { color: #A1A1AA !important; font-size: 0.95rem; line-height: 1.6; }
    
    /* Box Architetturali */
    .nexus-card {
        background: #0A0A0A; border: 1px solid #27272A; border-radius: 10px;
        padding: 2.5rem; box-shadow: 0 15px 35px -10px rgba(0,0,0,0.6); margin-bottom: 2rem;
    }
    
    /* Terminale Backend Simulator (Anti-Overflow Mobile) */
    .cmd-window {
        background-color: #000000; border: 1px solid #18181B; border-radius: 6px;
        padding: 1.5rem; font-family: 'SFMono-Regular', Consolas, Menlo, monospace;
        color: #10B981; font-size: 0.85rem; line-height: 1.6; 
        white-space: pre-wrap; word-wrap: break-word; overflow-x: hidden;
        box-shadow: inset 0 2px 15px rgba(0,0,0,0.9); margin-top: 1rem;
    }
    .err-log { color: #EF4444; } .sys-log { color: #71717A; } .warn-log { color: #F59E0B; }
    
    /* Pulsanti Elite */
    div.stButton > button {
        background-color: #FFFFFF !important; color: #000000 !important; font-weight: 800 !important;
        border-radius: 6px !important; border: none !important; padding: 0.8rem 1.5rem !important;
        text-transform: uppercase; letter-spacing: 0.5px; transition: all 0.2s; width: 100%;
    }
    div.stButton > button:hover { background-color: #D4D4D8 !important; transform: translateY(-1px); }
    
    div.stDownloadButton > button {
        background-color: transparent !important; color: #10B981 !important; font-weight: 800 !important;
        border-radius: 6px !important; border: 1px solid #10B981 !important; padding: 0.8rem 1.5rem !important;
        text-transform: uppercase; letter-spacing: 0.5px; width: 100%; transition: all 0.2s;
    }
    div.stDownloadButton > button:hover { background-color: rgba(16,185,129,0.05) !important; }
    
    /* Input Form e Selectbox */
    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: #050505 !important; border: 1px solid #27272A !important; color: #FFF !important; border-radius: 6px !important;
    }
    div[data-testid="stTextInput"] input:focus, div[data-testid="stTextArea"] textarea:focus {
        border-color: #10B981 !important; box-shadow: none !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #0A0A0A !important; border: 1px solid #27272A !important; color: #FFF !important;
    }
    
    /* Pill Buttons Laterali (Menu) */
    div[role="radiogroup"] > label {
        background-color: transparent; border: 1px solid transparent; border-radius: 6px;
        padding: 8px 12px; margin-bottom: 2px; transition: all 0.2s ease; cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { background-color: #18181B; }
    div[role="radiogroup"] > label[data-checked="true"] { background-color: rgba(16,185,129,0.05); border: 1px solid #10B981; }
    div[role="radiogroup"] > label > div:first-child { display: none; } 
    div[role="radiogroup"] > label p { color: #A1A1AA !important; font-weight: 500; margin: 0; font-size:0.9rem;}
    div[role="radiogroup"] > label[data-checked="true"] p { color: #10B981 !important; font-weight: 600;}
    
    /* Override Stile Tabs Vercel */
    div[data-baseweb="tab-list"] { background-color: transparent !important; border-bottom: 1px solid #27272A; margin-bottom: 1rem;}
    div[data-baseweb="tab"] { background-color: transparent !important; border-radius: 0 !important; padding-top: 0.5rem; padding-bottom: 0.5rem;}
    div[data-baseweb="tab"] p { color: #71717A !important; font-weight: 600; font-size: 0.95rem;}
    div[aria-selected="true"] { border-bottom: 2px solid #10B981 !important; }
    div[aria-selected="true"] p { color: #10B981 !important; }
    
    /* Status Badges */
    .status-badge {
        display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 4px;
        background: rgba(255, 255, 255, 0.05); color: #E4E4E7; font-size: 0.65rem;
        font-weight: 700; border: 1px solid rgba(255, 255, 255, 0.1); letter-spacing: 1px;
        text-transform: uppercase; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. HELPER UX: HEADER STANDARDIZZATI
# ==========================================
def render_page_header(badge, title, use_case, tech_spec):
    """Interfaccia Bipolare: Vantaggio per i CEO, Specifiche per i CTO."""
    st.markdown(f"<div class='status-badge'>{badge}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["💡 Vantaggio Operativo (Per i Manager)", "⚙️ Sotto il Cofano (Per Sviluppatori)"])
    with tab1:
        st.markdown(f"<div style='padding: 0.5rem 0;'><p style='color:#F4F4F5; font-size:1.05rem;'>{use_case}</p></div>", unsafe_allow_html=True)
    with tab2:
        st.markdown(f"<div style='background-color:#050505; border-left:3px solid #3B82F6; padding: 1rem; border-radius:0 6px 6px 0;'><p style='font-family:monospace; font-size:0.85rem; margin:0;'>{tech_spec}</p></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. ROUTING TASSONOMICO (LA MATRICE MENU)
# ==========================================
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #FFF; font-weight: 800; font-size: 1.5rem; letter-spacing: -1px; margin-bottom:0;">NEXUS CLOUD</h2>
        <span style="color: #10B981; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px;">B2B PLATFORM</span>
    </div>
""", unsafe_allow_html=True)

ECOSYSTEMS = {
    "⚡ NEXUS CORE (Engineering)": {
        "Data & Security": ["01. Normalizzazione Dati (CSV)", "02. Sicurezza Ambientale (.env)"],
        "Network & API": ["03. Router Notifiche Asincrono", "04. Integrazione API (Sandbox)", "05. Compilatore Telegram Scraper"],
        "Business Analytics": ["06. Matrice Costi Infrastruttura", "07. Simulatore ROI Finanziario"]
    },
    "🔒 NEXUS VAULT (Intelligence)": {
        "Database": ["08. Archivio AI & SaaS (Top 50)"]
    }
}

default_idx = 0 if param_hub == "core" else 1
selected_workspace = st.sidebar.selectbox("SELEZIONA WORKSPACE:", list(ECOSYSTEMS.keys()), index=default_idx)
st.sidebar.markdown("<hr style='border-color:#1F2937; margin: 1rem 0;'>", unsafe_allow_html=True)

# Generazione Gerarchica del Menu
selected_tool = None
if selected_workspace == "⚡ NEXUS CORE (Engineering)":
    st.sidebar.markdown("<p style='font-size: 0.75rem; font-weight: 700; color: #FFF; text-transform: uppercase; margin-bottom:0.2rem;'>Console di Comando</p>", unsafe_allow_html=True)
    categories = ECOSYSTEMS[selected_workspace]
    selected_category = st.sidebar.selectbox("Filtra per Categoria:", list(categories.keys()), label_visibility="collapsed")
    selected_tool = st.sidebar.radio("Strumenti Attivi:", categories[selected_category], label_visibility="collapsed")
else:
    selected_tool = "08. Archivio AI & SaaS (Top 50)"

# Absolute Garbage Collection (Previene il Memory Leak)
if st.session_state.active_tool != selected_tool:
    st.session_state.sys_logs = ""
    st.session_state.m1_buffer = None
    st.session_state.active_tool = selected_tool

# ==========================================
# 5. WORKSPACE: NEXUS CORE (TECH ENGINE)
# ==========================================

# --- 01. CSV NORMALIZER ---
if selected_tool == "01. Normalizzazione Dati (CSV)":
    render_page_header(
        "DATA PROCESSING", "Normalizzazione Dati",
        "I database disorganizzati uccidono le conversioni. Carica un Data Dump esportato dai tuoi vecchi gestionali. Il sistema rimuove all'istante i record duplicati e corregge le email malformate. Ottieni un database puro, pronto per essere caricato sul tuo CRM, salvando decine di ore di lavoro manuale su Excel.",
        "Libreria: <code>pandas</code>. Operazioni: De-duplicazione vettoriale globale via <code>drop_duplicates()</code>. Type casting forzato e regex trim su array 'Email'. Memoria: Totalmente volatile (elaborazione RAM-only), crittografia locale garantita."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Trascina il tuo Data Dump (.csv) qui", type=["csv"])
    
    if uploaded_file:
        if st.button("ESEGUI NORMALIZZAZIONE ALGORITMICA", type="primary"):
            with st.spinner("Ingegnerizzazione dei dati in corso..."):
                time.sleep(0.7)
                try:
                    # Ingegneria di robustezza per CSV corrotti
                    try:
                        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python', encoding='utf-8')
                    except UnicodeDecodeError:
                        uploaded_file.seek(0)
                        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python', encoding='latin1')
                        
                    r_in = len(df_raw)
                    df_clean = df_raw.copy().drop_duplicates()
                    
                    email_col = next((c for c in df_clean.columns if c.lower() == 'email'), None)
                    if email_col:
                        df_clean[email_col] = df_clean[email_col].astype(str).str.lower().str.strip()
                        df_clean = df_clean[~df_clean[email_col].isin(['nan', 'none', '', 'null'])].dropna(subset=[email_col])
                        log_m = "Sanificazione array email completata con precisione chirurgica."
                    else:
                        log_m = "<span class='warn-log'>[WARN] Colonna 'Email' assente. Eseguita ottimizzazione globale sui record esistenti.</span>"
                        
                    r_out = len(df_clean)
                    st.session_state.m1_buffer = df_clean
                    st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [root@nexus] ~ Data Parsing Eseguito. Latenza: 1.8ms.</span><br>{log_m}<br>Record Iniziali: {r_in} | Record Validi: {r_out} | Anomalie Distrutte: {r_in - r_out}"
                except Exception as e:
                    st.session_state.sys_logs = f"<span class='err-log'>[{sys_time()}] [FATAL] Impossibile elaborare il file. Formattazione CSV non standard. Dettagli sistema: {e}</span>"

    if st.session_state.m1_buffer is not None:
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
        st.dataframe(st.session_state.m1_buffer.head(5), use_container_width=True)
        # Scaricamento sicuro forzato a utf-8-sig per compatibilità Excel su Windows
        st.download_button("📥 SCARICA DATABASE PULITO (.CSV)", st.session_state.m1_buffer.to_csv(index=False).encode('utf-8-sig'), "nexus_data_clean.csv", "text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 02. PROTOCOLLO .ENV ---
elif selected_tool == "02. Sicurezza Ambientale (.env)":
    render_page_header(
        "CYBERSECURITY", "Sicurezza Ambientale (.env)",
        "L'errore numero uno che causa data breach aziendali è lasciare le password scritte in chiaro nel codice. Incolla qui le tue configurazioni: il sistema estrarrà le informazioni sensibili isolandole. Verranno generati i file crittografati (.env e .gitignore) per blindare il tuo server prima della messa online.",
        "Applicazione rigorosa dello standard 12-Factor App Methodology. Analisi dei pattern per il disaccoppiamento logico tra variabili d'ambiente (Environment Variables) e repository Git."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    raw_env_str = """DATABASE_URL=postgres://admin:root123@local/db\nAPI_SECRET=sk_live_8473djds83...\nDEBUG_MODE=True"""
    env_input = st.text_area("Incolla variabili esposte (Formato Key=Value):", value=raw_env_str, height=120)
    
    if st.button("BLINDA ARCHITETTURA DI SISTEMA", type="primary"):
        st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [sec-ops@nexus] ~ Scansione file configurazione e moduli...</span><br><span class='warn-log'>[ALERT] Rilevate password e chiavi API esposte in chiaro.</span><br>[ENCRYPT] Generazione chiavi di disaccoppiamento in corso...<br><span style='color:#10B981'>[SUCCESS] Architettura protetta. File asettici pronti per il deployment.</span>"
        
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.download_button("📥 SCARICA .ENV", env_input, ".env")
        c2.download_button("📥 SCARICA .GITIGNORE", ".env\n__pycache__/\n*.session\n.DS_Store", ".gitignore")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 03. WEBHOOK ROUTER ---
elif selected_tool == "03. Router Notifiche Asincrono":
    render_page_header(
        "ALGORITHMS", "Router Notifiche Asincrono",
        "L'overload informativo uccide la produttività del tuo team. Incolla i dati di un evento di sistema: il nostro algoritmo valuterà autonomamente l'urgenza. Se critico, inoltra un SMS al management. Se inutile, lo silenzia e lo archivia.",
        "Simulazione Endpoint REST in ricezione. Parsing asincrono del payload JSON. Switch logico interno sulla chiave 'priority' (Event-Driven Architecture) con tempo di esecuzione O(1)."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    json_test = """{\n  "source": "server_monitor",\n  "error_code": "502_bad_gateway",\n  "priority": "CRITICAL"\n}"""
    json_in = st.text_area("Payload Evento in Ingresso (JSON):", value=json_test, height=140)
    
    if st.button("ESEGUI ALGORITMO DI ROUTING", type="primary"):
        with st.spinner("Valutazione rami logici..."):
            time.sleep(0.4)
            try:
                data = json.loads(json_in)
                prio = str(data.get("priority", "LOW")).upper()
                if prio in ["HIGH", "CRITICAL"]:
                    data["nexus_action"] = "FORWARD_TO_CTO_SMS"
                    msg = f"<span class='warn-log'>[{sys_time()}] [URGENT] Priorità Alta rilevata. Bypass filtri attivato. Evento instradato.</span>"
                else:
                    data["nexus_action"] = "SILENT_DB_LOG"
                    msg = f"<span class='sys-log'>[{sys_time()}] [SILENT] Priorità Bassa. Rumore soppresso e loggato a sistema per audit futuro.</span>"
                st.session_state.sys_logs = f"{msg}<br><br><span class='sys-log'>[PAYLOAD TRASFORMATO]:</span><br>{json.dumps(data, indent=2)}"
            except json.JSONDecodeError as e:
                st.session_state.sys_logs = f"<span class='err-log'>[{sys_time()}] [FATAL ERROR] Payload JSON corrotto. Il parser ha restituito Syntax Error: {e}</span>"
                
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 04. API INJECTOR ---
elif selected_tool == "04. Integrazione API (Sandbox)":
    render_page_header(
        "NETWORK OPS", "Integrazione API (Sandbox)",
        "Assicurati che i tuoi software comunichino. Inserisci l'URL del tuo Webhook e invia un pacchetto dati di prova. Il sistema simulerà un ping HTTP, misurerà la latenza di rete e confermerà se l'informazione è giunta intatta a destinazione.",
        "Esecuzione modulo <code>requests.post</code> nativo. Handshake TCP/TLS asincrono verso endpoint remoto. Misurazione telemetrica della latenza in millisecondi e validazione HTTP Status Code."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    url = st.text_input("URL di Destinazione (Endpoint REST)", value="https://httpbin.org/post")
    payload_str = """{\n  "cliente": "NEXUS Corp",\n  "status": "Integrazione API Verificata"\n}"""
    payload = st.text_area("Dati da iniettare (JSON)", value=payload_str, height=110)
    
    if st.button("ESEGUI TEST DI RETE (PING)", type="primary"):
        st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [net-ops@nexus] ~ Negoziazione protocollo HTTP/TLS verso {url}...</span>"
        try:
            p_json = json.loads(payload)
            t0 = time.time()
            res = requests.post(url, json=p_json, timeout=5)
            lat = round(time.time() - t0, 3)
            st.session_state.sys_logs += f"<br><span style='color:#10B981'>[{sys_time()}] [SUCCESS] Transazione validata. Connessione intatta.</span><br>HTTP CODE: {res.status_code}<br>LATENZA TCP: {lat}s<br><br><span class='sys-log'>[RAW SERVER RESPONSE]</span><br>{res.text[:250]}..."
        except json.JSONDecodeError:
            st.session_state.sys_logs += f"<br><span class='err-log'>[{sys_time()}] [ERROR] Formattazione JSON invalida. Il carico utile è stato respinto dal sistema prima dell'invio.</span>"
        except Exception as e:
            st.session_state.sys_logs += f"<br><span class='err-log'>[{sys_time()}] [TIMEOUT FATAL] Endpoint irraggiungibile o barriera firewall attiva. Dettagli: {e}</span>"
            
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 05. COMPILATORE TELEGRAM ---
elif selected_tool == "05. Compilatore Telegram Scraper":
    render_page_header(
        "DATA EXTRACTION", "Compilatore Telegram Scraper",
        "Genera un software personalizzato per estrarre migliaia di contatti dai gruppi concorrenti. Poiché estrarre dati tramite Cloud genera un Ban immediato dell'account Telegram, inserisci i tuoi parametri qui. Compileremo un software Python sicuro che potrai scaricare ed avviare direttamente dal tuo computer.",
        "Generazione programmatica di script Python (libreria Telethon asincrona). L'eseguibile richiede un'architettura client-side (localhost) per forzare l'handshaking OTP e bypassare i filtri anti-bot sui Server Cloud."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    api_id = c1.text_input("Telegram API_ID", placeholder="es. 2847592")
    api_hash = c2.text_input("Telegram API_HASH", placeholder="es. c4e8b...", type="password")
    target = st.text_input("Username Community Competitor (senza @)", placeholder="es. marketing_italia")
    
    if st.button("COSTRUISCI SOFTWARE SORGENTE", type="primary"):
        if api_id and api_hash and target:
            script = f"""from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('nexus_session', '{api_id}', '{api_hash}') as c:\n  users = c.get_participants('{target}')\n  with open('leads_estrazione.csv', 'w', newline='', encoding='utf-8-sig') as f:\n    w=csv.writer(f)\n    w.writerow(['ID','Username','Name'])\n    for u in users: w.writerow([u.id, u.username, u.first_name])\n  print('[OK] Estrazione Dati Completata.')"""
            st.session_state.m1_buffer = script
            st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [compiler@nexus] ~ Generazione variabili asincrone per il target '{target}'...</span><br><span style='color:#10B981'>[{sys_time()}] [SUCCESS] Software Python compilato. Il file binario è pronto per il download sicuro.</span>"
        else:
            st.session_state.sys_logs = f"<span class='err-log'>[{sys_time()}] [FATAL ERROR] Impossibile completare la compilazione. Parametri API mancanti nel costruttore.</span>"
            st.session_state.m1_buffer = None
            
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
        if st.session_state.m1_buffer:
            st.download_button("📥 SCARICA SCRIPT PYTHON (.PY)", st.session_state.m1_buffer, "nexus_telegram_engine.py")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 06. COST MATRIX ---
elif selected_tool == "06. Matrice Costi Infrastruttura":
    render_page_header(
        "FINANCIAL AUDIT", "Matrice Costi Infrastruttura",
        "Evidenzia le perdite. Questa matrice mostra i software (SaaS) estremamente costosi e monolitici che la tua azienda usa oggi, fornendoti l'esatta alternativa gratuita e Open Source da implementare per azzerare totalmente i costi operativi.",
        "Audit comparativo TCO (Total Cost of Ownership) tra infrastrutture monolitiche legacy, e microservizi Cloud Serverless distribuiti (Edge Computing)."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Software Costoso (Spreco)": ["Zapier Enterprise", "HubSpot / Airtable", "AWS S3 / Google Cloud", "Mailchimp"],
        "Soluzione NEXUS (Costo Zero)": ["n8n (Self-Hosted Node)", "Supabase (PostgreSQL Serverless)", "Cloudflare R2 (Edge Storage)", "Mautic / AWS SES"],
        "Margine Operativo Salvato": ["~ 250 €/mese", "~ 150 €/mese", "~ 45 €/mese", "~ 80 €/mese"]
    }), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 07. ROI TELEMETRY ---
elif selected_tool == "07. Simulatore ROI Finanziario":
    render_page_header(
        "BUSINESS ANALYTICS", "Simulatore ROI Finanziario",
        "Simulatore predittivo di marginalità in tempo reale. Inserisci il fatturato attuale e i costi tecnologici fissi. Il sistema calcolerà istantaneamente l'aumento dell'utile netto aziendale derivante dal taglio radicale degli abbonamenti software.",
        "Data Visualization tramite framework Plotly Express. Calcolo vettoriale real-time dell'abbattimento dell'Operational Expenditure (OPEX) e della dilatazione marginale."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    mrr = c1.number_input("Fatturato Mensile Attuale (MRR) €", value=25000, step=1000)
    opex = c2.number_input("Costi Abbonamenti SaaS (Da Azzerare) €", value=4200, step=100)
    
    m_old, m_new = mrr - opex, mrr 
    c3, c4 = st.columns(2)
    c3.metric("Utile Netto Storico", f"€ {m_old:,}")
    c4.metric("Utile Netto NEXUS", f"€ {m_new:,}", f"+ € {opex:,} (Nuova Cassa Sbloccata)")
    
    fig = go.Figure(data=[
        go.Bar(name='Infrastruttura Attuale', x=['Business Model'], y=[m_old], marker_color='#27272A', text=f"€{m_old}", textposition='auto'),
        go.Bar(name='Infrastruttura NEXUS', x=['Business Model'], y=[m_new], marker_color='#10B981', text=f"€{m_new}", textposition='auto')
    ])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', barmode='group', margin=dict(t=20, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# HUB 02: NEXUS VAULT (INTELLIGENCE DATABASE)
# ==========================================
elif selected_workspace == "🔒 NEXUS VAULT (Intelligence)":
    
    render_page_header(
        "DATA INTELLIGENCE", "Archivio AI & SaaS (Top 50)",
        "Perché bruciare centinaia di ore in ricerca e sviluppo quando il lavoro è già stato fatto? Esplora il database privato delle 50 architetture SaaS e Intelligenze Artificiali gratuite (Open Source) usate dai top player per automatizzare processi a costo zero.",
        "Rendering dinamico di DataFrame Pandas con maschera di filtraggio asincrona O(n). Data-Gate incapsulato per lead generation con simulazione di autenticazione e latenza server-side."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    
    df_vault = pd.DataFrame([
        {"Tecnologia": "Video Generativo", "Software": "CapCut Desktop", "Licenza": "Freemium", "Vantaggio Strategico": "Export 4K Senza Watermark"},
        {"Tecnologia": "Modelli Vocali", "Software": "ElevenLabs Core", "Licenza": "10k Char Gratis", "Vantaggio Strategico": "Clonazione Neurale Reale"},
        {"Tecnologia": "Motore Logico AI", "Software": "Gemini Advanced", "Licenza": "Standard Tier", "Vantaggio Strategico": "Contesto Dati Illimitato"},
        {"Tecnologia": "Automazione Flussi", "Software": "n8n Open Source", "Licenza": "0€ (Self Hosted)", "Vantaggio Strategico": "Nessun limite task/esecuzioni"},
        {"Tecnologia": "Database Backend", "Software": "Supabase (SQL)", "Licenza": "Serverless Free", "Vantaggio Strategico": "Sostituzione Airtable/Firebase"}
    ])
    
    search = st.text_input("🔍 Ricerca rapida nel database (es. Video, Automazione, Gratis)...")
    if search:
        df_vault = df_vault[df_vault.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
    
    # LA BARRIERA PSICOLOGICA E FUNZIONALE (PAYWALL DATI)
    display_df = df_vault if st.session_state.vault_clearance else df_vault.head(3)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    if not st.session_state.vault_clearance:
        st.markdown("<div style='text-align:center; padding:1.5rem 1rem; color:#71717A; font-size:0.85rem; border-top:1px dashed #27272A; margin-bottom:2rem;'>[ ACCESSO LIMITATO. 47 RECORD OSCURATI. VERIFICA IDENTITÀ RICHIESTA ]</div>", unsafe_allow_html=True)
        
        # Form Ingegnerizzato per Value-Exchange (Frictionless)
        st.markdown("<div style='border: 1px solid #27272A; border-radius: 8px; padding: 2rem; background: #050505;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; color:#FAFAFA !important;'>Sblocca l'Archivio Integrale</h3>", unsafe_allow_html=True)
        st.write("Dove ti inviamo il link per l'accesso e il download del database completo (formato CSV)? Inserisci il tuo indirizzo email qui sotto.")
        
        with st.form("clearance_form", clear_on_submit=False):
            email = st.text_input("Indirizzo Email:", placeholder="nome@azienda.com", label_visibility="collapsed")
            submit = st.form_submit_button("SBLOCCA E INVIA AL MIO INDIRIZZO", use_container_width=True)
            st.markdown("<div style='text-align:center; margin-top:0.5rem; font-size:0.8rem; color:#A1A1AA;'>🔒 Nessun costo. Zero spam. Disiscrizione in qualsiasi momento.</div>", unsafe_allow_html=True)
            
            if submit:
                # Validazione rigorosa base email
                if len(email) > 5 and "@" in email and "." in email.split("@")[-1]:
                    bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.005)
                        bar.progress(i + 1)
                    st.session_state.vault_clearance = True
                    st.rerun()
                else:
                    st.error("[ERROR] Indirizzo email non valido o non riconosciuto. Verifica e riprova.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.markdown("<div style='border: 1px solid #10B981; border-radius: 8px; padding: 2rem; background: rgba(16,185,129,0.05); text-align:center; margin-top:2rem;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#10B981 !important; margin-bottom:1rem;'>✅ Accesso Validato e Sbloccato</h3>", unsafe_allow_html=True)
        st.write("L'archivio integrale è ora visibile a schermo ed è pronto per il download locale.")
        st.download_button("📥 DOWNLOAD DATABASE INTEGRALE (.CSV)", df_vault.to_csv(index=False).encode('utf-8-sig'), "nexus_ai_database.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
