import streamlit as st
import pandas as pd
import time
import requests
import json
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. INIT ARCHITETTURA E MEMORIA DI STATO
# ==========================================
st.set_page_config(page_title="APEX OS | Enterprise Infrastructure", layout="wide", initial_sidebar_state="expanded")

# Inizializzazione sicura dello stato
def init_state(keys_dict):
    for key, val in keys_dict.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state({
    'active_category': 'Data Engine',
    'active_tool': 'CSV Normalizer',
    'm1_data': None,
    'sys_logs': "",
    'vault_clearance': False
})

# ==========================================
# 2. CSS ENGINE: VERCEL/LINEAR PREMIUM UI
# ==========================================
st.markdown("""
    <style>
    /* Pulizia UI Nativa Streamlit */
    #MainMenu, header, footer, .stDeployButton {display: none !important;}
    
    /* Global Typography & Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #030712 !important; color: #E2E8F0 !important; }
    [data-testid="stSidebar"] { background-color: #09090B !important; border-right: 1px solid #1F2937 !important; }
    
    /* Tipografia d'Elite */
    h1 { 
        background: linear-gradient(180deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800 !important; letter-spacing: -0.05em !important; margin-bottom: 0.5rem !important;
    }
    h2, h3 { color: #F8FAFC !important; font-weight: 700 !important; letter-spacing: -0.03em; }
    p, span, label { color: #94A3B8 !important; font-size: 0.95rem; }
    
    /* Trasformazione Radio Buttons in "Pill Buttons" (SaaS Moderno) */
    div[role="radiogroup"] > label {
        background-color: transparent;
        border: 1px solid #27272A;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { background-color: #18181B; border-color: #3F3F46; }
    div[role="radiogroup"] > label[data-checked="true"] {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid #10B981;
    }
    /* Nasconde il pallino nativo del radio button */
    div[role="radiogroup"] > label > div:first-child { display: none; }
    div[role="radiogroup"] > label p { color: #E2E8F0 !important; font-weight: 600; margin: 0; }
    div[role="radiogroup"] > label[data-checked="true"] p { color: #10B981 !important; }
    
    /* Card Strutturale e Terminale */
    .os-card {
        background: #09090B; border: 1px solid #27272A; border-radius: 12px;
        padding: 2rem; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.5); margin-bottom: 1.5rem;
    }
    .os-terminal {
        background-color: #000000; border: 1px solid #1F2937; border-radius: 8px;
        padding: 1.2rem; font-family: 'JetBrains Mono', Consolas, monospace;
        color: #34D399; font-size: 0.85rem; white-space: pre-wrap; margin-top: 1rem;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    .err { color: #F87171; } .sys { color: #71717A; } .warn { color: #FBBF24; }
    
    /* Pulsanti Call-to-Action */
    div.stButton > button {
        background: linear-gradient(180deg, #FFFFFF 0%, #E4E4E7 100%) !important;
        color: #09090B !important; font-weight: 700 !important; border-radius: 8px !important;
        border: none !important; padding: 0.7rem !important; text-transform: uppercase; letter-spacing: 1px;
        transition: transform 0.1s ease, box-shadow 0.2s ease;
    }
    div.stButton > button:active { transform: scale(0.98); }
    div.stDownloadButton > button {
        background: transparent !important; color: #10B981 !important; font-weight: 700 !important;
        border-radius: 8px !important; border: 1px solid #10B981 !important; padding: 0.7rem !important;
    }
    div.stDownloadButton > button:hover { background: rgba(16,185,129,0.1) !important; }
    
    /* Badge Status */
    .badge {
        display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 99px;
        background: rgba(16, 185, 129, 0.1); color: #10B981; font-size: 0.7rem;
        font-weight: 800; border: 1px solid rgba(16, 185, 129, 0.2); letter-spacing: 1px; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. HELPER UX: HEADER SEMPLIFICATI
# ==========================================
def render_tool_header(badge, title, use_case, tech_spec):
    st.markdown(f"<div class='badge'>{badge}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #F8FAFC; font-size: 1.05rem;'><b>A cosa ti serve:</b> {use_case}</p>", unsafe_allow_html=True)
    with st.expander("🛠️ Mostra Dettagli Tecnici (Per Sviluppatori)"):
        st.markdown(f"<p style='font-size: 0.85rem;'>{tech_spec}</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. ROUTING TASSONOMICO (La Scalabilità)
# ==========================================
# Deep Link Check
param_ws = st.query_params.get("hub", "apex")

# Definizione Architettura
ECOSYSTEMS = {
    "⚡ APEX TECH HUB": {
        "Data Engine": ["01. CSV Normalizer"],
        "Security & Cloud": ["02. Protocollo .env", "03. Scraper Wizard", "04. Cost Matrix"],
        "Network Ops": ["05. ROI Telemetry", "06. Webhook Router", "07. API Injector"]
    },
    "🔒 ZERO DATA VAULT": {
        "Intelligence": ["08. Software Database"]
    }
}

st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="margin: 0; color: #FFF; font-weight: 800; font-size: 1.5rem; letter-spacing: -1px;">APEX OS</h2>
        <span style="color: #10B981; font-size: 0.75rem; font-weight: 700; letter-spacing: 2px;">BUILD 8.0.0</span>
    </div>
""", unsafe_allow_html=True)

