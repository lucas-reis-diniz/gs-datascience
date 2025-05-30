import streamlit as st

st.set_page_config(
    page_title="Análise de Incêndios Florestais",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 Análise de Incêndios Florestais nos EUA")

st.markdown("""
Bem-vindo à análise interativa de dados sobre incêndios florestais nos Estados Unidos.

Utilize o menu lateral para navegar pelas diferentes seções da análise:

- **Visão Geral**: Carregamento dos dados e estatísticas descritivas básicas.
- **Distribuição e Causas**: Análise da distribuição do tamanho dos incêndios, causas e estados mais afetados.
- **Tendências Temporais**: Exploração das tendências anuais e sazonais dos incêndios.
- **Análise de Regressão**: Resultados da análise de regressão para identificar fatores influentes.
- **Conclusões e Recomendações**: Principais conclusões e recomendações baseadas na análise.

Os dados utilizados nesta análise são simulados, mas baseados em padrões reais de incêndios florestais.
""")

st.sidebar.success("Selecione uma análise acima.")

