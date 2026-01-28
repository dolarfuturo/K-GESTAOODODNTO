import streamlit as st
import pandas as pd

# Configuração para Tablet
st.set_page_config(page_title="Painel Odonto", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stButton button { height: 38px; border-radius: 8px; font-weight: bold; }
    hr { margin: 0.1rem 0px !important; }
    div[data-testid="column"] { padding: 0px 5px; }
    .status-w { color: #25D366; font-weight: bold; }
    .status-e { color: #0078D4; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Disparo de Resgate Auditável")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo a planilha (forçando colunas de link como texto)
    df = pd.read_csv(sheet_url, dtype=str)

    # Convertendo valores para cálculo
    df['TOTAL EM ATRASO'] = pd.to_numeric(df['TOTAL EM ATRASO'], errors='coerce').fillna(0)

    c1, c2 = st.columns(2)
    c1.metric("Pendentes", len(df))
    c2.metric("Total Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    
    st.divider()

    # Cabeçalho
    h1, h2, h3, h4 = st.columns([3, 2, 1.5, 3.5])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**CANAL**") # Agora auditável
    h4.write("**AÇÃO**")

    for index, row in df.iterrows():
        nome = str(row.iloc[0])
        atraso = row['TOTAL EM ATRASO']
        
        # STATUS AUDITÁVEL (Coluna F - índice 5)
        canal_bruto = str(row.iloc[5]).upper().strip()
        if canal_bruto == "W":
            status_html = '<span class="status-w">🟢 WHATSAPP</span>'
        elif canal_bruto == "E":
            status_html = '<span class="status-e">🔵 E-MAIL</span>'
        else:
            status_html = "🟡 NÃO DEFINIDO"

        # LINKS (Colunas G e H - índices 6 e 7)
        link_zap = str(row.iloc[6])
        link_mail = str(row.iloc[7])

        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1.5, 3.5])
            col1.write(nome)
            col2.write(f"R$ {atraso:,.2f}")
            col3.markdown(status_html, unsafe_allow_html=True)
            
            with col4:
                col_z, col_m = st.columns(2)
                
                # Botão ZAP aparece se houver "http" no link da Coluna G
                if "http" in link_zap.lower():
                    col_z.link_button("🟢 ZAP", link_zap, use_container_width=True)
                else:
                    col_z.button("🚫 S/ LINK", disabled=True, use_container_width=True)
                
                # Botão MAIL aparece se houver "mailto" no link da Coluna H
                if "mailto" in link_mail.lower():
                    col_m.link_button("📩 MAIL", link_mail, use_container_width=True)
                else:
                    col_m.button("🚫 S/ LINK", disabled=True, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro ao carregar painel: {e}")
