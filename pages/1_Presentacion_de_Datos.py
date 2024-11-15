import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Presentación de Datos")

df = pd.read_csv('datos_coches.csv')

marca = st.sidebar.multiselect('Selecciona Marca', df['marca'].unique())
modelo = st.sidebar.multiselect('Selecciona Modelo', df['modelo'].unique())

if marca:
    df = df[df['marca'].isin(marca)]
if modelo:
    df = df[df['modelo'].isin(modelo)]

st.map(df[['latitud', 'longitud']])

fig = px.histogram(df, x='precio', nbins=50)
st.plotly_chart(fig)