import streamlit as st
import pandas as pd
import urllib.parse

# CONFIGURAÇÃO DA PÁGINA PARA OCUPAR TODA A TELA
st.set_page_config(page_title="Gestão Odonto", layout="wide", initial_sidebar_state="collapsed")

# CSS PARA DIMINUIR O ESPAÇAMENTO (DEIXAR TUDO JUNTINHO)
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    .stMarkdown p {font-size: 14px; margin-bottom: 0px;}
    hr {margin-top: 5px !important; margin-bottom: 5px !important;}
    div[data-testid="stVerticalBlock"] > div {padding: 2px 0px;}
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Lista de Cobrança")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(SHEET_URL)
    df.columns = df.columns.str.strip()

    # Cabeçalho da Tabela
    c1, c2, c3 = st.columns([4, 2, 2])
    c1.caption("PACIENTE")
    c2.caption("VALOR")
    c3.caption("AÇÃO")
    st.divider()

    for index, row in df.iterrows():
        if pd.isna(row['NOME']): continue
            
        nome = str(row['NOME']).upper()
        valor_num = row['TOTAL EM ATRASO']
        valor_formatado = f"R$ {valor_num:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        canal = str(row['CANAL']).upper().strip()
        celular = str(row['TELEFONE']).split('.')[0]
        
        with st.container():
            col1, col2, col3 = st.columns([4, 2, 2])
            
            col1.write(f"**{nome}**")
            col2.write(f"**{valor_formatado}**")

            if canal == "WATS":
                msg = f"Oi {nome}! Eu sou da clínica Odonto Excellence. 🦷\n\n📌 Total em atraso: {valor_formatado}\n\n📞 wa.me/5551997194306"
                link_zap = f"https://wa.me/{celular}?text={urllib.parse.quote(msg)}"
                col3.markdown(f'''<a href="{link_zap}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">ZAP</button></a>''', unsafe_allow_html=True)
            
            elif canal == "EMAIL":
                email = str(row['EMAIL'])
                link_mail = f"mailto:{email}?subject=Cobranca&body=Oi {nome}"
                col3.markdown(f'''<a href="{link_mail}"><button style="background-color: #D14836; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%;">EMAIL</button></a>''', unsafe_allow_html=True)
        
        st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
