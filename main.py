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
    df = pd.read_csv(sheet_url)

    # 1. BLOCO DE PERFORMANCE (KPIs)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric("Total em Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    with col_kpi2:
        st.metric("Meta de Resgate (Entradas)", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}", delta_color="normal")
    with col_kpi3:
        st.metric("Pacientes na Lista", len(df))

    st.divider()

    # 2. FILTROS PARA A GERENTE
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        busca = st.text_input("🔍 Localizar Paciente", placeholder="Digite o nome...")
    with col_f2:
        canal_filtro = st.selectbox("🎯 Canal de Resgate", ["Todos", "WhatsApp", "E-mail"])

    # Lógica de Filtro
    df_filtrado = df.copy()
    if busca:
        df_filtrado = df_filtrado[df_filtrado.iloc[:, 0].str.contains(busca, case=False, na=False)]
    
    # 3. CABEÇALHO DA TABELA
    st.markdown("""
        <style>
        .header-text { font-weight: bold; color: #555; }
        </style>
        """, unsafe_allow_stdio=True)
    
    c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
    c1.markdown("<p class='header-text'>PACIENTE</p>", unsafe_allow_stdio=True)
    c2.markdown("<p class='header-text'>PENDÊNCIA</p>", unsafe_allow_stdio=True)
    c3.markdown("<p class='header-text'>ENTRADA</p>", unsafe_allow_stdio=True)
    c4.markdown("<p class='header-text'>AÇÃO</p>", unsafe_allow_stdio=True)

    # 4. LISTAGEM DE OPERAÇÃO
    for index, row in df_filtrado.iterrows():
        nome = row.iloc[0]
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        tel = str(row['TELEFONE']).split('.')[0]
        email = row['EMAIL']
        pix = row['CODIGO PIX']

        # Mensagem Automática
        msg = f"Oi {nome}! Sou o RENATO da Odonto Excellence. Sentimos sua falta! Para seu tratamento não parar, conseguimos uma condição especial de retorno: Entrada de R$ {entrada}. PIX: {pix}"
        link_wats = f"https://wa.me/{tel}?text={quote(msg)}"

        # Linhas do Painel
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            col1.write(f"**{nome}**")
            col2.markdown(f":red[R$ {atraso:,.2f}]")
            col3.write(f"R$ {entrada:,.2f}")
            
            with col4:
                # Se o filtro for Todos ou WhatsApp, mostra o botão verde
                if canal_filtro in ["Todos", "WhatsApp"]:
                    st.link_button("🟢 WATS", link_wats, use_container_width=True)
                # Se o filtro for E-mail, mostra o botão azul
                if canal_filtro == "E-mail":
                    st.link_button("📩 MAIL", f"mailto:{email}", use_container_width=True)
            st.divider()

except Exception as e:
    st.error("Ops! Verifique se a planilha está compartilhada como 'Qualquer pessoa com o link'.")
    st.info(f"Erro: {e}")
