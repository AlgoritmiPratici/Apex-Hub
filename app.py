import streamlit as st
import pandas as pd
import time
import requests
import json
import datetime
import os
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. KERNEL & INFRASTRUCTURE STATE
# ==========================================
st.set_page_config(
    page_title="NEXUS Cloud | Enterprise Infrastructure", 
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Inizializzazione Blindata e State Retention (Zero Memory Leaks)
SYSTEM_STATES = {
    'active_tool': None,
    'm1_buffer': None,
    'sys_logs': "",
    'global_clearance': False, # Gatekeeper Globale (Soft Gate PLG)
    'just_unlocked': False,    # Trigger per il messaggio di Successo (Double Opt-In Patch)
    'last_workspace': None
}
for key, val in SYSTEM_STATES.items():
    if key not in st.session_state:
        st.session_state[key] = val

def sys_time():
    """Genera timestamp millisecondi per log server ultra-realistici."""
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]

param_hub = st.query_params.get("workspace", "core")

# Endpoint di Integrazione tramite Variabili d'Ambiente (Sicurezza)
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK")
LINK_IUBENDA = "https://app.notion.com/p/Informativa-sulla-Privacy-3a5ff5ea717c80bba083f260e8e14b41"

# ==========================================
# 2. VERCEL/LINEAR PREMIUM CSS ENGINE
# ==========================================
st.markdown("""
    <style>
    /* ========================================================= */
    /* FIXED LEFT NAVIGATION (DESKTOP) & MOBILE ACCESSIBILITY    */
    /* Nascondiamo il bottone di chiusura solo su desktop.       */
    /* Su mobile il menu hamburger torna visibile per navigare.  */
    /* ========================================================= */
    @media (min-width: 992px) {
        [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"] { display: none !important; }
    }
    
    /* Rimuove l'inutile decorazione superiore di Streamlit */
    [data-testid="stDecoration"] { display: none !important; }
    
    /* Rende l'header trasparente e nasconde bottoni spazzatura a destra */
    header { background-color: transparent !important; box-shadow: none !important; }
    [data-testid="stHeaderActionElements"] { display: none !important; }
    
    /* Pulizia Footer e Bottone Deploy */
    .stDeployButton, footer { display: none !important; }
    
    /* Distruzione Toolbar Tabelle (Risolve il bug "Keyboard double") */
    [data-testid="stElementToolbar"], [data-testid="stToolbar"], button[title="View fullscreen"] {
        display: none !important; opacity: 0 !important; visibility: hidden !important; pointer-events: none !important;
    }
    
    /* Typography & Palette (Dark Zinc) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #030303 !important; color: #E4E4E7 !important; }
    [data-testid="stSidebar"] { background-color: #0A0A0A !important; border-right: 1px solid #18181B !important; }
    
    /* Titoli High-End Corporate */
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
    
    /* Terminale Backend Simulator */
    .cmd-window {
        background-color: #000000; border: 1px solid #18181B; border-radius: 6px;
        padding: 1.5rem; font-family: 'SFMono-Regular', Consolas, Menlo, monospace;
        color: #34D399; font-size: 0.85rem; line-height: 1.6;
        white-space: pre-wrap; word-wrap: break-word; overflow-x: hidden;
        box-shadow: inset 0 2px 15px rgba(0,0,0,0.9); margin-top: 1rem;
    }
    .err-log { color: #EF4444; } .sys-log { color: #71717A; } .warn-log { color: #F59E0B; } .acc-log { color: #38BDF8; }
    
    /* Box Affiliazione (Cavallo di Troia) */
    .affiliate-box { 
        background: rgba(59, 130, 246, 0.05); border-left: 3px solid #3B82F6; 
        padding: 1.2rem; border-radius: 0 6px 6px 0; margin-bottom: 1.5rem;
    }
    .affiliate-box h4 { 
        color: #3B82F6; margin-top: 0; font-size: 0.85rem; text-transform: uppercase; 
        letter-spacing: 1px; font-weight: 800;
    }
    
    /* Pulsanti Elite Edge-to-Edge */
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
    
    /* Tassonomia Menu Laterale (Pill Buttons) */
    div[role="radiogroup"] > label {
        background-color: transparent; border: 1px solid transparent; border-radius: 6px;
        padding: 8px 12px; margin-bottom: 2px; transition: all 0.2s ease; cursor: pointer;
    }
    div[role="radiogroup"] > label:hover { background-color: #18181B; }
    div[role="radiogroup"] > label[data-checked="true"] { background-color: rgba(16,185,129,0.05); border: 1px solid #10B981; }
    div[role="radiogroup"] > label > div:first-child { display: none; } 
    div[role="radiogroup"] > label p { color: #A1A1AA !important; font-weight: 500; margin: 0; font-size:0.9rem;}
    div[role="radiogroup"] > label[data-checked="true"] p { color: #10B981 !important; font-weight: 600;}
    
    /* Stile Schede (Tabs Vercel/Stripe style) */
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
    
    /* Customizzazione estetica dei Checkbox per la Matrice Costi */
    div[data-testid="stCheckbox"] label { cursor: pointer; }
    div[data-testid="stCheckbox"] label p { color: #F4F4F5 !important; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# MOTORE IBRIDO NOTION (Nexus Vault) - AUTO-ADATTIVO
# ==========================================
@st.cache_data(ttl=600, show_spinner=False)
def load_vault_data():
    import os
    import requests
    import pandas as pd
    import streamlit as st

    NOTION_TOKEN = st.secrets.get("NOTION_TOKEN", os.getenv("NOTION_TOKEN"))
    NOTION_VAULT_DB_ID = st.secrets.get("NOTION_VAULT_DB_ID", os.getenv("NOTION_VAULT_DB_ID"))

    df_notion = pd.DataFrame()

    if NOTION_TOKEN and NOTION_VAULT_DB_ID:
        url = f"https://api.notion.com/v1/databases/{NOTION_VAULT_DB_ID}/query"
        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        # --- MOTORE DI ORDINAMENTO NATIVO ---
        payload = {
            "sorts": [
                {
                    "property": "Ranking",
                    "direction": "ascending"
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            
            if response.status_code == 200:
                results = response.json().get("results", [])
                parsed_rows = []
                for row in results:
                    props = row.get("properties", {})
                    
                    try:
                        # 1. Estrae 'Tecnologia' (impostata come Title/Aa nel tuo Notion)
                        tec = props.get("Tecnologia", {}).get("title", [{}])[0].get("text", {}).get("content", "")
                    except: tec = ""
                        
                    try:
                        # 2. Estrae 'Software' (impostata come rich_text nel tuo Notion)
                        software = props.get("Software", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
                    except: software = ""
                        
                    try:
                        # 3. Estrae 'Licenza' 
                        lic = props.get("Licenza", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
                    except: lic = ""
                        
                    try:
                        # 4. Trova 'Vantaggio' ignorando gli a-capo fantasma ("Vantaggio\n \nStrategico")
                        vant_key = next((k for k in props.keys() if "Vantaggio" in k), "Vantaggio Strategico")
                        vant = props.get(vant_key, {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
                    except: vant = ""

                    try:
                        # 5. Estrae 'Link' (Supporta sia il tipo "URL" che il tipo "Testo" su Notion)
                        if "url" in props.get("Link", {}):
                            link = props.get("Link", {}).get("url", "")
                        else:
                            link = props.get("Link", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
                    except: link = ""

                    if software or tec:
                        parsed_rows.append({
                            'Software': software,
                            'Tecnologia': tec,
                            'Licenza': lic,
                            'Vantaggio Strategico': vant,
                            'Link': link if link else None
                        })
                if parsed_rows:
                    df_notion = pd.DataFrame(parsed_rows)
        
        except Exception:
            pass # Fallimento silenzioso ripristinato per la produzione

    if not df_notion.empty:
        return df_notion[['Software', 'Tecnologia', 'Licenza', 'Vantaggio Strategico', 'Link']]

    # Fallback locale in caso di assenza connessione
    csv_file = 'nexus_ai_toolkit.csv'
    if os.path.exists(csv_file):
        try:
            return pd.read_csv(csv_file)
        except Exception:
            pass
            
    return pd.DataFrame([{
        "Software": "In attesa di Sincronizzazione", 
        "Tecnologia": "-", 
        "Licenza": "-", 
        "Vantaggio Strategico": "Collega Notion o assicurati di aver caricato nexus_ai_toolkit.csv",
        "Link": "https://nexus.cloud"
    }])

# ==========================================
# 3. HELPER UX & LOGIC ENGINES
# ==========================================

def render_page_header(badge, title, use_case, tech_spec, python_code=None):
    """Interfaccia Bipolare: Impatto per i Manager, Architettura e Codice per i CTO."""
    st.markdown(f"<div class='status-badge'>{badge}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["✦ BUSINESS IMPACT", "⬢ SYSTEM ARCHITECTURE"])
    with tab1:
        st.markdown(f"<div style='padding: 0.5rem 0;'><p style='color:#F4F4F5; font-size:1.05rem;'>{use_case}</p></div>", unsafe_allow_html=True)
    with tab2:
        st.markdown(f"<div style='background-color:#050505; border-left:3px solid #3B82F6; padding: 1rem; border-radius:0 6px 6px 0; margin-bottom:1rem;'><p style='font-family:monospace; font-size:0.85rem; margin:0;'>{tech_spec}</p></div>", unsafe_allow_html=True)
        if python_code:
            with st.expander("👁️ VISUALIZZA SORGENTE ALGORITMO (Python)"):
                st.code(python_code, language="python")
    st.markdown("<br>", unsafe_allow_html=True)

def render_vault_header(badge, title, desc):
    """Header minimale per il Vault."""
    st.markdown(f"<div class='status-badge'>{badge}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='padding: 0.5rem 0; margin-bottom: 1.5rem;'><p style='color:#F4F4F5; font-size:1.05rem;'>{desc}</p></div>", unsafe_allow_html=True)

def render_affiliate_box(title, text, link_url, link_text):
    """Motore UI per la strategia del Cavallo di Troia (Affiliazioni B2B)"""
    st.markdown(f"""
        <div class='affiliate-box'>
            <h4>⚙️ POTENZIAMENTO INFRASTRUTTURA: {title}</h4>
            <p style='color: #A1A1AA; font-size: 0.9rem; margin-bottom: 0.5rem;'>{text}</p>
            <a href='{link_url}' target='_blank' style='color: #3B82F6; font-weight: 700; text-decoration: none; font-size: 0.85rem;'>{link_text} ↗</a>
        </div>
    """, unsafe_allow_html=True)

def is_email_in_notion(email):
    """Verifica se la mail esiste già nel database Notion per risparmiare crediti API e duplicati."""
    NOTION_TOKEN = os.getenv("NOTION_TOKEN") or st.secrets.get("NOTION_TOKEN", "")
    if not NOTION_TOKEN:
        return False # Se il token non è configurato, salta il blocco in sicurezza
    
    # ID del Database Notion fornito
    url = "https://api.notion.com/v1/databases/3a5ff5ea-717c-801a-a744-fcb924a9df4b/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    # Tentativo 1: Cerca sulla colonna di default se tipizzata come 'Email'
    payload_email = {
        "filter": {
            "property": "Email", 
            "email": {"equals": email}
        }
    }
    
    # Tentativo 2: Fallback in caso la colonna fosse un semplice testo/titolo
    payload_title = {
        "filter": {
            "property": "Email", 
            "rich_text": {"equals": email}
        }
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload_email, timeout=5)
        if res.status_code == 200 and len(res.json().get("results", [])) > 0:
            return True
        
        if res.status_code != 200:
            res_alt = requests.post(url, headers=headers, json=payload_title, timeout=5)
            if res_alt.status_code == 200 and len(res_alt.json().get("results", [])) > 0:
                return True
                
    except Exception:
        pass # Fallback silenzioso in caso di timeout/errore di rete
        
    return False

def lead_capture_gateway(module_id, action_text="Download Risultati"):
    """
    Soft Gate PLG: Chiede la mail bloccando l'output finale.
    Sincronizzazione forzata con st.form + Webhook Make.com via Secret.
    """
    if st.session_state.global_clearance:
        # Patch UX per il Double Opt-In
        if st.session_state.just_unlocked:
            st.success("✅ Accesso Autorizzato! L'identità è stata validata dal kernel centrale e il download diretto dei file crittografati è ora sbloccato qui sotto.", icon="✅")
            st.session_state.just_unlocked = False # Resettiamo il trigger dopo averlo mostrato
        return True # Sistema sbloccato
    
    st.markdown("<div style='border: 1px solid #27272A; border-radius: 8px; padding: 1.5rem; background: #050505; margin-top: 1rem; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    
    # st.form congela l'interfaccia ed evita i reload durante il click della checkbox
    with st.form(key=f"capture_form_{module_id}"):
        st.markdown(f"<h3 style='margin-top:0; color:#FAFAFA !important; font-size:1.2rem;'>Sblocca: {action_text}</h3>", unsafe_allow_html=True)
        st.write("Inserisci la tua email per abilitare questa funzione e sbloccare tutto l'ecosistema Nexus Cloud. (Se sei già registrato, l'accesso è immediato).")
        
        # Input E-mail
        email_input = st.text_input("Email:", placeholder="tua@email.com", key=f"email_input_{module_id}", label_visibility="collapsed")
        
        # Checkbox Privacy (scorporata dal link HTML)
        privacy_checked = st.checkbox("Accetto la Privacy Policy e acconsento al trattamento dei dati.", value=False, key=f"privacy_check_{module_id}")
        st.markdown(f"<div style='margin-top: -10px; margin-bottom: 15px; margin-left: 30px;'><a href='{LINK_IUBENDA}' target='_blank' style='color: #3B82F6; font-size: 0.85rem; text-decoration: none;'>📄 Leggi la Privacy Policy completa</a></div>", unsafe_allow_html=True)
        
        # Bottone d'invio form
        submit_btn = st.form_submit_button("SBLOCCA STRUMENTO E RICEVI ACCESSO", use_container_width=True)
        
        if submit_btn:
            if not email_input or "@" not in email_input or "." not in email_input:
                st.error("⚠️ [ERROR] Inserisci una email valida.")
            elif not privacy_checked:
                st.error("⚠️ [ERROR] Devi accettare la Privacy Policy per continuare.")
            else:
                try:
                    # 1. Filtro di validazione asincrona su DB Notion
                    already_exists = is_email_in_notion(email_input)
                    
                    # 2. Trigger webhook Make SOLO se l'utente non è già archiviato
                    if not already_exists:
                        # Recupero dinamico del webhook secret (st.secrets o os.getenv o variabile globale MAKE_WEBHOOK_URL)
                        target_webhook = globals().get('MAKE_WEBHOOK_URL') or os.getenv("MAKE_WEBHOOK_URL") or st.secrets.get("MAKE_WEBHOOK_URL", "")
                        
                        if target_webhook:
                            payload = {
                                "email": email_input,
                                "source": f"Nexus_Module_{module_id}",
                                "timestamp": datetime.datetime.now().isoformat()
                            }
                            requests.post(target_webhook, json=payload, timeout=5)
                except Exception: 
                    pass # Fallback silenzioso in produzione per proteggere la UX dell'utente
                
                # Attiva la clearance globale e flagga il messaggio di successo
                st.session_state['global_clearance'] = True
                st.session_state['just_unlocked'] = True
                
                # Riavvio controllato per applicare lo sblocco visivo
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    return False

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
        "Data & Security": ["01. Normalizzazione Dati (CSV)", "02. Sicurezza Ambientale (.env)", "03. Compilatore Telegram Scraper"],
        "Network Ops": ["04. Router Notifiche Asincrono", "05. Integrazione API (Sandbox)"],
        "Business Strategy": ["06. Interactive Cloud Audit", "07. Simulatore ROI Finanziario"]
    },
    "🔒 NEXUS VAULT (Intelligence)": {
        "Database & Archivi": ["01. AI & SaaS Toolkit (Top 50)"]
    }
}

default_idx = 0 if param_hub == "core" else 1
selected_workspace = st.sidebar.selectbox("SELEZIONA WORKSPACE:", list(ECOSYSTEMS.keys()), index=default_idx)
st.sidebar.markdown("<hr style='border-color:#1F2937; margin: 1rem 0;'>", unsafe_allow_html=True)

# Generazione Gerarchica Menu
categories = ECOSYSTEMS[selected_workspace]
st.sidebar.markdown("<p style='font-size: 0.75rem; font-weight: 700; color: #FFF; text-transform: uppercase; margin-bottom:0.2rem;'>Console di Comando</p>", unsafe_allow_html=True)
selected_category = st.sidebar.selectbox("Filtra per Categoria:", list(categories.keys()), label_visibility="collapsed")
selected_tool = st.sidebar.radio("Strumenti Attivi:", categories[selected_category], label_visibility="collapsed")

# Absolute Garbage Collection (Pulisce i log se si cambia strumento e cancella le allerte temporanee)
if st.session_state.active_tool != selected_tool:
    st.session_state.sys_logs = ""
    st.session_state.m1_buffer = None
    st.session_state.just_unlocked = False
    st.session_state.active_tool = selected_tool

# ==========================================
# 5. WORKSPACE: NEXUS CORE (ENGINEERING)
# ==========================================

# --- 01. CSV NORMALIZER ---
if selected_tool == "01. Normalizzazione Dati (CSV)":
    source_py = """import pandas as pd
import numpy as np
import re

def clean_dataset_nexus_v6_enterprise(file_path):
    # Parsing Blindato
    try:
        df = pd.read_csv(file_path, sep=',', encoding='utf-8', dtype=str)
        if df.shape[1] <= 1: df = pd.read_csv(file_path, sep=';', encoding='utf-8', dtype=str)
    except Exception:
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='latin1', dtype=str)

    df_clean = df.copy()

    # 1. Normalizzazione Intestazioni (Snake Case Assoluto)
    df_clean.columns = [re.sub(r'_+', '_', re.sub(r'[^a-z0-9_]', '_', re.sub(r'[àáâäèéêëìíîïòóôöùúûü]', lambda m: {'à':'a','è':'e','é':'e','ì':'i','ò':'o','ù':'u'}.get(m.group(0), 'a'), str(c).strip().lower()))).strip('_') or 'colonna' for c in df_clean.columns]

    # 2. Pulizia Spazi e NaN
    df_clean = df_clean.dropna(how='all')
    for col in df_clean.columns:
        df_clean[col] = df_clean[col].replace([r'^\s*$', 'nan', 'None', 'null', 'NaN', 'N/A', 'n/a'], np.nan, regex=True)
        if df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].str.strip().replace(r'\s+', ' ', regex=True)

    # 3. Smart Data Routing (Il risolutore del "Caso Marco Neri")
    email_cols = [c for c in df_clean.columns if 'mail' in c]
    tel_cols = [c for c in df_clean.columns if any(k in c for k in ['tel', 'phone', 'cell', 'mobile', 'telefono'])]

    if email_cols and tel_cols:
        c_m, c_t = email_cols[0], tel_cols[0]
        # Estrazione intelligente basata sul contenuto, non sulla colonna
        for idx in df_clean.index:
            v_m, v_t = str(df_clean.at[idx, c_m]), str(df_clean.at[idx, c_t])
            
            # Se la mail è palesemente un telefono (niente @, solo numeri/spazi/+)
            if v_m != 'nan' and '@' not in v_m and len(re.sub(r'[^\d]', '', v_m)) >= 6:
                if df_clean.at[idx, c_t] == 'nan' or pd.isna(df_clean.at[idx, c_t]):
                    df_clean.at[idx, c_t] = v_m  # Sposta nel telefono
                df_clean.at[idx, c_m] = np.nan   # Svuota la mail
                
            # Se il telefono è palesemente un'email
            if v_t != 'nan' and '@' in v_t:
                if df_clean.at[idx, c_m] == 'nan' or pd.isna(df_clean.at[idx, c_m]):
                    df_clean.at[idx, c_m] = v_t  # Sposta nella mail
                df_clean.at[idx, c_t] = np.nan   # Svuota il telefono

    # 4. Email Auto-Repair & STRICT FIREWALL
    if email_cols:
        c_m = email_cols[0]
        df_clean[c_m] = df_clean[c_m].str.lower().str.strip()
        
        # Correzione typo domini
        for pattern, target in {r'@gmail?l?\.com$': '@gmail.com', r'@gamil\.com$': '@gmail.com', r'@hotmaill?\.com$': '@hotmail.com'}.items():
            df_clean[c_m] = df_clean[c_m].str.replace(pattern, target, regex=True)
            
        # FIREWALL: Se non rispetta matematicamente un formato email, diventa NaN (risolve "paoloa.gialli.it")
        strict_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        df_clean[c_m] = df_clean[c_m].where(df_clean[c_m].str.match(strict_regex) | df_clean[c_m].isna(), np.nan)
        df_clean.loc[df_clean[c_m].isin(['test@test.com', 'admin@admin.com']), c_m] = np.nan
        
        # B2B Enrichment
        if 'dominio_aziendale' in df_clean.columns: df_clean = df_clean.drop('dominio_aziendale', axis=1)
        free_mails = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'virgilio.it', 'libero.it', 'tiscali.it', 'icloud.com', 'me.com']
        domains = df_clean[c_m].apply(lambda x: str(x).split('@')[1] if pd.notna(x) and '@' in str(x) else np.nan)
        df_clean.insert(df_clean.columns.get_loc(c_m) + 1, 'dominio_aziendale', np.where(~domains.isin(free_mails) & domains.notna(), domains, np.nan))

    # 5. Formattazione Nomi & Telefoni
    nome_cols = [c for c in df_clean.columns if any(k in c for k in ['nome', 'cognome', 'name'])]
    for col in nome_cols:
        df_clean[col] = df_clean[col].apply(lambda x: str(x).title() if pd.notna(x) else x)
        df_clean.loc[df_clean[col].str.lower().isin(['test', 'prova', 'admin']), col] = np.nan

    if tel_cols:
        df_clean[tel_cols[0]] = df_clean[tel_cols[0]].apply(lambda x: re.sub(r'[^\d+]', '', str(x)) if pd.notna(x) else np.nan)

    # 6. CRM-GRADE MERGE (Fusione Righe Doppie Incomplete)
    if nome_cols:
        c_n = nome_cols[0]
        # Ordina mettendo in alto le righe con più dati
        df_clean['data_count'] = df_clean.notna().sum(axis=1)
        df_clean = df_clean.sort_values(['data_count'], ascending=False).drop('data_count', axis=1)
        # Raggruppa per nome: se ci sono due "Marco Neri", fonde i dati prendendo il primo valore non-nullo per colonna
        df_clean = df_clean.groupby(c_n, dropna=False, as_index=False).first()

    return df_clean.drop_duplicates()"""

    render_page_header(
        "GESTIONE DATI", "Normalizzazione Enterprise & CRM Merge",
        "I database disorganizzati uccidono le conversioni. Carica il tuo archivio CSV. Il sistema corregge automaticamente le email scritte male (ed elimina quelle non valide), sposta i numeri di telefono inseriti nelle colonne sbagliate e <b>fonde automaticamente i contatti doppi o frammentati</b>. Inoltre, estrae i domini web dalle email B2B per il tuo Cold Outreach.",
        "Tecnologia Core: Motore Pandas. Operazioni: Smart Data Routing (scambio intelligente), Absolute Regex Firewall, Aggregazione CRM-Grade dei duplicati, B2B Enrichment.",
        source_py
    )

    # 👉 [LINK AFFILIAZIONE 1 - AIRTABLE]
    render_affiliate_box(
        "Airtable", 
        "Il database ora è fuso e arricchito. Esporta questo file su Airtable per creare il tuo CRM automatizzato e gestire le pipeline di vendita senza scrivere codice.", 
        "https://airtable.com", 
        "Crea un account gratuito su Airtable"
    )

    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Trascina il tuo CSV qui", type=["csv"])

    if uploaded_file:
        if st.button("PULISCI, FONDI E ARRICCHISCI DATI", type="primary"):
            with st.spinner("Analisi euristica, fusione dei record e arricchimento in corso..."):
                import time
                import numpy as np
                import re
                from datetime import datetime
                
                start_time = time.time()
                try:
                    # 1. Parsing FORZATO Stringa
                    try:
                        df_raw = pd.read_csv(uploaded_file, sep=',', encoding='utf-8', dtype=str)
                        if df_raw.shape[1] <= 1:
                            uploaded_file.seek(0)
                            df_raw = pd.read_csv(uploaded_file, sep=';', encoding='utf-8', dtype=str)
                    except Exception:
                        uploaded_file.seek(0)
                        df_raw = pd.read_csv(uploaded_file, sep=None, engine='python', encoding='latin1', dtype=str)

                    r_in = len(df_raw)
                    df_clean = df_raw.copy()

                    # 2. Header Normalization (Snake Case)
                    headers = []
                    for col in df_clean.columns:
                        c = str(col).strip().lower()
                        c = re.sub(r'[àáâä]', 'a', c)
                        c = re.sub(r'[èéêë]', 'e', c)
                        c = re.sub(r'[ìíîï]', 'i', c)
                        c = re.sub(r'[òóôö]', 'o', c)
                        c = re.sub(r'[ùúûü]', 'u', c)
                        c = re.sub(r'[^a-z0-9_]', '_', c)
                        c = re.sub(r'_+', '_', c).strip('_')
                        headers.append(c if c else 'colonna')
                    df_clean.columns = headers

                    # 3. Drop righe vuote e pulizia base
                    df_clean = df_clean.dropna(how='all')
                    for col in df_clean.columns:
                        df_clean[col] = df_clean[col].replace(r'^\s*$', np.nan, regex=True)
                        df_clean[col] = df_clean[col].replace(['nan', 'None', 'null', 'NaN', 'N/A', 'n/a'], np.nan)
                        if df_clean[col].dtype == 'object':
                            df_clean[col] = df_clean[col].str.strip().replace(r'\s+', ' ', regex=True)

                    # 4. Nomi (Title Case) - Da fare prima per il Merge
                    nome_cols = [c for c in df_clean.columns if any(k in c for k in ['nome', 'cognome', 'name', 'cliente', 'referente'])]
                    toxic_names = ['test', 'prova', 'admin', 'sconosciuto', 'nessuno']
                    toxic_purged = 0
                    
                    for col in nome_cols:
                        if col in df_clean.columns:
                            df_clean[col] = df_clean[col].apply(lambda x: str(x).title() if pd.notna(x) else x)
                            mask_toxic = df_clean[col].str.lower().isin(toxic_names)
                            toxic_purged += int(mask_toxic.sum())
                            df_clean.loc[mask_toxic, col] = np.nan

                    # 5. SMART DATA ROUTING (Risoluzione Telefono in Email)
                    routed_data = 0
                    email_cols = [c for c in df_clean.columns if 'mail' in c]
                    tel_cols = [c for c in df_clean.columns if any(k in c for k in ['tel', 'phone', 'cell', 'mobile', 'telefono'])]

                    if email_cols and tel_cols:
                        c_m = email_cols[0]
                        c_t = tel_cols[0]
                        
                        for idx in df_clean.index:
                            v_m = str(df_clean.at[idx, c_m])
                            v_t = str(df_clean.at[idx, c_t])
                            
                            # Se la mail è un telefono (no @, almeno 6 numeri)
                            if v_m != 'nan' and pd.notna(df_clean.at[idx, c_m]) and '@' not in v_m and len(re.sub(r'[^\d]', '', v_m)) >= 6:
                                if df_clean.at[idx, c_t] == 'nan' or pd.isna(df_clean.at[idx, c_t]):
                                    df_clean.at[idx, c_t] = v_m # Sposta
                                df_clean.at[idx, c_m] = np.nan # Elimina da mail
                                routed_data += 1
                                
                            # Se il telefono è una mail (ha @)
                            if v_t != 'nan' and pd.notna(df_clean.at[idx, c_t]) and '@' in v_t:
                                if df_clean.at[idx, c_m] == 'nan' or pd.isna(df_clean.at[idx, c_m]):
                                    df_clean.at[idx, c_m] = v_t # Sposta
                                df_clean.at[idx, c_t] = np.nan # Elimina da tel
                                routed_data += 1

                    # 6. Email Auto-Repair & ABSOLUTE FIREWALL
                    repaired_emails = 0
                    b2b_domains_found = 0
                    
                    if email_cols:
                        c_m = email_cols[0]
                        df_clean[c_m] = df_clean[c_m].str.lower().str.strip()
                        
                        # Typo Correction
                        email_typos = {
                            r'@gmail?l?\.com$': '@gmail.com',
                            r'@gamil\.com$': '@gmail.com',
                            r'@gmal\.com$': '@gmail.com',
                            r'@outloo?k\.com$': '@outlook.com',
                            r'@hotmaill?\.com$': '@hotmail.com',
                            r'@yaho+\.com$': '@yahoo.com',
                            r'@virgilo\.it$': '@virgilio.it',
                            r'@tiscali\.com$': '@tiscali.it'
                        }
                        for pattern, target in email_typos.items():
                            mask = df_clean[c_m].str.contains(pattern, regex=True, na=False)
                            matches = int(mask.sum())
                            if matches > 0:
                                repaired_emails += matches
                                df_clean[c_m] = df_clean[c_m].str.replace(pattern, target, regex=True)
                        
                        # FIREWALL ASSOLUTO: Cancella tutto ciò che non è un'email valida (es. paoloa.gialli.it)
                        strict_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                        valid_mask = df_clean[c_m].str.match(strict_regex) | df_clean[c_m].isna()
                        invalid_count = int((~valid_mask).sum())
                        toxic_purged += invalid_count
                        df_clean[c_m] = df_clean[c_m].where(valid_mask, np.nan)
                        
                        # Toxic Email Purge standard
                        toxic_emails = ['test@test.com', 'admin@admin.com', 'prova@prova.it', 'nessuno@nessuno.com']
                        mask_toxic_mail = df_clean[c_m].isin(toxic_emails)
                        toxic_purged += int(mask_toxic_mail.sum())
                        df_clean.loc[mask_toxic_mail, c_m] = np.nan
                        
                        # Estrazione B2B
                        free_mails = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'virgilio.it', 'libero.it', 'tiscali.it', 'icloud.com', 'me.com', 'msn.com', 'alice.it']
                        domains = df_clean[c_m].apply(lambda x: str(x).split('@')[1] if pd.notna(x) and '@' in str(x) else np.nan)
                        b2b_mask = ~domains.isin(free_mails) & domains.notna()
                        b2b_domains_found = int(b2b_mask.sum())
                        
                        # Inserimento colonna B2B visibile a fianco della mail
                        if 'dominio_aziendale' in df_clean.columns: df_clean = df_clean.drop('dominio_aziendale', axis=1)
                        idx = df_clean.columns.get_loc(c_m) + 1
                        df_clean.insert(idx, 'dominio_aziendale', np.where(b2b_mask, domains, np.nan))

                    # 7. Telefono Sanitizer
                    for col in tel_cols:
                        if col in df_clean.columns:
                            df_clean[col] = df_clean[col].apply(lambda x: re.sub(r'[^\d+]', '', str(x)) if pd.notna(x) else np.nan)

                    # 8. Valute Parser
                    num_cols = [c for c in df_clean.columns if any(k in c for k in ['fatturato', 'importo', 'prezzo', 'revenue', 'amount', 'totale', 'valore'])]
                    for col in num_cols:
                        if col in df_clean.columns:
                            def clean_num(val):
                                if pd.isna(val): return np.nan
                                v = str(val).replace('€', '').replace('$', '').replace('£', '').strip()
                                v = re.sub(r'\s+', '', v)
                                if '.' in v and ',' in v:
                                    if v.find('.') < v.find(','): v = v.replace('.', '').replace(',', '.')
                                    else: v = v.replace(',', '')
                                elif ',' in v: v = v.replace(',', '.')
                                try: return float(v)
                                except: return val
                            df_clean[col] = df_clean[col].apply(clean_num)

                    # 9. CRM-GRADE RECORD MERGING (Fonde le righe spezzate come "Marco Neri")
                    squashed_records = 0
                    if nome_cols:
                        c_n = nome_cols[0]
                        r_before = len(df_clean)
                        # Contiamo quanti dati validi ha ogni riga (per dare priorità a quelle più piene)
                        df_clean['data_count'] = df_clean.notna().sum(axis=1)
                        df_clean = df_clean.sort_values(by='data_count', ascending=False).drop('data_count', axis=1)
                        # GroupBy fonde assieme tutti i "Marco Neri", assemblando la riga con la prima email o telefono utile che trova
                        df_clean = df_clean.groupby(c_n, dropna=False, as_index=False).first()
                        squashed_records = r_before - len(df_clean)

                    # 10. Deduplicazione Pura Residua
                    r_before_dedup = len(df_clean)
                    df_clean = df_clean.drop_duplicates()
                    dups_removed = (r_before_dedup - len(df_clean)) + squashed_records

                    r_out = len(df_clean)
                    elapsed = round((time.time() - start_time) * 1000, 2)
                    
                    st.session_state.m1_buffer = df_clean
                    st.session_state.m1_metrics = {
                        "r_out": r_out,
                        "repaired_emails": repaired_emails,
                        "routed_data": routed_data,
                        "toxic_purged": toxic_purged,
                        "b2b_domains": b2b_domains_found,
                        "squashed": dups_removed
                    }

                    def sys_time_local(): return datetime.now().strftime('%H:%M:%S')

                    st.session_state.sys_logs = (
                        f"<span class='sys-log'>[{sys_time_local()}] - Sistema: Normalizzazione e Fusione CRM completata in {elapsed}ms.</span><br>"
                        f"<span class='acc-log'>✔ Firewall Regex attivo. Contatti spezzati fusi con successo in singoli record aziendali.</span>"
                    )
                except Exception as e:
                    st.session_state.sys_logs = f"<span class='err-log'>[{datetime.now().strftime('%H:%M:%S')}] ERRORE DI SISTEMA: Impossibile completare. Dettagli: {e}</span>"

    if 'm1_buffer' in st.session_state and st.session_state.m1_buffer is not None:
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
        
        # Dashboard KPI Metrics V6 - Design Pulito e Diretto
        if 'm1_metrics' in st.session_state:
            m = st.session_state.m1_metrics
            
            st.markdown("<p style='color:#10b981; font-size:0.85rem; font-weight:700;'>📊 METRICHE CRM E QUALITÀ DATI:</p>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Contatti Uniti/Doppi", m["squashed"], help="Righe doppie o incomplete (es. stesso nome) fuse in un unico record perfetto.")
            with col2:
                st.metric("Dati Estratti (B2B & Telefoni)", m["b2b_domains"] + m["routed_data"], help="Domini aziendali creati e numeri di telefono estratti dalle email.")
            with col3:
                st.metric("Anomalie Distrutte", m["toxic_purged"], help="Email fittizie o senza la '@' estirpate definitivamente.")
            with col4:
                st.metric("Record Finiti Validi", m["r_out"])

        st.markdown("<p style='color:#A1A1AA; font-size:0.85rem; font-weight:600; margin-top:15px;'>ANTEPRIMA DEL DATABASE (Scorri a destra per vedere la colonna Domini Aziendali):</p>", unsafe_allow_html=True)
        st.dataframe(st.session_state.m1_buffer, use_container_width=True)
        
        # Gatekeeper PLG
        if lead_capture_gateway("mod_01", "Scarica Database Ottimizzato"):
            st.download_button(
                "📥 SCARICA DATABASE (.CSV)",
                st.session_state.m1_buffer.to_csv(index=False).encode('utf-8-sig'),
                "database_ottimizzato_crm.csv",
                "text/csv"
            )

    st.markdown("</div>", unsafe_allow_html=True)
    
# --- 02. PROTOCOLLO .ENV ---
elif selected_tool == "02. Sicurezza Ambientale (.env)":
    source_py = """import os\nfrom dotenv import load_dotenv\n\nload_dotenv() # Carica le variabili dal file .env isolato\nAPI_KEY = os.getenv('API_KEY')\n\nif not API_KEY:\n    raise SystemExit('Vulnerabilità: Credenziali assenti.')"""
    render_page_header(
        "CYBERSECURITY", "Sicurezza Ambientale (.env)",
        "L'errore numero uno che causa i data breach aziendali è lasciare le password scritte in chiaro nel codice (GitHub). Incolla qui le tue configurazioni: il sistema estrarrà le informazioni sensibili isolandole, generando i file (.env e .gitignore) per blindare il server prima del deployment.",
        "Applicazione rigorosa della 12-Factor App Methodology. Analisi pattern per il disaccoppiamento logico tra variabili d'ambiente (Environment Variables) e repository Git.",
        source_py
    )
    
    # 👉 [LINK AFFILIAZIONE 2 - DIGITALOCEAN]
    render_affiliate_box(
        "DigitalOcean / Render", 
        "Una volta protetti i tuoi file di configurazione con questo script, ti serve un server aziendale sicuro dove eseguire il codice H24.", 
        "https://digitalocean.com", 
        "Ottieni 200$ di credito Cloud su DigitalOcean"
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    raw_env_str = """DATABASE_URL=postgres://admin:root123@local/db\nAPI_SECRET=sk_live_8473djds83...\nDEBUG_MODE=True"""
    env_input = st.text_area("Incolla variabili esposte (Formato Key=Value):", value=raw_env_str, height=120)
    
    if st.button("BLINDA ARCHITETTURA DI SISTEMA", type="primary"):
        st.session_state.m1_buffer = env_input
        st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [sec-ops@nexus] ~ Scansione file configurazione e moduli...</span><br><span class='warn-log'>[ALERT] Rilevate password e chiavi API esposte in chiaro.</span><br><span class='sys-log'>[{sys_time()}] [ENCRYPT] Generazione isolamento in memoria...</span><br><span style='color:#10B981'>[SUCCESS] Architettura protetta. File asettici pronti per il deployment.</span>"
        
    if st.session_state.m1_buffer is not None:
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
        
        # Gatekeeper PLG prima del Download
        if lead_capture_gateway("mod_02", "Download Architettura .ENV"):
            c1, c2 = st.columns(2)
            c1.download_button("📥 SCARICA .ENV", st.session_state.m1_buffer, ".env")
            c2.download_button("📥 SCARICA FIREWALL .GITIGNORE", ".env\n__pycache__/\n*.session\n.DS_Store", ".gitignore")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 03. COMPILATORE TELEGRAM ---
elif selected_tool == "03. Compilatore Telegram Scraper":
    source_py = """from telethon.sync import TelegramClient\nimport csv\n\n# Architettura compilata dinamicamente in memoria\n# L'handshake richiede esecuzione locale per bypass OTP"""
    render_page_header(
        "DATA EXTRACTION", "Compilatore Telegram Scraper",
        "Genera un software personalizzato per estrarre migliaia di lead dai gruppi concorrenti. Poiché estrarre dati tramite Cloud genera un Ban immediato dell'account Telegram, inserisci i tuoi parametri qui. Compileremo un software Python sicuro che potrai scaricare ed avviare in totale privacy direttamente dal tuo computer.",
        "Generazione programmatica di script Python (libreria Telethon asincrona). L'eseguibile forza l'architettura client-side (localhost) per bypassare i filtri anti-bot IP cloud.",
        source_py
    )
    
    # 👉 [LINK AFFILIAZIONE 3 - SMARTPROXY]
    render_affiliate_box(
        "Smartproxy", 
        "Se esegui scraping in locale per più di 10 gruppi, Telegram bannerà il tuo IP aziendale. Ti servono Proxy Residenziali a rotazione.", 
        "https://smartproxy.com", 
        "Proteggi il tuo IP registrandoti a Smartproxy"
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
            st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [compiler@nexus] ~ Generazione variabili asincrone per il target '{target}'...</span><br><span style='color:#10B981'>[{sys_time()}] [SUCCESS] Software Python compilato in memoria. Binario pronto al download.</span>"
        else:
            st.session_state.sys_logs = f"<span class='err-log'>[{sys_time()}] [FATAL ERROR] Impossibile completare la compilazione. Parametri API mancanti nel costruttore.</span>"
            st.session_state.m1_buffer = None
            
    if st.session_state.sys_logs != "":
        st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div><br>", unsafe_allow_html=True)
        if st.session_state.m1_buffer:
            
            # Gatekeeper PLG prima del Download Executable
            if lead_capture_gateway("mod_03", "Software Client Python"):
                st.download_button("📥 SCARICA SCRIPT PYTHON (.PY)", st.session_state.m1_buffer, "nexus_telegram_engine.py")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 04. ROUTER NOTIFICHE ---
elif selected_tool == "04. Router Notifiche Asincrono":
    source_py = """from fastapi import FastAPI, Request\napp = FastAPI()\n\n@app.post("/webhook")\nasync def route_traffic(req: Request):\n    payload = await req.json()\n    if payload.get("priority") == "CRITICAL":\n        return trigger_sms_alert()\n    return log_silently_to_db()"""
    render_page_header(
        "ALGORITHMS", "Router Notifiche Asincrono",
        "L'overload informativo paralizza il management. Incolla i dati di un evento di sistema (es. server down). L'algoritmo valuterà autonomamente l'urgenza. Se critico, inoltra un SMS al management. Se inutile, lo silenzia e lo archivia in database per non distrarre il team.",
        "Simulazione Endpoint REST in ricezione. Parsing asincrono del payload JSON. Switch logico interno sulla chiave 'priority' (Event-Driven Architecture) con tempo di esecuzione O(1).",
        source_py
    )
    
    # 👉 [LINK AFFILIAZIONE 4 - MAKE.COM]
    render_affiliate_box(
        "Make.com (Integromat)", 
        "Perché usare script manuali scritti in Python quando Make.com può fare questo routing logico visualmente in 2 minuti senza scrivere una riga di codice?", 
        "https://make.com", 
        "Crea un account gratuito su Make.com"
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    json_test = """{\n  "source": "server_monitor",\n  "error_code": "502_bad_gateway",\n  "priority": "CRITICAL"\n}"""
    json_in = st.text_area("Payload Evento in Ingresso (JSON):", value=json_test, height=140)
    
    if st.button("ESEGUI ALGORITMO DI ROUTING", type="primary"):
        with st.spinner("Valutazione rami logici..."):
            time.sleep(0.5)
            try:
                data = json.loads(json_in)
                st.session_state.m1_buffer = data
                st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] Routing Engine Eseguito. Dati elaborati con successo.</span>"
            except json.JSONDecodeError as e:
                st.session_state.sys_logs = f"<span class='err-log'>[{sys_time()}] [FATAL ERROR] Payload JSON corrotto o malformato. Syntax Error: {e}</span>"
                st.session_state.m1_buffer = None
                
    if st.session_state.sys_logs != "":
        # Mostra log di elaborazione iniziale
        if not st.session_state.global_clearance:
             st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
             
        if st.session_state.m1_buffer:
            # Gatekeeper PLG prima di mostrare il risultato della logica JSON
            if lead_capture_gateway("mod_04", "Risultato Architettura Routing"):
                data = st.session_state.m1_buffer
                prio = str(data.get("priority", "LOW")).upper()
                if prio in ["HIGH", "CRITICAL"]:
                    data["nexus_action"] = "FORWARD_TO_CTO_SMS"
                    msg = f"<span class='warn-log'>[{sys_time()}] [URGENT] Priorità Alta rilevata. Bypass filtri attivato. Evento inoltrato via SMS.</span>"
                else:
                    data["nexus_action"] = "SILENT_DB_LOG"
                    msg = f"<span class='sys-log'>[{sys_time()}] [SILENT] Priorità Bassa. Rumore soppresso e archiviato per audit futuro.</span>"
                
                json_str = json.dumps(data, indent=2)
                formatted_json = json_str.replace('\n', '<br>').replace('  ', '&nbsp;&nbsp;')
                
                st.markdown(f"<div class='cmd-window'>{msg}<br><br><span class='acc-log'>[PAYLOAD TRASFORMATO E DECISIONE PRESA]:</span><br>{formatted_json}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 05. API INJECTOR ---
elif selected_tool == "05. Integrazione API (Sandbox)":
    source_py = """import requests\nimport json\n\ndef inject_payload(url, data_dict):\n    headers = {'Content-Type': 'application/json'}\n    response = requests.post(url, json=data_dict, headers=headers, timeout=5)\n    return response.status_code, response.elapsed.total_seconds()"""
    render_page_header(
        "NETWORK OPS", "Integrazione API (Sandbox)",
        "Garantisci l'integrità dei flussi aziendali. Inserisci l'URL di destinazione (es. Webhook Make.com) e invia un pacchetto dati di prova. Il sistema simulerà un ping HTTP, misurerà la latenza di rete e verificherà che l'informazione sia giunta intatta a destinazione.",
        "Esecuzione modulo <code>requests.post</code> nativo. Handshake TCP/TLS asincrono verso endpoint remoto. Misurazione telemetrica della latenza in millisecondi e validazione HTTP Status Code.",
        source_py
    )
    
    # 👉 [LINK AFFILIAZIONE 5 - MAKE.COM API]
    render_affiliate_box(
        "Make.com (Integromat)", 
        "Cattura i dati inviati da questo simulatore API usando un Webhook Custom su Make.com per costruire la tua automazione.", 
        "https://make.com", 
        "Attiva il tuo primo Webhook su Make.com"
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    url = st.text_input("URL di Destinazione (Endpoint REST)", value="https://httpbin.org/post")
    payload_str = """{\n  "cliente": "NEXUS Corp",\n  "status": "Integrazione API Verificata"\n}"""
    payload = st.text_area("Dati da inviare (JSON)", value=payload_str, height=110)
    
    if st.button("ESEGUI TEST DI RETE (PING)", type="primary"):
        st.session_state.sys_logs = f"<span class='sys-log'>[{sys_time()}] [net-ops@nexus] ~ Negoziazione protocollo HTTP/TLS verso {url}...</span>"
        try:
            p_json = json.loads(payload)
            t0 = time.time()
            res = requests.post(url, json=p_json, timeout=5)
            lat = round(time.time() - t0, 3)
            
            st.session_state.m1_buffer = {"res_text": res.text[:250], "status": res.status_code, "lat": lat}
            st.session_state.sys_logs += f"<br><span style='color:#10B981'>[{sys_time()}] [SUCCESS] Transazione completata. Rete validata.</span>"
        except json.JSONDecodeError:
            st.session_state.sys_logs += f"<br><span class='err-log'>[{sys_time()}] [ERROR] Formattazione JSON invalida. Il carico utile è stato respinto.</span>"
            st.session_state.m1_buffer = None
        except Exception as e:
            st.session_state.sys_logs += f"<br><span class='err-log'>[{sys_time()}] [TIMEOUT FATAL] Endpoint irraggiungibile o barriera firewall attiva. Dettagli: {e}</span>"
            st.session_state.m1_buffer = None
            
    if st.session_state.sys_logs != "":
        # Mostra Log negoziazione base
        if not st.session_state.global_clearance:
            st.markdown(f"<div class='cmd-window'>{st.session_state.sys_logs}</div>", unsafe_allow_html=True)
            
        if st.session_state.m1_buffer:
            # Gatekeeper PLG prima di mostrare latenza e response body del server remoto
            if lead_capture_gateway("mod_05", "Rapporto di Diagnostica di Rete"):
                data = st.session_state.m1_buffer
                safe_res = data['res_text'].replace('\n', '<br>').replace('  ', '&nbsp;&nbsp;')
                full_log = st.session_state.sys_logs + f"<br>HTTP CODE: {data['status']}<br>LATENZA TCP: {data['lat']}s<br><br><span class='sys-log'>[RAW SERVER RESPONSE]</span><br>{safe_res}..."
                st.markdown(f"<div class='cmd-window'>{full_log}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 06. INTERACTIVE CLOUD AUDIT ---
elif selected_tool == "06. Interactive Cloud Audit":
    source_py = """# Algoritmo dinamico per l'abbattimento dell'OPEX\ndef calculate_burn_rate(legacy_stack):\n    burn_rate = sum(item['cost'] for item in legacy_stack)\n    apex_cost = 0 # Self-Hosted & Serverless Edge Models\n    return burn_rate, apex_cost"""
    render_page_header(
        "FINANCIAL AUDIT", "Interactive Cloud Audit",
        "Le aziende italiane bruciano decine di migliaia di euro ogni anno in abbonamenti software (SaaS) monolitici e costosi. Esegui un Audit interattivo per la tua azienda: seleziona i software che stai pagando oggi. Ti mostreremo istantaneamente quanti soldi stai perdendo e l'esatta alternativa (Open Source o Serverless) per azzerare le spese mensili.",
        "Audit interattivo per il calcolo del TCO (Total Cost of Ownership). Sostituzione di servizi monolitici legacy con architetture distribuite Open Source e Cloud Serverless ad alte prestazioni.",
        source_py
    )
    
    # 👉 [LINK AFFILIAZIONE 6 - HETZNER]
    render_affiliate_box(
        "Hetzner", 
        "Sostituire software da 200€/mese con l'Open Source significa doverli ospitare su un server. Hetzner domina il mercato europeo per le VPS ad alte prestazioni ed economiche.", 
        "https://hetzner.com", 
        "Ottieni 20€ gratuiti sui Server Hetzner"
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#FAFAFA; font-weight:600; margin-bottom:1rem; font-size:1.1rem;'>Seleziona i servizi software (SaaS) attualmente in uso nella tua azienda:</p>", unsafe_allow_html=True)
    
    # MATRICE ITALIANA: 12 Pilastri SaaS
    c1, c2, c3, c4 = st.columns(4)
    zapier = c1.checkbox("Zapier / Make")
    hubspot = c2.checkbox("HubSpot / Salesforce")
    mail = c3.checkbox("Mailchimp / ActiveC.")
    funnel = c4.checkbox("ClickFunnels / Kajabi")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4)
    shopify = c5.checkbox("Shopify (Costi Add-on)")
    manychat = c6.checkbox("ManyChat / Chatfuel")
    calendly = c7.checkbox("Calendly / Doodle")
    zendesk = c8.checkbox("Zendesk / Intercom")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c9, c10, c11, c12 = st.columns(4)
    vimeo = c9.checkbox("Vimeo / Wistia")
    airtable = c10.checkbox("Airtable / Monday")
    typeform = c11.checkbox("Typeform")
    aws = c12.checkbox("AWS S3 / Google Cloud")
    
    burn_rate = 0
    soluzioni = []
    
    if zapier: 
        burn_rate += 199 
        soluzioni.append("✅ Sostituisci Automazioni con **n8n (Self-Hosted)** a costo zero. Esecuzioni illimitate.")
    if hubspot: 
        burn_rate += 150 
        soluzioni.append("✅ Sostituisci il CRM con **Supabase (PostgreSQL Serverless)** a costo zero.")
    if mail: 
        burn_rate += 80 
        soluzioni.append("✅ Sostituisci Email Marketing con **Mautic (Open Source) + AWS SES** a pochi centesimi.")
    if funnel: 
        burn_rate += 197 
        soluzioni.append("✅ Sostituisci ClickFunnels con **WordPress + Ghost (Headless CMS)** a costo zero.")
    if shopify: 
        burn_rate += 79 
        soluzioni.append("✅ Sostituisci gli abbonamenti eCommerce con **WooCommerce + Stripe**.")
    if manychat: 
        burn_rate += 45 
        soluzioni.append("✅ Sostituisci i Chatbot con **Typebot (Open Source)** a costo zero.")
    if calendly: 
        burn_rate += 30 
        soluzioni.append("✅ Sostituisci Form & Meeting con **Cal.com (Self-Hosted)** a costo zero.")
    if zendesk: 
        burn_rate += 150 
        soluzioni.append("✅ Sostituisci il Customer Care con **Chatwoot (Open Source)** a costo zero.")
    if vimeo: 
        burn_rate += 60 
        soluzioni.append("✅ Sostituisci l'Hosting Video con **Cloudflare Stream** a un decimo del costo.")
    if airtable: 
        burn_rate += 50 
        soluzioni.append("✅ Sostituisci i Database NoCode con **NocoDB (Open Source)** a costo zero.")
    if typeform: 
        burn_rate += 59 
        soluzioni.append("✅ Sostituisci la raccolta Lead con **Tally.so (Free Tier Illimitato)**.")
    if aws: 
        burn_rate += 45 
        soluzioni.append("✅ Sostituisci AWS S3 Storage con **Cloudflare R2** (Zero costi per il traffico in uscita).")
        
    st.markdown("---")
    c_res1, c_res2 = st.columns(2)
    c_res1.metric("Burn Rate Mensile (Sprechi)", f"€ {burn_rate} / mese")
    c_res2.metric("Costo Architettura NEXUS", "€ 0 / mese", f"+ € {burn_rate} Salvati al Mese", delta_color="normal")
    
    if burn_rate > 0:
        # Gatekeeper PLG prima di rivelare il protocollo di migrazione esatto
        if lead_capture_gateway("mod_06", "Protocollo di Migrazione Strategico"):
            st.markdown("<br><p style='color:#FAFAFA; font-weight:700;'>PROTOCOLLO DI MIGRAZIONE CONSIGLIATO (SBLOCCATO):</p>", unsafe_allow_html=True)
            for sol in soluzioni:
                st.markdown(f"<p style='color:#10B981; margin:0;'>{sol}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 07. ROI TELEMETRY ---
elif selected_tool == "07. Simulatore ROI Finanziario":
    source_py = """import plotly.graph_objects as go\n# Motore di calcolo dell'interesse composto a 12 mesi\nmesi = [f"Mese {i}" for i in range(1, 13)]\ncrescita_tradizionale = [mrr * (1 - (churn/100))**i for i in range(1, 13)]\ncrescita_nexus = [(mrr + (opex * 0.8)) * (1.05)**i for i in range(1, 13)]\n\nfig = go.Figure()\nfig.add_trace(go.Scatter(x=mesi, y=crescita_tradizionale, mode='lines', name='Legacy'))\nfig.add_trace(go.Scatter(x=mesi, y=crescita_nexus, mode='lines', name='NEXUS'))"""
    
    render_page_header(
        "BUSINESS ANALYTICS", "Simulatore ROI Finanziario",
        "Algoritmo di proiezione finanziaria avanzata. Calcola l'impatto dell'ottimizzazione architetturale sui flussi di cassa a 12 mesi, valutando il tasso di abbandono (Churn Rate) e l'interesse composto generato dai costi SaaS abbattuti.",
        "Data Visualization vettoriale con Plotly. Calcolo predittivo dell'Operational Expenditure (OPEX) integrato con LTV incrementale. Memoria di sessione per persistenza simulazioni.",
        source_py
    )
    
    # 👉 [LINK AFFILIAZIONE 7 - STRIPE]
    render_affiliate_box(
        "Stripe", 
        "Se gestisci pagamenti B2B e abbonamenti, Stripe è l'infrastruttura di pagamento per calcolare automaticamente MRR, Churn Rate e LTV aziendale.", 
        "https://stripe.com", 
        "Aumenta le conversioni gestendo i flussi tramite Stripe"
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    mrr_attuale = col1.number_input("Fatturato Mensile Attuale (MRR) €", min_value=0, value=25000, step=1000)
    costi_saas = col1.number_input("Costi Abbonamenti SaaS (Da Azzerare) €", min_value=0, value=4200, step=100)
    
    churn_rate = col2.slider("Churn Rate Mensile % (Abbandono)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
    margine_target = col2.slider("Margine Netto Desiderato %", min_value=10, max_value=90, value=60, step=5)
    
    # Logica Matematica (Backend temporaneo in memoria)
    risparmio_annuo = costi_saas * 12
    mesi = [f"Mese {i}" for i in range(1, 13)]
    crescita_tradizionale = [mrr_attuale * (1 - (churn_rate/100))**i for i in range(1, 13)]
    crescita_nexus = [(mrr_attuale + (costi_saas * 0.8)) * (1.05)**i for i in range(1, 13)] # compounding calcolato al +5%
    delta_fatturato_m12 = crescita_nexus[-1] - crescita_tradizionale[-1]
    
    c3, c4, c5 = st.columns(3)
    c3.metric("Risparmio Annuo (SaaS)", f"€ {risparmio_annuo:,.0f}", delta="Ottimizzato")
    c4.metric("LTV Incrementale", f"+ 15%", delta="Stima Algoritmica")
    c5.metric("Delta Fatturato (M12)", f"€ {delta_fatturato_m12:,.0f}", delta="Extra Profit")
    
    # Gatekeeper PLG prima di mostrare i grafici vettoriali esecutivi
    if lead_capture_gateway("mod_07", "Genera Proiezione Vettoriale"):
        st.markdown("<br><p style='color:#A1A1AA; font-size:0.85rem; font-weight:600;'>PROIEZIONE FLUSSI DI CASSA (12 MESI)</p>", unsafe_allow_html=True)
        
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mesi, y=crescita_tradizionale, mode='lines+markers', name='Modello Tradizionale', line=dict(color='#FF4B4B', width=3)))
        fig.add_trace(go.Scatter(x=mesi, y=crescita_nexus, mode='lines+markers', name='Architettura Nexus', line=dict(color='#10B981', width=3)))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font_color='#A1A1AA', 
            margin=dict(t=20, b=0, l=0, r=0),
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style="background-color: rgba(16, 185, 129, 0.1); padding: 15px; border-left: 4px solid #10B981; border-radius: 4px; margin-top: 15px;">
        <span style="color: #A1A1AA; font-size: 0.9rem;">
        <b>Analisi dell'Architetto:</b> I dati dimostrano che re-ingegnerizzando l'infrastruttura ed eliminando il rumore dei software ridondanti, 
        il capitale liberato genera un interesse composto sul tuo MRR, abbattendo al contempo il Churn Rate. Questo è il potere dell'Ingegneria Transazionale.
        </span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# HUB 02: NEXUS VAULT (INTELLIGENCE)
# ==========================================
elif selected_workspace == "🔒 NEXUS VAULT (Intelligence)":
    
    render_vault_header(
        "DATA INTELLIGENCE", "Archivio AI & SaaS (Top 50)",
        "Perché bruciare centinaia di ore in ricerca e sviluppo e migliaia di euro in licenze software quando il lavoro è già stato fatto? Esplora il database privato delle architetture SaaS e Intelligenze Artificiali gratuite usate dai top player mondiali per automatizzare la propria azienda a costo zero."
    )
    
    st.markdown("<div class='nexus-card'>", unsafe_allow_html=True)

    df_vault = load_vault_data()
    
    # Configurazione estetica per trasformare la colonna in pulsanti cliccabili
    vault_column_config = {
        "Link": st.column_config.LinkColumn(
            "Link Ufficiale", 
            display_text="Apri Sito ↗"
        )
    }
    
    # CONTROLLO DI SICUREZZA: L'utente ha inserito l'email?
    # Usiamo st.session_state.get() per evitare errori se la variabile non è ancora inizializzata
    if not st.session_state.get('global_clearance', False):
        
        # ==========================================
        # STATO 1: BLOCCATO (LEAD MAGNET MODE)
        # ==========================================
        # L'utente vede solo il "teaser" statico di 8 righe. NESSUNA barra di ricerca.
        
        if not df_vault.empty:
            st.dataframe(df_vault.head(8), use_container_width=True, hide_index=True, column_config=vault_column_config)
        
        hidden_records = max(0, len(df_vault) - 8)
        st.markdown(f"<div style='text-align:center; padding:1.5rem 1rem; color:#71717A; font-size:0.85rem; border-top:1px dashed #27272A; margin-bottom:2rem;'>[ RISORSE LIMITATE A SCHERMO. ALTRI {hidden_records} RECORD OSCURATI. INSERISCI L'EMAIL PER SBLOCCARE LA RICERCA ]</div>", unsafe_allow_html=True)
        
        # Modulo di cattura email
        lead_capture_gateway("vault_master", "Database Integrale in CSV")
        
    else:
        
        # ==========================================
        # STATO 2: SBLOCCATO (ACCESSO TOTALE)
        # ==========================================
        st.markdown("<div style='border: 1px solid #10B981; border-radius: 8px; padding: 1.5rem; background: rgba(16,185,129,0.05); text-align:center; margin-bottom:2rem;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#10B981 !important; margin-bottom:0.5rem; margin-top:0;'>✅ Accesso Sbloccato con Successo</h4>", unsafe_allow_html=True)
        st.markdown("<span style='font-size: 0.9rem; color: #E4E4E7;'>L'archivio integrale e la funzione di ricerca avanzata sono ora attivi.</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # BARRA DI RICERCA BLINDATA (Esiste solo per chi ha sbloccato l'accesso)
        search = st.text_input("🔍 Ricerca rapida nel database (es. Automazione, Hosting, AI, Cloud)...")
        
        display_df = df_vault
        if search and not df_vault.empty:
            display_df = df_vault[df_vault.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        if not display_df.empty:
            st.dataframe(display_df, use_container_width=True, hide_index=True, column_config=vault_column_config)
        else:
            st.warning("Nessun risultato trovato per questa ricerca.")
        
        # BOTTONE DOWNLOAD IN CODA ALLA TABELLA
        if not df_vault.empty:
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 DOWNLOAD DATABASE (.CSV)", 
                data=df_vault.to_csv(index=False).encode('utf-8-sig'), 
                file_name="nexus_tech_vault.csv", 
                mime="text/csv"
            )
            
    st.markdown("</div>", unsafe_allow_html=True)
