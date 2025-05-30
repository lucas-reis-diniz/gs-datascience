import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Tendências Temporais", page_icon="📅", layout="wide")

st.markdown("# Tendências Temporais dos Incêndios")
st.sidebar.header("Tendências Temporais")
st.write("""
Análise das tendências anuais e sazonais dos incêndios florestais, observando tanto o número de ocorrências quanto a área total queimada.
""")

# Função para carregar os dados (cache para eficiência)
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            # Especificar low_memory=False pode ajudar com tipos mistos
            df = pd.read_csv(file_path, low_memory=False)
            # Tentar converter colunas de data após o carregamento
            df['DISCOVERY_DATE_CONVERTED'] = pd.to_datetime(df['DISCOVERY_DATE'], errors='coerce')
            df['CONT_DATE_CONVERTED'] = pd.to_datetime(df['CONT_DATE'], errors='coerce')
            df['FIRE_YEAR'] = df['DISCOVERY_DATE_CONVERTED'].dt.year
            df['DISCOVERY_MONTH'] = df['DISCOVERY_DATE_CONVERTED'].dt.month
            df['CONT_DATE'] = pd.to_numeric(df['CONT_DATE'], errors='coerce')
            df['FIRE_YEAR'] = df['DISCOVERY_DATE_CONVERTED'].dt.year
            df['DISCOVERY_MONTH'] = df['DISCOVERY_DATE_CONVERTED'].dt.month
            return df
        except Exception as e:
            st.error(f"Erro ao processar o arquivo CSV: {e}")
            return None
    else:
        st.error(f"Erro: Arquivo de dados não encontrado em {file_path}")
        return None

# Caminho para o arquivo de dados
data_path = "data/wildfires.csv"

# Carrega os dados
df = load_data(data_path)

if df is not None:
    # --- Tendências Anuais ---
    st.subheader("Tendências Anuais")
    yearly_trends = df.groupby('FIRE_YEAR').agg(
        Numero_Incendios=('FOD_ID', 'count'),
        Area_Queimada_Total=('FIRE_SIZE', 'sum')
    ).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Número de Incêndios por Ano**")
        fig_yearly_count = px.line(yearly_trends, x='FIRE_YEAR', y='Numero_Incendios',
                                   title="Número Total de Incêndios por Ano",
                                   labels={"FIRE_YEAR": "Ano", "Numero_Incendios": "Número de Incêndios"})
        st.plotly_chart(fig_yearly_count, use_container_width=True)

    with col2:
        st.markdown("**Área Total Queimada por Ano**")
        fig_yearly_size = px.line(yearly_trends, x='FIRE_YEAR', y='Area_Queimada_Total',
                                  title="Área Total Queimada por Ano (Acres)",
                                  labels={"FIRE_YEAR": "Ano", "Area_Queimada_Total": "Área Queimada (Acres)"})
        st.plotly_chart(fig_yearly_size, use_container_width=True)

    # --- Padrões Sazonais ---
    st.subheader("Padrões Sazonais (Mensais)")
    monthly_trends = df.groupby('DISCOVERY_MONTH').agg(
        Numero_Incendios=('FOD_ID', 'count'),
        Tamanho_Medio=('FIRE_SIZE', 'mean')
    ).reset_index()
    
    # Mapear número do mês para nome
    month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
                 7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
    monthly_trends['Mes'] = monthly_trends['DISCOVERY_MONTH'].map(month_map)
    # Ordenar por mês
    monthly_trends = monthly_trends.sort_values('DISCOVERY_MONTH')

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Número Médio de Incêndios por Mês**")
        fig_monthly_count = px.bar(monthly_trends, x='Mes', y='Numero_Incendios',
                                   title="Número Médio de Incêndios por Mês",
                                   labels={"Mes": "Mês", "Numero_Incendios": "Número Médio de Incêndios"})
        fig_monthly_count.update_layout(xaxis={'categoryorder':'array', 'categoryarray':list(month_map.values())})
        st.plotly_chart(fig_monthly_count, use_container_width=True)

    with col4:
        st.markdown("**Tamanho Médio do Incêndio por Mês**")
        fig_monthly_size = px.bar(monthly_trends, x='Mes', y='Tamanho_Medio',
                                  title="Tamanho Médio do Incêndio por Mês (Acres)",
                                  labels={"Mes": "Mês", "Tamanho_Medio": "Tamanho Médio (Acres)"})
        fig_monthly_size.update_layout(xaxis={'categoryorder':'array', 'categoryarray':list(month_map.values())})
        st.plotly_chart(fig_monthly_size, use_container_width=True)

else:
    st.warning("Não foi possível carregar os dados para gerar as visualizações. Verifique a página 'Visão Geral'.")

