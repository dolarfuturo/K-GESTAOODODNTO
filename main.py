import streamlit as st
import pandas as pd
from urllib.parse import quote

# Configuração para Tablet
st.set_page_config(page_title="Resgate Odonto", layout="wide")

st.title("🦷 Painel Resgate Odonto")
st.markdown("---")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)

    # 1. BLOCO DE PERFORMANCE
    c1, c2, c3 = st.columns(3)
    c1.metric("Total em Aberto", f"R$ {df['TOTAL EM ATRASO'].sum():,.2f}")
    c2.metric("Meta de Entradas", f"R$ {df['VALOR DE ENTRADA'].sum():,.2f}")
    c3.metric("Pacientes na Lista", len(df))

    st.divider()

    # 2. LISTAGEM
    # Cabeçalho
    h1, h2, h3, h4, h5 = st.columns([3, 2, 2, 1, 2])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**ENTRADA**")
    h4.write("**TIPO**")
    h5.write("**AÇÃO**")

    for index, row in df.iterrows():
        # Mapeando os dados conforme sua fórmula da planilha
        nome    = str(row.iloc[0])        # Coluna A
        tel     = str(row.iloc[1]).strip().split('.')[0] # Coluna B
        email_p = str(row.iloc[2])        # Coluna C
        atraso  = row['TOTAL EM ATRASO']  # Coluna D
        entrada = row['VALOR DE ENTRADA'] # Coluna E
        tipo    = str(row.iloc[5])        # Coluna F (W ou E)
        pix     = str(row.iloc[7])        # Coluna H

        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 2])
            
            col1.write(nome)
            col2.markdown(f":red[R$ {atraso:,.2f}]")
            col3.write(f"R$ {entrada:,.2f}")
            col4.write(tipo)

            with col5:
                # SE FOR WHATSAPP (W) - Recriando sua fórmula exatamente igual
                if tipo == "W":
                    texto_zap = (
                        f"Oi! Tudo bem? Eu sou RENATO, da clínica Odonto Excellence! Sentimos sua falta, "
                        f"vimos que você não compareceu mais nas consultas! Seu tratamento não pode parar! 🦷\n\n"
                        f"📌 Total em atraso: R$ {atraso:,.2f}\n"
                        f"🤝 Entrada para Retorno: R$ {entrada:,.2f}\n\n"
                        f"👉 DIGITE OK E ENVIA ✅\n\n"
                        f"Caso contrário, segue a chave PIX para a entrada:\n"
                        f"🔑 {pix}\n\nAguardamos você! 🏥"
                    )
                    link_zap = f"https://wa.me/{tel}?text={quote(texto_zap)}"
                    st.link_button("🟢 WHATSAPP", link_zap, use_container_width=True)

                # SE FOR E-MAIL (E) - Recriando sua fórmula de e-mail
                elif tipo == "E":
                    texto_mail = (
                        f"Olá! Sentimos sua falta. Seu tratamento não pode parar. "
                        f"Total em atraso: R$ {atraso:,.2f}. PIX para retorno: {pix}."
                    )
                    link_mail = f"mailto:{email_p}?subject=Odonto%20Excellence&body={quote(texto_mail)}"
                    st.link_button("📩 E-MAIL", link_mail, use_container_width=True)
                
                else:
                    st.write("Verificar F")
            st.divider()

except Exception as e:
    st.error(f"Erro ao processar dados: {e}")
