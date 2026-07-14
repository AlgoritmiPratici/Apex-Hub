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
    page_title="APEX Cloud | Enterprise Workspace", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Inizializzazione Session State per Memoria di Sistema
if 'workspace_data' not in st.session_state:
    st.session_state.workspace_data = None
if 'lead_vault' not in st.session_state:
    st.session_state.lead_vault = False

hub_richiesto = st.query_params.get("workspace", "apex")

# ==========================================
# 2. VERCEL/STRIPE-LIKE PREMIUM CSS
# ==========================================
st.markdown("""
    <style>
    /* Pulizia Totale UI Nativia */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tipografia d'Elite e Colori di Base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    /* Sfondi e Card Glassmorphism Vercel-Style */
    .stApp { background-color: #000000; }
    
    .premium-card {
        background: linear-gradient(145deg, #111111 0%, #0A0A0A 100%);
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
        margin-bottom: 1.5rem;
    }
    
    /* Titoli Gradient e Indicatori di Status */
    .gradient-text {
        background: linear-gradient(90deg, #10B981 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -0.05em;
    }
    .status-dot {
        height: 8px; width: 8px; background-color: #10B981;
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 8px #10B981; margin-right: 8px;
    }
    
    /* Pulsanti Primary & Secondary (Stripe Style) */
    div.stButton > button {
        background-color: #FFFFFF !important; color: #000000 !important;
        font-weight: 600 !important; border-radius: 8px !important;
        padding: 0.5rem 1rem !important; border: 1px solid #FFFFFF !important;
        transition: all 0.2s; width: 100%;
    }
    div.stButton > button:hover { background-color: #E5E5E5 !important; transform: translateY(-1px); }
    
    div.stDownloadButton > button {
        background-color: transparent !important; color: #10B981 !important;
        font-weight: 600 !important; border-radius: 8px !important;
        border: 1px solid #10B981 !important; width: 100%; transition: all 0.2s;
    }
    div.stDownloadButton > button:hover { background: rgba(16,185,129,0.1) !important; }
    
    /* Terminal Console Estetica */
    .terminal-box {
        background-color: #0A0A0A; border: 1px solid #333; border-radius: 6px;
        padding: 1rem; font-family: 'Courier New', Courier, monospace;
        color: #10B981; font-size: 0.85rem; margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. ENTERPRISE SIDEBAR NAVIGATOR
# ==========================================
st.sidebar.markdown("""
<div style='text-align:center; padding-bottom: 2rem;'>
    <span class='status-dot'></span><span style='color:#A1A1AA; font-weight:600; letter-spacing:1px;'>SYSTEM ONLINE</span>
</div>
""", unsafe_allow_html=True)

workspace = st.sidebar.selectbox("SELECT WORKSPACE", ["⚡ APEX CLOUD", "🔒 ZERO VAULT (Data)"], index=0 if hub_richiesto=="apex" else 1)
st.sidebar.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)

# ==========================================
# WORKSPACE: APEX CLOUD (TECH)
# ==========================================
if workspace == "⚡ APEX CLOUD":
    app_scelta = st.sidebar.radio("APPLICATIONS", [
        "Database Refining Engine", 
        "Security .env Vault", 
        "Telegram Scraper (Wizard)", 
        "Serverless Architecture", 
        "Financial Analytics Live", 
        "Webhook Traffic Router", 
        "API Payload Injector"
    ])
    
    if app_scelta == "Database Refining Engine":
        st.markdown("<h1 class='gradient-text'>Data Refining Engine</h1>", unsafe_allow_html=True)
        st.write("Identificazione e rimozione anomalie dai flussi CSV in ambiente protetto.")
        
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drop CSV Dump Here", type=["csv"])
        
        if uploaded_file:
            with st.spinner("Compilazione algoritmi di normalizzazione..."):
                time.sleep(1.2)
                df = pd.read_csv(uploaded_file, sep=None, engine='python')
                righe_in = len(df)
                df_clean = df.drop_duplicates()
                if 'Email' in df_clean.columns:
                    df_clean['Email'] = df_clean['Email'].astype(str).str.lower().str.strip()
                    df_clean = df_clean[~df_clean['Email'].isin(['nan', 'none', '', 'null'])].dropna(subset=['Email'])
                righe_out = len(df_clean)
                st.session_state.workspace_data = df_clean
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Raw Records", righe_in)
                col2.metric("Valid Records", righe_out)
                col3.metric("Anomalies Purged", righe_in - righe_out, delta="-Ottimizzato", delta_color="inverse")
                
                st.dataframe(st.session_state.workspace_data.head(5), use_container_width=True)
                st.download_button("DOWNLOAD REFINED CSV", st.session_state.workspace_data.to_csv(index=False).encode('utf-8'), "apex_refined.csv", "text/csv")
        st.markdown("</div>", unsafe_allow_html=True)

    elif app_scelta == "Telegram Scraper (Wizard)":
        st.markdown("<h1 class='gradient-text'>Telethon Wizard Engine</h1>", unsafe_allow_html=True)
        st.write("Le policy di Telegram vietano lo scraping da IP Cloud. Compila le tue chiavi qui sotto per generare un'architettura di estrazione privata e sicura da eseguire sul tuo server locale.")
        
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        api_id = st.text_input("Inserisci Telegram API_ID", placeholder="es. 1234567")
        api_hash = st.text_input("Inserisci Telegram API_HASH", placeholder="es. 8a7b6c5d4e3f2g1h...", type="password")
        target = st.text_input("Username Gruppo Target", placeholder="es. competitors_group")
        
        if st.button("GENERATE CUSTOM SCRIPT"):
            if api_id and api_hash and target:
                custom_script = f"""# APEX CUSTOM ENGINE
from telethon.sync import TelegramClient
import csv

API_ID = '{api_id}'
API_HASH = '{api_hash}'
TARGET = '{target}'

with TelegramClient('apex_session', API_ID, API_HASH) as client:
    print("[SYSTEM] Estrazione da", TARGET)
    utenti = client.get_participants(TARGET)
    with open('apex_leads.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Username', 'Name'])
        for u in utenti: writer.writerow([u.id, u.username, u.first_name])
    print("[SUCCESS] Dati acquisiti.")
