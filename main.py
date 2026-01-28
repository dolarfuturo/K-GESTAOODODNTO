import streamlit as st
import pandas as pd
from urllib.parse import quote, urlparse, parse_qs

# 1. CONFIGURAÇÃO
st.set_page_config(page_title="Painel de Resgate Odonto", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 4rem; }
    .metric-card {
        background-color: white; padding: 15px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #1E88E5; margin-bottom: 10px;
    }
    .stButton button { height: 42px; border-radius: 8px; font-weight: bold; }
    .header-row {
        background-color: #1E88E5; color: white; padding: 10px;
        border-radius: 8px; margin-bottom: 10px; font-weight: bold;
    }
    hr { margin: 0.2rem 0px !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# TOPO
t1, t2 = st.columns([4, 1])
with t1:
    st.title("🦷 Painel de Resgate Odonto")
with t2:
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    
    # 2. FILTROS
    f1, f2 = st.columns([2, 1])
    busca = f1.text_input("🔍 Localizar Paciente (Nome):", "").upper()
    canal_ativo = f2.radio("Canal de Contato:", ["WhatsApp", "E-mail"], horizontal=True)

    st.divider()
    st.markdown('<div class="header-row"> <div style="display: flex; justify-content: space-between;"> <span style="width:30%">PACIENTE</span> <span style="width:20%">TOTAL EM ATRASO</span> <span style="width:20%">ENTRADA</span> <span style="width:30%">AÇÃO</span> </div> </div>', unsafe_allow_html=True)

    df_filtrado = df[df.iloc[:, 0].str.upper().str.contains(busca, na=False)]

    for index, row in df_filtrado.iterrows():
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0]
        v_atraso = pd.to_numeric(row.iloc[3], errors='coerce') or 0
        v_entrada = pd.to_numeric(row.iloc[4], errors='coerce') or 0
        
        # A MÁGICA ESTÁ AQUI: 
        # Ele tenta pegar a mensagem pronta da Coluna G (índice 6) da planilha
        try:
            link_completo = str(row.iloc[6])
            # Extrai apenas o texto que está após o "?text="
            parsed_url = urlparse(link_completo)
            msg_da_planilha = parse_qs(parsed_url.query)['text'][0]
        except:
            # Caso a planilha esteja vazia, usa um padrão de segurança
            msg_da_planilha = f"Oi {nome}, temos um assunto pendente na Odonto Excellence."

        with st.container():
            c1, c2, c3, c4 = st.columns([3, 2, 2, 3])
            c1.markdown(f"**{nome}**")
            c2.markdown(f"R$ {v_atraso:,.2f}")
            c3.markdown(f"R$ {v_entrada:,.2f}")
            
            with c4:
                if canal_ativo == "WhatsApp":
                    # Usa EXATAMENTE o que está na planilha
                    url_final = f"https://wa.me/{tel}?text={quote(msg_da_planilha)}"
                    st.link_button("🟢 WHATSAPP", url_final, use_container_width=True)
                else:
                    url_email = f"mailto:?subject=Odonto Excellence&body={quote(msg_da_planilha)}"
                    st.link_button("📩 E-MAIL", url_email, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
