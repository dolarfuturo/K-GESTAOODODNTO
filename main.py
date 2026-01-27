import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Gestão Odonto", layout="wide")

# CSS para visual ultra compacto e sem cortes no tablet
st.markdown("""
    <style>
    .block-container {padding-top: 0.5rem; padding-bottom: 0.5rem;}
    .lista-item {
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        padding: 4px 0px;
        border-bottom: 1px solid #f0f0f0;
    }
    .nome-paciente { font-size: 14px; font-weight: bold; flex: 2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .valor-paciente { font-size: 14px; flex: 1; text-align: center; color: #d32f2f; font-weight: bold; }
    .botao-link { flex: 1; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# FUNÇÃO PARA BUSCAR DADOS COM ATUALIZAÇÃO AUTOMÁTICA (CACHE)
@st.cache_data(ttl=20)
def carregar_dados(url):
    df_novo = pd.read_csv(url)
    df_novo.columns = df_novo.columns.str.strip()
    return df_novo

SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    # Carrega os dados da planilha (atualiza a cada 20s)
    df_planilha = carregar_dados(SHEET_URL)
    
    # Se não houver edição manual no app, usa os dados da planilha
    if 'df' not in st.session_state:
        st.session_state.df = df_planilha

    st.title("🦷 Cobrança Odonto")

    for index, row in st.session_state.df.iterrows():
        if pd.isna(row['NOME']): continue
        
        nome = str(row['NOME']).upper()
        telefone = str(row['TELEFONE']).split('.')[0]
        email = str(row['EMAIL'])
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        pix = str(row['PIX']) if 'PIX' in row else "CHAVE_NA_PLANILHA"
        canal = str(row['CANAL']).upper().strip()

        # Formatação de Moeda
        def fmt(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        # MONTAGEM DA MENSAGEM IGUAL À SUA FÓRMULA
        texto_whats = (
            f"Oi {nome}! Eu sou da clínica Odonto Excellence. 🦷\n\n"
            f"📌 Total em atraso: {fmt(atraso)}\n"
            f"🤝 Entrada para Retorno: {fmt(entrada)}\n\n"
            f"📞 Se preferir que eu te ligue, CLIQUE AQUI: wa.me/5551997194306\n\n"
            f"Caso contrário, segue a chave PIX para a entrada:\n"
            f"🔑 {pix}\n\n"
            f"Após o pagamento, venha até a clínica para darmos continuidade ao seu tratamento! 🏥"
        )

        link_zap = f"https://wa.me/{telefone}?text={urllib.parse.quote(texto_whats)}"
        
        # EXIBIÇÃO NA TELA
        if canal == "WATS":
            st.markdown(f'''
                <div class="lista-item">
                    <div class="nome-paciente">{nome}</div>
                    <div class="valor-paciente">{fmt(atraso)}</div>
                    <div class="botao-link"><a href="{link_zap}" target="_blank" style="color:#25D366; font-weight:bold; text-decoration:none; font-size:16px;">ZAP 📲</a></div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            link_mail = f"mailto:{email}?subject=Odonto Excellence - Pendência&body={urllib.parse.quote(texto_whats)}"
            st.markdown(f'''
                <div class="lista-item">
                    <div class="nome-paciente">{nome}</div>
                    <div class="valor-paciente">{fmt(atraso)}</div>
                    <div class="botao-link"><a href="{link_mail}" style="color:#D14836; font-weight:bold; text-decoration:none; font-size:16px;">MAIL 📩</a></div>
                </div>
            ''', unsafe_allow_html=True)

    st.write("")
    with st.expander("⚙️ CONFIGURAÇÕES E EDIÇÃO"):
        st.write("Edite aqui e clique em salvar para atualizar os botões acima.")
        edited = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
        if st.button("SALVAR ALTERAÇÕES"):
            st.session_state.df = edited
            st.rerun()

except Exception as e:
    st.error(f"Erro: {e}")
