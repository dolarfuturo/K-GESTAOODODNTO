
import streamlit as st
import pandas as pd

# Conecta na sua planilha
df = pd.read_csv("SUA_PLANILHA_LINK_AQUI")

for index, row in df.iterrows():
    col1, col2 = st.columns([3, 1])
    col1.write(f"Paciente: {row['NOME']} - R$ {row['VALOR']}")
    
    # Cria o link do WhatsApp
    link = f"https://wa.me/{row['CELULAR']}?text=Oi...Sua entrada é R$ {row['VALOR']}"
    
    if col2.button("Enviar", key=index):
        st.markdown(f'<a href="{link}" target="_blank">Abrir WhatsApp</a>', unsafe_allow_html=True)