"""
                st.markdown("<div class='terminal-box'>[SYSTEM] Compilazione script personalizzato... DONE. Pronto per il download.</div>", unsafe_allow_html=True)
                st.download_button("DOWNLOAD SCRIPT (.py)", custom_script, "apex_telegram_scraper.py")
            else:
                st.error("Inserisci tutti i parametri per compilare il software.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif app_scelta == "Financial Analytics Live":
        st.markdown("<h1 class='gradient-text'>Interactive ROI Engine</h1>", unsafe_allow_html=True)
        st.write("Simulatore finanziario di marginalità basato sull'efficienza infrastrutturale.")
        
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        mrr = col1.number_input("MRR Mensile (€)", value=15000, step=1000)
        saas_cost = col2.number_input("Costi SaaS Inutili (€)", value=2500, step=100)
        dev_cost = col3.number_input("Costi Dev Manuale (€)", value=4000, step=100)
        
        margine_attuale = mrr - saas_cost - dev_cost
        margine_apex = mrr - 0 - 0 # Simuliamo il costo zero infrastrutturale
        
        st.markdown("### Proiezione Operativa")
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Margine Attuale", f"€ {margine_attuale:,}")
        col_res2.metric("Margine con APEX Cloud", f"€ {margine_apex:,}", f"+€ {saas_cost + dev_cost:,} (Recuperati)")
        
        df_proj = pd.DataFrame({
            "Modello": ["Infrastruttura Attuale", "Infrastruttura APEX"],
            "Utile Netto (€)": [margine_attuale, margine_apex]
        })
        fig = px.bar(df_proj, x="Modello", y="Utile Netto (€)", color="Modello", color_discrete_sequence=['#EF4444', '#10B981'])
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#E2E8F0')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif app_scelta == "API Payload Injector":
        st.markdown("<h1 class='gradient-text'>API Injection Sandbox</h1>", unsafe_allow_html=True)
        st.write("Testa in tempo reale le connessioni Webhook verso il tuo CRM o n8n.")
        
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        endpoint_url = st.text_input("Endpoint URL (Make.com, Zapier, n8n)", value="https://httpbin.org/post")
        st.caption("*Di default punta a httpbin.org per testare le connessioni sicure.*")
        
        test_payload = '{\n  "lead_name": "Elon M.",\n  "company": "Apex Corp",\n  "status": "qualified"\n}'
        payload_input = st.text_area("JSON Payload", value=test_payload, height=150)
        
        if st.button("EXECUTE API PUSH"):
            terminal = st.empty()
            terminal.markdown("<div class='terminal-box'>[SYSTEM] Handshake TCP in corso...</div>", unsafe_allow_html=True)
            time.sleep(0.5)
            try:
                parsed_json = json.loads(payload_input)
                response = requests.post(endpoint_url, json=parsed_json, timeout=5)
                terminal.markdown(f"<div class='terminal-box'>[SYSTEM] POST inviata.<br>[RESPONSE] Status Code: {response.status_code}<br>[LATENCY] {response.elapsed.total_seconds()}s<br>[MSG] Transazione Completata.</div>", unsafe_allow_html=True)
            except json.JSONDecodeError:
                terminal.markdown("<div class='terminal-box' style='color:#EF4444;'>[ERROR] JSON malformato. Verifica la sintassi.</div>", unsafe_allow_html=True)
            except Exception as e:
                terminal.markdown(f"<div class='terminal-box' style='color:#EF4444;'>[FATAL] Connessione fallita: {str(e)}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown(f"<h1 class='gradient-text'>{app_scelta}</h1>", unsafe_allow_html=True)
        st.markdown("<div class='premium-card'>Modulo in fase di deploy asincrono. Consultare la documentazione.</div>", unsafe_allow_html=True)

# ==========================================
# WORKSPACE: ZERO VAULT (DATABASE)
# ==========================================
elif workspace == "🔒 ZERO VAULT (Data)":
    st.markdown("<h1 class='gradient-text'>ZERO Vault Data Center</h1>", unsafe_allow_html=True)
    st.write("L'archivio aziendale dei migliori strumenti SaaS per l'arbitraggio del tempo.")
    
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    
    df_tools = pd.DataFrame([
        {"Category": "Video Gen", "Software": "CapCut Enterprise", "Pricing Model": "Freemium / Export 4K", "Protocol": "Video"},
        {"Category": "Voice AI", "Software": "ElevenLabs Core", "Pricing Model": "10k Char Free/Month", "Protocol": "Audio"},
        {"Category": "LLM Engine", "Software": "Gemini 1.5 Pro", "Pricing Model": "Advanced Tier", "Protocol": "Text"},
        {"Category": "Automation", "Software": "n8n Open Source", "Pricing Model": "Free (Self-Hosted)", "Protocol": "Backend"},
        {"Category": "Database", "Software": "Supabase PostgreSQL", "Pricing Model": "Serverless Tier", "Protocol": "Data"}
    ])
    
    query = st.text_input("Filtra il database per query (es. Video, Free, Backend)...")
    if query:
        mask = df_tools.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        df_tools = df_tools[mask]
        
    st.dataframe(df_tools, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    if not st.session_state.lead_vault:
        st.markdown("### 🔐 Unlock Full Vault Access")
        email = st.text_input("Inserisci l'email aziendale per il download integrale:")
        if st.button("AUTHORIZE ACCESS"):
            if "@" in email and "." in email:
                st.session_state.lead_vault = True
                st.rerun()
            else:
                st.error("Credenziali respinte. Formato non valido.")
    
    if st.session_state.lead_vault:
        st.success("Accesso Concesso. Autorizzazione verificata.")
        st.download_button("DOWNLOAD ENTIRE VAULT (.csv)", df_tools.to_csv(index=False).encode('utf-8'), "zero_vault_data.csv", "text/csv")
    
    st.markdown("</div>", unsafe_allow_html=True)
