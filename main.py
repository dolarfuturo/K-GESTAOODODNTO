import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Gestão Odonto", layout="wide")

# CSS para visual compacto e sem cortes
st.markdown("""
    <style>
    .block-container {padding-top: 1rem; padding-bottom: 1rem;}
    .lista-item {
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        padding: 4px 0px;
        border-bottom: 1px solid #f0f0f0;
    }
    .nome-paciente { font-size: 14px; font-weight: bold; flex: 2; color: #333; }
    .valor-paciente { font-size: 14px; flex: 1; text-align: center; color: #666; }
    .botao-link { flex: 1; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    if 'df' not in st.session_state:
        st.session_state.df = pd.read_csv(SHEET_URL)
        st.session_state.df.columns = st.session_state.df.columns.str.strip()

    st.title("🦷 Cobrança Odonto")

    for index, row in st.session_state.df.iterrows():
        if pd.isna(row['NOME']): continue
        
        nome = str(row['NOME']).upper()
        valor_raw = row['TOTAL EM ATRASO']
        valor_f = f"R$ {valor_raw:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        canal = str(row['CANAL']).upper().strip()
        celular = str(row['TELEFONE']).split('.')[0]
        
        # MENSAGEM COMPLETA COM PIX E RETORNO
        # Ajuste a chave PIX abaixo se for diferente de 'odonto@email.com'
        chave_pix = "CHAVE PIX AQUI" 
        
        texto_whatsapp = (
            f"Oi {nome}! Eu sou da clínica Odonto Excellence. 🦷\n\n"
            f"📌 Consta um valor pendente de {valor_f}.\n\n"
            f"Caso queira pagar via PIX, a chave é:\n🔑 {chave_pix}\n\n"
            f"Se preferir falar conosco, clique aqui: wa.me/5551997194306"
        )
        
        link_zap = f"https://wa.me/{celular}?text={urllib.parse.quote(texto_whatsapp)}"

        if canal == "WATS":
            st.markdown(f'''
                <div class="lista-item">
                    <div class="nome-paciente">{nome}</div>
                    <div class="valor-paciente">{valor_f}</div>
                    <div class="botao-link"><a href="{link_zap}" target="_blank" style="color:#25D366; font-weight:bold; text-decoration:none;">ZAP 📲</a></div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            email = str(row['EMAIL'])
            link_m = f"mailto:{email}?subject=Odonto&body={urllib.parse.quote(texto_whatsapp)}"
            st.markdown(f'''
                <div class="lista-item">
                    <div class="nome-paciente">{nome}</div>
                    <div class="valor-paciente">{valor_f}</div>
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
