import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Distribuição e Causas", page_icon="🔥", layout="wide")

st.markdown("# 🔥 Distribuição e Causas dos Incêndios")
st.sidebar.header("Distribuição e Causas")
st.write("""
Esta página analisa os tamanhos dos incêndios, suas causas principais e os estados mais afetados.
""")

# Carregar dados com cache
@st.cache_data
def load_data():
    path = "data/wildfires.csv"
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            df["FIRE_SIZE"] = pd.to_numeric(df["FIRE_SIZE"], errors="coerce")
            return df.dropna(subset=["FIRE_SIZE"])
        except Exception as e:
            st.error(f"Erro ao ler o CSV: {e}")
            return pd.DataFrame()
    else:
        st.error("Arquivo 'wildfires.csv' não encontrado na pasta 'data'.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Nenhum dado disponível.")
else:
    # 🔹 Distribuição dos tamanhos dos incêndios
    st.subheader("📏 Tamanho dos Incêndios")
    st.write("A maioria dos incêndios é pequena, mas existem eventos extremos. Usamos escala logarítmica para visualizar melhor.")

        # Garantir valores positivos
    df["FIRE_SIZE"] = pd.to_numeric(df["FIRE_SIZE"], errors="coerce")
    df_filtrado = df[df["FIRE_SIZE"] > 0]

    # Criar categorias de tamanho
    bins = [0, 1, 10, 100, 1000, 10000, df_filtrado["FIRE_SIZE"].max()]
    labels = ['<1 acre', '1-10 acres', '10-100 acres', '100-1.000 acres', '1.000-10.000 acres', '10.000+ acres']
    df_filtrado["FIRE_SIZE_BIN"] = pd.cut(df_filtrado["FIRE_SIZE"], bins=bins, labels=labels)

    # Plotar gráfico de barras por categoria
    import plotly.express as px

    fig_cat = px.histogram(df_filtrado, x="FIRE_SIZE_BIN", 
                        title="Distribuição de Tamanho dos Incêndios por Faixa",
                        labels={"FIRE_SIZE_BIN": "Faixa de Tamanho"},
                        color_discrete_sequence=["cian", "darkorange", "firebrick"])
    fig_cat.update_layout(xaxis_title="Faixa de Tamanho (acres)", yaxis_title="Número de Incêndios")
    fig_cat.update_xaxes(categoryorder="total descending")
    st.write("A distribuição dos tamanhos dos incêndios mostra que a maioria é pequena, mas há eventos extremos significativos.")
    st.plotly_chart(fig_cat, use_container_width=True)

    # 🔹 Causas gerais
    st.subheader("📌 Causas Gerais")
    st.write("Principais razões que deram origem aos incêndios florestais.")

    causas = df["NWCG_GENERAL_CAUSE"].value_counts().reset_index()
    causas.columns = ["Causa Geral", "Quantidade"]

    fig_causa = px.bar(causas, x="Causa Geral", y="Quantidade", 
                       title="Número de Incêndios por Causa Geral")
    st.plotly_chart(fig_causa, use_container_width=True)

    # 🔹 Tamanho médio por causa
    st.subheader("🔥 Tamanho Médio por Causa")
    st.write("Algumas causas tendem a gerar incêndios maiores, como raios ou linhas de energia.")

    media_causa = df.groupby("NWCG_GENERAL_CAUSE")["FIRE_SIZE"].mean().sort_values(ascending=False).reset_index()
    media_causa.columns = ["Causa Geral", "Tamanho Médio (acres)"]

    fig_media = px.bar(media_causa, x="Causa Geral", y="Tamanho Médio (acres)",
                       title="Tamanho Médio dos Incêndios por Causa")
    st.plotly_chart(fig_media, use_container_width=True)

    # 🔹 Estados mais afetados
    st.subheader("🗺️ Estados Mais Afetados")
    st.write("Visualize os 15 estados com maior número de incêndios registrados.")

    estados = df["STATE"].value_counts().head(15).reset_index()
    estados.columns = ["Estado", "Incêndios"]

    fig_estado = px.bar(estados, x="Estado", y="Incêndios",
                        title="Top 15 Estados com Mais Incêndios")
    st.plotly_chart(fig_estado, use_container_width=True)
    st.write("Os estados mais afetados mostram a distribuição geográfica dos incêndios florestais nos EUA.")