import streamlit as st
import pandas as pd

# 1. SETUP DO PAINEL (TABLET)
st.set_page_config(page_title="Disparo Odonto", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stButton button { height: 38px; border-radius: 8px; font-weight: bold; }
    hr { margin: 0.15rem 0px !important; }
    div[data-testid="column"] { padding: 0px 5px; }
    .status-w { color: #25D366; font-weight: bold; font-size: 13px; }
    .status-e { color: #0078D4; font-weight: bold; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Disparo de Resgate Auditável")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo a planilha (tudo como texto para evitar erros de link)
    df = pd.read_csv(sheet_url, dtype=str)

    # Convertendo valores numéricos para o cabeçalho
    atraso_total = pd.to_numeric(df.iloc[:, 3], errors='coerce').sum()

    c1, c2 = st.columns(2)
    c1.metric("Pacientes Pendentes", len(df))
    c2.metric("Total em Aberto", f"R$ {atraso_total:,.2f}")
    
    st.divider()

    # 2. CABEÇALHO COM A COLUNA DE ENTRADA
    h1, h2, h3, h4, h5 = st.columns([2.5, 1.5, 1.5, 1.5, 3])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**ENTRADA**")
    h4.write("**CANAL**")
    h5.write("**AÇÃO**")

    # 3. LISTAGEM DOS PACIENTES
    for index, row in df.iterrows():
        nome = str(row.iloc[0]) # Coluna A
        valor_atraso = str(row.iloc[3]) # Coluna D
        valor_entrada = str(row.iloc[4]) # Coluna E
        
        # Status Auditável (Coluna F)
        canal_bruto = str(row.iloc[5]).upper().strip()
        if canal_bruto == "W":
            status_html = '<span class="status-w">🟢 WHATSAPP</span>'
        elif canal_bruto == "E":
            status_html = '<span class="status-e">🔵 E-MAIL</span>'
        else:
            status_html = "🟡 PENDENTE"

        # Links das Colunas G e H
        link_zap = str(row.iloc[6]) 
        link_mail = str(row.iloc[7])

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2.5, 1.5, 1.5, 1.5, 3])
            
            col1.write(nome)
            col2.write(f"R$ {valor_atraso}")
            col3.write(f"R$ {valor_entrada}")
            col4.markdown(status_html, unsafe_allow_html=True)
            
            with col5:
                col_z, col_m = st.columns(2)
                
                # Botão WhatsApp (com key única para evitar erro de ID)
                if "http" in link_zap.lower():
                    col_z.link_button("🟢 ZAP", link_zap, use_container_width=True, key=f"z_{index}")
                else:
                    col_z.button("🚫 S/L", disabled=True, use_container_width=True, key=f"dz_{index}")
                
                # Botão E-mail
                if "mailto" in link_mail.lower():
                    col_m.link_button("📩 MAIL", link_mail, use_container_width=True, key=f"m_{index}")
                else:
                    col_m.button("🚫 S/L", disabled=True, use_container_width=True, key=f"dm_{index}")
            
            st.divider()

except Exception as e:
    st.error(f"Erro ao carregar painel: {e}")
