import streamlit as st

st.set_page_config(page_title="Conclusões e Recomendações", page_icon="💡", layout="wide")

st.markdown("# Conclusões e Recomendações")
st.sidebar.header("Conclusões")
st.write("""
Com base nas análises realizadas nas seções anteriores, apresentamos as principais conclusões e algumas recomendações
para a gestão e prevenção de incêndios florestais.
""")

st.subheader("Principais Conclusões")

st.markdown("""
*   **Distribuição Assimétrica:** A grande maioria dos incêndios é pequena, mas poucos incêndios muito grandes são responsáveis pela maior parte da área queimada. Isso sugere a importância de conter incêndios rapidamente antes que se tornem grandes.
*   **Causas Humanas Dominantes:** Causas humanas, como detritos queimados (Debris Burning) e incêndios criminosos (Arson), são responsáveis por uma parcela significativa dos incêndios. Campanhas de conscientização e fiscalização são cruciais.
*   **Causas Naturais (Raio):** Embora menos frequentes, incêndios causados por raios (Lightning) tendem a ter um tamanho médio maior, possivelmente por ocorrerem em áreas mais remotas e de difícil acesso.
*   **Variação Geográfica:** A incidência de incêndios varia significativamente entre os estados, com alguns estados (como Califórnia, Geórgia, Texas) apresentando um número muito maior de ocorrências.
*   **Tendência Anual:** Observa-se uma variabilidade no número de incêndios e na área queimada ao longo dos anos, o que pode estar relacionado a fatores climáticos e de gestão.
*   **Sazonalidade Marcada:** Há um pico claro no número de incêndios durante os meses de verão (especialmente Julho e Agosto), coincidindo com condições mais quentes e secas em muitas regiões. O tamanho médio dos incêndios também tende a ser maior nesses meses.
*   **Fatores Influentes (Regressão):** A análise de regressão (embora simplificada aqui) sugere que tanto a causa do incêndio quanto a localização (estado) podem ter um impacto significativo no tamanho final do incêndio. Outros fatores não incluídos (como condições meteorológicas, topografia, tipo de vegetação específico) também são importantes.
""")

st.subheader("Recomendações")

st.markdown("""
1.  **Foco na Prevenção:** Intensificar campanhas de educação e conscientização sobre as principais causas humanas de incêndios (queima de detritos, fogueiras, cigarros) e aumentar a fiscalização em períodos de alto risco.
2.  **Resposta Rápida:** Priorizar a detecção precoce e a resposta rápida, especialmente para incêndios com potencial de crescimento rápido, para evitar que se tornem grandes desastres.
3.  **Alocação Estratégica de Recursos:** Direcionar recursos de combate e prevenção para as áreas e períodos de maior risco identificados na análise (estados com alta incidência, meses de pico sazonal).
4.  **Gestão Diferenciada por Causa:** Desenvolver estratégias específicas para lidar com diferentes causas. Por exemplo, monitoramento aprimorado de raios em áreas remotas e programas de prevenção focados em atividades humanas em áreas mais povoadas.
5.  **Monitoramento Contínuo e Análise Aprofundada:** Manter o monitoramento contínuo dos dados e realizar análises mais aprofundadas, incorporando variáveis adicionais (meteorologia, topografia, dados de vegetação) para refinar os modelos preditivos e as estratégias de gestão.
6.  **Adaptação às Mudanças Climáticas:** Considerar os potenciais impactos das mudanças climáticas nas tendências futuras de incêndios e adaptar as estratégias de longo prazo.
""")

st.info("Nota: Estas conclusões e recomendações são baseadas em dados simulados e uma análise exploratória. Uma gestão eficaz requer dados reais, modelos mais complexos e a colaboração entre diferentes agências e especialistas.")

