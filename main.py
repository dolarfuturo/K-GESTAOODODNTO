import streamlit as st
import pandas as pd
import urllib.parse

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão Odonto Excellence", layout="wide")
st.title("🦷 Cobrança - Odonto Excellence")

# LINK CORRIGIDO PARA FORMATO CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    # Lendo os dados
    df = pd.read_csv(SHEET_URL)
    
    # Limpando nomes de colunas (remove espaços extras)
    df.columns = df.columns.str.strip()

    for index, row in df.iterrows():
        # Ignora linhas totalmente vazias
        if pd.isna(row['NOME']):
            continue
            
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])
            
            nome = str(row['NOME'])
            # Formata o valor com vírgula para parecer real (R$ 1000,00)
            valor_num = row['TOTAL EM ATRASO']
            valor_formatado = f"R$ {valor_num:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            
            canal = str(row['CANAL']).upper().strip()
            celular = str(row['TELEFONE']).split('.')[0] # Remove .0 se houver
            
            col1.write(f"**{nome}**")
            col2.write(f"Dívida: **{valor_formatado}**")

            # LÓGICA DO BOTÃO BASEADA NA COLUNA 'CANAL'
            if canal == "WATS":
                msg = f"Oi {nome}! Eu sou da clínica Odonto Excellence. 🦷\n\n📌 Total em atraso: {valor_formatado}\n\n📞 Se preferir que eu te ligue, clique aqui: wa.me/5551997194306"
                link_zap = f"https://wa.me/{celular}?text={urllib.parse.quote(msg)}"
                col3.markdown(f'[![WhatsApp](https://img.shields.io/badge/Enviar-WhatsApp-25D366?style=for-the-badge&logo=whatsapp)]({link_zap})')
            
            elif canal == "EMAIL":
                email = str(row['EMAIL'])
                link_mail = f"mailto:{email}?subject=Odonto Excellence&body=Oi {nome}, temos uma pendência de {valor_formatado}."
                col3.markdown(f'[![Email](https://img.shields.io/badge/Enviar-Email-D14836?style=for-the-badge&logo=gmail)]({link_mail})')
            
            st.divider()

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.info("Certifique-se de que a planilha tem as colunas: NOME, TELEFONE, EMAIL, TOTAL EM ATRASO, CANAL")
