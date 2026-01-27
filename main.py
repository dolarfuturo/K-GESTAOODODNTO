import streamlit as st
import pandas as pd
import urllib.parse

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão Odonto Excellence", layout="wide")
st.title("🦷 Cobrança - Odonto Excellence")

# --- COLOQUE O LINK DA SUA PLANILHA ABAIXO ---
# No Google Sheets: Arquivo > Compartilhar > Publicar na Web (formato CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg/gviz/tq?tqx=out:csv"

try:
    df = pd.read_csv(SHEET_URL)
    
    for index, row in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])
            
            nome = str(row['NOME'])
            valor = f"R$ {row['VALOR_ATRASO']:.2f}".replace('.', ',')
            canal = str(row['CANAL']).upper()
            celular = str(row['WHATSAPP']).replace('.0', '')
            pix = str(row['PIX'])

            col1.write(f"**{nome}**")
            col2.write(f"Dívida: {valor}")

            # LÓGICA DO BOTÃO
            if canal == "WATS":
                msg = f"Oi {nome}! Eu sou da clínica Odonto Excellence. 🦷\n\n📌 Total em atraso: {valor}\n\n📞 Se preferir que eu te ligue, clique aqui: wa.me/5551997194306\n\nCaso contrário, segue o PIX:\n🔑 {pix}"
                link_zap = f"https://wa.me/{celular}?text={urllib.parse.quote(msg)}"
                col3.markdown(f'[![WhatsApp](https://img.shields.io/badge/Enviar-WhatsApp-25D366?style=for-the-badge&logo=whatsapp)]({link_zap})')
            
            elif canal == "EMAIL":
                email = str(row['EMAIL'])
                link_mail = f"mailto:{email}?subject=Odonto Excellence&body=Oi {nome}..."
                col3.markdown(f'[![Email](https://img.shields.io/badge/Enviar-Email-D14836?style=for-the-badge&logo=gmail)]({link_mail})')
            
            st.divider()

except Exception as e:
    st.error("Erro: Verifique se o link da planilha foi publicado como CSV.")
