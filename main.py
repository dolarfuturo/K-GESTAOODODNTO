import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Resgate Odonto", layout="wide")

st.title("🦷 Painel de Resgate - Gestão Odonto")
st.markdown("---")

# 2. CONEXÃO COM A PLANILHA (Link que você forneceu)
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo os dados
    df = pd.read_csv(sheet_url)

    # 3. CABEÇALHO DO PAINEL (Resumo para a Gerente)
    c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
    c_kpi1.metric("Total em Atraso", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    c_kpi2.metric("Meta de Entradas", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")
    c_kpi3.metric("Total Pacientes", len(df))

    st.markdown("### Lista de Resgate")
    
    # 4. FILTROS RÁPIDOS
    col_busca, col_canal = st.columns([2, 1])
    with col_busca:
        busca = st.text_input("🔍 Buscar por Nome do Paciente")
    with col_canal:
        filtro_canal = st.selectbox("🎯 Canal", ["Todos", "WhatsApp", "E-mail"])

    # Aplicando busca
    if busca:
        df = df[df.iloc[:, 0].str.contains(busca, case=False, na=False)]

    st.divider()

    # 5. LISTAGEM PROFISSIONAL (Nome, Atraso, Entrada, Status)
    # Cabeçalho da Tabela
    h1, h2, h3, h4, h5 = st.columns([3, 2, 2, 2, 2])
    h1.write("**NOME PACIENTE**")
    h2.write("**TOTAL ATRASO**")
    h3.write("**ENTRADA**")
    h4.write("**STATUS**")
    h5.write("**AÇÃO**")

    for index, row in df.iterrows():
        nome = str(row.iloc[0])
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        # Supondo que o Status esteja na coluna CANAL (W ou E)
        status = "Pendente" if pd.isna(row['CANAL']) else "Contatado"
        email = str(row['EMAIL'])
        
        # LINK DO WHATSAPP (Vem direto da sua Coluna G - índice 6)
        link_zap = str(row.iloc[6]) 
        
        # LÓGICA DO E-MAIL (Extrai a mensagem do link da Coluna G para não criar texto novo)
        mensagem_original = link_zap.split("text=")[1] if "text=" in link_zap else ""
        link_mail = f"mailto:{email}?subject=Contato Odonto Excellence&body={mensagem_original}"

        # Exibição da Linha
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
            
            col1.write(nome)
            col2.markdown(f":red[R$ {atraso:,.2f}]")
            col3.write(f"R$ {entrada:,.2f}")
            col4.write(f"ℹ️ {status}")
            
            with col5:
                if filtro_canal in ["Todos", "WhatsApp"]:
                    st.link_button("🟢 WATS", link_zap, use_container_width=True)
                if filtro_canal == "E-mail":
                    st.link_button("📩 MAIL", link_mail, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
