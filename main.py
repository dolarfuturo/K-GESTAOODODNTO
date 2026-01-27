import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Gestão Odonto", layout="wide")

# CSS para visual ultra compacto para o tablet
st.markdown("""
    <style>
    .block-container {padding-top: 0.5rem; padding-bottom: 0.5rem;}
    .lista-item {
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        padding: 6px 0px;
        border-bottom: 1px solid #f0f0f0;
    }
    .nome-paciente { font-size: 14px; font-weight: bold; flex: 2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .valor-paciente { font-size: 14px; flex: 1; text-align: center; color: #d32f2f; font-weight: bold; }
    .botao-link { flex: 1; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# CARREGAR DADOS COM ATUALIZAÇÃO AUTOMÁTICA (TTL 10 SEG)
@st.cache_data(ttl=10)
def carregar_dados(url):
    df_novo = pd.read_csv(url)
    # Limpa nomes de colunas (tira espaços extras e deixa em maiúsculo)
    df_novo.columns = df_novo.columns.str.strip().str.upper()
    return df_novo

SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    df_planilha = carregar_dados(SHEET_URL)
    st.title("🦷 Cobrança Odonto")

    for index, row in df_planilha.iterrows():
        if pd.isna(row.get('NOME')): continue
        
        nome = str(row['NOME']).upper()
        telefone = str(row['TELEFONE']).split('.')[0]
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        
        # AJUSTE: Procurando 'CODIGO PIX' sem acento conforme a imagem
        pix = str(row['CODIGO PIX']) if 'CODIGO PIX' in row and pd.notna(row['CODIGO PIX']) else "Solicitar Chave"
        
        canal = str(row['CANAL']).upper().strip()

        def fmt(v): return f"R$ {v:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        # MENSAGEM COMPLETA
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
        
        if canal == "WATS":
            st.markdown(f'''
                <div class="lista-item">
                    <div class="nome-paciente">{nome}</div>
                    <div class="valor-paciente">{fmt(atraso)}</div>
                    <div class="botao-link"><a href="{link_zap}" target="_blank" style="color:#25D366; font-weight:bold; text-decoration:none; font-size:16px;">ZAP 📲</a></div>
                </div>
            ''', unsafe_allow_html=True)
        else:
            email = str(row['EMAIL'])
            link_mail = f"mailto:{email}?subject=Odonto Excellence - Pendência&body={urllib.parse.quote(texto_whats)}"
            st.markdown(f'''
                <div class="lista-item">
                    <div class="nome-paciente">{nome}</div>
                    <div class="valor-paciente">{fmt(atraso)}</div>
                    <div class="botao-link"><a href="{link_mail}" style="color:#D14836; font-weight:bold; text-decoration:none; font-size:16px;">MAIL 📩</a></div>
                </div>
            ''', unsafe_allow_html=True)

    with st.expander("⚙️ CONFERIR PLANILHA"):
        st.dataframe(df_planilha)

except Exception as e:
    st.error(f"Erro: {e}")
