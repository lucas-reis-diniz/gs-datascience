import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
import numpy as np
import os

st.set_page_config(page_title="Análise de Regressão", page_icon="📈", layout="wide")

st.markdown("# Análise de Regressão")
st.sidebar.header("Regressão")
st.write("""
Nesta seção, apresentamos os resultados de uma análise de regressão linear múltipla (OLS - Ordinary Least Squares)
para identificar os fatores que podem influenciar o tamanho dos incêndios (logaritmo natural de FIRE_SIZE).
""")

# Função para carregar os dados (cache para eficiência)
@st.cache_data
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, low_memory=False)
            # Conversões e tratamento de dados necessários para a regressão
            df["NWCG_GENERAL_CAUSE"] = df["NWCG_GENERAL_CAUSE"].astype("category")
            df["STATE"] = df["STATE"].astype("category")
            df["DISCOVERY_DATE"] = pd.to_numeric(df["DISCOVERY_DATE"], errors="coerce")
            df["DISCOVERY_DATE_CONVERTED"] = pd.to_datetime(df["DISCOVERY_DATE"] - pd.Timestamp(0).to_julian_date(), unit="D")
            df["FIRE_YEAR"] = df["DISCOVERY_DATE_CONVERTED"].dt.year
            df["DISCOVERY_MONTH"] = df["DISCOVERY_DATE_CONVERTED"].dt.month
            # Log do tamanho do incêndio (adicionando 1 para evitar log(0))
            df["LOG_FIRE_SIZE"] = np.log(df["FIRE_SIZE"] + 1)
            # Criar variáveis dummy para categorias
            df = pd.get_dummies(df, columns=["NWCG_GENERAL_CAUSE", "STATE"], drop_first=True)
            return df
        except Exception as e:
            st.error(f"Erro ao processar o arquivo CSV para regressão: {e}")
            return None
    else:
        st.error(f"Erro: Arquivo de dados não encontrado em {file_path}")
        return None

# Caminho para o arquivo de dados
data_path = "data/wildfires.csv"

# Carrega os dados
df_reg = load_data(data_path)

if df_reg is not None:
    st.subheader("Resultados da Regressão Linear Múltipla (OLS)")
    
    # Selecionar variáveis preditoras e a variável dependente
    # Nota: Esta é uma seleção simplificada. Uma análise real exigiria seleção cuidadosa de variáveis.
    predictor_cols = [col for col in df_reg.columns if col.startswith("STAT_CAUSE_DESCR_") or col.startswith("STATE_")]
    # Adicionar outras variáveis numéricas se relevante (ex: FIRE_YEAR, DISCOVERY_MONTH)
    # predictor_cols.extend(["FIRE_YEAR", "DISCOVERY_MONTH"])
    
    # Verificar se há colunas preditoras suficientes
    if not predictor_cols:
        st.warning("Não foi possível encontrar colunas preditoras suficientes após a criação de dummies.")
    else:
        X = df_reg[predictor_cols]
        y = df_reg["LOG_FIRE_SIZE"]
        
        # Adicionar uma constante ao modelo (intercepto)
        X = sm.add_constant(X)
        X = X.astype(float)
        y = y.astype(float)
        
        try:
            # Ajustar o modelo OLS
            model = sm.OLS(y, X, missing="drop") # Remover linhas com NaNs nas variáveis usadas
            results = model.fit()
            
            st.text("Sumário do Modelo de Regressão:")
            st.text(results.summary())
            
            st.markdown("**Interpretação:**")
            st.write("""
            - **R-squared (R²)**: Indica a proporção da variância na variável dependente (log do tamanho do incêndio) que é explicada pelas variáveis independentes incluídas no modelo.
            - **Coeficientes (coef)**: Mostram a mudança esperada no logaritmo do tamanho do incêndio para uma mudança de uma unidade na variável preditora, mantendo as outras constantes. Para variáveis dummy (causas, estados), o coeficiente representa a diferença média em relação à categoria de referência.
            - **P>|t|**: Valor-p associado ao teste t para cada coeficiente. Valores menores que 0.05 geralmente indicam que o coeficiente é estatisticamente significativo.
            """)
            
            # Visualização dos Coeficientes (Top N maiores e menores)
            st.subheader("Principais Coeficientes Significativos (P < 0.05)")
            params = results.params.drop("const") # Excluir intercepto
            p_values = results.pvalues.drop("const")
            significant_params = params[p_values < 0.05]
            
            if not significant_params.empty:
                # Ordenar por valor absoluto para pegar os mais influentes
                significant_params_sorted = significant_params.abs().sort_values(ascending=False).head(20)
                top_params = params.loc[significant_params_sorted.index].sort_values()

                fig_coeffs = px.bar(top_params, x=top_params.index, y=top_params.values,
                                    title="Top 20 Coeficientes Significativos (Positivos e Negativos)",
                                    labels={"index": "Variável Preditora", "y": "Coeficiente"})
                fig_coeffs.update_layout(xaxis_title="Variável Preditora", yaxis_title="Coeficiente (Impacto no Log do Tamanho)")
                st.plotly_chart(fig_coeffs, use_container_width=True)
                st.write("Variáveis com coeficientes positivos estão associadas a incêndios maiores, enquanto coeficientes negativos estão associados a incêndios menores, em relação à categoria de referência.")
            else:
                st.write("Nenhum coeficiente foi considerado estatisticamente significativo (P < 0.05) neste modelo simplificado.")

        except Exception as e:
            st.error(f"Ocorreu um erro durante a análise de regressão: {e}")
            st.warning("Pode ser necessário ajustar a seleção de variáveis ou tratar dados ausentes/infinitos.")

else:
    st.warning("Não foi possível carregar os dados para realizar a análise de regressão. Verifique a página 'Visão Geral'.")

