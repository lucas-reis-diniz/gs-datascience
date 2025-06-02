import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import os

st.set_page_config(page_title="Análise de Regressão", page_icon="📊", layout="wide")

st.markdown("# 📊 Análise de Regressão Linear")
st.sidebar.header("Análise de Regressão")
st.write("""
Usamos regressão linear para entender como fatores como o ano, o mês e a causa do incêndio influenciam o tamanho dos focos registrados.
""")

# Carregamento de dados com cache
@st.cache_data
def load_data():
    path = "data/wildfires.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            df["FIRE_SIZE"] = pd.to_numeric(df["FIRE_SIZE"], errors="coerce")
            df = df.dropna(subset=["FIRE_SIZE", "NWCG_GENERAL_CAUSE", "STATE", "DISCOVERY_DATE"])
            df["DISCOVERY_DATE"] = pd.to_datetime(df["DISCOVERY_DATE"], errors="coerce")
            df["FIRE_YEAR"] = df["DISCOVERY_DATE"].dt.year
            df["DISCOVERY_MONTH"] = df["DISCOVERY_DATE"].dt.month
            df["LOG_FIRE_SIZE"] = df["FIRE_SIZE"].apply(lambda x: np.log(x + 1))
            df = pd.get_dummies(df, columns=["NWCG_GENERAL_CAUSE", "STATE"], drop_first=True)
            return df
        except Exception as e:
            st.error(f"Erro ao processar os dados: {e}")
            return pd.DataFrame()
    else:
        st.error("Arquivo 'wildfires.csv' não encontrado na pasta 'data'.")
        return pd.DataFrame()

import numpy as np
df = load_data()

if df.empty:
    st.warning("Dados insuficientes para realizar a regressão.")
else:
    st.subheader("Modelo de Regressão Linear")

    # Seleciona variáveis explicativas
    features = [col for col in df.columns if col.startswith("NWCG_GENERAL_CAUSE_") or col.startswith("STATE_")]
    features += ["FIRE_YEAR", "DISCOVERY_MONTH"]

    X = df[features].astype(float)
    y = df["LOG_FIRE_SIZE"].astype(float)

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    st.text("Sumário do modelo:")
    st.text(model.summary())

    st.subheader("Variáveis mais influentes")
    pvals = model.pvalues.drop("const")
    coef = model.params.drop("const")
    significativas = coef[pvals < 0.05]
    top_coef = significativas.abs().sort_values(ascending=False).head(20)

    fig = px.bar(x=top_coef.index, y=coef[top_coef.index],
                 labels={"x": "Variável", "y": "Coeficiente"},
                 title="Principais Variáveis com Impacto no Tamanho do Incêndio (log)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Interpretação:**
    - Coeficientes positivos indicam aumento no tamanho dos incêndios.
    - Coeficientes negativos indicam associação com incêndios menores.
    - Apenas variáveis com p-valor < 0.05 foram consideradas.
    """)
