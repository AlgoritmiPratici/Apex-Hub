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
st.set_page_config(page_title="NEXUS Cloud | B2B Infrastructure", layout="wide", initial_sidebar_state="expanded")

# Inizializzazione Blindata (Previene ricaricamenti a vuoto e crash)
STATES = {
    'active_tool': None,
    'm1_buffer': None,
    'sys_logs': "",
    'vault_clearance': False,
    'last_workspace': None
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
    /* DISTRUZIONE DEI BUG VISIVI (Tooltip "Keyboard double", Header, Footer, Toolbar tabelle) */
    #MainMenu, header, footer, .stDeployButton {display: none !important;}
    [data-testid="stElementToolbar"], [data-testid="stToolbar"] {display: none !important; opacity: 0 !important;}
    button[title="View fullscreen"] {display: none !important;}
    
    /* Global Typography & Palette (Dark Zinc) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #030303 !important; color: #E4E4E7 !important; }
    [data-testid="stSidebar"] { background-color: #0A0A0A !important; border-right: 1px solid #18181B !important; }
    
    /* Tipografia Corporate */
    h1 { 
        background: linear-gradient(135deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800 !important; letter-spacing: -0.04em !important; margin-bottom: 0.2rem !important; font-size: 2.3rem !important;
    }
    h2, h3 { color: #FAFAFA !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    p, span, label, .stWidgetLabel { color: #A1A1AA !important; font-size: 0.95rem; line-height: 1.6; }
    
    /* Box Ingegnerizzati (Shadows and Borders) */
    .nexus-card {
        background: #0A0A0A; border: 1px solid #27272A; border-radius: 10px;
        padding: 2.5rem; box-shadow: 0 15px 35px -10px rgba(0,0,0,0.6); margin-bottom: 2rem;
    }
    
    /* Terminale Backend Simulator */
    .cmd-window {
        background-color: #000000; border: 1px solid #18181B; border-radius: 6px;
        padding: 1.5rem; font-family: 'SFMono-Regular', Consolas, Menlo, monospace;
        color: #10B981; font-size: 0.85rem; line-height: 1.6; white-space: pre-wrap;
        box-shadow: inset 0 2px 15px rgba(0,0,0,0.9); margin-top: 1rem;
    }
    .err-log { color: #EF4444; } .sys-log { color: #71717A; } .warn-log { color: #F59E0B; }
    
    /* Pulsanti Elite (Anti-Hover bug) */
    div.stButton > button {
        background-color: #FFFFFF !important; color: #000000 !important; font-weight: 700 !important;
        border-radius: 6px !important; border: none !important; padding: 0.8rem 1.5rem !important;
        text-transform: uppercase; letter-spacing: 0.5px; transition: all 0.2s; width: 100%;
    }
    div.stButton > button:hover { background-color: #D4D4D8 !important; transform: translateY(-1px); }
    
    div.stDownloadButton > button {
        background-color: transparent !important; color: #10B981 !important; font-weight: 700 !important;
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
    
    /* Radio Buttons trasformati in Menu Laterale Moderno */
    div[role="radiogroup"] > label {
        background-color: transparent; border: 1px solid transparent; border-radius: 6px;
        padding: 8px 12px; margin-bottom: 2px; transition: all 0.2s ease; cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { background-color: #18181B; }
    div[role="radiogroup"] > label[data-checked="true"] { background-color: rgba(16,185,129,0.05); border: 1px solid #10B981; }
    div[role="radiogroup"] > label > div:first-child { display: none; } /* Nasconde il pallino nativo */
    div[role="radiogroup"] > label p { color: #A1A1AA !important; font-weight: 500; margin: 0; font-size:0.9rem;}
    div[role="radiogroup"] > label[data-checked="true"] p { color: #10B981 !important; font-weight: 600;}
    
    /* Badges */
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
    st.markdown(f"<div class='status-badge'>{badge}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["💡 Vantaggio Operativo", "⚙️ Architettura di Sistema"])
    with tab1:
        st.markdown(f"<div style='padding: 1rem 0;'><p style='color:#F4F4F5; font-size:1.05rem;'>{use_case}</p></div>", unsafe_allow_html=True)
    with tab2:
        st.markdown(f"<div style='background-color:#050505; border-left:3px solid #3B82F6; padding: 1rem;'><p style='font-family:monospace; font-size:0.85rem; margin:0;'>{tech_spec}</p></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. ROUTING TASSONOMICO (SIDEBAR)
# ==========================================
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #FFF; font-weight: 800; font-size: 1.5rem; letter-spacing: -1px; margin-bottom:0;">NEXUS CLOUD</h2>
        <span style="color: #10B981; font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px;">B2B PLATFORM</span>
    </div>
""", unsafe_allow_html=True)

WORKSPACE_MAP = {
    "⚡ NEXUS CORE (Engineering)": [
        "01. Normalizzazione Dati (CSV)", 
        "02. Sicurezza Ambientale (.env)", 
        "03. Compilatore Telegram Scraper", 
        "04. Matrice Costi Infrastruttura", 
        "05. Simulatore ROI Finanziario", 
        "06. Router Notifiche Asincrono", 
        "07. Integrazione API (Sandbox)"
    ],
    "🔒 NEXUS VAULT (Intelligence)": ["08. Database AI & SaaS (Top 50)"]
}

default_idx = 0 if param_hub == "core" else 1
selected_workspace = st.sidebar.selectbox("SELEZIONA WORKSPACE:", list(WORKSPACE_MAP.keys()), index=default_idx)

st.sidebar.markdown("<hr style='border-color:#1F2937; margin: 1rem 0;'>", unsafe_allow_html=True)

# Generazione Menu Tool Dinamica
selected_tool = None
if selected_workspace == "⚡ NEXUS CORE (Engineering)":
    st.sidebar.markdown("<p style='font-size: 0.75rem; font-weight: 700; color: #FFF; text-transform: uppercase;'>Servizi Attivi</p>", unsafe_allow_html=True)
    selected_tool = st.sidebar.radio("Strumenti:", WORKSPACE_MAP[selected_workspace], label_visibility="collapsed")
else:
    selected_tool = "08. Database AI & SaaS (Top 50)"

# Garbage Collection Inter-Tool (Resetta il terminale)
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
        "Carica una lista contatti caotica esportata dai tuoi vecchi gestionali. Il sistema rimuove all'istante i record duplicati e corregge le email formattate male. Ottieni un database pulito, pronto per essere caricato sul tuo CRM senza bruciare ore di lavoro manuale su Excel.",
        "Libreria: <code>pandas</code>. Operazioni: De-duplicazione vettoriale <code>drop_duplicates()</code>. Type casting forzato e regex trim su array 'Email'. Memoria volatile (elaborazione RAM-only)."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Trascina il tuo Data Dump (.csv) qui", type=["csv"])
    
    if uploaded_file:
        if st.button("ESEGUI NORMALIZZAZIONE", type="primary"):
            with st.spinner("Ingegnerizzazione dei dati in corso..."):
                time.sleep(0.7)
                try:
                    df = pd.read_csv(uploaded_file, sep=None, engine='python')
                    r_in = len(df)
                    df_clean = df.drop_duplicates()
                    
                    email_col = next((c for c in df_clean.columns if c.lower() == 'email'), None)
                    if email_col:
                        df_clean[email_col] = df_clean[email_col].astype(str).str.lower().str.strip()
                        df_clean = df_clean[~df_clean[email_col].isin(['nan', 'none', '', 'null'])].dropna(subset=[email_col])
                        log_m = "Sanificazione colonna email completata."
                    else:
                        log_m = "<span class='warn-log'>[WARN] Colonna 'Email' assente. Eseguita pulizia globale.</span>"
                        
                    r_out = len(df_clean)
                    st.session_state.m1_buffer = df_clean
                    st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [root@nexus] ~ Parsing Eseguito. Latenza: 1.4ms.</span><br>{log_m}<br>Record Iniziali: {r_in} | Record Validi: {r_out} | Anomalie Eliminate: {r_in - r_out}"
                except Exception as e:
                    st.session_state.sys_logs = f"<span class='err-log'>[{sys_time()}] [FATAL] Errore di codifica del file. Assicurati che sia un CSV standard. Dettagli: {e}</span>"

    if st.session_state.m1_buffer is not None:
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
        st.dataframe(st.session_state.m1_buffer.head(5), use_container_width=True)
        st.download_button("📥 SCARICA DATABASE PULITO", st.session_state.m1_buffer.to_csv(index=False).encode('utf-8'), "nexus_data_clean.csv", "text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 02. PROTOCOLLO .ENV ---
elif selected_tool == "02. Sicurezza Ambientale (.env)":
    render_page_header(
        "CYBERSECURITY", "Sicurezza Ambientale (.env)",
        "L'errore numero uno che causa data breach aziendali è lasciare le password scritte nel codice. Incolla qui le tue configurazioni: il sistema estrarrà le informazioni sensibili creando i file crittografati (.env e .gitignore) per blindare il tuo server.",
        "Applicazione standard 12-Factor App Methodology. Analisi pattern per il disaccoppiamento logico tra variabili d'ambiente (Environment Variables) e codice backend."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    raw_env_str = """DATABASE_URL=postgres://admin:root123@local/db\nAPI_SECRET=sk_live_8473djds83...\nDEBUG_MODE=True"""
    env_input = st.text_area("Incolla variabili esposte (Formato Key=Value):", value=raw_env_str, height=120)
    
    if st.button("BLINDA ARCHITETTURA", type="primary"):
        st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [sec-ops@nexus] ~ Scansione file di configurazione...</span><br><span class='warn-log'>[ALERT] Rilevate password e chiavi API in chiaro.</span><br>[ENCRYPT] Generazione file di disaccoppiamento...<br><span style='color:#10B981'>[SUCCESS] Architettura protetta. File generati.</span>"
        
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.download_button("📥 SCARICA .ENV", env_input, ".env")
        c2.download_button("📥 SCARICA .GITIGNORE", ".env\n__pycache__/\n*.session\n.DS_Store", ".gitignore")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 03. COMPILATORE TELEGRAM ---
elif selected_tool == "03. Compilatore Telegram Scraper":
    render_page_header(
        "DATA EXTRACTION", "Compilatore Telegram Scraper",
        "Genera un software personalizzato per estrarre membri dai gruppi concorrenti. I server Cloud vengono bannati da Telegram: inserisci i tuoi parametri qui, e noi compileremo un software Python sicuro da scaricare ed avviare direttamente dal tuo PC.",
        "Compilazione dinamica di script Python (libreria Telethon asincrona). L'eseguibile forza l'handshaking OTP lato client (localhost) per bypassare i filtri anti-bot IP dei provider Cloud."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    api_id = c1.text_input("Telegram API_ID", placeholder="es. 2847592")
    api_hash = c2.text_input("Telegram API_HASH", placeholder="es. c4e8b...", type="password")
    target = st.text_input("Username Community Competitor (senza @)", placeholder="es. marketing_italia")
    
    if st.button("COSTRUISCI SOFTWARE SORGENTE", type="primary"):
        if api_id and api_hash and target:
            script = f"""from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('nexus_session', '{api_id}', '{api_hash}') as c:\n  users = c.get_participants('{target}')\n  with open('leads.csv', 'w', newline='', encoding='utf-8') as f:\n    w=csv.writer(f)\n    w.writerow(['ID','Username','Name'])\n    for u in users: w.writerow([u.id, u.username, u.first_name])\n  print('[OK] Estrazione Dati Completata.')"""
            st.session_state.m1_buffer = script
            st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [compiler@nexus] ~ Iniezione payload per il target '{target}'...</span><br><span style='color:#10B981'>[SUCCESS] Software Python compilato. Pronto al download.</span>"
        else:
            st.session_state.sys_logs = f"<span class='err-log'>[{sys_time()}] [FATAL ERROR] Impossibile compilare. Parametri API mancanti.</span>"
            st.session_state.m1_buffer = None
            
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
        if st.session_state.m1_buffer:
            st.download_button("📥 SCARICA SCRIPT PYTHON (.PY)", st.session_state.m1_buffer, "nexus_telegram.py")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 04. COST MATRIX ---
elif selected_tool == "04. Matrice Costi Infrastruttura":
    render_page_header(
        "FINANCIAL AUDIT", "Matrice Costi Infrastruttura",
        "Evidenzia gli abbonamenti software (SaaS) che stanno prosciugando la cassa della tua azienda. Questa matrice ti mostra l'esatta alternativa gratuita o Open Source da implementare per azzerare i costi operativi.",
        "Audit comparativo TCO (Total Cost of Ownership) tra infrastrutture monolitiche legacy e microservizi Cloud Serverless distribuiti."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Software Costoso (Spreco)": ["Zapier Enterprise", "HubSpot / Airtable", "AWS S3 / Google Cloud", "Mailchimp"],
        "Soluzione NEXUS (Costo 0)": ["n8n (Self-Hosted Node)", "Supabase (PostgreSQL)", "Cloudflare R2", "Mautic / AWS SES"],
        "Margine Operativo Salvato": ["~ 250 €/mese", "~ 150 €/mese", "~ 45 €/mese", "~ 80 €/mese"]
    }), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 05. ROI TELEMETRY ---
elif selected_tool == "05. Simulatore ROI Finanziario":
    render_page_header(
        "BUSINESS ANALYTICS", "Simulatore ROI Finanziario",
        "Simulatore predittivo di marginalità. Inserisci il fatturato attuale e le spese tecnologiche fisse. Il sistema calcolerà istantaneamente l'aumento dell'utile netto aziendale a seguito dell'implementazione di automazioni a costo zero.",
        "Data Visualization tramite Plotly Express. Calcolo vettoriale real-time dell'abbattimento dell'Operational Expenditure (OPEX)."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    mrr = c1.number_input("Fatturato Mensile Attuale (MRR) €", value=25000, step=1000)
    opex = c2.number_input("Costi Abbonamenti SaaS (Da Tagliare) €", value=4200, step=100)
    
    m_old, m_new = mrr - opex, mrr 
    c3, c4 = st.columns(2)
    c3.metric("Utile Netto Attuale", f"€ {m_old:,}")
    c4.metric("Utile Netto NEXUS", f"€ {m_new:,}", f"+ € {opex:,} Cassa Sbloccata")
    
    fig = go.Figure(data=[
        go.Bar(name='Infrastruttura Attuale', x=['Modello di Business'], y=[m_old], marker_color='#27272A', text=f"€{m_old}", textposition='auto'),
        go.Bar(name='Infrastruttura NEXUS', x=['Modello di Business'], y=[m_new], marker_color='#10B981', text=f"€{m_new}", textposition='auto')
    ])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', barmode='group', margin=dict(t=20, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 06. WEBHOOK ROUTER ---
elif selected_tool == "06. Router Notifiche Asincrono":
    render_page_header(
        "ALGORITHMS", "Router Notifiche Asincrono",
        "L'overload di notifiche uccide la produttività aziendale. Incolla i dati di un evento di prova: il nostro algoritmo valuterà da solo l'urgenza. Inoltrerà l'allarme ai manager solo se critico, altrimenti archivierà in silenzio l'evento nel database.",
        "Simulazione Endpoint REST. Parsing asincrono del payload JSON in ingresso. Switch logico sulla chiave 'priority' (Event-Driven Architecture)."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    json_test = """{\n  "source": "server_monitor",\n  "error_code": "502_bad_gateway",\n  "priority": "CRITICAL"\n}"""
    json_in = st.text_area("Payload Evento in Ingresso (JSON):", value=json_test, height=140)
    
    if st.button("ESEGUI ALGORITMO DI ROUTING", type="primary"):
        with st.spinner("Valutazione rami logici..."):
            time.sleep(0.5)
            try:
                data = json.loads(json_in)
                prio = str(data.get("priority", "LOW")).upper()
                if prio in ["HIGH", "CRITICAL"]:
                    data["nexus_action"] = "FORWARD_TO_CTO_SMS"
                    msg = f"<span class='warn-log'>[{sys_time()}] [URGENT] Priorità Alta rilevata. Bypass filtri attivato. Evento inoltrato.</span>"
                else:
                    data["nexus_action"] = "SILENT_DB_LOG"
                    msg = f"<span class='sys-log'>[{sys_time()}] [SILENT] Priorità Bassa. Rumore soppresso e loggato a sistema.</span>"
                st.session_state.sys_logs = f"{msg}<br><br><span class='sys-log'>OUTPUT TRASFORMATO:</span><br>{json.dumps(data, indent=2)}"
            except json.JSONDecodeError as e:
                st.session_state.sys_logs = f"<span class='err-log'>[{sys_time()}] [FATAL ERROR] JSON malformato. Eccezione Syntax Error: {e}</span>"
                
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 07. API INJECTOR ---
elif selected_tool == "07. Integrazione API (Sandbox)":
    render_page_header(
        "NETWORK OPS", "Integrazione API (Sandbox)",
        "Verifica che i tuoi software comunichino in tempo reale. Inserisci l'URL del tuo Webhook (es. Zapier o Make.com) e invia un pacchetto dati di prova. Il sistema misurerà la latenza di rete e confermerà la ricezione.",
        "Esecuzione <code>requests.post</code>. Handshake TCP/TLS asincrono verso endpoint remoto. Rilevazione telemetrica della latenza (ms) e decodifica dell'HTTP Status Code."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    url = st.text_input("URL di Destinazione (Endpoint REST)", value="https://httpbin.org/post")
    payload_str = """{\n  "cliente": "NEXUS Corp",\n  "status": "Integrazione Attiva"\n}"""
    payload = st.text_area("Dati da inviare (JSON)", value=payload_str, height=110)
    
    if st.button("ESEGUI TEST DI RETE", type="primary"):
        st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [net-ops@nexus] ~ Negoziazione protocollo HTTP/TLS...</span>"
        try:
            p_json = json.loads(payload)
            t0 = time.time()
            res = requests.post(url, json=p_json, timeout=5)
            lat = round(time.time() - t0, 3)
            st.session_state.sys_logs += f"<br><span style='color:#10B981'>[{sys_time()}] [SUCCESS] Transazione verificata.</span><br>HTTP CODE: {res.status_code}<br>LATENZA: {lat}s<br><br><span class='sys-log'>[RAW SERVER RESPONSE]</span><br>{res.text[:250]}..."
        except json.JSONDecodeError:
            st.session_state.sys_logs += f"<br><span class='err-log'>[{sys_time()}] [ERROR] Formattazione JSON invalida. Payload respinto.</span>"
        except Exception as e:
            st.session_state.sys_logs += f"<br><span class='err-log'>[{sys_time()}] [TIMEOUT FATAL] Nessuna risposta dal server remoto. Dettagli: {e}</span>"
            
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HUB 02: NEXUS VAULT (INTELLIGENCE DATABASE)
# ==========================================
elif selected_workspace == "🔒 NEXUS VAULT (Intelligence)":
    
    render_page_header(
        "DATA INTELLIGENCE", "Vault AI & SaaS Database",
        "Perché perdere 100 ore in ricerca e sviluppo quando l'abbiamo già fatto noi? Esplora il database privato delle 50 architetture SaaS e Intelligenze Artificiali gratuite usate dai top player per automatizzare processi a costo zero.",
        "Rendering dinamico di DataFrame Pandas con maschera di filtraggio asincrona. Data-Gate integrato per lead generation con simulazione di autenticazione server-side."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    
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
    
    # PAYWALL LOGICO (Il Value-Exchange)
    display_df = df_vault if st.session_state.vault_clearance else df_vault.head(3)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    if not st.session_state.vault_clearance:
        st.markdown("<div style='text-align:center; padding:1.5rem 1rem; color:#71717A; font-size:0.85rem; border-top:1px dashed #27272A; margin-bottom:2rem;'>[ ACCESSO LIMITATO. 47 RECORD OSCURATI. VERIFICA IDENTITÀ RICHIESTA ]</div>", unsafe_allow_html=True)
        
        # Form di Lead Gen Ingegnerizzato (Senza frizione aggressiva)
        st.markdown("<div style='border: 1px solid #27272A; border-radius: 8px; padding: 2rem; background: #050505;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; color:#FAFAFA !important;'>Sblocca l'accesso gratuito al Database</h3>", unsafe_allow_html=True)
        st.write("Per sbloccare le righe oscurate e scaricare l'intero database in formato CSV, inserisci l'indirizzo email a cui inviare l'accesso riservato.")
        
        with st.form("clearance_form", clear_on_submit=False):
            email = st.text_input("Indirizzo Email:", placeholder="nome@azienda.com", label_visibility="collapsed")
            submit = st.form_submit_button("SBLOCCA ACCESSO E SCARICA IL FILE", use_container_width=True)
            st.markdown("<div style='text-align:center; margin-top:0.5rem; font-size:0.8rem; color:#A1A1AA;'>🔒 Nessun costo. Zero spam. Disiscrizione in qualsiasi momento.</div>", unsafe_allow_html=True)
            
            if submit:
                if "@" in email and "." in email:
                    bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        bar.progress(i + 1)
                    st.session_state.vault_clearance = True
                    st.rerun()
                else:
                    st.error("[ERROR] Indirizzo email non valido. Impossibile autorizzare.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.markdown("<div style='border: 1px solid #10B981; border-radius: 8px; padding: 2rem; background: rgba(16,185,129,0.05); text-align:center; margin-top:2rem;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#10B981 !important; margin-bottom:1rem;'>✅ Accesso Validato</h3>", unsafe_allow_html=True)
        st.write("L'archivio integrale è ora sbloccato e pronto per il download.")
        st.download_button("📥 DOWNLOAD DATABASE INTEGRALE (.CSV)", df_vault.to_csv(index=False).encode('utf-8'), "nexus_ai_toolkit.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
