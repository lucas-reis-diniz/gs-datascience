import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Visão Geral dos Dados", page_icon="📊", layout="wide")

st.markdown("# Visão Geral dos Dados")
st.sidebar.header("Visão Geral")
st.write("""
Nesta página, carregamos o conjunto de dados de incêndios florestais e apresentamos uma visão geral inicial,
incluindo as primeiras linhas, informações sobre os tipos de dados e estatísticas descritivas básicas.
""")

# Função para carregar os dados
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error(f"Erro: Arquivo de dados não encontrado em {file_path}")
        return None

# Caminho para o arquivo de dados
data_path = "data/wildfires.csv"

# Carrega os dados
df = load_data(data_path)

if df is not None:
    st.subheader("Amostra dos Dados")
    st.dataframe(df.head())

    st.subheader("Informações Gerais")
    st.text("Informações sobre os tipos de dados e valores não nulos:")
    # Captura a saída de df.info()
    from io import StringIO
    buffer = StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    st.subheader("Estatísticas Descritivas")
    st.dataframe(df.describe())
else:
    st.warning("Não foi possível carregar os dados. Verifique se o arquivo 'wildfires.csv' está na pasta 'data'.")

