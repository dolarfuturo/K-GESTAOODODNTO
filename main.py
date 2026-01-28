import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. CONFIGURAÇÃO E IDENTIDADE
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
    # Lendo a planilha (forçando para ler tudo como texto para não dar erro)
    df = pd.read_csv(sheet_url, dtype=str)
    
    # 2. PEGA O MODELO DA J2 (Linha 1, Coluna J)
    # No pandas, a coluna J é o índice 9
    modelo_raw = str(df.iloc[0, 9]) if not pd.isna(df.iloc[0, 9]) else "Oi {nome}, temos um assunto pendente."

    # TRATAMENTO DE VALORES PARA O RESUMO
    df_numerico = df.copy()
    df_numerico.iloc[:, 3] = pd.to_numeric(df_numerico.iloc[:, 3], errors='coerce').fillna(0)
    df_numerico.iloc[:, 4] = pd.to_numeric(df_numerico.iloc[:, 4], errors='coerce').fillna(0)

    # FILTROS
    f1, f2 = st.columns([2, 1])
    busca = f1.text_input("🔍 Localizar Paciente (Nome):", "").upper()
    canal_ativo = f2.radio("Canal de Contato:", ["WhatsApp", "E-mail"], horizontal=True)

    # RESUMO
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card">👥 <b>Pacientes</b><br><span style="font-size:22px">{len(df)}</span></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card" style="border-left-color: #d32f2f">🚩 <b>Total em Atraso</b><br><span style="font-size:22px; color:#d32f2f">R$ {df_numerico.iloc[:, 3].sum():,.2f}</span></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card" style="border-left-color: #388e3c">💰 <b>Total Entradas</b><br><span style="font-size:22px; color:#388e3c">R$ {df_numerico.iloc[:, 4].sum():,.2f}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="header-row"> <div style="display: flex; justify-content: space-between;"> <span style="width:30%">PACIENTE</span> <span style="width:20%">TOTAL EM ATRASO</span> <span style="width:20%">ENTRADA</span> <span style="width:30%">AÇÃO</span> </div> </div>', unsafe_allow_html=True)

    # Filtro de busca
    df_filtrado = df[df.iloc[:, 0].str.upper().str.contains(busca, na=False)]

    for index, row in df_filtrado.iterrows():
        nome_paciente = str(row.iloc[0])
        telefone = str(row.iloc[1]).strip().split('.')[0]
        email_paciente = str(row.iloc[2])
        val_atraso = f"{pd.to_numeric(row.iloc[3], errors='coerce'):,.2f}"
        val_entrada = f"{pd.to_numeric(row.iloc[4], errors='coerce'):,.2f}"
        chave_pix = str(row.iloc[8])

        # AQUI ESTÁ O SEGREDO: ELE TROCA INDEPENDENTE DE SER MAIÚSCULO OU MINÚSCULO
        msg_personalizada = modelo_raw.replace("{nome}", nome_paciente).replace("{NOME}", nome_paciente)\
                                      .replace("{atraso}", val_atraso).replace("{ATRASO}", val_atraso)\
                                      .replace("{entrada}", val_entrada).replace("{ENTRADA}", val_entrada)\
                                      .replace("{pix}", chave_pix).replace("{PIX}", chave_pix)

        with st.container():
            c1, c2, c3, c4 = st.columns([3, 2, 2, 3])
            c1.markdown(f"**{nome_paciente}**")
            c2.markdown(f"R$ {val_atraso}")
            c3.markdown(f"R$ {val_entrada}")
            
            with c4:
                if canal_ativo == "WhatsApp":
                    url = f"https://wa.me/{telefone}?text={quote(msg_personalizada)}"
                    st.link_button("🟢 WHATSAPP", url, use_container_width=True)
                else:
                    url = f"mailto:{email_paciente}?subject=Odonto Excellence&body={quote(msg_personalizada)}"
                    st.link_button("📩 E-MAIL", url, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
