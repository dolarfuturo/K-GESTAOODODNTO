import streamlit as st
import pandas as pd
from urllib.parse import quote

# Configuração Compacta para Tablet
st.set_page_config(page_title="Resgate Odonto", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stButton button { height: 35px; }
    hr { margin: 0.2rem 0px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Painel Resgate Automático")

sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo a planilha (Garantindo que o Python veja tudo como texto)
    df = pd.read_csv(sheet_url, dtype=str)

    # KPIs Rápidos
    c1, c2, c3, c4 = st.columns([1,1,1,2])
    c1.metric("Lista", len(df))
    with c4:
        canal = st.radio("Canal de Envio:", ["WhatsApp", "E-mail"], horizontal=True)

    st.divider()

    # Cabeçalho
    h1, h2, h3, h4 = st.columns([4, 2, 2, 2])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**STATUS**")
    h4.write("**AÇÃO**")

    for index, row in df.iterrows():
        nome = row.iloc[0]
        telefone = str(row.iloc[1]).strip().split('.')[0]
        email_cliente = row.iloc[2]
        valor_atraso = row.iloc[3]
        status_atual = "✅ OK" if not pd.isna(row['CANAL']) else "⏳ Pend."
        
        # --- AQUI ESTÁ A MUDANÇA ---
        # Em vez de escrever o texto aqui, o Python pega o que estiver 
        # na célula de texto da sua planilha. 
        # Vou assumir que o texto bruto está na coluna logo antes do link (Coluna F ou similar)
        # Se o texto completo estiver em outra coluna, basta ajustar o índice abaixo.
        texto_da_planilha = str(row.iloc[6]) # Exemplo: pegando da coluna G bruta
        
        # Limpa o texto de possíveis erros de exportação do CSV
        texto_limpo = texto_da_planilha.replace("_", " ").strip()
        
        with st.container():
            col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
            col1.write(nome)
            col2.write(f"R$ {valor_atraso}")
            col3.write(status_atual)
            
            with col4:
                if canal == "WhatsApp":
                    # O segredo para não faltar palavras é o quote() no texto da planilha
                    link_final = f"https://wa.me/{telefone}?text={quote(texto_limpo)}"
                    st.link_button("🟢 ZAP", link_final, use_container_width=True)
                else:
                    link_final = f"mailto:{email_cliente}?subject=Odonto Excellence&body={quote(texto_limpo)}"
                    st.link_button("📩 MAIL", link_final, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro ao ler planilha: {e}")
