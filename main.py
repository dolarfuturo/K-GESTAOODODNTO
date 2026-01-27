import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Gestão Odonto", layout="wide")

# CSS CORRIGIDO: Espaçamento pequeno, mas sem sobrepor os textos
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    .patient-row {
        padding: 10px;
        border-bottom: 1px solid #eee;
        display: flex;
        align-items: center;
    }
    .stMarkdown p {font-size: 16px; margin-bottom: 0px; line-height: 1.2;}
    </style>
    """, unsafe_allow_html=True)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(SHEET_URL)
        st.session_state.df.columns = st.session_state.df.columns.str.strip()

    st.title("🦷 Cobrança Odonto")

    # EXIBIÇÃO ORGANIZADA POR LINHAS
    for index, row in st.session_state.df.iterrows():
        if pd.isna(row['NOME']): continue
        
        nome = str(row['NOME']).upper()
        valor = row['TOTAL EM ATRASO']
        valor_f = f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        canal = str(row['CANAL']).upper().strip()
        celular = str(row['TELEFONE']).split('.')[0]
        
        # Grid para alinhar sem embolar
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            st.write(f"**{nome}**")
        with col2:
            st.write(f"**{valor_f}**")
        with col3:
            if canal == "WATS":
                msg = f"Oi {nome}! O valor para acerto é {valor_f}. 🦷"
                link = f"https://wa.me/{celular}?text={urllib.parse.quote(msg)}"
                st.markdown(f'[:green[**ENVIAR ZAP**]]({link})')
            else:
                email = str(row['EMAIL'])
                link_m = f"mailto:{email}?subject=Odonto&body=Oi {nome}"
                st.markdown(f'[:red[**ENVIAR MAIL**]]({link_m})')
        
        st.markdown("---") # Linha divisória fina entre pacientes

    # MENU DE EDIÇÃO ESCONDIDO NO FINAL
    st.write("")
    with st.expander("⚙️ CLIQUE PARA EDITAR VALORES OU NOMES"):
        st.info("Altere os dados na tabela abaixo e clique em SALVAR.")
        edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
        if st.button("SALVAR ALTERAÇÕES"):
            st.session_state.df = edited_df
            st.rerun()

except Exception as e:
    st.error(f"Erro ao carregar: {e}")
