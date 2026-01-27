import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Gestão Odonto", layout="wide")

# CSS para estilo compacto
st.markdown("<style>.block-container {padding-top: 1rem;}</style>", unsafe_allow_html=True)

st.title("🦷 Sistema de Cobrança Editável")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    # Carrega os dados
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(SHEET_URL)
        st.session_state.df.columns = st.session_state.df.columns.str.strip()

    # 1. ÁREA DE EDIÇÃO (Parece uma planilha)
    st.subheader("📝 Edite os valores abaixo:")
    edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
    
    if st.button("🔄 Atualizar Botões com Novos Valores"):
        st.session_state.df = edited_df
        st.success("Valores atualizados no app!")

    st.divider()

    # 2. ÁREA DE BOTÕES (Gera as mensagens)
    st.subheader("📲 Enviar Cobranças:")
    for index, row in st.session_state.df.iterrows():
        if pd.isna(row['NOME']): continue
        
        nome = str(row['NOME']).upper()
        valor = row['TOTAL EM ATRASO']
        valor_f = f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        canal = str(row['CANAL']).upper().strip()
        celular = str(row['TELEFONE']).split('.')[0]
        
        col1, col2, col3 = st.columns([3, 2, 2])
        col1.write(f"**{nome}**")
        col2.write(f"Valor: {valor_f}")
        
        if canal == "WATS":
            msg = f"Oi {nome}! O valor atualizado para acerto é {valor_f}. 🦷\n📞 wa.me/5551997194306"
            link = f"https://wa.me/{celular}?text={urllib.parse.quote(msg)}"
            col3.markdown(f'[:green[ENVIAR WHATSAPP]]({link})')
        else:
            col3.write("📧 Enviar por E-mail")
        st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
