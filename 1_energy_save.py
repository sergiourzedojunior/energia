import streamlit as st
import pandas as pd
import time
import webbrowser  # Import needed to use webbrowser for opening URLs

# Load data paths
# path = "D:\\OneDrive\\energia_lab\\data\\"
# path1 = "D:\\OneDrive\\energia_lab\\streamlit\\data_steamlit\\" 

# Set Streamlit page config
st.set_page_config(
    layout="wide",
    page_title="Eficiência Energética Labdados"
)

# Function to load data with caching
@st.cache_data
def load_duration_data():
    duration = pd.read_csv( "Duration_Years_projects_mean.csv")
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return duration

@st.cache_data
def load_proj1_data():
    
    df_proj = pd.read_csv( "projeto1.csv")
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return df_proj

@st.cache_data
def load_uproj_data():
    df_uproj = pd.read_csv( "termino_ultimo_proj.csv")
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return df_uproj

@st.cache_data
def load_unidos_data():
    df_unidos = pd.read_csv( "df_unidos.csv")
    time.sleep(5)  # Simulated delay to mimic a long loading process
    return df_unidos

# App main interface
st.markdown("# Eficiência Energética! ⚡")
st.sidebar.markdown("Desenvolvido por [SergioUrzedoJr_github](https://github.com/sergiourzedojunior/sergiourzedojunior.git)")

# Ensure session state initialization
if 'Duration_Years' not in st.session_state:
    st.session_state['Duration_Years'] = load_duration_data()

if 'df_proj' not in st.session_state:
    st.session_state['df_proj'] = load_proj1_data()

if 'df_uproj' not in st.session_state:
    st.session_state['df_uproj'] = load_uproj_data()

if 'df_unidos' not in st.session_state:
    st.session_state['df_unidos'] = load_unidos_data()

btn = st.button("Acesse os dados no dadosabertos - ANEEL")
if btn:
    webbrowser.open_new_tab("https://dadosabertos.aneel.gov.br/dataset/projetos-de-eficiencia-energetica")

st.markdown(
    """
O Programa de Eficiência Energética tem como objetivo promover o uso eficiente da energia elétrica em todos os setores da economia por meio de projetos que demonstrem a importância e a viabilidade econômica de melhoria da eficiência energética de equipamentos, processos e usos finais de energia. Busca-se maximizar os benefícios públicos da energia economizada e da demanda evitada, promovendo a transformação do mercado de eficiência energética, estimulando o desenvolvimento de novas tecnologias e a criação de hábitos e práticas racionais de uso da energia elétrica.

A tabela apresenta os valores investidos em programa de eficiência energética a partir da publicação da Resolução Normativa ANEEL nº 300/2008.

Para detalhamento de projetos específicos, acessar: https://siase.aneel.gov.br/WebOpee/

Resumo do arquivo: Armazena dados referentes aos Projetos, por distribuidora de energia elétrica, tipologia do projeto, demanda retirada da ponta, valor anual de energia economizada (GWh/ano) e o investimento no projeto.
"""
)

st.markdown("---")  # Markdown syntax for a horizontal line

df_duration_ = st.session_state["Duration_Years"]
df_proj_ = st.session_state["df_proj"]
df_uproj_ = st.session_state["df_uproj"]
col1, col2, col3, col4 = st.columns(4)

st.markdown("---")  # Markdown syntax for a horizontal line

#col1.markdown(f"**DURAÇÃO MÉDIA DOS PROJETOS:** {df_duration_['Duration_Years'].mean().round(2)}")
col1.metric(label="**duração média dos projetos em anos:**", value=df_duration_['Duration_Years'].mean().round(2))
col2.metric(label="**data início do primeiro projeto resgistrado:**", value=df_proj_['DatInicioProjeto'].max())
col3.metric(label="**data do último projeto finalizado:**", value=df_uproj_['DatConclusaoProjeto'].max())


st.markdown("""
Para facilitar a interpretação dos dados foi criado o KPI "Score" que representa os projetos em relação a sua de eficiência energética.

Quanto maior o valor do "Score", melhor o projeto em relação a eficiência energética. Range 1 a 10.

A pontuação é calculada usando a seguinte fórmula onde VlrCustoTotal é sempre diferente de zero (retirados da base projetos com custo zero):

$$
\\text{Score} = \\frac{\\text{VlrEnergiaEconomizadaTotal} + \\text{VlrRetiradaDemandaPontaTotal}}{\\text{VlrCustoTotal} + \\epsilon}
$$

Onde:
- $\text{VlrEnergiaEconomizadaTotal}$ é o valor total de energia economizada,
- $\text{VlrRetiradaDemandaPontaTotal}$ é o valor total da retirada de demanda de pico,
- $\text{VlrCustoTotal}$ é o custo total, e
- $\epsilon$ é uma pequena constante para prevenir a divisão por zero.
""")


