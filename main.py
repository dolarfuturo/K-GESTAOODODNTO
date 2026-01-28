import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. CONFIGURAÇÃO DE TELA E ESTILO
st.set_page_config(page_title="Resgate Odonto", layout="wide")

# CSS para remover espaços e deixar o layout bem justo
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    [data-testid="stMetricValue"] { font-size: 22px !important; }
    div[data-testid="stVerticalBlock"] > div { gap: 0rem; }
    hr { margin: 0.1rem 0px !important; }
    .stButton button { height: 35px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Gestão de Resgate")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    # 2. SELETOR DE CANAL E KPIs
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    c1.metric("Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.0f}")
    c2.metric("Pacientes", len(df))
    with c4:
        canal = st.radio("Selecione o Canal de Envio:", ["WhatsApp", "E-mail"], horizontal=True)

    st.divider()

    # 3. CABEÇALHO
    h1, h2, h3, h4, h5 = st.columns([3, 1.5, 1.5, 1.2, 1.8])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**ENTRADA**")
    h4.write("**STATUS**")
    h5.write("**AÇÃO**")

    # 4. LISTAGEM COM TEXTOS SEPARADOS
    for index, row in df.iterrows():
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0]
        email_p = str(row.iloc[2])
        v_atraso = row['TOTAL EM ATRASO']
        v_entrada = row['VALOR DE ENTRADA']
        pix = str(row.iloc[7])
        status = "✅ OK" if not pd.isna(row['CANAL']) else "⏳ Pend."

        # --- TEXTO ESPECÍFICO PARA WHATSAPP ---
        texto_whatsapp = (
            f"Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! Sentimos sua falta, "
            f"vimos que você não compareceu mais nas consultas! Seu tratamento não pode parar! 🦷\n\n"
            f"📌 Total em atraso: R$ {v_atraso:,.2f}\n"
            f"🤝 Entrada para Retorno: R$ {v_entrada:,.2f}\n\n"
            f"👉 DIGITE OK E ENVIA ✅\n\n"
            f"Chave PIX: {pix}\n\nAguardamos você! 🏥"
        )

        # --- TEXTO ESPECÍFICO PARA E-MAIL ---
        texto_email = (
            f"Olá! Sentimos sua falta. Seu tratamento não pode parar.\n\n"
            f"Total em atraso: R$ {v_atraso:,.2f}.\n"
            f"PIX para retorno: {pix}."
        )

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1.5, 1.2, 1.8])
            col1.write(nome)
            col2.markdown(f":red[R$ {v_atraso:,.2f}]")
            col3.write(f"R$ {v_entrada:,.2f}")
            col4.write(status)
            
            with col5:
                if canal == "WhatsApp":
                    link_zap = f"https://wa.me/{tel}?text={quote(texto_whatsapp)}"
                    st.link_button("🟢 ZAP", link_zap, use_container_width=True)
                else:
                    link_mail = f"mailto:{email_p}?subject=Odonto%20Excellence&body={quote(texto_email)}"
                    st.link_button("📩 MAIL", link_mail, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
