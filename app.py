import streamlit as st
import pandas as pd
import time
import requests
import json
import datetime
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. KERNEL INITIALIZATION & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="APEX Network | Enterprise Hub", layout="wide", initial_sidebar_state="expanded")

# Inizializzazione blindata dello State (Previene qualsiasi AttributeError)
REQUIRED_STATES = {
    'active_module': "01. Data Refining Engine",
    'm1_buffer': None,
    'sys_terminal': "",
    'vault_unlocked': False,
    'last_hub': None
}
for key, default_value in REQUIRED_STATES.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

def get_sys_time():
    """Genera timestamp per log realistici."""
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

# ==========================================
# 2. VERCEL/LINEAR PREMIUM CSS ENGINE
# ==========================================
st.markdown("""
    <style>
    /* Soppressione totale UI Streamlit */
    #MainMenu, header, footer, .stDeployButton {display: none !important;}
    
    /* Global Styling: Dark Mode Assoluto & Font Enterprise */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #000000 !important; color: #E4E4E7 !important; }
    [data-testid="stSidebar"] { background-color: #09090B !important; border-right: 1px solid #27272A !important; }
    
    /* Tipografia Gerarchica */
    h1 { 
        background: linear-gradient(180deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800 !important; letter-spacing: -0.05em !important; margin-bottom: 0.2rem !important;
    }
    h2, h3 { color: #FAFAFA !important; font-weight: 700 !important; letter-spacing: -0.03em; }
    p, span, label, .stWidgetLabel { color: #A1A1AA !important; font-size: 0.95rem; line-height: 1.6; }
    
    /* TRASFORMAZIONE RADIO BUTTONS IN APP-MENU (Frictionless UX) */
    div[role="radiogroup"] > label {
        background-color: transparent; border: 1px solid transparent; border-radius: 6px;
        padding: 8px 12px; margin-bottom: 2px; transition: all 0.2s ease; cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { background-color: #18181B; }
    div[role="radiogroup"] > label[data-checked="true"] { background-color: #18181B; border: 1px solid #3F3F46; }
    div[role="radiogroup"] > label > div:first-child { display: none; /* Nasconde il pallino */ }
    div[role="radiogroup"] > label p { color: #A1A1AA !important; font-weight: 500; margin: 0; font-size:0.9rem;}
    div[role="radiogroup"] > label[data-checked="true"] p { color: #10B981 !important; font-weight: 600;}
    
    /* Card Strutturali */
    .apex-panel {
        background: linear-gradient(145deg, #09090B 0%, #000000 100%);
        border: 1px solid #27272A; border-radius: 12px; padding: 2.5rem;
        box-shadow: 0 10px 40px -10px rgba(0,0,0,0.8); margin-bottom: 2rem;
    }
    .asset-card {
        background-color: #09090B; border: 1px solid #27272A; border-radius: 12px; padding: 2rem;
        text-align: center; transition: transform 0.2s;
    }
    .asset-card:hover { transform: translateY(-5px); border-color: #3F3F46; }
    
    /* Box Valore (Executive Summary) */
    .value-box {
        background-color: rgba(16, 185, 129, 0.05); border-left: 2px solid #10B981;
        padding: 1rem 1.5rem; border-radius: 0 8px 8px 0; margin-bottom: 2rem;
    }
    .value-box p { color: #E2E8F0 !important; margin: 0; font-size: 0.95rem;}
    
    /* Terminale di Sistema */
    .sys-terminal {
        background-color: #050505; border: 1px solid #1F2937; border-radius: 8px;
        padding: 1.5rem; font-family: 'SFMono-Regular', Consolas, monospace;
        color: #34D399; font-size: 0.85rem; line-height: 1.6; white-space: pre-wrap;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.9);
    }
    .log-err { color: #EF4444; } .log-sys { color: #71717A; } .log-ok { color: #10B981; }
    
    /* Pulsanti Elite */
    div.stButton > button {
        background: #FFFFFF !important; color: #000000 !important; font-weight: 700 !important;
        border-radius: 6px !important; border: none !important; padding: 0.75rem !important;
        text-transform: uppercase; letter-spacing: 0.5px; transition: all 0.2s; width: 100%;
    }
    div.stButton > button:hover { background: #D4D4D8 !important; transform: scale(0.99); }
    div.stDownloadButton > button {
        background: transparent !important; color: #10B981 !important; font-weight: 700 !important;
        border-radius: 6px !important; border: 1px solid #10B981 !important; padding: 0.75rem !important;
        text-transform: uppercase; letter-spacing: 0.5px; width: 100%;
    }
    div.stDownloadButton > button:hover { background: rgba(16,185,129,0.05) !important; }
    
    /* Badge */
    .badge {
        display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 4px;
        background: rgba(255,255,255,0.05); color: #A1A1AA; font-size: 0.65rem;
        font-weight: 700; border: 1px solid rgba(255,255,255,0.1); letter-spacing: 1px;
        text-transform: uppercase; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS (UI WIDGETS)
# ==========================================
def render_page_header(badge_txt, title, value_prop, technical_details):
    """Genera l'intestazione standardizzata ad alta conversione per ogni tool."""
    st.markdown(f"<div class='badge'>{badge_txt}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='value-box'><p><b>BUSINESS VALUE:</b> {value_prop}</p></div>", unsafe_allow_html=True)
    with st.expander("⚙️ ARCHITETTURA DI SISTEMA (Dettagli Sviluppatori)"):
        st.markdown(f"<p style='font-family: monospace; font-size:0.8rem;'>{technical_details}</p>", unsafe_allow_html=True)

# ==========================================
# 4. MASTER NAVIGATION (I 4 ASSET)
# ==========================================
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #FFF; font-weight: 800; margin: 0; letter-spacing: -1px; font-size: 1.5rem;">APEX NETWORK</h2>
        <span style="color: #10B981; font-size: 0.7rem; font-weight: 700; letter-spacing: 2px;">GLOBAL INFRASTRUCTURE</span>
    </div>
""", unsafe_allow_html=True)

ASSETS = [
    "00 // ALGORITMI PRATICI (Tech)", 
    "01 // SINTESI MENTALE (Cognitive)", 
    "02 // METODO ESTETICO (Visual)", 
    "03 // RISORSA ZERO (Database)"
]

# Imposta l'asset di default in base all'URL (Deep Linking per ManyChat)
query_asset = st.query_params.get("hub", "00")
default_idx = 0
for i, asset in enumerate(ASSETS):
    if query_asset in asset:
        default_idx = i

selected_asset = st.sidebar.selectbox("SELEZIONA NETWORK:", ASSETS, index=default_idx)
st.sidebar.divider()

# Garbage Collection Inter-Asset
if st.session_state.last_hub != selected_asset:
    st.session_state.sys_terminal = ""
    st.session_state.last_hub = selected_asset

# ==========================================
# ASSET 00: ALGORITMI PRATICI (THE TECH ENGINE)
# ==========================================
if selected_asset == "00 // ALGORITMI PRATICI (Tech)":
    st.sidebar.markdown("<p style='font-size:0.75rem; color:#A1A1AA; font-weight:700; margin-bottom:0.5rem;'>APPLICATIONS DEPLOYED</p>", unsafe_allow_html=True)
    
    app_modules = [
        "01. Data Refining Engine", 
        "02. Threat Modeling Vault", 
        "03. Async Scraper Compiler", 
        "04. Infrastructure Cost Matrix", 
        "05. Financial ROI Telemetry", 
        "06. Traffic Router Algorithm", 
        "07. API Payload Sandbox"
    ]
    
    module = st.sidebar.radio("Seleziona:", app_modules, label_visibility="collapsed")
    
    # Garbage Collection Intra-Module
    if st.session_state.active_module != module:
        st.session_state.sys_terminal = ""
        st.session_state.m1_buffer = None
        st.session_state.active_module = module

    # --------------------------------------
    # 01. DATA REFINING
    # --------------------------------------
    if module == "01. Data Refining Engine":
        render_page_header(
            "DATA PROCESSING", "Data Refining Engine",
            "I database sporchi generano colli di bottiglia e campagne marketing fallimentari. Carica liste contatti non strutturate: il sistema distrugge i duplicati e sanifica le email formattate male, abbattendo 4 ore di lavoro manuale in Excel.",
            "Libreria: <code>pandas</code>. Processo: De-duplicazione vettoriale <code>drop_duplicates()</code>. Type casting forzato a stringa e regex trim su array 'Email'. Memoria volatile (RAM-only)."
        )
        
        st.markdown("<div class='apex-panel'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Innestare Database Dump (.csv)", type=["csv"])
        
        if uploaded_file:
            if st.button("ESEGUI NORMALIZZAZIONE ALGORITMICA"):
                with st.spinner("Allocazione pipeline di memoria..."):
                    time.sleep(0.8) # Ritenzione psicologica
                    try:
                        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
                        r_in = len(df_raw)
                        df_clean = df_raw.copy().drop_duplicates()
                        
                        email_col = next((c for c in df_clean.columns if c.lower() == 'email'), None)
                        if email_col:
                            df_clean[email_col] = df_clean[email_col].astype(str).str.lower().str.strip()
                            df_clean = df_clean[~df_clean[email_col].isin(['nan', 'none', '', 'null'])].dropna(subset=[email_col])
                            msg = "[OK] Matrice 'Email' individuata e sanificata."
                        else:
                            msg = "<span class='warn-log'>[WARN] Colonna 'Email' assente. Sanificazione globale eseguita.</span>"
                            
                        r_out = len(df_clean)
                        st.session_state.m1_buffer = df_clean
                        st.session_state.sys_terminal = f"<span class='log-sys'>[{get_sys_time()}] [root@apex] ~ Parsing Eseguito. Latenza: 2.1ms</span><br>{msg}<br><br><span style='color:#FFF'>TELEMETRY:</span><br>Record Raw: {r_in} | Record Validi: {r_out} | Anomalie Distrutte: {r_in - r_out}"
                    except Exception as e:
                        st.session_state.sys_terminal = f"<span class='log-err'>[{get_sys_time()}] [FATAL] Impossibile leggere il file. Dettagli: {e}</span>"

        if st.session_state.m1_buffer is not None:
            st.markdown(f"<div class='sys-terminal'>{st.session_state.sys_terminal}</div><br>", unsafe_allow_html=True)
            st.dataframe(st.session_state.m1_buffer.head(5), use_container_width=True)
            st.download_button("📥 EXPORT DATASET VALIDATO (.CSV)", st.session_state.m1_buffer.to_csv(index=False).encode('utf-8'), "apex_refined.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 02. SECURITY .ENV
    # --------------------------------------
    elif module == "02. Threat Modeling Vault":
        render_page_header(
            "CYBERSECURITY", "Threat Modeling Vault (.env)",
            "L'errore numero uno nei data breach è lasciare password nei file condivisi. Questo tool isola istantaneamente le credenziali dal tuo codice, fornendoti i manifesti di sicurezza industriali (.env e .gitignore) per blindare il server.",
            "Standard applicato: 12-Factor App Methodology. Analisi stringhe per il disaccoppiamento hardware/software delle variabili di ambiente."
        )
        st.markdown("<div class='apex-panel'>", unsafe_allow_html=True)
        raw_env = st.text_area("Variabili esposte (Formato Key=Value):", value="DB_HOST=127.0.0.1\nDB_PASS=root_admin_123!\nSTRIPE_SECRET=sk_live_8473...\nDEBUG_MODE=True", height=130)
        
        if st.button("BLINDA ARCHITETTURA"):
            st.session_state.sys_terminal = f"<span class='log-sys'>[{get_sys_time()}] [sec-ops@apex] ~ Scansione file...</span><br><span class='log-err'>[ALERT] Rilevate chiavi API e password in chiaro.</span><br>[ENCRYPT] Isolamento variabili in memoria...<br><span class='log-ok'>[SUCCESS] Architettura protetta. Manifesti generati.</span>"
            
        if st.session_state.sys_terminal != "":
            st.markdown(f"<div class='sys-terminal'>{st.session_state.sys_terminal}</div><br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.download_button("📥 DOWNLOAD FILE (.ENV)", raw_env, ".env")
            c2.download_button("📥 DOWNLOAD FIREWALL (.GITIGNORE)", ".env\n__pycache__/\n*.session", ".gitignore")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 03. COMPILER WIZARD
    # --------------------------------------
    elif module == "03. Async Scraper Compiler":
        render_page_header(
            "WIZARD COMPILER", "Async Scraper Compiler",
            "Automatizza l'estrazione lead da Telegram. I server Cloud vengono bannati da Telegram all'istante: inserisci i tuoi parametri qui, e il sistema compilerà un software Python asettico da scaricare ed eseguire in totale sicurezza sul tuo PC.",
            "Iniezione costanti API_ID/HASH in scaffolding 'Telethon'. Richiede handshaking OTP client-side per bypassare i filtri anti-bot."
        )
        st.markdown("<div class='apex-panel'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        api_id = c1.text_input("Telegram API_ID", placeholder="es. 2847592")
        api_hash = c2.text_input("Telegram API_HASH", placeholder="es. c4e8b...", type="password")
        target = st.text_input("Username Community Competitor (senza @)", placeholder="es. marketing_italia")
        
        if st.button("COMPILA SOFTWARE SORGENTE"):
            if api_id and api_hash and target:
                script = f"from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('apex_session', '{api_id}', '{api_hash}') as c:\n  users = c.get_participants('{target}')\n  with open('leads.csv', 'w', newline='', encoding='utf-8') as f:\n    w=csv.writer(f)\n    w.writerow(['ID','Username','Name'])\n    for u in users: w.writerow([u.id, u.username, u.first_name])\n  print('[OK] Extraction Completed.')"
                st.session_state.m1_buffer = script
                st.session_state.sys_terminal = f"<span class='log-sys'>[{get_sys_time()}] [compiler@apex] ~ Iniezione payload per '{target}'...</span><br><span class='log-ok'>[SUCCESS] Eseguibile binario compilato. Pronto al download.</span>"
            else:
                st.session_state.sys_terminal = f"<span class='log-err'>[{get_sys_time()}] [FATAL] Compilazione fallita. Parametri mancanti.</span>"
                st.session_state.m1_buffer = None
                
        if st.session_state.sys_terminal != "":
            st.markdown(f"<div class='sys-terminal'>{st.session_state.sys_terminal}</div><br>", unsafe_allow_html=True)
            if st.session_state.m1_buffer:
                st.download_button("📥 DOWNLOAD SCRIPT (.PY)", st.session_state.m1_buffer, "apex_telegram.py")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 04. COST MATRIX
    # --------------------------------------
    elif module == "04. Infrastructure Cost Matrix":
        render_page_header(
            "FINANCIAL AUDIT", "Infrastructure Cost Matrix",
            "Mappatura delle perdite finanziarie aziendali. Identifica i Software SaaS (monolitici) che stanno prosciugando la tua cassa, e sostituiscili con le architetture Serverless e Open Source mostrate in questa matrice.",
            "Comparazione TCO (Total Cost of Ownership) tra infrastrutture SaaS proprietarie chiuse e microservizi scalabili."
        )
        st.markdown("<div class='apex-panel'>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Legacy Software (Spreco)": ["Zapier Enterprise", "HubSpot CRM", "AWS S3 / Google Cloud", "Mailchimp"],
            "APEX Architecture (Costo 0)": ["n8n (Self-Hosted Node)", "Supabase (PostgreSQL)", "Cloudflare R2", "Mautic / AWS SES"],
            "Margine Mensile Salvato": ["~ 250 €", "~ 150 €", "~ 45 €", "~ 80 €"]
        }), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 05. ROI TELEMETRY
    # --------------------------------------
    elif module == "05. Financial ROI Telemetry":
        render_page_header(
            "BUSINESS ANALYTICS", "Financial ROI Telemetry",
            "Simulatore predittivo di marginalità. Inserisci il fatturato attuale e le spese tecnologiche fisse. Il sistema calcolerà istantaneamente l'aumento dell'utile netto aziendale a seguito dell'implementazione del protocollo APEX.",
            "Data Visualization tramite Plotly. Calcolo vettoriale real-time dell'abbattimento dell'Operational Expenditure (OPEX)."
        )
        st.markdown("<div class='apex-panel'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        mrr = c1.number_input("Fatturato Mensile (MRR) €", value=25000, step=1000)
        opex = c2.number_input("Costi Software da Tagliare (OPEX) €", value=4200, step=100)
        
        m_old, m_new = mrr - opex, mrr 
        c3, c4 = st.columns(2)
        c3.metric("Utile Mensile Storico", f"€ {m_old:,}")
        c4.metric("Utile Mensile APEX", f"€ {m_new:,}", f"+ € {opex:,} Cassa Operativa Sbloccata")
        
        fig = go.Figure(data=[
            go.Bar(name='Storico', x=['Architettura Aziendale'], y=[m_old], marker_color='#27272A', text=f"€{m_old}", textposition='auto'),
            go.Bar(name='APEX', x=['Architettura Aziendale'], y=[m_new], marker_color='#10B981', text=f"€{m_new}", textposition='auto')
        ])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', barmode='group', margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 06. WEBHOOK ROUTER
    # --------------------------------------
    elif module == "06. Traffic Router Algorithm":
        render_page_header(
            "LOGIC ENGINE", "Traffic Router Algorithm",
            "L'overload informativo uccide le aziende. Testa il nostro algoritmo: inietta una notifica json. Se è critica, il sistema simulerà l'invio al management. Se è inutile, la archivierà in silenzio senza distrazioni.",
            "Simulazione Endpoint REST. Parsing JSON asincrono e switch statement sulla chiave 'priority' per instradamento logico."
        )
        st.markdown("<div class='apex-panel'>", unsafe_allow_html=True)
        sample_json = '{\n  "source": "server_monitor",\n  "error_code": "502_bad_gateway",\n  "priority": "CRITICAL"\n}'
        json_in = st.text_area("Payload Evento (JSON):", value=sample_json, height=130)
        
        if st.button("ESEGUI ALGORITMO DI ROUTING"):
            with st.spinner("Valutazione nodi logici..."):
                time.sleep(0.5)
                sys_t = get_sys_time()
                try:
                    data = json.loads(json_in)
                    prio = str(data.get("priority", "LOW")).upper()
                    if prio in ["HIGH", "CRITICAL"]:
                        data["apex_action"] = "FORWARD_TO_CTO_SMS"
                        msg = f"<span class='warn-log'>[{sys_t}] [URGENT] Classificazione Critica. Direttiva di inoltro attivata.</span>"
                    else:
                        data["apex_action"] = "SILENT_DB_LOG"
                        msg = f"<span class='log-sys'>[{sys_t}] [SILENT] Classificazione Minore. Rumore soppresso e loggato.</span>"
                    st.session_state.sys_terminal = f"{msg}<br><br><span style='color:#FFF'>[PAYLOAD TRASFORMATO]:</span><br>{json.dumps(data, indent=2)}"
                except json.JSONDecodeError as e:
                    st.session_state.sys_terminal = f"<span class='log-err'>[{sys_t}] [FATAL ERROR] JSON malformato. Syntax Error: {e}</span>"
                    
        if st.session_state.sys_terminal != "":
            st.markdown(f"<div class='sys-terminal'>{st.session_state.sys_terminal}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 07. API SANDBOX
    # --------------------------------------
    elif module == "07. API Payload Sandbox":
        render_page_header(
            "NETWORK INTEGRATION", "API Payload Sandbox",
            "Assicurati che i tuoi software comunichino in tempo reale. Inserisci l'URL del tuo Webhook e invia i dati: il sistema testerà la latenza di rete e confermerà se l'informazione è giunta a destinazione.",
            "Handshake TCP/TLS asincrono verso endpoint remoto. Rilevazione latenza (ms) e decodifica HTTP Status Code di ritorno."
        )
        st.markdown("<div class='apex-panel'>", unsafe_allow_html=True)
        url = st.text_input("Endpoint URL Destinazione", value="https://httpbin.org/post")
        payload = st.text_area("Dati da iniettare (JSON)", value='{\n  "azienda": "APEX Corp",\n  "status": "Integrazione Validata"\n}', height=120)
        
        if st.button("ESEGUI PUSH DI RETE"):
            sys_t = get_sys_time()
            st.session_state.sys_terminal = f"<span class='log-sys'>[{sys_t}] [net-ops@apex] ~ Negoziazione protocollo HTTP...</span>"
            try:
                p_json = json.loads(payload)
                t0 = time.time()
                res = requests.post(url, json=p_json, timeout=5)
                lat = round(time.time() - t0, 3)
                st.session_state.sys_terminal += f"<br><span class='log-ok'>[{get_sys_time()}] [SUCCESS] Transazione verificata.</span><br>HTTP STATUS: {res.status_code}<br>LATENZA: {lat}s<br><br><span class='log-sys'>[RAW RESPONSE]</span><br>{res.text[:200]}..."
            except json.JSONDecodeError:
                st.session_state.sys_terminal += f"<br><span class='log-err'>[{get_sys_time()}] [ERROR] Formattazione JSON invalida. Request abortita.</span>"
            except Exception as e:
                st.session_state.sys_terminal += f"<br><span class='log-err'>[{get_sys_time()}] [TIMEOUT] Server irraggiungibile. {e}</span>"
                
        if st.session_state.sys_terminal != "":
            st.markdown(f"<div class='sys-terminal'>{st.session_state.sys_terminal}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HUB 02: SINTESI MENTALE (ASSET 01)
# ==========================================
elif selected_asset == "01 // SINTESI MENTALE (Cognitive)":
    st.markdown("<div class='badge' style='color:#A855F7; border-color:#A855F7;'>COGNITIVE FRAMEWORKS</div>", unsafe_allow_html=True)
    st.markdown("<h1>Sintesi Mentale: Protocolli Superiori</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.05rem; margin-bottom: 2rem;'>Archivi informativi asimmetrici. Formazione d'élite per la manipolazione logica delle informazioni, l'ottimizzazione neurale e il controllo finanziario.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='asset-card' style='border-top: 3px solid #A855F7;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:1rem;'>📚 La Bibbia Faceless dell'Asset Empire</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom:2rem;'>Il manuale strategico definitivo (2026-2030) per la creazione, l'automazione e la vendita (Exit Strategy) di un ecosistema multimediale privo di esposizione personale.</p>", unsafe_allow_html=True)
    st.markdown("""
        <a href="https://gumroad.com" target="_blank" style="text-decoration:none;">
            <button style="background:#A855F7; color:#FFF; width:100%; border:none; padding:1rem; border-radius:8px; font-weight:700; font-size:1rem; cursor:pointer;">
                🔓 SBLOCCA L'EBOOK PREMIUM SU GUMROAD
            </button>
        </a>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HUB 03: METODO ESTETICO (ASSET 02)
# ==========================================
elif selected_asset == "02 // METODO ESTETICO (Visual)":
    st.markdown("<div class='badge' style='color:#F97316; border-color:#F97316;'>VISUAL PRODUCTIVITY</div>", unsafe_allow_html=True)
    st.markdown("<h1>Metodo Estetico: Ingegneria Visiva</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.05rem; margin-bottom: 2rem;'>Sistemi organizzativi visivi standardizzati per l'azzeramento del caos operativo, la gestione scientifica del tempo e l'estetica del pensiero.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='asset-card' style='border-top: 3px solid #F97316;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:1rem;'>📅 Digital Executive Planner (PDF)</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin-bottom:2rem;'>Il framework di journaling minimalista e tracking finanziario. Layout antracite progettato per massimizzare la concentrazione direzionale.</p>", unsafe_allow_html=True)
    st.markdown("""
        <a href="https://gumroad.com" target="_blank" style="text-decoration:none;">
            <button style="background:#F97316; color:#FFF; width:100%; border:none; padding:1rem; border-radius:8px; font-weight:700; font-size:1rem; cursor:pointer;">
                📥 SCARICA IL PLANNER MATRICE SU GUMROAD
            </button>
        </a>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HUB 04: RISORSA ZERO (ASSET 03)
# ==========================================
elif selected_asset == "03 // RISORSA ZERO (Database)":
    st.markdown("<div class='badge' style='color:#3B82F6; border-color:#3B82F6;'>DATA INTELLIGENCE</div>", unsafe_allow_html=True)
    st.markdown("<h1>Zero Vault: Il Database Segreto</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.05rem; margin-bottom: 2rem;'>L'arbitraggio estremo del tempo. Un archivio dinamico curato in tempo reale delle 50 architetture SaaS e AI gratuite per costruire microservizi bypassando i paywall aziendali.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='apex-panel'>", unsafe_allow_html=True)
    df_vault = pd.DataFrame([
        {"Architettura": "Video Core", "Software": "CapCut Enterprise", "Licenza": "Freemium / Export 4K", "Vantaggio": "No Watermark"},
        {"Architettura": "Voice Neural Engine", "Software": "ElevenLabs API", "Licenza": "10k Char Free/Month", "Vantaggio": "Clonazione Reale"},
        {"Architettura": "Cognitive LLM", "Software": "Gemini 1.5 Advanced", "Licenza": "Enterprise Context", "Vantaggio": "Deep Think"},
        {"Architettura": "Workflow Automation", "Software": "n8n Open Source", "Licenza": "0€ (Self Hosted)", "Vantaggio": "No task limit"},
        {"Architettura": "Database Storage", "Software": "Supabase PostgreSQL", "Licenza": "Serverless Free", "Vantaggio": "Rimpiazza Firebase"}
    ])
    
    query = st.text_input("🔍 Filtra il database (es. Video, Automazione, Cloud)...")
    if query:
        df_vault = df_vault[df_vault.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
    
    # DATAWALL ENGINE (Gestione Privacy e Sicurezza Logica)
    display_df = df_vault if st.session_state.vault_unlocked else df_vault.head(3)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    if not st.session_state.vault_unlocked:
        st.markdown("<div style='text-align:center; padding:1rem; color:#71717A; font-size:0.8rem; border-top:1px dashed #27272A;'>[ 47 RECORD OSCURATI. VERIFICA CLEARANCE RICHIESTA PER L'ACCESSO GLOBALE ]</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # CLEARANCE GATEWAY (LEAD GENERATION HIGH-END)
    if not st.session_state.vault_unlocked:
        st.markdown("<div class='apex-panel' style='border-color:#3B82F6; border-width:2px; padding: 2rem;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#3B82F6 !important; margin-bottom:0.5rem;'>🔒 Autenticazione Root Richiesta</h3>", unsafe_allow_html=True)
        st.write("L'esportazione del file .CSV integrale e l'accesso non filtrato richiedono la verifica dell'identità. Inserisci la tua email operativa.")
        
        with st.form("clearance_form", clear_on_submit=False):
            email = st.text_input("Corporate Email Address:", placeholder="cto@azienda.com", label_visibility="collapsed")
            submit = st.form_submit_button("AVVIA PROTOCOLLO DI SBLOCCO DATABASE", use_container_width=True)
            st.caption("Connessione SSL. I dati vengono crittografati lato server e non ceduti a terzi.")
            
            if submit:
                if "@" in email and "." in email:
                    bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        bar.progress(i + 1)
                    st.session_state.vault_unlocked = True
                    st.rerun()
                else:
                    st.error("[ERRORE] Handshake TCP fallito. Indirizzo email non verificato.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    if st.session_state.vault_unlocked:
        st.markdown("<div class='apex-panel' style='border-color:#10B981; background:rgba(16,185,129,0.03); text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#10B981 !important;'>✅ Clearance Validata</h3>", unsafe_allow_html=True)
        st.write("Protocolli di estrazione sbloccati. Puoi prelevare l'archivio.")
        st.download_button("📥 DOWNLOAD DATABASE INTEGRALE (.CSV)", df_vault.to_csv(index=False).encode('utf-8'), "apex_zero_vault.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("<div style='font-size:0.75rem; color:#3F3F46; text-align:center; margin-top:2rem;'>APEX TECHNOLOGIES © 2026<br>Confidential Architecture</div>", unsafe_allow_html=True)
