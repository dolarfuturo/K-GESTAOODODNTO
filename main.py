import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. CONFIGURAÇÃO DE TELA
st.set_page_config(page_title="Resgate Odonto", layout="wide")

# CSS para espremer as linhas e aproveitar o espaço do tablet
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    h1 { font-size: 22px !important; }
    [data-testid="stMetricValue"] { font-size: 18px !important; }
    div[data-testid="stVerticalBlock"] > div { gap: 0rem; }
    hr { margin: 0.1rem 0px !important; }
    .stButton button { height: 30px; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Painel Resgate Odonto")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    # 2. TOPO: KPIs E SELETOR DE CANAL
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    c1.metric("Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.0f}")
    c2.metric("Meta", f"R$ {df['VALOR DE ENTRADA'].sum():,.0f}")
    c3.metric("Lista", len(df))
    with c4:
        canal = st.radio("Canal de Envio:", ["WhatsApp", "E-mail"], horizontal=True)

    st.divider()

    # 3. CABEÇALHO
    h1, h2, h3, h4, h5 = st.columns([3, 1.5, 1.5, 1.5, 2])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**ENTRADA**")
    h4.write("**STATUS**")
    h5.write("**AÇÃO**")

    # 4. LISTAGEM
    for index, row in df.iterrows():
        # Dados das colunas
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0]
        email_dest = str(row.iloc[2])
        v_atraso = row['TOTAL EM ATRASO']
        v_entrada = row['VALOR DE ENTRADA']
        pix = str(row.iloc[7])
        status = "✅ OK" if not pd.isna(row['CANAL']) else "⏳ Pend."

        # MENSAGEM (Corrigido erro de f-string da imagem 2)
        # Usamos parênteses para o Python aceitar as quebras de linha sem erro
        msg = (
            f"Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! "
            f"Sentimos sua falta! Seu tratamento não pode parar! 🦷\n\n"
            f"📌 Total em atraso: R$ {v_atraso:,.2f}\n"
            f"🤝 Entrada: R$ {v_entrada:,.2f}\n\n"
            f"👉 DIGITE OK E ENVIA ✅\n\n"
            f"Chave PIX: {pix}\n\nAguardamos você! 🏥"
        )

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1.5, 1.5, 2])
            col1.write(nome)
            col2.markdown(f":red[R$ {v_atraso:,.2f}]")
            col3.write(f"R$ {v_entrada:,.2f}")
            col4.write(status)
            
            with col5:
                if canal == "WhatsApp":
                    link = f"https://wa.me/{tel}?text={quote(msg)}"
                    st.link_button("🟢 ZAP", link, use_container_width=True)
                else:
                    link = f"mailto:{email_dest}?subject=Odonto%20Excellence&body={quote(msg)}"
                    st.link_button("📩 MAIL", link, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
