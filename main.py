import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. AJUSTES DE TELA PARA TABLET
st.set_page_config(page_title="Gestão Odonto", layout="wide")

# CSS para eliminar espaços vazios e deixar a linha bem "magra"
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    div[data-testid="stVerticalBlock"] > div { gap: 0rem; }
    hr { margin: 0.1rem 0px !important; }
    .stButton button { height: 35px; border-radius: 8px; font-weight: bold; }
    [data-testid="stMetricValue"] { font-size: 22px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Painel Resgate Odonto")

# Link da planilha
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo os dados brutos
    df = pd.read_csv(sheet_url)

    # 2. TOPO: KPIs E TROCA DE CANAL NO PAINEL
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    c1.metric("Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.0f}")
    c2.metric("Meta", f"R$ {df['VALOR DE ENTRADA'].sum():,.0f}")
    c3.metric("Pacientes", len(df))
    with c4:
        canal_selecionado = st.radio("Trocar Canal de Envio:", ["WhatsApp", "E-mail"], horizontal=True)

    st.divider()

    # 3. CABEÇALHO DA TABELA
    h1, h2, h3, h4, h5 = st.columns([3, 1.5, 1.5, 1.2, 1.8])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**ENTRADA**")
    h4.write("**STATUS**")
    h5.write("**AÇÃO**")

    # 4. LISTAGEM COM RECONSTRUÇÃO DA SUA FÓRMULA
    for index, row in df.iterrows():
        # Dados das colunas (B, C, D, E, H)
        nome = str(row.iloc[0])
        telefone = str(row.iloc[1]).strip().split('.')[0] # Coluna B
        email_cliente = str(row.iloc[2]) # Coluna C
        v_atraso = row['TOTAL EM ATRASO'] # Coluna D
        v_entrada = row['VALOR DE ENTRADA'] # Coluna E
        chave_pix = str(row.iloc[7]) # Coluna H
        status = "✅ OK" if not pd.isna(row['CANAL']) else "⏳ Pend."

        # RECONSTRUÇÃO DA MENSAGEM (IGUAL À SUA FÓRMULA DA PLANILHA)
        msg_zap = (
            f"Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! Sentimos sua falta, "
            f"vimos que você não compareceu mais nas consultas! Seu tratamento não pode parar! 🦷\n\n"
            f"📌 Total em atraso: R$ {v_atraso:,.2f}\n"
            f"🤝 Entrada para Retorno: R$ {v_entrada:,.2f}\n\n"
            f"👉 DIGITE OK E ENVIA ✅\n\n"
            f"Caso contrário, segue a chave PIX para a entrada:\n"
            f"🔑 {chave_pix}\n\nAguardamos você! 🏥"
        )

        msg_email = (
            f"Olá! Sentimos sua falta. Seu tratamento não pode parar. "
            f"Total em atraso: R$ {v_atraso:,.2f}. PIX para retorno: {chave_pix}."
        )

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1.5, 1.2, 1.8])
            col1.write(nome)
            col2.markdown(f":red[R$ {v_atraso:,.2f}]")
            col3.write(f"R$ {v_entrada:,.2f}")
            col4.write(status)
            
            with col5:
                # O 'quote' garante que o texto não corte e os emojis funcionem
                if canal_selecionado == "WhatsApp":
                    link = f"https://wa.me/{telefone}?text={quote(msg_zap)}"
                    st.link_button("🟢 ZAP", link, use_container_width=True)
                else:
                    link = f"mailto:{email_cliente}?subject=Odonto Excellence&body={quote(msg_email)}"
                    st.link_button("📩 MAIL", link, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
