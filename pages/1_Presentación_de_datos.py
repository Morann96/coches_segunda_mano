import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import folium
from streamlit_folium import st_folium
from folium import Choropleth, GeoJson
import geopandas as gpd
import plotly.graph_objects as go
import numpy as np


# Función para conectar a la base de datos
def conectar_base_datos():
    conn = st.connection('mysql', type='sql')
    return conn

# Función para extraer y mostrar datos
def mostrar_datos(tabla):
    conn = conectar_base_datos()
    query = f"SELECT * FROM {tabla}"
    conn.query(query)  # Consulta SQL
    df = conn.query(query)  # Extraer datos como DataFrame
    return df

df = mostrar_datos("vista_prestaciones")

st.title("Análisis Visual de Coches de Segunda Mano")



st.markdown("---")

#st.markdown("""### Relación entre kilometraje y precio al contado según el año de matriculación""")

# Crear gráfico con Plotly
fig = px.scatter(
    df,
    x="kilometraje",
    y="precio_contado",
    color="ano_matriculacion",
    color_continuous_scale="Viridis",
    opacity=0.6,  # Puntos traslúcidos
    labels={
        "kilometraje": "Kilometraje",
        "precio_contado": "Precio contado",
        "ano_matriculacion": "Año de matriculación"
    },
    title="Relación entre kilometraje y precio al contado según el año de matriculación",
    log_y=True
)

# Personalizar diseño del gráfico
fig.update_traces(marker=dict(size=10))
fig.update_layout(
    height=800,  # Altura del gráfico
    font=dict(size=18),  # Tamaño del texto general
    title_font=dict(size=24),  # Tamaño del título
    coloraxis_colorbar=dict(title="Año de Matriculación") 
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)



st.markdown("---")

#st.title("Distribución del Precio Contado por Distintivo Ambiental")

