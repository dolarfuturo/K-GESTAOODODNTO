import streamlit as st
import pandas as pd
from urllib.parse import quote

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Painel Resgate Odonto", layout="wide", page_icon="🦷")

# Título Principal
st.title("🦷 Painel Resgate Odonto")
st.markdown("---")

# 2. CONEXÃO COM A PLANILHA
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    # 3. BLOCO DE PERFORMANCE
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric("Total em Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    with col_kpi2:
        st.metric("Meta de Resgate (Entradas)", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")
    with col_kpi3:
        st.metric("Pacientes na Lista", len(df))

    st.divider()

    # 4. FILTROS
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        busca = st.text_input("🔍 Localizar Paciente", placeholder="Digite o nome...")
    with col_f2:
        canal_filtro = st.selectbox("🎯 Canal de Resgate", ["Todos", "WhatsApp", "E-mail"])

    # Lógica de Filtro
    df_filtrado = df.copy()
    if busca:
        coluna_nome = df.columns[0]
        df_filtrado = df_filtrado[df_filtrado[coluna_nome].str.contains(busca, case=False, na=False)]
    
    # 5. CABEÇALHO
    st.markdown("""<style>.header-text { font-weight: bold; color: #555; font-size: 18px; }</style>""", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
    c1.markdown("<p class='header-text'>PACIENTE</p>", unsafe_allow_html=True)
    c2.markdown("<p class='header-text'>PENDÊNCIA</p>", unsafe_allow_html=True)
    c3.markdown("<p class='header-text'>ENTRADA</p>", unsafe_allow_html=True)
    c4.markdown("<p class='header-text'>AÇÃO</p>", unsafe_allow_html=True)

    # 6. LISTAGEM COM TEU TEXTO ORIGINAL
    for index, row in df_filtrado.iterrows():
        nome = str(row.iloc[0])
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        tel = str(row['TELEFONE']).split('.')[0]
        email = str(row['EMAIL'])
        pix = str(row['CODIGO PIX'])

        # TEU TEXTO ORIGINAL
        teu_texto = f"Oi {nome}! Sou o RENATO da Odonto Excellence. Sentimos sua falta! Para seu tratamento não parar, conseguimos uma condição especial de retorno: Entrada de R$ {entrada}. PIX: {pix}"
        
        # Links formatados
        link_wats = f"https://wa.me/{tel}?text={quote(teu_texto)}"
        
        assunto = quote("Importante: Seu Tratamento na Odonto Excellence")
        link_email = f"mailto:{email}?subject={assunto}&body={quote(teu_texto)}"

        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            col1.write(f"**{nome}**")
            col2.markdown(f":red[R$ {atraso:,.2f}]")
            col3.write(f"R$ {entrada:,.2f}")
            
            with col4:
                if canal_filtro in ["Todos", "WhatsApp"]:
                    st.link_button("🟢 WATS", link_wats, use_container_width=True)
                if canal_filtro in ["Todos", "E-mail"]:
                    st.link_button("📩 MAIL", link_email, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
