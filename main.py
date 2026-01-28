import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. AJUSTE DE LAYOUT (Estreito para Tablet)
st.set_page_config(page_title="Resgate Odonto", layout="wide")
st.markdown("""
    <style>
    .block-container { padding: 1rem 2rem; }
    .stButton button { height: 35px; border-radius: 5px; }
    hr { margin: 0.2rem 0px !important; }
    p { margin-bottom: 0px !important; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Painel de Resgate")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo a planilha (forçando tudo como texto para não sumir número)
    df = pd.read_csv(sheet_url, dtype=str)

    # 2. CONTROLE SUPERIOR
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    c1.metric("Lista", len(df))
    with c4:
        canal = st.radio("Escolha como enviar:", ["WhatsApp", "E-mail"], horizontal=True)

    st.divider()

    # 3. LISTAGEM COMPACTA
    h1, h2, h3, h4, h5 = st.columns([3, 1.5, 1.5, 1.2, 2])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**ENTRADA**")
    h4.write("**STATUS**")
    h5.write("**AÇÃO**")

    for index, row in df.iterrows():
        # Pegando os dados conforme a ordem das colunas (A, B, C, D, E, F, G, H)
        nome     = str(row.iloc[0]) # Coluna A
        telefone = str(row.iloc[1]).strip().split('.')[0] # Coluna B
        email    = str(row.iloc[2]) # Coluna C
        atraso   = str(row.iloc[3]) # Coluna D
        entrada  = str(row.iloc[4]) # Coluna E
        tipo_f   = str(row.iloc[5]).upper() # Coluna F
        pix      = str(row.iloc[7]) # Coluna H
        status   = "✅ OK" if not pd.isna(row['CANAL']) else "⏳ Pend."

        # MONTANDO A MENSAGEM IGUAL À SUA FÓRMULA (Para vir completa)
        texto_base = (
            f"Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! Sentimos sua falta! 🦷\n\n"
            f"📌 Total em atraso: R$ {atraso}\n"
            f"🤝 Entrada para Retorno: R$ {entrada}\n\n"
            f"👉 DIGITE OK E ENVIA ✅\n\n"
            f"Chave PIX: {pix}\n\nAguardamos você! 🏥"
        )

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1.5, 1.2, 2])
            col1.write(nome)
            col2.write(f"R$ {atraso}")
            col3.write(f"R$ {entrada}")
            col4.write(status)
            
            with col5:
                # O 'quote' garante que o texto não quebre e não falte palavras
                if canal == "WhatsApp":
                    link = f"https://wa.me/{telefone}?text={quote(texto_base)}"
                    st.link_button("🟢 ZAP", link, use_container_width=True)
                else:
                    link = f"mailto:{email}?subject=Odonto Excellence&body={quote(texto_base)}"
                    st.link_button("📩 MAIL", link, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
