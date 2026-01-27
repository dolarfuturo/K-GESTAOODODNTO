import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Gestão Odonto", layout="wide")

# CSS PARA DEIXAR TUDO MUITO PRÓXIMO E COMPACTO
st.markdown("""
    <style>
    .block-container {padding-top: 0.5rem; padding-bottom: 0rem;}
    div[data-testid="stVerticalBlock"] > div {padding: 0px 0px; margin-bottom: -15px;}
    .stMarkdown p {font-size: 15px; margin-bottom: 0px;}
    hr {margin-top: 2px !important; margin-bottom: 2px !important;}
    button {height: 25px; padding: 0px 5px !important;}
    </style>
    """, unsafe_allow_html=True)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(SHEET_URL)
        st.session_state.df.columns = st.session_state.df.columns.str.strip()

    st.subheader("🦷 Cobrança Rápida")

    # EXIBIÇÃO DOS PACIENTES (BEM PRÓXIMOS)
    for index, row in st.session_state.df.iterrows():
        if pd.isna(row['NOME']): continue
        
        nome = str(row['NOME']).upper()
        valor = row['TOTAL EM ATRASO']
        valor_f = f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        canal = str(row['CANAL']).upper().strip()
        celular = str(row['TELEFONE']).split('.')[0]
        
        c1, c2, c3 = st.columns([4, 2, 2])
        c1.write(f"**{nome}**")
        c2.write(f"{valor_f}")
        
        if canal == "WATS":
            msg = f"Oi {nome}! O valor para acerto é {valor_f}. 🦷\n📞 wa.me/5551997194306"
            link = f"https://wa.me/{celular}?text={urllib.parse.quote(msg)}"
            c3.markdown(f'''<a href="{link}" target="_blank"><button style="background-color:#25D366; color:white; border:none; border-radius:4px; width:100%; font-weight:bold; cursor:pointer;">ZAP</button></a>''', unsafe_allow_html=True)
        else:
            email = str(row['EMAIL'])
            link_m = f"mailto:{email}?subject=Odonto&body=Oi {nome}"
            c3.markdown(f'''<a href="{link_m}"><button style="background-color:#D14836; color:white; border:none; border-radius:4px; width:100%; font-weight:bold; cursor:pointer;">MAIL</button></a>''', unsafe_allow_html=True)
        
        st.divider()

    # BOTÃO PARA ESCONDER A EDIÇÃO NO FINAL
    with st.expander("⚙️ EDITAR VALORES OU NOMES"):
        edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
        if st.button("SALVAR ALTERAÇÕES"):
            st.session_state.df = edited_df
            st.rerun()

except Exception as e:
    st.error(f"Erro: {e}")
