import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. Título do Painel
st.title("🦷 Cobrança Odonto")

# 2. Carregar os dados (Ajuste o link para o seu CSV do Google Sheets)
# Substitua 'LINK_DA_PLANILHA' pelo link de exportação CSV da sua planilha
sheet_url = "LINK_DA_PLANILHA_AQUI"
df = pd.read_csv(sheet_url)

# 3. O Loop de Operação (Onde estava o erro)
for index, row in df.iterrows():
    # Coleta os dados de cada linha da planilha
    nome = row['NOME'] 
    atraso = row['TOTAL EM ATRASO']
    tel = str(row['TELEFONE'])
    email = row['EMAIL']
    pix = row['CODIGO PIX']

    # Prepara a mensagem do WhatsApp
    msg = f"Oi! Sou o RENATO da Odonto Excellence. Seu tratamento não pode parar! Total: R$ {atraso}. PIX: {pix}"
    link_wats = f"https://wa.me/{tel}?text={quote(msg)}"
    
    # Cria as colunas no Painel
    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
    
    with col1:
        st.write(nome)
    with col2:
        st.write(f":red[R$ {atraso:,.2f}]") # Valor em vermelho
    with col3:
        st.link_button("🟢 WATS", link_wats)
    with col4:
        st.link_button("📩 MAIL", f"mailto:{email}")
