import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. CONFIGURAÇÃO DE TELA
st.set_page_config(page_title="Resgate Odonto", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stButton button { height: 40px; border-radius: 8px; font-weight: bold; width: 100%; }
    hr { margin: 0.15rem 0px !important; }
    div[data-testid="column"] { padding: 0px 5px; }
    .status-w { color: #25D366; font-weight: bold; }
    .status-e { color: #0078D4; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Gestão de Resgate Odonto")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Carregar dados
    df = pd.read_csv(sheet_url)
    
    # Tratamento de valores numéricos para o resumo
    df['TOTAL EM ATRASO'] = pd.to_numeric(df.iloc[:, 3], errors='coerce').fillna(0)
    df['VALOR DE ENTRADA'] = pd.to_numeric(df.iloc[:, 4], errors='coerce').fillna(0)

    # 2. ÁREA DE FILTROS E BUSCA
    col_busca, col_canal = st.columns([2, 1])
    busca = col_busca.text_input("🔍 Buscar Paciente pelo Nome:", "").upper()
    canal_ativo = col_canal.radio("Canal de Envio:", ["WhatsApp", "E-mail"], horizontal=True)

    # 3. PAINEL DE TOTAIS
    c1, c2, c3 = st.columns(3)
    c1.metric("Pacientes", len(df))
    c2.metric("Total em Atraso", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    c3.metric("Total das Entradas", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")

    st.divider()

    # 4. CABEÇALHO DA LISTA
    h1, h2, h3, h4, h5 = st.columns([2.5, 1.5, 1.5, 1.5, 3])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**ENTRADA**")
    h4.write("**CANAL**")
    h5.write("**AÇÃO**")

    # Filtrar DataFrame pela busca
    df_filtrado = df[df.iloc[:, 0].str.upper().str.contains(busca, na=False)]

    # 5. LISTAGEM DINÂMICA
    for index, row in df_filtrado.iterrows():
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0]
        email = str(row.iloc[2])
        v_atraso = row['TOTAL EM ATRASO']
        v_entrada = row['VALOR DE ENTRADA']
        pix = str(row.iloc[8]) # Coluna I
        canal_pref = str(row.iloc[5]).upper().strip()

        # Definição visual do canal preferencial da planilha
        status_txt = "🟢 ZAP" if canal_pref == "W" else "🔵 MAIL"
        
        # Montagem do Texto (Sempre atualizado)
        texto_envio = f"""Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! 🦷

📌 Total em atraso: R$ {v_atraso:,.2f}
🤝 Entrada para Retorno: R$ {v_entrada:,.2f}

👉 DIGITE OK E ENVIA ✅

Chave PIX:
🔑 {pix}"""

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2.5, 1.5, 1.5, 1.5, 3])
            col1.write(nome)
            col2.write(f"R$ {v_atraso:,.2f}")
            col3.write(f"R$ {v_entrada:,.2f}")
            col4.write(status_txt)
            
            with col5:
                # O botão só abre o link do canal selecionado no rádio do topo
                if canal_ativo == "WhatsApp":
                    link = f"https://wa.me/{tel}?text={quote(texto_envio)}"
                    st.link_button("ENVIAR WHATSAPP", link)
                else:
                    link = f"mailto:{email}?subject=Odonto Excellence&body={quote(texto_envio)}"
                    st.link_button("ENVIAR E-MAIL", link)
            st.divider()

except Exception as e:
    st.error(f"Erro ao carregar o sistema: {e}")
