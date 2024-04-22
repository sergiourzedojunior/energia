import streamlit as st
import pandas as pd
import time
import webbrowser  # Import needed to use webbrowser for opening URLs


# Set Streamlit page config
st.set_page_config(
    layout="wide",
    page_title="Eficiência Energética Labdados"
)

# App main interface
st.markdown("# tabelas! ⚡")

# Ensure session state initialization
if 'Duration_Years' not in st.session_state:
    st.session_state['Duration_Years'] = load_duration_data()

if 'df_proj' not in st.session_state:
    st.session_state['df_proj'] = load_proj1_data()

if 'df_uproj' not in st.session_state:
    st.session_state['df_uproj'] = load_uproj_data()

if 'df_unidos' not in st.session_state:
    st.session_state['df_unidos'] = load_unidos_data()


st.markdown("---")  # Markdown syntax for a horizontal line



# Display data in the app
#st.session_state['df_unidos'] = st.session_state['df_unidos'].drop(columns=['Unnamed: 0'])
st.session_state['df_unidos'] = st.session_state['df_unidos']
st.write("tabela de dados - tratados", st.session_state['df_unidos'])





