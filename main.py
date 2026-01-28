import streamlit as st
import pandas as pd
from urllib.parse import quote

# Configuração da Página para Tablet
st.set_page_config(page_title="Resgate Odonto", layout="wide")

# Título Profissional
st.title("🦷 Painel Resgate Odonto")
st.markdown("---")

# Link da sua planilha
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Carregando os dados
    df = pd.read_csv(sheet_url)

    # 1. BLOCO DE PERFORMANCE (KPIs)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric("Total em Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    with col_kpi2:
        st.metric("Meta de Resgate (Entradas)", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")
    with col_kpi3:
        st.metric("Pacientes na Lista", len(df))

    st.divider()

    # 2. FILTROS PARA A GERENTE
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        busca = st.text_input("🔍 Localizar Paciente", placeholder="Digite o nome...")
    with col_f2:
        canal_filtro = st.selectbox("🎯 Canal de Resgate", ["Todos", "WhatsApp", "E-mail"])

    # Lógica de Filtro por Nome
    df_filtrado = df.copy()
    if busca:
        df_filtrado = df_filtrado[df_filtrado.iloc[:, 0].str.contains(busca, case=False, na=False)]
    
    # 3. CABEÇALHO DA TABELA (Correção do Erro: unsafe_allow_html)
    st.markdown("""
        <style>
        .header-text { font-weight: bold; color: #555; font-size: 16px; }
        </style>
        """, unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
    c1.markdown("<p class='header-text'>PACIENTE</p>", unsafe_allow_html=True)
    c2.markdown("<p class='header-text'>PENDÊNCIA</p>", unsafe_allow_html=True)
    c3.markdown("<p class='header-text'>ENTRADA</p>", unsafe_allow_html=True)
    c4.markdown("<p class='header-text'>STATUS</p>", unsafe_allow_html=True)
    c5.markdown("<p class='header-text'>AÇÃO</p>", unsafe_allow_html=True)

    # 4. LISTAGEM DE OPERAÇÃO
    for index, row in df_filtrado.iterrows():
        nome = str(row.iloc[0])
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        email = str(row['EMAIL'])
        # Status baseado na coluna CANAL
        status_v = "Pendente" if pd.isna(row['CANAL']) else "Contatado"
        
        # LINK DO WHATSAPP (Pegando direto da sua Coluna G - índice 6)
        link_wats_planilha = str(row.iloc[6]) 

        # LÓGICA DO E-MAIL (Extraindo a mensagem do seu link na coluna G)
        mensagem_corpo = link_wats_planilha.split("text=")[1] if "text=" in link_wats_planilha else ""
        link_email = f"mailto:{email}?subject=Contato%20Odonto%20Excellence&body={mensagem_corpo}"

        # Linhas do Painel
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
            col1.write(f"**{nome}**")
            col2.markdown(f":red[R$ {atraso:,.2f}]")
            col3.write(f"R$ {entrada:,.2f}")
            col4.write(status_v)
            
            with col5:
                if canal_filtro in ["Todos", "WhatsApp"]:
                    st.link_button("🟢 WATS", link_wats_planilha, use_container_width=True)
                if canal_filtro in ["Todos", "E-mail"]:
                    st.link_button("📩 MAIL", link_email, use_container_width=True)
            st.divider()

except Exception as e:
    st.error("Erro ao carregar dados. Verifique o compartilhamento da planilha.")
    st.info(f"Detalhe: {e}")
