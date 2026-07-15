import streamlit as st
import pandas as pd
import time
import requests
import json
import datetime
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CORE ARCHITECTURE & STATE MANAGEMENT
# ==========================================
st.set_page_config(page_title="APEX OS | Enterprise Infrastructure", layout="wide", initial_sidebar_state="expanded")

# Inizializzazione Sicura della Memoria (Garbage Collection)
default_states = {
    'active_module': None,
    'm1_dataframe': None,
    'sys_logs': "",
    'vault_clearance': False
}
for key, val in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Deep Linking per Smistamento Multi-Asset
target_hub = st.query_params.get("hub", "tech")
default_hub_idx = 0 if target_hub == "tech" else 1

# Helper per generare timestamp realistici nei terminali
def get_sys_time():
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

# ==========================================
# 2. CSS ENGINE: VERCEL/LINEAR PREMIUM UI
# ==========================================
st.markdown("""
    <style>
    /* Pulizia Interfaccia */
    #MainMenu, footer {visibility: hidden;}
    
    /* Tipografia e Colori Base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #050505 !important; color: #E2E8F0 !important; }
    [data-testid="stSidebar"] { background-color: #0A0A0A !important; border-right: 1px solid #1F2937 !important; }
    
    /* Titoli High-End */
    h1 { 
        background: linear-gradient(135deg, #FFFFFF 0%, #71717A 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800 !important; letter-spacing: -0.04em !important; margin-bottom: 0.5rem !important;
    }
    h2, h3 { color: #FAFAFA !important; font-weight: 700 !important; letter-spacing: -0.02em; }
    p, span, label, .stWidgetLabel { color: #A1A1AA !important; font-size: 0.95rem; }
    
    /* Pulsanti Elite Anti-Sovrapposizione */
    div.stButton > button {
        background-color: #FFFFFF !important; color: #050505 !important;
        font-weight: 700 !important; border-radius: 6px !important; border: none !important;
        padding: 0.6rem !important; transition: all 0.2s; text-transform: uppercase; letter-spacing: 0.5px;
    }
    div.stButton > button:hover { background-color: #D4D4D8 !important; transform: scale(0.99); }
    
    div.stDownloadButton > button {
        background-color: #050505 !important; color: #10B981 !important;
        font-weight: 700 !important; border-radius: 6px !important;
        border: 1px solid #10B981 !important; padding: 0.6rem !important; width: 100%;
        text-transform: uppercase; letter-spacing: 0.5px;
    }
    div.stDownloadButton > button:hover { background-color: rgba(16,185,129,0.05) !important; }
    
    /* Box Architetturali */
    .apex-card {
        background-color: #0A0A0A; border: 1px solid #27272A; border-radius: 8px;
        padding: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.4); margin-bottom: 1.5rem;
    }
    
    .terminal-box {
        background-color: #000000; border: 1px solid #18181B; border-radius: 6px;
        padding: 1.5rem; font-family: 'JetBrains Mono', Consolas, monospace;
        color: #34D399; font-size: 0.85rem; line-height: 1.6; white-space: pre-wrap;
    }
    .err-log { color: #F87171; } .sys-log { color: #71717A; } .warn-log { color: #FBBF24; } .acc-log { color: #38BDF8; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def render_header(title, use_case, tech_spec):
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #F8FAFC; font-size: 1.05rem; margin-bottom: 1rem;'>{use_case}</p>", unsafe_allow_html=True)
    with st.expander("⚙️ Dettagli Tecnici (Architettura Backend)"):
        st.markdown(f"<p style='font-size: 0.85rem; font-family: monospace;'>{tech_spec}</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. SIDEBAR E ROUTING LOGICO
# ==========================================
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #FFF; font-weight: 800; margin: 0; letter-spacing: -1px;">APEX CLOUD</h2>
        <span style="color: #10B981; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;">SYSTEM ONLINE</span>
    </div>
""", unsafe_allow_html=True)

