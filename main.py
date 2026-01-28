import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. ESTILO ORIGINAL (MANTIDO)
st.set_page_config(page_title="Painel de Resgate Odonto", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 4rem; }
    .metric-card {
        background-color: white; padding: 15px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #1E88E5; margin-bottom: 10px;
    }
    .header-row {
        background-color: #1E88E5; color: white; padding: 10px;
        border-radius: 8px; margin-bottom: 15px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS E CONEXÃO
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    
    # PEGA O MODELO DA J2 (QUE VOCÊ ACABOU DE AJUSTAR)
    modelo_base = str(df.iloc[0, 9]) 

    st.title("🦷 Painel de Resgate Odonto")
    
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

    # CABEÇALHO DA LISTA EXATAMENTE COMO ESTAVA
    st.markdown('<div class="header-row"> <div style="display: flex; justify-content: space-between;"> <span style="width:30%">PACIENTE</span> <span style="width:20%">TOTAL EM ATRASO</span> <span style="width:20%">ENTRADA</span> <span style="width:30%">AÇÃO</span> </div> </div>', unsafe_allow_html=True)

    for index, row in df.iterrows():
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0]
        v_atraso = f"{pd.to_numeric(row.iloc[3], errors='coerce'):,.2f}"
        v_entrada = f"{pd.to_numeric(row.iloc[4], errors='coerce'):,.2f}"
        pix = str(row.iloc[8])

        # O BOTÃO MONTA A MENSAGEM COM O TEXTO QUE ESTÁ NA J2
        msg_final = modelo_base.replace("{nome}", nome).replace("{atraso}", v_atraso).replace("{entrada}", v_entrada).replace("{pix}", pix)

        with st.container():
            c1, c2, c3, c4 = st.columns([3, 2, 2, 3])
            c1.markdown(f"**{nome}**")
            c2.markdown(f"R$ {v_atraso}")
            c3.markdown(f"R$ {v_entrada}")
            with c4:
                # Link do WhatsApp usando o texto da planilha
                url_wa = f"https://wa.me/{tel}?text={quote(msg_final)}"
                st.link_button("🟢 ENVIAR WHATSAPP", url_wa, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
