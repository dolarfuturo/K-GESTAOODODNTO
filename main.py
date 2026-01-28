import streamlit as st
import pandas as pd
from urllib.parse import quote

# ... (parte onde você carrega sua planilha 'df') ...

for index, row in df.iterrows():
    # Variáveis da sua planilha
    nome = row['B'] # Nome (ajuste se for outra coluna)
    tel = str(row['TELEFONE']).replace(".0", "")
    email = row['EMAIL']
    atraso = row['TOTAL EM ATRASO']
    entrada = row['VALOR DE ENTRADA']
    pix = row['CODIGO PIX']

    # Texto do WhatsApp (Seu original completo)
    msg_wats = f"Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! Sentimos sua falta. Seu tratamento não pode parar! 🦷\n\n📌 Total em atraso: R$ {atraso}\n🤝 Entrada para Retorno: R$ {entrada}\n\n👉 DIGITE OK E ENVIA ✅\n\nChave PIX: {pix}"
    link_wats = f"https://wa.me/{tel}?text={quote(msg_wats)}"

    # Texto do E-mail (Mais curto para não travar)
    msg_email = f"Olá! Sentimos sua falta na Odonto Excellence. Total em atraso: R$ {atraso}. PIX para entrada: {pix}."
    link_email = f"mailto:{email}?subject=Odonto%20Excellence&body={quote(msg_email)}"

    # Criando o visual do Painel
    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
    with col1:
        st.write(f"**{nome}**")
    with col2:
        st.write(f":red[R$ {atraso:,.2f}]")
    with col3:
        st.link_button("🟢 WATS", link_wats)
    with col4:
        st.link_button("🔵 MAIL", link_email)
