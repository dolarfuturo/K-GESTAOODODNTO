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
    # Lendo a planilha e garantindo que tudo seja tratado como texto para não dar erro
    df = pd.read_csv(sheet_url)

    # 1. KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Total em Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    c2.metric("Meta Entradas", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")
    c3.metric("Pacientes", len(df))

    st.divider()

    # 2. BUSCA
    busca = st.text_input("🔍 Localizar Paciente")
    df_f = df.copy()
    if busca:
        df_f = df_f[df_f.iloc[:, 0].str.contains(busca, case=False, na=False)]
    
    # 3. CABEÇALHO
    st.markdown("""<style>.h { font-weight: bold; color: #555; }</style>""", unsafe_allow_html=True)
    h1, h2, h3, h4, h5 = st.columns([3, 2, 2, 2, 2])
    h1.markdown("<p class='h'>PACIENTE</p>", unsafe_allow_html=True)
    h2.markdown("<p class='h'>PENDÊNCIA</p>", unsafe_allow_html=True)
    h3.markdown("<p class='h'>ENTRADA</p>", unsafe_allow_html=True)
    h4.markdown("<p class='h'>STATUS</p>", unsafe_allow_html=True)
    h5.markdown("<p class='h'>AÇÃO</p>", unsafe_allow_html=True)

    # 4. LISTAGEM
    for index, row in df_f.iterrows():
        nome = str(row.iloc[0])
        atraso = row['TOTAL EM ATRASO']
        entrada = row['VALOR DE ENTRADA']
        email = str(row['EMAIL']).strip()
        status = "Pendente" if pd.isna(row['CANAL']) else "Contatado"
        
        # --- CORREÇÃO DO LINK DA COLUNA G ---
        # Usamos .strip() para remover qualquer espaço invisível que quebra o link
        link_g = str(row.iloc[6]).strip() 

        # Se o link não começar com http, nós forçamos o formato correto
        if not link_g.startswith("http"):
            link_final = f"https://{link_g}" if "wa.me" in link_g else link_g
        else:
            link_final = link_g

        # E-MAIL: Pega a mensagem do link do Zap
        msg_e = link_final.split("text=")[1] if "text=" in link_final else ""
        link_mail = f"mailto:{email}?subject=Odonto%20Excellence&body={msg_e}"

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
            col1.write(f"**{nome}**")
            col2.markdown(f":red[R$ {atraso:,.2f}]")
            col3.write(f"R$ {entrada:,.2f}")
            col4.write(status)
            with col5:
                # O botão agora força a abertura do link externo
                st.link_button("🟢 WATS", link_final, use_container_width=True)
                st.link_button("📩 MAIL", link_mail, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro: {e}")
