import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(page_title="Gestão Odonto", layout="wide")
st.title("🦷 Painel de Operação - Odonto Excellence")

# Link formatado para exportação automática da sua planilha
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo a planilha (df)
    df = pd.read_csv(sheet_url)
    
    # Exibe um resumo rápido no topo
    total_atraso = df['TOTAL EM ATRASO'].sum()
    st.metric("Total em Aberto", f"R$ {total_atraso:,.2f}")

    st.divider()

    # Loop para gerar as linhas de contato
    for index, row in df.iterrows():
        # Ajuste exato dos nomes das colunas da sua planilha
        nome = "Paciente" if pd.isna(row.iloc[0]) else row.iloc[0]
        telefone = str(row['TELEFONE']).split('.')[0]
        email = row['EMAIL']
        valor_atraso = row['TOTAL EM ATRASO']
        valor_entrada = row['VALOR DE ENTRADA']
        pix = row['CODIGO PIX']

        # Criando as mensagens automáticas
        msg_whatsapp = f"Oi! Sou o RENATO da Odonto Excellence. Sentimos sua falta! Seu tratamento não pode parar. Total em atraso: R$ {valor_atraso}. Entrada para retorno: R$ {valor_entrada}. PIX: {pix}"
        link_whatsapp = f"https://wa.me/{telefone}?text={quote(msg_whatsapp)}"

        # Layout do Painel
        col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
        
        with col1:
            st.write(f"👤 **{nome}**")
        with col2:
            st.write(f":red[R$ {valor_atraso:,.2f}]")
        with col3:
            st.link_button("🟢 WATS", link_whatsapp, use_container_width=True)
        with col4:
            st.link_button("📩 MAIL", f"mailto:{email}", use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: Verifique se a planilha está compartilhada como 'Qualquer pessoa com o link'.")
    st.info(f"Detalhe técnico: {e}")