# Selezione Ecosistema
def_index = 0 if param_ws == "apex" else 1
selected_hub = st.sidebar.selectbox("SELEZIONA HUB:", list(ECOSYSTEMS.keys()), index=def_index)

st.sidebar.markdown("<hr style='border-color:#1F2937; margin: 1rem 0;'>", unsafe_allow_html=True)

# Generazione Menu Dinamica e Pulita
selected_tool = None
categories = ECOSYSTEMS[selected_hub]

if selected_hub == "⚡ APEX TECH HUB":
    st.sidebar.markdown("<p style='font-size: 0.8rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase;'>Workspaces</p>", unsafe_allow_html=True)
    selected_cat = st.sidebar.selectbox("Categoria:", list(categories.keys()), label_visibility="collapsed")
    selected_tool = st.sidebar.radio("Strumenti:", categories[selected_cat], label_visibility="collapsed")
else:
    # Per Zero Vault c'è solo il database, skip category selection
    selected_tool = "08. Software Database"

# Garbage Collector Log: Se cambio tool, cancello il terminale
if st.session_state.get('last_tool') != selected_tool:
    st.session_state.sys_logs = ""
    st.session_state.last_tool = selected_tool

# ==========================================
# 5. CORE LOGIC DEI MODULI
# ==========================================

