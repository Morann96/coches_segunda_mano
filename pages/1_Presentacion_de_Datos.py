import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import folium
from streamlit_folium import st_folium
from folium import Choropleth, GeoJson
import geopandas as gpd


st.set_page_config(page_title="Análisis de Datos de Coches", layout="wide")

st.title("Análisis Visual de Coches de Segunda Mano")

st.markdown("""
A continuación, varios gráficos con información clave sobre los coches tratados en el proyecto.
""")

imagenes = {
    "Kilometraje vs Precio": {
        "ruta": "bin/imagenes/grafico_kilometraje_precio.png",
        "descripcion": """
        Este gráfico muestra la relación entre el kilometraje y el precio de los coches. 
        Podemos ver claramente cómo el precio desciende según aumenta el kilometraje.
        Hay que tener en cuenta que la bajada no es lineal ya que los datos de precio están en escala logarítmica.

        En menor mdedida también apreciamos que los coches más viejos son más baratos.
        """
    },
    "Precio por Tipo Distintivo": {
        "ruta": "bin/imagenes/grafico_precio_distintivo.png",
        "descripcion": """
        Aquí puedes observar cómo varían los precios según los distintivos de los coches, 
        destacando diferencias significativas entre categorías.
        """
    },
    "Distribución de Precios": {
        "ruta": "bin/imagenes/grafico_precio_nuevo_contado.png",
        "descripcion": """
        Un histograma que detalla la distribución de los precios de los coches, 
        mostrando picos interesantes en ciertos rangos.
        """
    },
    "Relación entre Potencia y Precio": {
        "ruta": "bin/imagenes/grafico_precio_potencia.png",
        "descripcion": """
        Este gráfico destaca cómo la potencia del coche afecta al precio. 
        Los coches con mayor potencia tienden a ser más costosos.
        """
    },

    "Mapa de Cantidades por Provincia": {
        "ruta": "bin/mapa_cantidad.png",
        "descripcion": """
        Este mapa muestra la cantidad de coches ofertados por provincia.

        Vemos claramente cómo Madrid y Barcelona son las provincisa con más coches ofertadas y el resto están muy distribuidas. 
        En León, Palencia, Segovia y Teruel se ofertan notoriamente menos coches que en el resto de provincias
        """
    },
        "Mapa de Precios por Provincia": {
        "ruta": "bin/mapa_precio.png",
        "descripcion": """
        Este mapa muestra el precio medio de coches ofertados por provincia.

        En este caso no se aprecia una diferencia significativa en general. 
        En Coruña y Alicante hay precios extraordinariamente altos que probablemente se deban a datos repetidos de coches muy caros.
        """
    },
}

for titulo, contenido in imagenes.items():
    st.header(titulo)
    st.image(Image.open(contenido["ruta"]), use_column_width=True)
    st.markdown(contenido["descripcion"])
    st.markdown("---")