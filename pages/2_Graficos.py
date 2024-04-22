import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import webbrowser  # Import needed to use webbrowser for opening URLs
import plotly.express as px



# Define functions to load data
def load_duration_data():
    return pd.read_csv("duration_data.csv")

def load_proj1_data():
    return pd.read_csv("proj1_data.csv")

def load_uproj_data():
    return pd.read_csv("uproj_data.csv")

def load_unidos_data():
    return pd.read_csv("unidos_data.csv")

# Set Streamlit page config
st.set_page_config(
    layout="wide",
    page_title="Eficiência Energética Labdados"
)

# Ensure session state initialization
if 'Duration_Years' not in st.session_state:
    st.session_state['Duration_Years'] = load_duration_data()

if 'df_proj' not in st.session_state:
    st.session_state['df_proj'] = load_proj1_data()

if 'df_uproj' not in st.session_state:
    st.session_state['df_uproj'] = load_uproj_data()

if 'df_unidos' not in st.session_state:
    st.session_state['df_unidos'] = load_unidos_data()

# Use horizontal lines for separation
st.markdown("---")  

# Access data from session state
df_unidos_ = st.session_state["df_unidos"]
col1, col2, col3 = st.columns(3)

st.markdown("---")  # Markdown syntax for a horizontal line

######
# Card displays

# Calculate the mean 'Score' for each group
df_mean = df_unidos_.groupby(['NomAgente', 'DscTipologia'], as_index=False)['Score'].mean()

# Rename the 'Score' column to 'MeanScore'
df_mean.rename(columns={'Score': 'MeanScore'}, inplace=True)

# Merge the mean scores back into the original DataFrame
df_merged = pd.merge(df_unidos_, df_mean, on=['NomAgente', 'DscTipologia'])

# Get the index of the row with the maximum 'MeanScore' in each group
idx = df_merged.groupby(['NomAgente', 'DscTipologia'])['MeanScore'].idxmax()

# Use the idx to get the rows with the maximum 'MeanScore' in each group
df_max_mean_score = df_merged.loc[idx]

# Get the row with the maximum 'MeanScore'
max_score_row = df_max_mean_score.loc[df_max_mean_score['MeanScore'].idxmax()]

# Get 'NomAgente', 'DscTipologia', and 'MeanScore' from the row
nom_agente = max_score_row['NomAgente']
dsc_tipologia = max_score_row['DscTipologia']
max_score = max_score_row['MeanScore']

# Check if max_score is NaN
if pd.isna(max_score):
    max_score_display = 'NaN'
else:
    max_score_display = round(max_score, 2)

# Display 'NomAgente', 'DscTipologia', and the maximum 'MeanScore'
col1.markdown("**Projeto com melhor Score médio na dimensão**<br/>**Agente/Empresa e Tipo de Projeto:**", unsafe_allow_html=True)
col1.metric(label="", value=max_score_display)
col2.markdown(f'**Empresa:** {nom_agente}')
col3.markdown(f'**Tipo de Projeto:** {dsc_tipologia}')

######
# Primeiro gráfico: Score médio por Empresa

# Group by 'NomAgente' and calculate the mean 'Score'
df_grouped = df_unidos_.groupby('NomAgente')['Score'].mean().reset_index()

# Sort the DataFrame based on 'Score' column in descending order
df_grouped_sorted = df_grouped.sort_values('Score', ascending=False)

# Create a bar chart with Plotly
fig = px.bar(df_grouped_sorted, x='NomAgente', y='Score', color='Score',
             color_continuous_scale='Blues', labels={'NomAgente':'Empresa', 'Score':'Score'})

# Update x-axis labels and layout
fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
fig.update_layout(title='Score médio por Empresa', autosize=False, width=1000)

# Display the plot in Streamlit
st.plotly_chart(fig)

st.markdown("---")  # Markdown syntax for a horizontal line

######
# Segundo gráfico: Score médio por Tipo de Projeto

# Group by 'DscTipologia' and calculate the mean 'Score'
df_grouped1 = df_unidos_.groupby('DscTipologia')['Score'].mean().reset_index()

# Sort the DataFrame based on 'Score' column in descending order
df_grouped1_sorted = df_grouped1.sort_values('Score', ascending=False)

# Create a bar chart with Plotly
fig1 = px.bar(df_grouped1_sorted, x='DscTipologia', y='Score', color='Score',
              color_continuous_scale='Blues', labels={'DscTipologia':'Tipo de Projeto', 'Score':'Score'})

# Update x-axis labels and layout


# Update x-axis labels and layout
fig1.update_xaxes(tickangle=45, tickfont=dict(size=10))
fig1.update_layout(title='Score médio por tipo de projeto', autosize=False, width=1000)

# Display the plot in Streamlit
st.plotly_chart(fig1)

st.markdown("---")  # Markdown syntax for a horizontal line

######
# Análise agregada de custos e scores

df_aggregated = df_unidos_.groupby(['NomAgente', 'DscTipologia'], as_index=False).agg({'Score': 'mean', 'VlrCustoTotal': 'mean'})
df_ranked = df_aggregated.sort_values('VlrCustoTotal', ascending=False)

# Agora ao adicionar ranks, 'NomAgente' e 'DscTipologia' ainda serão parte do DataFrame
df_ranked['Rank_CustosProj'] = df_ranked['VlrCustoTotal'].rank(method='min', ascending=False)
df_ranked = df_ranked.sort_values('Score', ascending=False)
df_ranked['Rank_Score'] = df_ranked['Score'].rank(method='min', ascending=False)
df_ranked.reset_index(drop=True, inplace=True)


# Add a new column 'PointSize' to the DataFrame with a constant value
df_ranked['PointSize'] = 3

# Scatterplot: Score vs Valor Custo Total por Agente/Empresa e DscTipologia
fig2 = px.scatter(df_ranked, 
                  x='Score', 
                  y='VlrCustoTotal', 
                  color='Score', 
                  size='PointSize',  # Use the new column for the point size
                  hover_data=['NomAgente', 'DscTipologia'], 
                  color_continuous_scale='Earth')

fig2.update_layout(
    title='Score médio vs Valor Custo médio por Agente/Empresa e Tipologia de Projeto',
    xaxis_title='Score',
    yaxis_title='VlrCustoTotal',
    legend_title='NomAgente e DscTipologia',
    plot_bgcolor='rgba(245,245,245,1)'  # Configura a cor de fundo para cinza claro
)

# Display the plot in Streamlit
st.plotly_chart(fig2)
