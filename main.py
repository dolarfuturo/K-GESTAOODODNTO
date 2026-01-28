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
    # Carregando os dados
    df = pd.read_csv(sheet_url)

    # 3. PAINEL DE PERFORMANCE (Para encantar a gerente)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric("Total em Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    with col_kpi2:
        st.metric("Meta de Resgate (Entradas)", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")
    with col_kpi3:
        st.metric("Pacientes Pendentes", len(df))

    st.divider()

    # 4. FILTROS DE OPERAÇÃO
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        busca = st.text_input("🔍 Localizar Paciente", placeholder="Digite o nome para procurar...")
    with col_f2:
        canal_filtro = st.selectbox("🎯 Escolha o Canal de Contato", ["Todos", "WhatsApp", "E-mail"])

    # Lógica de Busca
    df_filtrado = df.copy()
    if busca:
        coluna_nome = df.columns[0]
        df_filtrado = df_filtrado[df_filtrado[coluna_nome].str.contains(busca, case=False, na=False)]
    
    # 5. CABEÇALHO DA LISTA (Estilizado)
    st.markdown("""
        <style>
        .header-text { font-weight: bold; color: #444; font-size: 16px; margin-bottom: 10px; }
        </style>
        """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
    c1.markdown("<p class='header-text'>NOME DO PACIENTE</p>", unsafe_allow_html=True)
    c2.markdown("<p class='header-text'>VALOR EM ATRASO</p>", unsafe_allow_html=True)
    c3.markdown("<p class='header-text'>VALOR ENTRADA</p>", unsafe_allow_html=True)
    c4.markdown("<p class='header-text'>AÇÃO RÁPIDA</p>", unsafe_allow_html=True)

    # 6. LISTAGEM DOS PACIENTES
    for index, row in df_filtrado.iterrows():
        nome = str(row.iloc[0])
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        tel = str(row['TELEFONE']).split('.')[0]
        email = str(row['EMAIL'])
        pix = str(row['CODIGO PIX'])

        # --- MENSAGEM DO WHATSAPP ---
        msg_wats = f"Olá {nome}! Tudo bem? Sou da Odonto Excellence. Notamos uma pendência de R$ {atraso:,.2f}. Para facilitar seu retorno, conseguimos uma entrada de R$ {entrada:,.2f}. Podemos agendar? Chave PIX: {pix}"
        link_wats = f"https://wa.me/{tel}?text={quote(msg_wats)}"

        # --- MENSAGEM DO E-MAIL (CORRIGIDA) ---
        assunto = quote("Aviso Importante: Seu Sorriso na Odonto Excellence")
        corpo_email = quote(f"Olá {nome},\n\nNotamos que o seu tratamento possui uma pendência de R$ {atraso:,.2f}.\n\nPara que possa dar continuidade ao seu tratamento, preparamos uma condição especial com entrada de R$ {entrada:,.2f}.\n\nChave PIX: {pix}\n\nAguardamos seu retorno!")
        link_email = f"mailto:{email}?subject={assunto}&body={corpo_email}"

        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            col1.write(f"**{nome}**")
            col2.markdown(f":red[R$ {atraso:,.2f}]")
            col3.write(f"R$ {entrada:,.2f}")
            
            with col4:
                if canal_filtro in ["Todos", "WhatsApp"]:
                    st.link_button("🟢 WHATSAPP", link_wats, use_container_width=True)
                if canal_filtro in ["Todos", "E-mail"]:
                    st.link_button("📩 ENVIAR E-MAIL", link_email, use_container_width=True)
            st.divider()

except Exception as e:
    st.error("Erro ao carregar os dados. Verifique o compartilhamento da planilha.")
    st.info(f"Detalhe: {e}")