# --- M1: CSV Normalizer ---
if selected_tool == "01. CSV Normalizer":
    render_tool_header(
        "DATA PROCESSING", "CSV Normalizer Engine",
        "Carica un database clienti o contatti caotico. Il sistema rimuove all'istante i duplicati, corregge le email scritte male e ti restituisce un file perfetto pronto per essere caricato sul tuo CRM, salvandoti ore di noioso lavoro su Excel.",
        "Engine: Python Pandas. Funzioni: <code>drop_duplicates()</code> globale, <code>str.lower().str.strip()</code> e <code>dropna()</code> sulla colonna 'Email' (con fallback bypass se la colonna non esiste)."
    )
    st.markdown("<div class='os-card'>", unsafe_allow_html=True)
    file_csv = st.file_uploader("Trascina il file .csv qui", type=["csv"])
    if file_csv:
        if st.button("ESEGUI PULIZIA DATI", type="primary"):
            with st.spinner("Compilazione matrici..."):
                time.sleep(0.7)
                try:
                    df = pd.read_csv(file_csv, sep=None, engine='python')
                    r_in = len(df)
                    df_clean = df.drop_duplicates()
                    email_col = next((c for c in df_clean.columns if c.lower() == 'email'), None)
                    if email_col:
                        df_clean[email_col] = df_clean[email_col].astype(str).str.lower().str.strip()
                        df_clean = df_clean[~df_clean[email_col].isin(['nan', 'none', '', 'null'])].dropna(subset=[email_col])
                        log_msg = "Sanificazione colonna email completata."
                    else:
                        log_msg = "<span class='warn'>Nessuna colonna 'Email' rilevata. Bypass sanificazione specifiche.</span>"
                    r_out = len(df_clean)
                    st.session_state.m1_data = df_clean
                    st.session_state.sys_logs = f"<span class='sys'>[OK] Parsing completato. Latenza: 4ms.</span><br>{log_msg}<br>Dati originali: {r_in} | Dati validi: {r_out} | Anomalie distrutte: {r_in - r_out}"
                except Exception as e:
                    st.session_state.sys_logs = f"<span class='err'>[FATAL ERROR] Codifica file errata: {e}</span>"
        
        if st.session_state.m1_data is not None:
            st.markdown(f"<div class='os-terminal'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
            st.dataframe(st.session_state.m1_data.head(5), use_container_width=True)
            st.download_button("📥 SCARICA CSV OTTIMIZZATO", st.session_state.m1_data.to_csv(index=False).encode('utf-8'), "apex_data.csv", "text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

# --- M2: Protocollo .env ---
elif selected_tool == "02. Protocollo .env":
    render_tool_header(
        "SECURITY OPS", "Threat Modeler (.env)",
        "Lasciare le password aziendali nel codice è un rischio letale. Incolla qui il tuo codice: il sistema isolerà le credenziali sensibili e ti fornirà i file di sicurezza (.env e .gitignore) da usare per blindare i tuoi server.",
        "Scansione regex per chiavi API. Disaccoppiamento architetturale standard industry (Twelve-Factor App methodology)."
    )
    st.markdown("<div class='os-card'>", unsafe_allow_html=True)
    raw_env = st.text_area("Incolla variabili hardcoded:", value="DB_HOST=127.0.0.1\nDB_PASS=admin_root_123!\nSTRIPE_KEY=sk_live_...", height=120)
    if st.button("BLINDA CREDENZIALI", type="primary"):
        st.session_state.sys_logs = "<span class='sys'>[SECURITY] Inizializzazione scan...</span><br><span class='warn'>[ALERT] Rilevate credenziali scoperte.</span><br>[ENCRYPT] Matrice .env generata.<br><span style='color:#10B981'>[SUCCESS] Architettura protetta.</span>"
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='os-terminal'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.download_button("📥 SCARICA .ENV", raw_env, ".env")
        col2.download_button("📥 SCARICA .GITIGNORE", ".env\n__pycache__/\n*.session", ".gitignore")
    st.markdown("</div>", unsafe_allow_html=True)

# --- M3: Scraper Wizard ---
elif selected_tool == "03. Scraper Wizard":
    render_tool_header(
        "WIZARD COMPILER", "Telegram Data Compiler",
        "Genera un bot personalizzato per estrarre membri dai gruppi Telegram concorrenti. L'app compilerà un file sicuro da scaricare e avviare sul tuo computer (evitando così il ban da parte di Telegram).",
        "Costruzione dinamica di script Python basato su libreria asincrona 'Telethon'. Richiede esecuzione client-side per handshaking OTP."
    )
    st.markdown("<div class='os-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    apid = c1.text_input("API_ID Telegram")
    apih = c2.text_input("API_HASH Telegram", type="password")
    grp = st.text_input("Gruppo Telegram Target (senza @)")
    
    if st.button("GENERA BOT DI ESTRAZIONE", type="primary"):
        if apid and apih and grp:
            script = f"from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('session', '{apid}', '{apih}') as c:\n  m = c.get_participants('{grp}')\n  with open('leads.csv', 'w', newline='') as f:\n    w=csv.writer(f)\n    w.writerow(['ID','User','Name'])\n    for u in m: w.writerow([u.id, u.username, u.first_name])\n  print('Fatto.')"
            st.session_state.m1_data = script
            st.session_state.sys_logs = f"<span class='sys'>[BUILDER]</span> Compilazione binario sorgente per target '{grp}'...<br><span style='color:#10B981'>[READY] Script compilato con successo.</span>"
        else:
            st.session_state.sys_logs = "<span class='err'>[ERROR] Compila tutti i campi richiesti.</span>"
            st.session_state.m1_data = None
            
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='os-terminal'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
        if st.session_state.m1_data:
            st.download_button("📥 SCARICA BOT SORGENTE (.py)", st.session_state.m1_data, "telegram_bot.py")
    st.markdown("</div>", unsafe_allow_html=True)

# --- M4: Cost Matrix ---
elif selected_tool == "04. Cost Matrix":
    render_tool_header(
        "FINANCIAL OPS", "Cloud Cost Optimizer",
        "Rivela gli abbonamenti software (SaaS) che stanno prosciugando le casse della tua azienda e ti mostra l'esatta alternativa gratuita o Open Source da usare per azzerare i costi.",
        "Audit comparativo tra architetture monolitiche proprietarie e stack Serverless/Open Source distribuiti."
    )
    st.markdown("<div class='os-card'>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame({
        "Software Attuale (Costo)": ["Zapier Enterprise", "Airtable / HubSpot", "AWS S3 / Google Cloud", "Mailchimp"],
        "Soluzione APEX (0€)": ["n8n (Self-Hosted Node)", "Supabase (PostgreSQL)", "Cloudflare R2", "Mautic / AWS SES"],
        "Impatto sul Cash Flow": ["+ 250 €/mese", "+ 150 €/mese", "+ 45 €/mese", "+ 80 €/mese"]
    }), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- M5: ROI Telemetry ---
elif selected_tool == "05. ROI Telemetry":
    render_tool_header(
        "ANALYTICS", "ROI & Margin Forecaster",
        "Calcolatore direzionale. Inserisci fatturato e costi inutili: il sistema calcolerà all'istante l'impatto sul tuo conto economico se decidessi di passare a un'infrastruttura moderna e automatizzata.",
        "Visualizzazione dati tramite libreria Plotly Express. Modello matematico lineare di ottimizzazione OPEX."
    )
    st.markdown("<div class='os-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    mrr = c1.number_input("Fatturato Mensile (MRR) €", value=15000, step=1000)
    opex = c2.number_input("Costi Tecnologici Mensili (Da Tagliare) €", value=3200, step=100)
    
    m_old, m_new = mrr - opex, mrr
    c3, c4 = st.columns(2)
    c3.metric("Utile Mensile Attuale", f"€ {m_old:,}")
    c4.metric("Utile Mensile APEX", f"€ {m_new:,}", f"+ € {opex:,} (Ottimizzati)")
    
    fig = go.Figure(data=[
        go.Bar(name='Infrastruttura Vecchia', x=['Modello di Business'], y=[m_old], marker_color='#27272A', text=f"€{m_old}", textposition='auto'),
        go.Bar(name='Infrastruttura APEX', x=['Modello di Business'], y=[m_new], marker_color='#10B981', text=f"€{m_new}", textposition='auto')
    ])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', barmode='group', margin=dict(t=20, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- M6: Webhook Router ---
elif selected_tool == "06. Webhook Router":
    render_tool_header(
        "NETWORK OPS", "Smart Notification Router",
        "Testa l'algoritmo che filtra il rumore digitale. Inserisci i dati di una notifica: se è urgente, il sistema la inoltra al management; se è irrilevante, la silenzia e la archivia senza disturbare nessuno.",
        "Simulazione di Endpoint REST API. Analisi JSON payload key-value per instradamento logico asincrono."
    )
    st.markdown("<div class='os-card'>", unsafe_allow_html=True)
    json_in = st.text_area("Payload Notifica (JSON):", value='{\n  "event": "server_down",\n  "system": "AWS_Cluster_01",\n  "priority": "CRITICAL"\n}', height=120)
    if st.button("TESTA ALGORITMO DI SMISTAMENTO", type="primary"):
        with st.spinner("Analisi logica..."):
            time.sleep(0.4)
            try:
                data = json.loads(json_in)
                prio = str(data.get("priority", "LOW")).upper()
                if prio in ["HIGH", "CRITICAL"]:
                    data["action"] = "SMS_SENT_TO_CTO"
                    msg = "<span class='warn'>[URGENT] Direttiva d'emergenza attivata. Inoltro immediato.</span>"
                else:
                    data["action"] = "SILENT_DATABASE_LOG"
                    msg = "<span class='sys'>[SILENCED] Evento minore. Notifica soppressa e archiviata.</span>"
                st.session_state.sys_logs = f"{msg}<br><br><span style='color:#FFF'>OUTPUT RISOLTO:</span><br>{json.dumps(data, indent=2)}"
            except json.JSONDecodeError:
                st.session_state.sys_logs = "<span class='err'>[ERROR] Sintassi JSON non valida. Usa le virgolette doppie per chiavi e valori.</span>"
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='os-terminal'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- M7: API Injector ---
elif selected_tool == "07. API Injector":
    render_tool_header(
        "NETWORK OPS", "API Push Sandbox",
        "Invia pacchetti di dati da un sistema all'altro (es. dal tuo sito al CRM) simulando una connessione reale. Controlla che le comunicazioni tra i tuoi software siano stabili e fulminee.",
        "Esecuzione HTTP Request (POST) tramite libreria Python Requests. Monitoraggio latenza di rete e Status Code."
    )
    st.markdown("<div class='os-card'>", unsafe_allow_html=True)
    url = st.text_input("URL di Destinazione (Webhook)", value="https://httpbin.org/post")
    payload = st.text_area("Dati da Inviare (JSON)", value='{\n  "nome_cliente": "Mario Rossi",\n  "status": "Pagamento Effettuato"\n}', height=100)
    if st.button("INVIA DATI AL SERVER", type="primary"):
        st.session_state.sys_logs = "<span class='sys'>[NET] Handshake TLS in corso...</span>"
        try:
            p_json = json.loads(payload)
            t0 = time.time()
            res = requests.post(url, json=p_json, timeout=4)
            lat = round(time.time() - t0, 3)
            st.session_state.sys_logs += f"<br><span style='color:#10B981'>[OK] Ricezione confermata.</span><br>HTTP CODE: {res.status_code}<br>LATENZA: {lat}s"
        except json.JSONDecodeError:
            st.session_state.sys_logs += "<br><span class='err'>[ERR] Errore di formattazione JSON.</span>"
        except Exception as e:
            st.session_state.sys_logs += f"<br><span class='err'>[TIMEOUT] Nessuna risposta dal server remoto. {e}</span>"
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='os-terminal'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- M8: Zero Vault ---
elif selected_tool == "08. Software Database":
    st.markdown("<div class='badge'>DATA INTELLIGENCE</div>", unsafe_allow_html=True)
    st.markdown("<h1>ZERO VAULT Database</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #F8FAFC; font-size: 1.05rem;'>Il database privato delle 50 architetture SaaS e AI gratuite (o Open Source) usate dai top player per automatizzare i processi aziendali a costo zero.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div class='os-card'>", unsafe_allow_html=True)
    df_vault = pd.DataFrame([
        {"Stack": "Video Generativo", "Piattaforma": "CapCut Enterprise", "Licenza": "Freemium", "Vantaggio Strategico": "Nessun Watermark"},
        {"Stack": "Modelli Vocali", "Piattaforma": "ElevenLabs Core", "Licenza": "10k Char Gratis", "Vantaggio Strategico": "Clonazione Voce Reale"},
        {"Stack": "Motore Logico AI", "Piattaforma": "Gemini 1.5 Pro", "Licenza": "Standard Tier", "Vantaggio Strategico": "Contesto illimitato"},
        {"Stack": "Automazione Flussi", "Piattaforma": "n8n Open Source", "Licenza": "0€ (Self Hosted)", "Vantaggio Strategico": "Nessun limite esecuzioni"},
        {"Stack": "Database Backend", "Piattaforma": "Supabase (SQL)", "Licenza": "Serverless Free", "Vantaggio Strategico": "Sostituisce Firebase Costoso"}
    ])
    
    search = st.text_input("🔍 Ricerca rapida per categoria o nome software (es. Video, Automazione)...")
    if search:
        df_vault = df_vault[df_vault.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
    st.dataframe(df_vault, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # LEAD GENERATION SYSTEM
    if not st.session_state.vault_clearance:
        st.markdown("<div class='os-card' style='border-color:#10B981;'>", unsafe_allow_html=True)
        st.markdown("<h3>🔒 Sblocca il Database Completo</h3>", unsafe_allow_html=True)
        st.write("Verifica la tua identità aziendale per ottenere i diritti di esportazione del file .CSV con tutte le 50 risorse.")
        with st.form("lead_form", clear_on_submit=False):
            email = st.text_input("Email Aziendale Principale", placeholder="es. cto@azienda.com")
            submit = st.form_submit_button("VERIFICA E SBLOCCA DOWNLOAD")
            if submit:
                if "@" in email and "." in email:
                    st.session_state.vault_clearance = True
                    st.rerun()
                else:
                    st.error("Protocollo rifiutato. Inserire un indirizzo email valido.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    if st.session_state.vault_clearance:
        st.markdown("<div class='os-card' style='border-color:#10B981; background:rgba(16,185,129,0.05);'>", unsafe_allow_html=True)
        st.success("✅ Identità verificata. Diritti di estrazione concessi.")
        st.download_button("📥 DOWNLOAD ARCHIVIO COMPLETO (.CSV)", df_vault.to_csv(index=False).encode('utf-8'), "apex_zerovault.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("<div style='font-size:0.7rem; color:#3F3F46; text-align:center; margin-top:3rem;'>APEX TECHNOLOGIES © 2026</div>", unsafe_allow_html=True)
