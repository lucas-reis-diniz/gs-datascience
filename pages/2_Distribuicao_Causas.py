import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Distribuição e Causas", page_icon="🔥", layout="wide")

st.markdown("# Distribuição e Causas dos Incêndios")
st.sidebar.header("Distribuição e Causas")
st.write("""
Esta seção explora a distribuição do tamanho dos incêndios, as causas mais comuns (gerais e específicas)
e os estados mais afetados.
""")

# Função para carregar os dados (cache para eficiência)
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo CSV: {e}")
            return None
    else:
        st.error(f"Erro: Arquivo de dados não encontrado em {file_path}")
        return None

# Caminho para o arquivo de dados
data_path = "data/wildfires.csv"

# Carrega os dados
df = load_data(data_path)

if df is not None:
    # --- Distribuição do Tamanho dos Incêndios ---
    st.subheader("Distribuição do Tamanho dos Incêndios (FIRE_SIZE)")
    st.write("Histograma mostrando a frequência dos incêndios por tamanho (em acres). Note que a escala do eixo X é logarítmica devido à grande variação nos tamanhos.")

    # Filtrar apenas tamanhos válidos e maiores que 0
    df_valid_fire_size = df[df['FIRE_SIZE'] > 0]

    # Verificação extra: mostrar estatísticas
    st.write("Estatísticas da coluna FIRE_SIZE:")
    st.write(df_valid_fire_size['FIRE_SIZE'].describe())

    if not df_valid_fire_size.empty:
        fig_hist = px.histogram(df_valid_fire_size, x="FIRE_SIZE", nbins=100, 
                                title="Distribuição do Tamanho dos Incêndios (Escala Log)",
                                labels={"FIRE_SIZE": "Tamanho do Incêndio (Acres)"},
                                log_x=True)  # Escala logarítmica
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.warning("Não há dados válidos de tamanho de incêndio maiores que zero para exibir o histograma.")

    # --- Análise das Causas ---
    st.subheader("Causas dos Incêndios")
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Causas Gerais (STAT_CAUSE_DESCR)**")
        cause_counts = df["NWCG_GENERAL_CAUSE"].value_counts()
        fig_cause_general = px.bar(cause_counts, x=cause_counts.index, y=cause_counts.values,
                                   title="Contagem por Causa Geral",
                                   labels={"index": "Causa Geral", "y": "Número de Incêndios"})
        fig_cause_general.update_layout(xaxis_title="", yaxis_title="Número de Incêndios")
        st.plotly_chart(fig_cause_general, use_container_width=True)

    with col2:
        st.markdown("**Tamanho Médio por Causa Geral**")
        mean_size_by_cause = df.groupby("NWCG_GENERAL_CAUSE")["FIRE_SIZE"].mean().sort_values(ascending=False)
        fig_mean_size = px.bar(mean_size_by_cause, x=mean_size_by_cause.index, y=mean_size_by_cause.values,
                               title="Tamanho Médio do Incêndio por Causa Geral",
                               labels={"index": "Causa Geral", "y": "Tamanho Médio (Acres)"})
        fig_mean_size.update_layout(xaxis_title="", yaxis_title="Tamanho Médio (Acres)")
        st.plotly_chart(fig_mean_size, use_container_width=True)

    # --- Estados Mais Afetados ---
    st.subheader("Estados Mais Afetados")
    state_counts = df["STATE"].value_counts().head(15) # Top 15 estados
    fig_states = px.bar(state_counts, x=state_counts.index, y=state_counts.values,
                        title="Top 15 Estados com Mais Incêndios Registrados",
                        labels={"index": "Estado", "y": "Número de Incêndios"})
    fig_states.update_layout(xaxis_title="Estado", yaxis_title="Número de Incêndios")
    st.plotly_chart(fig_states, use_container_width=True)

else:
    st.warning("Não foi possível carregar os dados para gerar as visualizações. Verifique a página 'Visão Geral'.")

