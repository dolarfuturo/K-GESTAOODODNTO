import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. CONFIGURAÇÃO E IDENTIDADE
st.set_page_config(page_title="Painel de Resgate Odonto", layout="wide")

# CSS AVANÇADO PARA LAYOUT PROFISSIONAL
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 1.5rem; }
    
    /* Cartões de Totais */
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #1E88E5;
        margin-bottom: 10px;
    }
    
    /* Botões */
    .stButton button {
        height: 42px;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    /* Cabeçalho da Tabela */
    .header-row {
        background-color: #1E88E5;
        color: white;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    /* Linhas da Tabela */
    .patient-row {
        background-color: white;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 6px;
        border: 1px solid #eee;
    }
    
    hr { margin: 0.2rem 0px !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# TÍTULO E BOTÃO DE ATUALIZAR
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
    df['TOTAL EM ATRASO'] = pd.to_numeric(df.iloc[:, 3], errors='coerce').fillna(0)
    df['VALOR DE ENTRADA'] = pd.to_numeric(df.iloc[:, 4], errors='coerce').fillna(0)

    # FILTROS
    f1, f2 = st.columns([2, 1])
    busca = f1.text_input("🔍 Localizar Paciente (Nome):", "").upper()
    canal_ativo = f2.radio("Canal de Contato:", ["WhatsApp", "E-mail"], horizontal=True)

    # RESUMO FINANCEIRO ESTILIZADO
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card">👥 <b>Pacientes</b><br><span style="font-size:22px">{len(df)}</span></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card" style="border-left-color: #d32f2f">🚩 <b>Total em Atraso</b><br><span style="font-size:22px; color:#d32f2f">R$ {df["TOTAL EM ATRASO"].sum():,.2f}</span></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card" style="border-left-color: #388e3c">💰 <b>Total Entradas</b><br><span style="font-size:22px; color:#388e3c">R$ {df["VALOR DE ENTRADA"].sum():,.2f}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="header-row"> <div style="display: flex; justify-content: space-between;"> <span style="width:30%">PACIENTE</span> <span style="width:20%">ATRASO</span> <span style="width:20%">ENTRADA</span> <span style="width:30%">AÇÃO</span> </div> </div>', unsafe_allow_html=True)

    # LISTAGEM
    df_filtrado = df[df.iloc[:, 0].str.upper().str.contains(busca, na=False)]

    for index, row in df_filtrado.iterrows():
        nome = str(row.iloc[0])
        tel = str(row.iloc[1]).strip().split('.')[0]
        email = str(row.iloc[2])
        v_atraso = row['TOTAL EM ATRASO']
        v_entrada = row['VALOR DE ENTRADA']
        pix = str(row.iloc[8])

        texto_mensagem = f"Oi! Tudo bem? Eu sou RENATO, da Odonto Excellence! 🦷\n\n📌 Total em atraso: R$ {v_atraso:,.2f}\n🤝 Entrada: R$ {v_entrada:,.2f}\n\nPIX: {pix}"

        with st.container():
            c1, c2, c3, c4 = st.columns([3, 2, 2, 3])
            c1.markdown(f"**{nome}**")
            c2.markdown(f"R$ {v_atraso:,.2f}")
            c3.markdown(f"R$ {v_entrada:,.2f}")
            
            with c4:
                if canal_ativo == "WhatsApp":
                    url = f"https://wa.me/{tel}?text={quote(texto_mensagem)}"
                    st.link_button("🟢 WHATSAPP", url, use_container_width=True)
                else:
                    url = f"mailto:{email}?subject=Resgate%20Odonto&body={quote(texto_mensagem)}"
                    st.link_button("📩 E-MAIL", url, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
