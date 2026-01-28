import streamlit as st
import pandas as pd
from urllib.parse import quote

# Configuração para Tablet
st.set_page_config(page_title="Resgate Odonto", layout="wide")

st.title("🦷 Painel Resgate Odonto")
st.markdown("---")

# Link da planilha
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo a planilha
    df = pd.read_csv(sheet_url)

    # 1. KPIs de Performance
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric("Total em Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    with col_kpi2:
        st.metric("Meta de Entradas", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")
    with col_kpi3:
        st.metric("Pacientes", len(df))

    st.divider()

    # 2. BUSCA
    busca = st.text_input("🔍 Localizar Paciente", placeholder="Digite o nome...")
    if busca:
        df = df[df.iloc[:, 0].str.contains(busca, case=False, na=False)]
    
    # 3. CABEÇALHO DA TABELA
    st.markdown("""<style>.header { font-weight: bold; color: #555; font-size: 16px; }</style>""", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
    c1.markdown("<p class='header'>PACIENTE</p>", unsafe_allow_html=True)
    c2.markdown("<p class='header'>PENDÊNCIA</p>", unsafe_allow_html=True)
    c3.markdown("<p class='header'>ENTRADA</p>", unsafe_allow_html=True)
    c4.markdown("<p class='header'>STATUS</p>", unsafe_allow_html=True)
    c5.markdown("<p class='header'>AÇÃO</p>", unsafe_allow_html=True)

    # 4. LISTAGEM PEGANDO O LINK DA COLUNA G
    for index, row in df.iterrows():
        nome = str(row.iloc[0])
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        email = str(row['EMAIL'])
        # Status da coluna CANAL
        status_v = "Pendente" if pd.isna(row['CANAL']) else "Contatado"
        
        # --- AQUI ESTÁ O QUE VOCÊ PEDIU ---
        # Coluna G é o índice 6 no Python
        link_pronto_coluna_g = str(row.iloc[6]) 

        # Extraindo a mensagem do link para o e-mail (pra não ficar vazio)
        if "text=" in link_pronto_coluna_g:
            msg_corpo = link_pronto_coluna_g.split("text=")[1]
        else:
            msg_corpo = quote("Olá, gostaria de falar sobre seu tratamento.")

        link_email = f"mailto:{email}?subject=Odonto%20Excellence&body={msg_corpo}"

        # Exibição na tela
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
            col1.write(f"**{nome}**")
            col2.markdown(f":red[R$ {atraso:,.2f}]")
            col3.write(f"R$ {entrada:,.2f}")
            col4.write(status_v)
            
            with col5:
                # O botão agora abre o link exatamente como está na Coluna G
                st.link_button("🟢 WATS", link_pronto_coluna_g, use_container_width=True)
                st.link_button("📩 MAIL", link_email, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro ao carregar a Coluna G: {e}")
