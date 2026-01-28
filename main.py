import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. CONFIGURAÇÃO DE TELA E ESTILO COMPACTO
st.set_page_config(page_title="Gestão de Resgate", layout="wide")

# CSS para eliminar espaços e deixar as linhas bem juntas
st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 1rem; }
    .stMetric { background: #f0f2f6; padding: 10px; border-radius: 10px; }
    div[data-testid="stVerticalBlock"] > div { font-size: 14px; }
    [data-testid="stMetricValue"] { font-size: 20px !important; }
    .stButton button { height: 35px; padding: 0px; }
    hr { margin: 0.2rem 0px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Painel Resgate Odonto")

# Link da planilha
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    # 2. TOPO: KPIs E CONTROLE DE CANAL
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    c1.metric("Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    c2.metric("Meta", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")
    c3.metric("Lista", len(df))
    
    with c4:
        # AQUI ELA TROCA O CANAL PARA A LISTA TODA
        canal_selecionado = st.radio("Escolha o Canal de Envio:", ["WhatsApp", "E-mail"], horizontal=True)

    st.divider()

    # 3. CABEÇALHO DA TABELA
    h1, h2, h3, h4, h5 = st.columns([3, 1.5, 1.5, 1.2, 1.8])
    h1.write("**NOME DO PACIENTE**")
    h2.write("**ATR.**")
    h3.write("**ENTR.**")
    h4.write("**STATUS**")
    h5.write("**AÇÃO**")

    # 4. LISTAGEM DINÂMICA
    for index, row in df.iterrows():
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0]
        email_p = str(row.iloc[2])
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        pix = str(row.iloc[7])
        status = "✅ OK" if not pd.isna(row['CANAL']) else "⏳ Pend."

        # Texto fiel à sua fórmula
        msg_corpo = (
            f"Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! Sentimos sua falta! 🦷\n\n"
            f"📌 Total em atraso: R$ {atraso:,.2f
