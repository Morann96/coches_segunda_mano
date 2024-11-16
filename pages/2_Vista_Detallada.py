import streamlit as st
import pandas as pd

st.title("Vista Detallada")

# Carga de datos
df = pd.read_csv('datos_coches.csv')

# Opciones de filtrado adicionales
anio = st.sidebar.slider('Año de Fabricación', int(df['anio'].min()), int(df['anio'].max()))
kilometraje = st.sidebar.slider('Kilometraje', int(df['kilometraje'].min()), int(df['kilometraje'].max()))

# Aplicar filtros
df_filtered = df[(df['anio'] >= anio) & (df['kilometraje'] <= kilometraje)]

# Mostrar datos
st.dataframe(df_filtered)