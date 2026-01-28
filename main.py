import streamlit as st
import pandas as pd

# Configuração de tela para Tablet (Sem margens inúteis)
st.set_page_config(page_title="Painel Odonto", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .stButton button { height: 38px; border-radius: 8px; font-weight: bold; }
    hr { margin: 0.1rem 0px !important; }
    div[data-testid="column"] { padding: 0px 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦷 Disparo de Resgate")

# Substitua pelo ID da sua planilha se necessário
sheet_id = "1HGC6di7KxDY3Jj-xl4NXCeDHbwJI0A7iumZt9p8isVg"
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # Lendo a planilha - O segredo é ler os links das colunas G e H
    df = pd.read_csv(sheet_url)

    c1, c2 = st.columns(2)
    c1.metric("Pendentes", len(df))
    c2.metric("Total Aberto", f"R$ {df.iloc[:, 3].sum():,.2f}")
    
    st.divider()

    # Cabeçalho da Lista conforme suas fotos
    h1, h2, h3, h4 = st.columns([3, 2, 1.5, 3.5])
    h1.write("**PACIENTE**")
    h2.write("**ATRASO**")
    h3.write("**STATUS**")
    h4.write("**AÇÃO**")

    for index, row in df.iterrows():
        nome = str(row.iloc[0])
        atraso = row.iloc[3]
        # Coluna F na sua foto é o CANAL/STATUS
        status_limpo = "⏳ Pendente" if pd.isna(row.iloc[5]) else str(row.iloc[5])
        
        # Pega os links prontos que as fórmulas criaram
        link_zap = str(row.iloc[6])   # Coluna G
        link_mail = str(row.iloc[7])  # Coluna H

        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1.5, 3.5])
            col1.write(nome)
            col2.write(f"R$ {atraso:,.2f}")
            col3.write(status_limpo)
            
            with col4:
                col_z, col_m = st.columns(2)
                
                # Só mostra o botão se houver link de verdade na planilha
                if "http" in link_zap:
                    col_z.link_button("🟢 ZAP", link_zap, use_container_width=True)
                
                if "mailto" in link_mail:
                    col_m.link_button("📩 MAIL", link_mail, use_container_width=True)
            st.divider()

except Exception as e:
    st.error(f"Erro ao ler a planilha: {e}")
