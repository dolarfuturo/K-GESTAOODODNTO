import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Gestão Odonto", layout="wide")

# CSS PARA DEIXAR TEXTO COMPLETO E LINHAS JUNTAS
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    .lista-item {
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        padding: 5px 0px;
        border-bottom: 1px solid #f0f0f0;
    }
    .nome-paciente { font-size: 14px; font-weight: bold; flex: 2; }
    .valor-paciente { font-size: 14px; flex: 1; text-align: center; }
    .botao-link { flex: 1; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(SHEET_URL)
        st.session_state.df.columns = st.session_state.df.columns.str.strip()

    st.title("🦷 Cobrança")

    for index, row in st.session_state.df.iterrows():
        if pd.isna(row['NOME']): continue
        
        nome = str(row['NOME']).upper()
        valor = f"R$ {row['TOTAL EM ATRASO']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        canal = str(row['CANAL']).upper().strip()
        celular = str(row['TELEFONE']).split('.')[0]
        
        # HTML customizado para garantir que o texto não quebre
        if canal == "WATS":
            msg = f"Oi {nome}! Valor: {valor}. 🦷"
            link = f"https://wa.me/{celular}?text={urllib.parse.quote(msg)}"
            st.markdown(f'''
                <div class="lista-item">
                    <div class="nome-paciente">{nome}</div>
                    <div class="valor-paciente">{valor}</div>
                    <div class="botao-link"><a href="{link}" target="_blank" style="color:#25D366; font-weight:bold; text-decoration:none;">ZAP 📲</a></div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            email = str(row['EMAIL'])
            link_m = f"mailto:{email}?subject=Odonto&body=Oi {nome}"
            st.markdown(f'''
                <div class="lista-item">
                    <div class="nome-paciente">{nome}</div>
                    <div class="valor-paciente">{valor}</div>
                    <div class="botao-link"><a href="{link_m}" style="color:#D14836; font-weight:bold; text-decoration:none;">EMAIL 📩</a></div>
                </div>
            ''', unsafe_allow_html=True)

    st.write("---")
    with st.expander("⚙️ EDITAR VALORES OU NOMES"):
        edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
        if st.button("SALVAR"):
            st.session_state.df = edited_df
            st.rerun()

except Exception as e:
    st.error(f"Erro: {e}")
