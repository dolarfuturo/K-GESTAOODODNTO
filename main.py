import streamlit as st
import pandas as pd
from urllib.parse import quote

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

st.title("🦷 Disparo de Resgate - 100% Funcional")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    c1, c2 = st.columns(2)
    c1.metric("Pacientes Pendentes", len(df))
    # Coluna D é o índice 3 (Atraso)
    atraso_total = pd.to_numeric(df.iloc[:, 3], errors='coerce').sum()
    c2.metric("Total em Aberto", f"R$ {atraso_total:,.2f}")
    
    st.divider()

    # Cabeçalho
    h1, h2, h3, h4, h5 = st.columns([2.5, 1.5, 1.5, 1.5, 3])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**ENTRADA**")
    h4.write("**CANAL**")
    h5.write("**AÇÃO**")

    for index, row in df.iterrows():
        nome = str(row.iloc[0])   # Coluna A
        tel = str(row.iloc[1]).strip().split('.')[0] # Coluna B
        email = str(row.iloc[2])  # Coluna C
        v_atraso = row.iloc[3]    # Coluna D
        v_entrada = row.iloc[4]   # Coluna E
        pix = str(row.iloc[8])    # Coluna I (Código PIX)
        
        # Status Auditável (Coluna F)
        canal_bruto = str(row.iloc[5]).upper().strip()
        status_html = f'<span class="status-w">🟢 WHATSAPP</span>' if canal_bruto == "W" else f'<span class="status-e">🔵 E-MAIL</span>'

        # --- O PYTHON MONTA O LINK AQUI PARA NÃO FALHAR ---
        texto_base = f"""Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! Sentimos sua falta! 🦷

📌 Total em atraso: R$ {v_atraso:,.2f}
🤝 Entrada para Retorno: R$ {v_entrada:,.2f}

👉 DIGITE OK E ENVIA ✅

Chave PIX:
🔑 {pix}"""

        link_zap = f"https://wa.me/{tel}?text={quote(texto_base)}"
        link_mail = f"mailto:{email}?subject=Odonto Excellence&body={quote(texto_base)}"

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2.5, 1.5, 1.5, 1.5, 3])
            
            col1.write(nome)
            col2.write(f"R$ {v_atraso:,.2f}")
            col3.write(f"R$ {v_entrada:,.2f}")
            col4.markdown(status_html, unsafe_allow_html=True)
            
            with col5:
                col_z, col_m = st.columns(2)
                # Agora os links são gerados pelo Python, então FUNCIONAM ao clicar
                col_z.link_button("🟢 ZAP", link_zap, use_container_width=True, key=f"z_{index}")
                col_m.link_button("📩 MAIL", link_mail, use_container_width=True, key=f"m_{index}")
            
            st.divider()

except Exception as e:
    st.error(f"Erro no painel: {e}")
