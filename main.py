import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. IDENTIDADE DO PAINEL
st.set_page_config(page_title="Painel de Resgate Odonto", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stButton button { height: 40px; border-radius: 8px; font-weight: bold; width: 100%; }
    [data-testid="stMetricValue"] { font-size: 24px; color: #1E88E5; }
    hr { margin: 0.15rem 0px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Painel de Resgate Odonto")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Carregar os dados
    df = pd.read_csv(sheet_url)
    
    # Tratamento Numérico (Colunas D e E)
    df['TOTAL EM ATRASO'] = pd.to_numeric(df.iloc[:, 3], errors='coerce').fillna(0)
    df['VALOR DE ENTRADA'] = pd.to_numeric(df.iloc[:, 4], errors='coerce').fillna(0)

    # 2. CONTROLES: BUSCA E SELETOR DE BOTÃO
    col_busca, col_canal = st.columns([2, 1])
    busca = col_busca.text_input("🔍 Localizar Paciente:", "").upper()
    canal_ativo = col_canal.radio("Ação do Botão:", ["WhatsApp", "E-mail"], horizontal=True)

    # 3. RESUMO FINANCEIRO (TOTAIS)
    c1, c2, c3 = st.columns(3)
    c1.metric("Qtd. Pacientes", len(df))
    c2.metric("Total em Atraso", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    c3.metric("Total para Receber", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")

    st.divider()

    # 4. CABEÇALHO DA LISTA
    h1, h2, h3, h4 = st.columns([3, 2, 2, 3])
    h1.write("**NOME PACIENTE**")
    h2.write("**TOTAL ATRASADO**")
    h3.write("**ENTRADA**")
    h4.write("**DISPARAR CONTATO**")

    # Filtro de busca em tempo real
    df_filtrado = df[df.iloc[:, 0].str.upper().str.contains(busca, na=False)]

    # 5. LISTAGEM DE PACIENTES
    for index, row in df_filtrado.iterrows():
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0]
        email = str(row.iloc[2])
        v_atraso = row['TOTAL EM ATRASO']
        v_entrada = row['VALOR DE ENTRADA']
        pix = str(row.iloc[8]) # Coluna I

        # Texto dinâmico que o sistema gera para você
        texto_corpo = f"""Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! 🦷

📌 Total em atraso: R$ {v_atraso:,.2f}
🤝 Entrada para Retorno: R$ {v_entrada:,.2f}

👉 DIGITE OK E ENVIA ✅

Chave PIX:
🔑 {pix}"""

        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
            col1.write(nome)
            col2.write(f"R$ {v_atraso:,.2f}")
            col3.write(f"R$ {v_entrada:,.2f}")
            
            with col4:
                if canal_ativo == "WhatsApp":
                    url = f"https://wa.me/{tel}?text={quote(texto_corpo)}"
                    st.link_button("🟢 ENVIAR WHATSAPP", url)
                else:
                    url = f"mailto:{email}?subject=Odonto Excellence&body={quote(texto_corpo)}"
                    st.link_button("📩 ENVIAR E-MAIL", url)
            st.divider()

except Exception as e:
    st.error(f"Erro ao sincronizar com a planilha: {e}")
