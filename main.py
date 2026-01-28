import streamlit as st
import pandas as pd
from urllib.parse import quote
import unicodedata

# 1. SETUP DO PAINEL
st.set_page_config(page_title="Resgate Odonto", layout="wide")

# CSS para layout compacto (ideal para tablet)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stButton button { height: 32px; font-size: 12px; }
    hr { margin: 0.3rem 0px !important; }
    div[data-testid="column"] { padding: 0px 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Gestão de Resgate")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo a planilha (forçando tudo como String para não perder dados)
    df = pd.read_csv(sheet_url, dtype=str)

    # 2. CONTROLE SUPERIOR
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    c1.metric("Total Aberto", f"R$ {df.iloc[:, 3].astype(float).sum():,.0f}")
    c2.metric("Pacientes", len(df))
    with c4:
        canal = st.radio("Selecione o Canal:", ["WhatsApp", "E-mail"], horizontal=True)

    st.divider()

    # 3. CABEÇALHO
    h1, h2, h3, h4 = st.columns([4, 2, 2, 2])
    h1.write("**NOME**")
    h2.write("**ATRASO**")
    h3.write("**STATUS**")
    h4.write("**AÇÃO**")

    # 4. LOOP DE PACIENTES
    for index, row in df.iterrows():
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0] # Remove o .0 se existir
        email = str(row.iloc[2])
        atraso = str(row.iloc[3])
        status = "✅ OK" if not pd.isna(row.get('CANAL')) else "⏳ Pend."

        # --- O SEGREDO PARA O TEXTO VIR CERTO ---
        # Pegamos o texto direto da Coluna G (índice 6)
        # O .strip() remove espaços sobrando e o quote() codifica para o navegador
        texto_planilha = str(row.iloc[6]).strip()
        
        # Se na Coluna G vier o texto "ENVIAR WHATSAPP" (erro de Hiperlink), 
        # nós avisamos ou usamos um texto padrão.
        if "ENVIAR" in texto_planilha.upper():
             # Aqui o código reconstrói se a Coluna G falhar
             texto_envio = f"Oi {nome}, vimos que seu tratamento parou. Pendência: R$ {atraso}. Vamos voltar?"
        else:
             texto_envio = texto_planilha

        with st.container():
            col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
            col1.write(nome)
            col2.write(f"R$ {atraso}")
            col3.write(status)
            
            with col4:
                # O quote() transforma acentos e espaços em códigos que o Zap entende
                link_encoded = quote(texto_envio)
                
                if canal == "WhatsApp":
                    st.link_button("🟢 ZAP", f"https://wa.me/{tel}?text={link_encoded}", use_container_width=True)
                else:
                    st.link_button("📩 MAIL", f"mailto:{email}?subject=OdontoExcellence&body={link_encoded}", use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro na Planilha: {e}")