# Crear gráfico con Plotly
fig = px.box(
    df,
    x="distintivo_ambiental",
    y="precio_contado",
    color="distintivo_ambiental",
    labels={
        "distintivo_ambiental": "Distintivo ambiental",
        "precio_contado": "Precio Contado"
    },
    title="Distribución del precio por distintivo ambiental",
    log_y=True,  # Escala logarítmica en el eje Y
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Personalizar diseño
fig.update_layout(
    height=800,
    font=dict(size=20),
    title_font=dict(size=26),
    xaxis_title="Distintivo ambiental",
    yaxis_title="Precio contado",
    xaxis=dict(tickfont=dict(size=18)),
    yaxis=dict(tickfont=dict(size=18))
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)





st.markdown("---")

precio_medio = (
    df.groupby("marca")[["precio_nuevo", "precio_contado"]]
    .mean()
    .sort_values(by="precio_contado", ascending=False)
)

# Configuración de Streamlit
#st.title("Comparación del Precio Nuevo y Precio Contado por Marca")

# Crear gráfico de barras con Plotly
fig = go.Figure()

# Agregar barras para 'precio_nuevo'
fig.add_trace(go.Bar(
    x=precio_medio.index,  # Marcas
    y=precio_medio["precio_nuevo"],  # Precio nuevo promedio
    name="Precio Nuevo",
    marker_color="blue"  # Color de las barras
))

# Agregar barras para 'precio_contado'
fig.add_trace(go.Bar(
    x=precio_medio.index,  # Marcas
    y=precio_medio["precio_contado"],  # Precio contado promedio
    name="Precio Contado",
    marker_color="orange"  # Color de las barras
))

# Personalizar diseño
fig.update_layout(
    title="Precio coche nuevo vs precio coche segunda mano por marca",
    xaxis_title="Marca",
    yaxis_title="Precio Medio",
    barmode="group",  # Barras agrupadas
    height=800,  # Altura del gráfico
    font=dict(size=18),  # Tamaño del texto general
    title_font=dict(size=24),  # Tamaño del título
    xaxis=dict(tickangle=45, tickfont=dict(size=12)),  # Etiquetas del eje X inclinadas
    yaxis=dict(tickfont=dict(size=12)),  # Etiquetas del eje Y
    legend_title=dict(font=dict(size=16))  # Tamaño del texto de la leyenda
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)





st.markdown("---")

#st.title("Relación entre Precio y Potencia por Tipo de Combustible")

# Paleta de colores personalizada con colores vivos
colores_vivos = [
    "#FF5733",  # Rojo
    "#33FF57",  # Verde
    "#3357FF",  # Azul
    "#FF33A1",  # Rosa
    "#FFC733",  # Amarillo
    "#33FFF6"   # Turquesa
]

# Crear gráfico con Plotly
fig = px.scatter(
    df,
    x="potencia_cv",
    y="precio_contado",
    color="combustible",
    color_discrete_sequence=colores_vivos,
    opacity=0.6,
    labels={"potencia_cv": "Potencia (cv)", "precio_contado": "Precio"},
    title="Relación entre precio y potencia según el combustible",
    log_y=True
)

# Personalizar tamaño de los puntos y diseño
fig.update_traces(marker=dict(size=15))
fig.update_layout(
    height=800,
    font=dict(size=18),
    title_font=dict(size=24),
    legend_title_font=dict(size=20),
    coloraxis_colorbar=dict(title="Tipo de Combustible") 
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)




st.markdown("---")

#st.title("Mapa Coroplético: Distribución de Coches por Provincia")

# Cargar los datos geográficos
mapa_provincias = gpd.read_file('bin/limites provinciales/recintos_provinciales_inspire_peninbal_etrs89.shp')

# Crear el DataFrame con las cantidades de coches por provincia
coches_por_provincia = df['provincia'].value_counts().reset_index()
coches_por_provincia.columns = ['provincia', 'cantidad']

# Ajustar nombres de provincias en el GeoDataFrame
def extraer_segundo_nombre(provincia):
    if '/' in provincia:
        return provincia.split('/')[1].strip()
    return provincia

mapa_provincias['NAMEUNIT'] = mapa_provincias['NAMEUNIT'].apply(extraer_segundo_nombre)
mapa_provincias['NAMEUNIT'] = mapa_provincias['NAMEUNIT'].replace({
    'A Coruña': 'La Coruña',
    'Bizkaia': 'Vizcaya',
    'Ourense': 'Orense',
    'Illes Balears': 'Islas Baleares',
    'Gipuzkoa': 'Guipúzcoa'
})

# Unir datos con el GeoDataFrame
mapa_provincias = mapa_provincias.merge(
    coches_por_provincia, left_on='NAMEUNIT', right_on='provincia', how='left'
)

# Rellenar valores nulos con 0 y calcular escala logarítmica
mapa_provincias['cantidad'] = mapa_provincias['cantidad'].fillna(0).astype(int)
mapa_provincias['cantidad_log'] = np.log1p(mapa_provincias['cantidad'])

# Crear el mapa con Plotly
fig = px.choropleth_mapbox(
    mapa_provincias,
    geojson=mapa_provincias.__geo_interface__,
    locations="NAMEUNIT",
    featureidkey="properties.NAMEUNIT",
    color="cantidad_log",
    color_continuous_scale="Oranges",
    mapbox_style="carto-positron",
    zoom=5.5,
    center={"lat": 40.4168, "lon": -3.7038},
    labels={"cantidad_log": "Cantidad (Log)"},
    title="Distribución de coches por provincia"
)

# Ajustar diseño del gráfico
fig.update_layout(
    height=700,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    coloraxis_colorbar={"title": "Cantidad de coches (Log)"}
)

# Mostrar el mapa en Streamlit
st.plotly_chart(fig, use_container_width=True)





st.markdown("---")

#st.title("Mapa Coroplético: Precio Medio de Coches por Provincia")

# Cargar el GeoDataFrame con datos geográficos

# Crear el DataFrame con el precio medio por provincia
precio_medio_por_provincia = df.groupby('provincia')['precio_contado'].mean().reset_index()
precio_medio_por_provincia.columns = ['provincia', 'precio_medio']

# Crear un diccionario para asignar precios medios a las provincias
precio_medio_dict = precio_medio_por_provincia.set_index('provincia')['precio_medio'].to_dict()

# Añadir el precio medio al GeoDataFrame
mapa_provincias['precio_medio'] = mapa_provincias['NAMEUNIT'].map(precio_medio_dict).fillna(0).round(2)

# Crear el mapa con Plotly
fig = px.choropleth_mapbox(
    mapa_provincias,
    geojson=mapa_provincias.__geo_interface__,  # Usar las geometrías del GeoDataFrame
    locations="NAMEUNIT",  # Columna que relaciona los datos con las geometrías
    featureidkey="properties.NAMEUNIT",  # Clave del GeoJSON para las provincias
    color="precio_medio",  # Columna con los valores a visualizar
    color_continuous_scale="Oranges",  # Escala de colores
    mapbox_style="carto-positron",  # Estilo del mapa base
    zoom=5.5,  # Nivel de zoom inicial
    center={"lat": 40.4168, "lon": -3.7038},  # Centro del mapa en España
    labels={"precio_medio": "Precio medio (€)"},  # Etiquetas de la leyenda
    title="Precio medio de coches por provincia"
)

# Ajustar diseño del gráfico
fig.update_layout(
    height=700,  # Altura del gráfico
    margin={"r": 0, "t": 50, "l": 0, "b": 0},  # Márgenes
    coloraxis_colorbar={"title": "Precio Medio (€)"}  # Título de la barra de colores
)

# Mostrar el mapa en Streamlit
st.plotly_chart(fig, use_container_width=True)