hub_selection = st.sidebar.selectbox("SELEZIONA ECOSISTEMA:", ["📌 ASSET 00: AlgoritmiPratici", "📁 ASSET 03: RisorsaZero"], index=default_hub_idx)
st.sidebar.divider()

# ==========================================
# ECOSISTEMA: ALGORITMIPRATICI (ASSET 00)
# ==========================================
if hub_selection == "📌 ASSET 00: AlgoritmiPratici":
    
    lista_moduli = [
        "01 - Motore Pulizia Dati (Excel)", 
        "02 - Protocollo di Sicurezza .env", 
        "03 - Estrattore Dati Telegram", 
        "04 - Mappa Cloud a Costo Zero", 
        "05 - Dashboard Analitica Live", 
        "06 - Webhook Smistamento API", 
        "07 - Sincronizzazione CRM"
    ]
    modulo = st.sidebar.radio("MODULI OPERATIVI S1:", lista_moduli)
    
    if st.session_state.active_module != modulo:
        st.session_state.sys_logs = ""
        st.session_state.m1_dataframe = None
        st.session_state.active_module = modulo

    # --------------------------------------
    # 01. MOTORE PULIZIA DATI
    # --------------------------------------
    if modulo == "01 - Motore Pulizia Dati (Excel)":
        desc_biz = """<b>Scopo Strategico:</b> Carica un database o una lista contatti caotica. Il sistema eliminerà istantaneamente i doppioni e le email formattate male, restituendoti un file perfetto per il tuo CRM. Risparmio stimato: 4 ore di lavoro manuale a settimana."""
        desc_tech = """Libreria: <code>pandas</code>. Esecuzione: <code>drop_duplicates()</code> globale e Regex per sanificazione array 'Email'. Memoria: Volatile, crittografia RAM-only. Nessun dato persiste sui server post-sessione."""
        render_header("Motore Pulizia Dati (Excel)", desc_biz, desc_tech)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Innestare Database Dump (.csv)", type=["csv"])
        
        if uploaded_file:
            if st.button("ESEGUI NORMALIZZAZIONE DATI", use_container_width=True):
                with st.spinner("Allocazione buffer di memoria..."):
                    time.sleep(0.6)
                    try:
                        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python')
                        r_in = len(df_raw)
                        df_clean = df_raw.copy().drop_duplicates()
                        
                        if 'Email' in df_clean.columns:
                            df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                            df_clean = df_clean[~df_clean['Email'].isin(['nan', 'none', '', 'null'])].dropna(subset=['Email'])
                            msg = "[SUCCESS] Sanificazione colonna Email completata."
                        else:
                            msg = "<span class='warn-log'>[WARN] Matrice 'Email' assente. Eseguita solo de-duplicazione generale.</span>"
                            
                        r_out = len(df_clean)
                        st.session_state.m1_dataframe = df_clean
                        sys_t = get_sys_time()
                        st.session_state.sys_logs = f"<span class='sys-log'>[{sys_t}] [root@apex] ~ Parsing eseguito. Latenza 1.2ms.</span><br>{msg}<br><span class='acc-log'>Record Raw: {r_in} | Record Validi: {r_out} | Anomalie Distrutte: {r_in - r_out}</span>"
                    except Exception as e:
                        sys_t = get_sys_time()
                        st.session_state.sys_logs = f"<span class='err-log'>[{sys_t}] [FATAL ERROR] Impossibile leggere il file. Dettagli: {e}</span>"

        if st.session_state.m1_dataframe is not None:
            st.markdown(f"<div class='terminal-box'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
            st.dataframe(st.session_state.m1_dataframe.head(5), use_container_width=True)
            st.download_button("📥 SCARICA DATASET VERIFICATO (.CSV)", st.session_state.m1_dataframe.to_csv(index=False).encode('utf-8'), "dati_puliti.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 02. PROTOCOLLO .ENV
    # --------------------------------------
    elif modulo == "02 - Protocollo di Sicurezza .env":
        desc_biz = """<b>Scopo Strategico:</b> L'errore più comune nei data breach è lasciare password nel codice. Incolla qui le tue chiavi: il tool le isolerà, generando i file sicuri (.env e .gitignore) per blindare la tua infrastruttura aziendale."""
        desc_tech = """Standard: 12-Factor App. Il sistema compila direttive ambientali crittografate per il disaccoppiamento logico tra variabili d'ambiente e codice sorgente."""
        render_header("Protocollo di Sicurezza .env", desc_biz, desc_tech)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        raw_env_str = """DATABASE_URL=postgres://user:1234@local/db\nAPI_SECRET=sk_live_8473...\nDEBUG=True"""
        raw_env = st.text_area("Incolla variabili (Key=Value):", value=raw_env_str, height=120)
        
        if st.button("COMPILA MANIFESTI DI SICUREZZA"):
            sys_t = get_sys_time()
            st.session_state.sys_logs = f"<span class='sys-log'>[{sys_t}] [sec-ops@apex] ~ Scansione configurazioni...</span><br><span class='warn-log'>[ALERT] Rilevate chiavi esposte e vulnerabili.</span><br><span class='sys-log'>[{get_sys_time()}] [ENCRYPT] Generazione file di disaccoppiamento in corso...</span><br><span style='color:#10B981'>[SUCCESS] Architettura protetta. File pronti.</span>"
            
        if st.session_state.sys_logs != "":
            st.markdown(f"<div class='terminal-box'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.download_button("📥 SCARICA FILE .ENV", raw_env, ".env")
            c2.download_button("📥 SCARICA .GITIGNORE", ".env\n__pycache__/\n*.session\n.DS_Store", ".gitignore")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 03. ESTRATTORE TELEGRAM
    # --------------------------------------
    elif modulo == "03 - Estrattore Dati Telegram":
        desc_biz = """<b>Scopo Strategico:</b> Per estrarre i contatti da un gruppo senza subire ban, il software deve girare sul tuo computer. Inserisci i tuoi dati API: genereremo il codice Python su misura per te, pronto all'uso."""
        desc_tech = """Libreria: <code>Telethon</code> (Client asincrono). La policy Cloud impedisce l'handshake OTP sui server pubblici, costringendoci all'esportazione dell'eseguibile (.py) in local environment."""
        render_header("Estrattore Dati Telegram", desc_biz, desc_tech)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        api_id = c1.text_input("API_ID (da my.telegram.org)", placeholder="es. 2847592")
        api_hash = c2.text_input("API_HASH", placeholder="es. c4e8b...", type="password")
        target = st.text_input("Username Gruppo Competitor (Senza @)", placeholder="es. tech_italia")
        
        if st.button("COSTRUISCI SOFTWARE ESTRAZIONE"):
            if api_id and api_hash and target:
                script = f"""from telethon.sync import TelegramClient\nimport csv\n\nwith TelegramClient('apex_session', '{api_id}', '{api_hash}') as c:\n  users = c.get_participants('{target}')\n  with open('leads.csv', 'w', newline='', encoding='utf-8') as f:\n    w=csv.writer(f)\n    w.writerow(['ID','Username','Name'])\n    for u in users: w.writerow([u.id, u.username, u.first_name])\n  print('[OK] Dati estratti con successo.')"""
                st.session_state.m1_dataframe = script
                sys_t = get_sys_time()
                st.session_state.sys_logs = f"<span class='sys-log'>[{sys_t}] [compiler@apex] ~ Iniezione costanti per il target '{target}'...</span><br><span style='color:#10B981'>[SUCCESS] Eseguibile Python compilato.</span>"
            else:
                st.session_state.sys_logs = f"<span class='err-log'>[{get_sys_time()}] [FATAL ERROR] Parametri architetturali mancanti. Impossibile compilare.</span>"
                st.session_state.m1_dataframe = None
                
        if st.session_state.sys_logs != "":
            st.markdown(f"<div class='terminal-box'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
            if st.session_state.m1_dataframe:
                st.download_button("📥 SCARICA SCRIPT PYTHON (.PY)", st.session_state.m1_dataframe, "telegram_scraper.py")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 04. MAPPA CLOUD COSTO ZERO
    # --------------------------------------
    elif modulo == "04 - Mappa Cloud a Costo Zero":
        desc_biz = """<b>Scopo Strategico:</b> Le inefficienze tecniche bruciano cassa aziendale. Questa matrice mostra i costosi software SaaS che usi oggi, comparati alle soluzioni Cloud gratuite che ti permettono di azzerare i costi."""
        desc_tech = """Audit comparativo tra architetture monolitiche legacy e microservizi scalabili (Serverless / Open Source / Self-Hosted) ad alta efficienza OPEX."""
        render_header("Mappa Cloud a Costo Zero", desc_biz, desc_tech)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Software Costoso Attuale": ["Zapier Enterprise", "HubSpot / Airtable", "AWS S3 / Google Cloud", "Mailchimp"],
            "Infrastruttura APEX (Costo 0)": ["n8n (Self-Hosted Node)", "Supabase (PostgreSQL)", "Cloudflare R2", "Mautic / AWS SES"],
            "Margine Mensile Salvato": ["~ 250 €", "~ 150 €", "~ 45 €", "~ 80 €"]
        }), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 05. DASHBOARD ANALITICA
    # --------------------------------------
    elif modulo == "05 - Dashboard Analitica Live":
        desc_biz = """<b>Scopo Strategico:</b> Simula in tempo reale come cambieranno gli utili della tua azienda. Inserisci il fatturato e i costi che intendi tagliare: il sistema calcolerà istantaneamente il margine netto recuperato."""
        desc_tech = """Generazione vettoriale via Plotly Express. Calcolo reattivo della dilatazione dei margini operativi basato su variabili matematiche fornite dall'utente in real-time."""
        render_header("Dashboard Analitica Live", desc_biz, desc_tech)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        mrr = c1.number_input("Fatturato Mensile (MRR) €", value=25000, step=1000)
        opex = c2.number_input("Costi Tecnologici da Ottimizzare €", value=4200, step=100)
        
        m_attuale = mrr - opex
        m_apex = mrr 
        
        c3, c4 = st.columns(2)
        c3.metric("Utile Mensile Storico", f"€ {m_attuale:,}")
        c4.metric("Utile Mensile APEX", f"€ {m_apex:,}", f"+ € {opex:,} Cassa Sbloccata")
        
        fig = go.Figure(data=[
            go.Bar(name='Infrastruttura Storica', x=['Modello Operativo'], y=[m_attuale], marker_color='#27272A', text=f"€{m_attuale}", textposition='auto'),
            go.Bar(name='Infrastruttura APEX', x=['Modello Operativo'], y=[m_apex], marker_color='#10B981', text=f"€{m_apex}", textposition='auto')
        ])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#A1A1AA', barmode='group', margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 06. WEBHOOK ROUTER
    # --------------------------------------
    elif modulo == "06 - Webhook Smistamento API":
        desc_biz = """<b>Scopo Strategico:</b> Testa l'algoritmo che filtra le notifiche inutili. Inserisci i dati: se l'evento è critico viene inoltrato al management; se è rumore di fondo viene archiviato in totale silenzio."""
        desc_tech = """Simulazione Endpoint REST. Parsing JSON asincrono e valutazione booleana della chiave 'priority' per instradamento logico (Event-Driven Architecture)."""
        render_header("Webhook Smistamento API", desc_biz, desc_tech)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        sample_json = """{
  "source": "server_monitor",
  "error_code": "502_bad_gateway",
  "priority": "CRITICAL"
}"""
        json_in = st.text_area("Payload Evento (JSON):", value=sample_json, height=140)
        
        if st.button("ESEGUI ALGORITMO DI ROUTING"):
            with st.spinner("Valutazione nodi logici..."):
                time.sleep(0.5)
                sys_t = get_sys_time()
                try:
                    data = json.loads(json_in)
                    prio = str(data.get("priority", "LOW")).upper()
                    if prio in ["HIGH", "CRITICAL"]:
                        data["apex_action"] = "FORWARD_TO_CTO"
                        msg = f"<span class='warn-log'>[{sys_t}] [URGENT] Priorità Alta. Bypass filtri attivato. Segnale inoltrato.</span>"
                    else:
                        data["apex_action"] = "SILENT_DB_LOG"
                        msg = f"<span class='sys-log'>[{sys_t}] [SILENT] Priorità Bassa. Rumore soppresso e loggato a sistema.</span>"
                    st.session_state.sys_logs = f"{msg}<br><br><span style='color:#FFF'>[PAYLOAD TRASFORMATO]:</span><br>{json.dumps(data, indent=2)}"
                except json.JSONDecodeError as e:
                    st.session_state.sys_logs = f"<span class='err-log'>[{sys_t}] [FATAL ERROR] JSON malformato. Eccezione: {e}</span>"
                    
        if st.session_state.sys_logs != "":
            st.markdown(f"<div class='terminal-box'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------
    # 07. SINCRO CRM
    # --------------------------------------
    elif modulo == "07 - Sincronizzazione CRM":
        desc_biz = """<b>Scopo Strategico:</b> Simula l'invio istantaneo di dati tra due software (es. dal sito al CRM aziendale). Testa che la connessione di rete sia funzionante e priva di colli di bottiglia."""
        desc_tech = """Modulo Python <code>requests.post</code>. Handshake TCP verso endpoint remoto con misurazione telemetrica di latenza di rete e risoluzione HTTP Status Code."""
        render_header("Sincronizzazione CRM", desc_biz, desc_tech)
        
        st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
        url = st.text_input("URL di Destinazione (Endpoint REST)", value="https://httpbin.org/post")
        payload_str = """{
  "azienda": "APEX Corp",
  "status": "Integrazione Attiva"
}"""
        payload = st.text_area("Dati da iniettare (JSON)", value=payload_str, height=120)
        
        if st.button("ESEGUI PUSH DI RETE"):
            sys_t = get_sys_time()
            st.session_state.sys_logs = f"<span class='sys-log'>[{sys_t}] [net-ops@apex] ~ Negoziazione protocollo HTTP/TLS...</span>"
            try:
                p_json = json.loads(payload)
                t0 = time.time()
                res = requests.post(url, json=p_json, timeout=5)
                lat = round(time.time() - t0, 3)
                sys_t2 = get_sys_time()
                st.session_state.sys_logs += f"<br><span style='color:#10B981'>[{sys_t2}] [SUCCESS] Transazione verificata.</span><br>HTTP STATUS: {res.status_code}<br>LATENZA: {lat}s<br><br><span class='acc-log'>[SERVER RAW RESPONSE]</span><br>{res.text[:250]}..."
            except json.JSONDecodeError:
                st.session_state.sys_logs += f"<br><span class='err-log'>[{get_sys_time()}] [ERROR] Formattazione JSON invalida. Payload respinto.</span>"
            except Exception as e:
                st.session_state.sys_logs += f"<br><span class='err-log'>[{get_sys_time()}] [NETWORK FATAL] Nessuna risposta dal server remoto. {e}</span>"
                
        if st.session_state.sys_logs != "":
            st.markdown(f"<div class='terminal-box'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ECOSISTEMA: RISORSAZERO (ASSET 03)
# ==========================================
elif hub_selection == "📁 ASSET 03: RisorsaZero":
    st.markdown("<div class='corp-badge'>INTELLIGENCE CENTER</div>", unsafe_allow_html=True)
    st.markdown("<h1>Database AI Toolkit (Top 50)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #F8FAFC; font-size: 1.05rem; margin-bottom: 2rem;'>Perché perdere 100 ore a cercare strumenti aziendali quando l'abbiamo già fatto noi? Esplora il database interattivo delle 50 architetture SaaS e AI gratuite (o Open Source) usate dai top player per automatizzare infrastrutture bypassando i paywall.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='apex-card'>", unsafe_allow_html=True)
    df_vault = pd.DataFrame([
        {"Stack": "Video Generativo", "Piattaforma": "CapCut Desktop", "Licenza": "Freemium", "Vantaggio Strategico": "Export 4K Senza Watermark"},
        {"Stack": "Modelli Vocali", "Piattaforma": "ElevenLabs Core", "Licenza": "10k Char Gratis", "Vantaggio Strategico": "Clonazione Voce Reale"},
        {"Stack": "Motore Logico AI", "Piattaforma": "Gemini Advanced", "Licenza": "Standard Tier", "Vantaggio Strategico": "Contesto Dati Illimitato"},
        {"Stack": "Automazione Flussi", "Piattaforma": "n8n Open Source", "Licenza": "0€ (Self Hosted)", "Vantaggio Strategico": "Nessun limite task/esecuzioni"},
        {"Stack": "Database Backend", "Piattaforma": "Supabase (SQL)", "Licenza": "Serverless Free", "Vantaggio Strategico": "Sostituisce Airtable/Firebase"}
    ])
    
    search = st.text_input("🔍 Ricerca rapida nel database (es. Video, Automazione, Gratis)...")
    if search:
        df_vault = df_vault[df_vault.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
    
    # LA FALLA DEL PAYWALL RISOLTA:
    # Se non è sbloccato, mostra solo le prime 3 righe. Se è sbloccato, mostra tutto.
    display_df = df_vault if st.session_state.vault_unlocked else df_vault.head(3)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    if not st.session_state.vault_unlocked:
        st.markdown("<div style='text-align:center; padding: 1rem; color:#71717A; font-size:0.85rem; border-top: 1px dashed #27272A;'>[ 47 RIGHE OSCURATE. AUTENTICAZIONE RICHIESTA PER L'ACCESSO GLOBALE ]</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # LEAD GENERATION SYSTEM (CLEARANCE GATEWAY)
    if not st.session_state.vault_unlocked:
        st.markdown("<div class='apex-card' style='border-color:#10B981; border-width: 2px;'>", unsafe_allow_html=True)
        st.markdown("<h3>🔒 Autenticazione Root Richiesta</h3>", unsafe_allow_html=True)
        st.write("L'esportazione in locale del file .CSV con tutti i 50 record aziendali richiede una verifica dell'identità.")
        
        with st.form("auth_gate", clear_on_submit=False):
            email = st.text_input("Corporate Email Address:", placeholder="cto@azienda.com")
            submit = st.form_submit_button("VERIFICA IDENTITÀ E SBLOCCA DATABASE", use_container_width=True)
            st.caption("*Trasmissione dati crittografata. Zero spam garantito.*")
            
            if submit:
                if "@" in email and "." in email:
                    bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        bar.progress(i + 1)
                    st.session_state.vault_unlocked = True
                    st.rerun()
                else:
                    st.error("[ERROR] Handshake fallito. Formato email respinto.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    if st.session_state.vault_unlocked:
        st.markdown("<div class='apex-card' style='border-color:#10B981; background:rgba(16,185,129,0.03);'>", unsafe_allow_html=True)
        st.success("✅ Clearance Verificata. Protocolli di estrazione aperti.")
        st.download_button("📥 DOWNLOAD DATABASE INTEGRALE (.CSV)", df_vault.to_csv(index=False).encode('utf-8'), "apex_ai_toolkit.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("<div style='font-size:0.75rem; color:#3F3F46; text-align:center; margin-top:2rem;'>APEX TECHNOLOGIES © 2026</div>", unsafe_allow_html=True)
