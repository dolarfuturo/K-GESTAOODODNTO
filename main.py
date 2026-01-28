import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. ESTILO DO PAINEL
st.set_page_config(page_title="Painel de Resgate Odonto", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background-color: white; padding: 15px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #1E88E5; margin-bottom: 10px;
    }
    .header-row {
        background-color: #1E88E5; color: white; padding: 10px;
        border-radius: 8px; margin-bottom: 15px; font-weight: bold;
    }
    .stButton button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXÃO COM A PLANILHA
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    
    # PEGA O MODELO NA J2 (Coluna 10)
    modelo_msg = str(df.iloc[0, 9]) 

    st.title("🦷 Painel de Resgate Odonto")
    
    if st.button("🔄 Atualizar Dados da Planilha"):
        st.cache_data.clear()
        st.rerun()

    # CABEÇALHO DA LISTA
    st.markdown('<div class="header-row"><div style="display: flex; justify-content: space-between;"><span style="width:25%">PACIENTE</span><span style="width:15%">ATRASO</span><span style="width:15%">ENTRADA</span><span style="width:45%; text-align:center;">ESCOLHA A FORMA DE ENVIO</span></div></div>', unsafe_allow_html=True)

    for index, row in df.iterrows():
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0]
        email = str(row.iloc[2]) # Supondo que o e-mail está na Coluna C (índice 2)
        v_atraso = f"{pd.to_numeric(row.iloc[3], errors='coerce'):,.2f}"
        v_entrada = f"{pd.to_numeric(row.iloc[4], errors='coerce'):,.2f}"
        pix = str(row.iloc[8])

        # PREPARA A MENSAGEM COM O TEXTO DA J2
        msg_final = modelo_msg.replace("{nome}", nome).replace("{atraso}", v_atraso).replace("{entrada}", v_entrada).replace("{pix}", pix)

        with st.container():
            c1, c2, c3, c4, c5 = st.columns([2.5, 1.5, 1.5, 2.2, 2.2])
            
            c1.markdown(f"**{nome}**")
            c2.markdown(f"R$ {v_atraso}")
            c3.markdown(f"R$ {v_entrada}")
            
            # BOTÃO WHATSAPP
            with c4:
                url_wa = f"https://wa.me/{tel}?text={quote(msg_final)}"
                st.link_button("🟢 WHATSAPP", url_wa)
            
            # BOTÃO E-MAIL
            with c5:
                # Assunto do e-mail fixo ou você pode criar uma coluna K para o assunto
                assunto = quote("Assunto Importante - Odonto Excellence")
                url_email = f"mailto:{email}?subject={assunto}&body={quote(msg_final)}"
                st.link_button("📧 E-MAIL", url_email)
            
            st.divider()

except Exception as e:
    st.error(f"Erro ao carregar sistema: {e}")
