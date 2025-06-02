import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Tendências Temporais", page_icon="🗓️", layout="wide")

st.markdown("# 🗓️ Tendências Temporais dos Incêndios")
st.sidebar.header("Tendências Temporais")
st.write("""
Análise ao longo do tempo mostra padrões anuais e mensais sobre os números de incêndios e o tamanho das áreas queimadas.
""")

# Carregamento com cache
@st.cache_data
def load_data():
    path = "data/wildfires.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            df["DISCOVERY_DATE"] = pd.to_datetime(df["DISCOVERY_DATE"], errors="coerce")
            df["FIRE_YEAR"] = df["DISCOVERY_DATE"].dt.year
            df["DISCOVERY_MONTH"] = df["DISCOVERY_DATE"].dt.month
            df["FIRE_SIZE"] = pd.to_numeric(df["FIRE_SIZE"], errors="coerce")
            return df.dropna(subset=["FIRE_YEAR", "DISCOVERY_MONTH", "FIRE_SIZE"])
        except Exception as e:
            st.error(f"Erro ao carregar os dados: {e}")
            return pd.DataFrame()
    else:
        st.error("Arquivo 'wildfires.csv' não encontrado na pasta 'data'.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Nenhum dado encontrado para gerar os gráficos.")
else:
    # Tendência anual
    st.subheader("📅 Evolução Anual dos Incêndios")
    anual = df.groupby("FIRE_YEAR").agg(
        Numero_Incendios=("FOD_ID", "count"),
        Area_Queimada=("FIRE_SIZE", "sum")
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.line(anual, x="FIRE_YEAR", y="Numero_Incendios",
                       title="Número de Incêndios por Ano",
                       labels={"FIRE_YEAR": "Ano", "Numero_Incendios": "Incêndios"})
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.line(anual, x="FIRE_YEAR", y="Area_Queimada",
                       title="Área Total Queimada por Ano",
                       labels={"FIRE_YEAR": "Ano", "Area_Queimada": "Área (acres)"})
        st.plotly_chart(fig2, use_container_width=True)

    # Tendência mensal
    st.subheader("🌧️ Padrões Sazonais (Mensais)")
    mensal = df.groupby("DISCOVERY_MONTH").agg(
        Numero_Incendios=("FOD_ID", "count"),
        Tamanho_Medio=("FIRE_SIZE", "mean")
    ).reset_index()

    month_names = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                   7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
    mensal["Mes"] = mensal["DISCOVERY_MONTH"].map(month_names)

    col3, col4 = st.columns(2)

    with col3:
        fig3 = px.bar(mensal, x="Mes", y="Numero_Incendios",
                      title="Incêndios por Mês",
                      labels={"Mes": "Mês", "Numero_Incendios": "Quantidade"})
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        fig4 = px.bar(mensal, x="Mes", y="Tamanho_Medio",
                      title="Tamanho Médio dos Incêndios por Mês",
                      labels={"Mes": "Mês", "Tamanho_Medio": "Tamanho Médio (acres)"})
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
    **Conclusões:**
    - Os meses de verão geralmente apresentam maior número de focos.
    - A área total queimada pode variar mesmo com menos ocorrências.
    """)
