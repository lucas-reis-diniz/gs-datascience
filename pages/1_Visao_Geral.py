import streamlit as st
import pandas as pd
import os
from io import StringIO

st.set_page_config(page_title="Visão Geral dos Dados", page_icon="📊", layout="wide")

st.markdown("# 📊 Visão Geral dos Dados")
st.sidebar.header("Visão Geral")
st.write("""
Nesta página, carregamos o conjunto de dados de incêndios florestais e apresentamos uma visão geral inicial,
com uma amostra dos dados, tipos de colunas e estatísticas descritivas.
""")

# Função para carregar os dados
@st.cache_data
def load_data():
    path = "data/wildfires.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            return df
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
            return pd.DataFrame()
    else:
        st.error("Arquivo 'wildfires.csv' não encontrado na pasta 'data'.")
        return pd.DataFrame()

# Carrega os dados
df = load_data()

if df.empty:
    st.warning("Não foi possível carregar os dados.")
else:
    st.subheader("📄 Amostra dos Dados")
    st.write("Visualize abaixo as primeiras linhas do conjunto de dados:")
    st.dataframe(df.head())

    st.subheader("🔢 Tipos de Dados e Valores Ausentes")
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    st.text(info_str)

    st.subheader("📊 Estatísticas Descritivas")
    st.write("Resumo estatístico das colunas numéricas:")
    st.dataframe(df.describe())
