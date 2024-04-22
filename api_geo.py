import pandas as pd
import numpy as np
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable


# Download and prepare the dataset
url = 'https://dadosabertos.aneel.gov.br/dataset/f9336ee6-7562-4c92-880a-d7217df6cc94/resource/28686698-544b-48e2-af58-ad4f7616246c/download/projetos-eficiencia-energetica-empresa.csv'
df = pd.read_csv(url, encoding='ISO-8859-1', sep=';', on_bad_lines='skip')

# Data cleaning and type conversion
df['DatGeracaoConjuntoDados'] = pd.to_datetime(df['DatGeracaoConjuntoDados'])
df['DatInicioProjeto'] = pd.to_datetime(df['DatInicioProjeto'])
df['DatConclusaoProjeto'] = pd.to_datetime(df['DatConclusaoProjeto'])
df.replace({',': '.'}, regex=True, inplace=True)  # Replace commas in numeric fields
numeric_fields = ['VlrRetiradaDemandaPontaTotal', 'VlrRcbGlobal', 'VlrEnergiaEconomizadaTotal', 'VlrCustoTotal']
df[numeric_fields] = df[numeric_fields].astype(float)
df = df[df['VlrCustoTotal'] != 0]  # Filter out rows with zero cost

# Calculating a score and filtering data
epsilon = 0.01
df['Score'] = (df['VlrEnergiaEconomizadaTotal'] + df['VlrRetiradaDemandaPontaTotal']) / (df['VlrCustoTotal'] + epsilon)
df = df.dropna(subset=['Score'])
df = df.sort_values('Score', ascending=False)
threshold_score = df['Score'].quantile(0.95)
df = df[df['Score'] > threshold_score]
df['Score'] = 1 + (df['Score'] - df['Score'].min()) * (10 - 1) / (df['Score'].max() - df['Score'].min())

# Geocoding locations using Nominatim
geolocator = Nominatim(user_agent="unique_user_agent", timeout=10)
def get_location(name):
    try:
        location = geolocator.geocode(name)
        return location.address if location else None, location.latitude if location else None, location.longitude if location else None
    except (GeocoderTimedOut, GeocoderUnavailable):
        time.sleep(5)
        return get_location(name)  # Retry

# Apply geocoding to unique agent names
unique_agents = df['NomAgente'].unique()
location_data = {name: get_location(name) for name in unique_agents}
df['Address'], df['Latitude'], df['Longitude'] = zip(*df['NomAgente'].map(location_data))

# Save updated DataFrame to a new CSV file
df.to_csv('df_unidos.csv', index=False)

# Analyze project durations
date_info = pd.read_csv('df_unidos.csv', usecols=['DatInicioProjeto', 'DatConclusaoProjeto'], parse_dates=['DatInicioProjeto', 'DatConclusaoProjeto'])
date_info['Duration_Years'] = (date_info['DatConclusaoProjeto'] - date_info['DatInicioProjeto']).dt.days / 365.25
duration_years_mean = date_info['Duration_Years'].mean()

# Save summary data to CSV files
pd.DataFrame([date_info['DatInicioProjeto'].min()], columns=['DatInicioProjeto']).to_csv('projeto1.csv', index=False)
pd.DataFrame([date_info['DatConclusaoProjeto'].max()], columns=['DatConclusaoProjeto']).to_csv('termino_ultimo_proj.csv', index=False)
pd.DataFrame([duration_years_mean], columns=['Duration_Years']).to_csv('Duration_Years_projects_mean.csv', index=False)


##### 