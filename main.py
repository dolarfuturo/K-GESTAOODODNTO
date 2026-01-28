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
    df = pd.read_csv(sheet_url)

    # 1. KPIs DE PERFORMANCE
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric("Total em Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    with col_kpi2:
        st.metric("Meta de Entradas", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")
    with col_kpi3:
        st.metric("Pacientes na Lista", len(df))

    st.divider()

    # 2. FILTROS
    busca = st.text_input("🔍 Localizar Paciente", placeholder="Digite o nome...")
    df_f = df.copy()
    if busca:
        df_f = df_f[df_f.iloc[:, 0].str.contains(busca, case=False, na=False)]

    # 3. CABEÇALHO DA TABELA
    st.markdown("""<style>.header { font-weight: bold; color: #555; }</style>""", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
    c1.markdown("<p class='header'>PACIENTE</p>", unsafe_allow_html=True)
    c2.markdown("<p class='header'>PENDÊNCIA</p>", unsafe_allow_html=True)
    c3.markdown("<p class='header'>ENTRADA</p>", unsafe_allow_html=True)
    c4.markdown("<p class='header'>STATUS</p>", unsafe_allow_html=True)
    c5.markdown("<p class='header'>AÇÃO</p>", unsafe_allow_html=True)

    # 4. LISTAGEM COM RECONSTRUÇÃO DA MENSAGEM (IGUAL À PLANILHA)
    for index, row in df_f.iterrows():
        # Captura de dados baseada nas colunas da sua fórmula
        nome = str(row.iloc[0]) # A
        tel = str(row.iloc[1]).strip().split('.')[0] # B
        email_p = str(row.iloc[2]) # C
        atraso_v = row['TOTAL EM ATRASO'] # D
        entrada_v = row['VALOR DE ENTRADA'] # E
        tipo = str(row.iloc[5]).upper() # F (W ou E)
        pix_chave = str(row.iloc[7]) # H
        
        # Status
        status_v = "Pendente" if pd.isna(row['CANAL']) else "Contatado"

        # RECONSTRUÇÃO DA MENSAGEM (CÓPIA FIEL DA SUA FÓRMULA)
        # O CARACT(10) vira \n no Python
        msg_completa = (
            f"Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! "
            f"Sentimos sua falta, vimos que você não compareceu mais nas consultas! "
            f"Seu tratamento não pode parar! 🦷\n\n"
            f"📌 Total em atraso: R$ {atraso_v:,.2f}\n"
            f"🤝 Entrada para Retorno: R$ {entrada_v:,.2f}\n\n"
            f"👉 DIGITE OK E ENVIA ✅\n\n"
            f"Caso contrário, segue a chave PIX para a entrada:\n"
            f"🔑 {pix_chave}\n\nAguardamos você! 🏥"
        )

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
            col1.write(f"**{nome}**")
            col2.markdown(f":red[R$ {atraso_v:,.2f}]")
            col3.write(f"R$ {entrada_v:,.2f}")
            col4.write(status_v)
            
            with col5:
                if "W" in tipo:
                    link_zap = f"https://wa.me/{tel}?text={quote(msg_completa)}"
                    st.link_button("🟢 WATS", link_zap, use_container_width=True)
                
                if "E" in tipo:
                    # E-mail usa uma versão resumida conforme sua fórmula
                    msg_email = (
                        f"Olá! Sentimos sua falta. Seu tratamento não pode parar. "
                        f"Total em atraso: R$ {atraso_v:,.2f}. PIX para retorno: {pix_chave}."
                    )
                    link_mail = f"mailto:{email_p}?subject=Odonto%20Excellence&body={quote(msg_email)}"
                    st.link_button("📩 MAIL", link_mail, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro ao processar painel: {e}")
