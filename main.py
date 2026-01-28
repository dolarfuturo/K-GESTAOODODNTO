import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. CONFIGURAÇÃO E IDENTIDADE
st.set_page_config(page_title="Painel de Resgate Odonto", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    /* Espaçamento no topo para o botão não sumir */
    .block-container { padding-top: 2.5rem; }
    
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #1E88E5;
        margin-bottom: 10px;
    }
    
    .stButton button {
        height: 42px;
        border-radius: 8px;
        font-weight: bold;
    }
    
    .header-row {
        background-color: #1E88E5;
        color: white;
        padding: 12px;
        border-radius: 8px 8px 0px 0px;
        font-weight: bold;
    }
    
    hr { margin: 0.2rem 0px !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# BOTÃO DE ATUALIZAR NO TOPO (COM ESPAÇO)
col_vazia, col_btn = st.columns([3, 1])
with col_btn:
    if st.button("🔄 Atualizar Planilha", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🦷 Painel de Resgate Odonto")

sheet_id = "1HGC
