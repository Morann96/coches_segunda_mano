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

# Personalizar diseño del gráfico y tooltip
fig.update_traces(
    marker=dict(size=10),
    hovertemplate=
        '<b>Kilometraje</b>: %{x:,}<br>' +  # Formato con separador de miles
        '<b>Precio contado</b>: %{y:,}€<br>' +  # Formato con separador de miles
        '<extra></extra>'
)

fig.update_layout(
    height=800,  # Altura del gráfico
    font=dict(size=18),  # Tamaño del texto general
    title_font=dict(size=24),  # Tamaño del título
    coloraxis_colorbar=dict(title="Año de Matriculación") 
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Relación entre kilometraje y precio al contado según el año de matriculación

Este gráfico de dispersión representa la relación entre el kilometraje de los coches y su precio al contado, categorizados según el año de matriculación.

#### Detalles del gráfico:
- **Eje X (Kilometraje)**: Representa la distancia recorrida por el coche en kilómetros (km). A mayor kilometraje, el vehículo ha sido más usado.
- **Eje Y (Precio contado)**: Indica el precio al contado del coche en euros (€), representado en escala logarítmica para mostrar tanto precios bajos como altos.
- **Colores**: Los puntos están coloreados de acuerdo con el año de matriculación del coche:
  - **Colores más claros (amarillo)**: Representan coches matriculados más recientemente (2020 o después).
  - **Colores más oscuros (morado)**: Representan coches matriculados hace más tiempo (2000 o antes).

#### Observaciones clave:
1. **Tendencia general**:
   - Existe una relación inversa entre el kilometraje y el precio: a mayor kilometraje, el precio suele ser más bajo. Esto es consistente con la depreciación del valor de los coches a medida que aumenta su uso.

2. **Año de matriculación**:
   - Los coches más nuevos (años recientes) tienden a tener precios más altos y menor kilometraje, lo que indica que son menos usados.
   - Los coches más antiguos (años anteriores) suelen tener kilometrajes más elevados y precios más bajos.

3. **Valores atípicos**:
   - Algunos coches tienen precios elevados incluso con kilometrajes altos, lo que podría indicar que pertenecen a marcas de lujo o son modelos exclusivos.

4. **Agrupaciones notables**:
   - Se observa una alta concentración de coches con kilometrajes bajos y precios moderados, probablemente correspondientes a coches seminuevos o de reciente matriculación.

#### Uso del gráfico:
Este gráfico permite:
- Analizar cómo el uso (kilometraje) afecta el precio de los coches.
- Identificar patrones de precio según el año de matriculación.
- Ayudar a los compradores a evaluar coches según su uso y edad.

**Nota**: La escala logarítmica en el eje Y facilita la visualización de una amplia gama de precios al contado.

""")


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

# Personalizar diseño y formato del tooltip
fig.update_traces(
    hovertemplate=
        '<b>Distintivo Ambiental</b>: %{x}<br>' +
        '<b>Precio contado</b>: %{y:,.2f} €<br>' +  # Formato con separador de miles y símbolo €
        '<b>Máximo</b>: %{hoverinfo.max}<br>' +
        '<b>Mínimo</b>: %{hoverinfo.min}<br>' +
        '<b>Mediana</b>: %{hoverinfo.median}<br>' +
        '<extra></extra>'
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

st.markdown("""
### Distribución del precio por distintivo ambiental

Este gráfico de caja y bigotes (boxplot) muestra la distribución del precio al contado de los coches según su distintivo ambiental.

#### Detalles del gráfico:
- **Eje X (Distintivo ambiental)**: Representa las diferentes categorías de distintivo ambiental otorgadas a los coches:
  - **C**: Vehículos modernos de gasolina o diésel con bajas emisiones.
  - **B**: Vehículos algo más antiguos con un nivel de emisiones mayor que los de categoría C.
  - **ECO**: Vehículos híbridos o de bajas emisiones.
  - **0 EMISIONES**: Vehículos completamente eléctricos o de hidrógeno, con cero emisiones.

- **Eje Y (Precio contado)**: Muestra el precio al contado de los coches en euros (€), representado en escala logarítmica para incluir tanto precios bajos como altos de manera proporcional.

- **Colores**: Cada distintivo ambiental tiene un color diferente para facilitar la comparación.

#### Observaciones clave:
1. **Coches con distintivo 0 EMISIONES**:
   - Tienen una mayor dispersión de precios, pero su mediana se encuentra por encima de las demás categorías, reflejando que son, en promedio, los más caros.

2. **Coches con distintivo ECO**:
   - Presentan precios intermedios entre los coches con distintivo C y 0 EMISIONES.
   - Tienen una distribución amplia, lo que indica la presencia de vehículos tanto accesibles como de gama alta.

3. **Coches con distintivo C y B**:
   - Los coches con distintivo C tienen precios más altos que los de distintivo B, lo que refleja la modernidad de los vehículos.
   - Los coches con distintivo B suelen ser los más asequibles, con una mediana de precio notablemente más baja.

4. **Valores atípicos (outliers)**:
   - En todas las categorías, especialmente en las de mayor precio, se observan valores atípicos (puntos fuera de los bigotes), que representan coches de precio significativamente superior al resto.

#### Uso del gráfico:
Este gráfico permite:
- Comparar los precios medios y rangos entre distintas categorías de distintivo ambiental.
- Identificar patrones de precios en función de las emisiones y tecnologías asociadas.
- Ayudar a compradores a decidir qué categoría de coche se adapta mejor a su presupuesto.

**Nota**: La escala logarítmica en el eje Y permite visualizar tanto precios bajos como altos sin que los extremos dominen el gráfico.

""")



st.markdown("---")

precio_medio = (
    df.groupby("marca")[["precio_nuevo", "precio_contado"]]
    .mean()
    .sort_values(by="precio_contado", ascending=False)
)

#st.title("Comparación del Precio Nuevo y Precio Contado por Marca")


fig = go.Figure()

# Agregar barras para 'precio_nuevo'
fig.add_trace(go.Bar(
    x=precio_medio.index,  # Marcas
    y=precio_medio["precio_nuevo"],  # Precio nuevo promedio
    name="Precio Nuevo",
    marker_color="blue",  # Color de las barras
    hovertemplate=
        '<b>Marca</b>: %{x}<br>' +
        '<b>Precio Nuevo</b>: %{y:,.2f} €<br>' +  # Formato con separadores de miles y símbolo €
        '<extra></extra>'
))

# Agregar barras para 'precio_contado'
fig.add_trace(go.Bar(
    x=precio_medio.index,  # Marcas
    y=precio_medio["precio_contado"],  # Precio contado promedio
    name="Precio Contado",
    marker_color="orange",  # Color de las barras
    hovertemplate=
        '<b>Marca</b>: %{x}<br>' +
        '<b>Precio Contado</b>: %{y:,.2f} €<br>' +  # Formato con separadores de miles y símbolo €
        '<extra></extra>'
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

st.markdown("""
### Precio coche nuevo vs precio coche de segunda mano por marca

Este gráfico de barras compara el precio medio de coches nuevos frente al precio medio de coches de segunda mano, categorizados por marca.

#### Detalles del gráfico:
- **Eje X (Marca)**: Muestra las diferentes marcas de coches disponibles en el mercado.
- **Eje Y (Precio Medio)**: Representa el precio medio de los coches en euros (€).
- **Barras Azules**: Indican el precio medio de coches nuevos para cada marca.
- **Barras Naranjas**: Indican el precio medio de coches de segunda mano (precio al contado) para cada marca.

#### Observaciones clave:
1. **Diferencias de precios**:
   - Las marcas de lujo como **Aston Martin**, **Ferrari** y **Lamborghini** tienen una diferencia significativa entre el precio de coches nuevos y de segunda mano, siendo el precio nuevo considerablemente mayor.
   - Marcas más accesibles, como **Dacia**, **Fiat** y **Citroën**, muestran diferencias más pequeñas entre los precios.

2. **Patrón general**:
   - En todas las marcas, el precio medio de los coches nuevos es mayor que el de los coches de segunda mano, lo que refleja la depreciación habitual de los vehículos al pasar a ser usados.
   - Las marcas de alta gama presentan precios mucho más altos en comparación con marcas generalistas.

3. **Comparación entre marcas**:
   - **Tesla** destaca con precios más elevados para coches nuevos en comparación con marcas generalistas, pero con una diferencia más reducida entre el precio nuevo y de segunda mano.
   - Marcas como **Mercedes-Benz** y **BMW** tienen precios nuevos más altos en comparación con el precio al contado de los coches usados.

#### Uso del gráfico:
Este gráfico es útil para:
- Analizar cómo varía el precio medio de coches nuevos frente al de segunda mano según la marca.
- Identificar marcas con menor depreciación en el precio.
- Ayudar a compradores y vendedores a entender las diferencias de valor entre coches nuevos y usados.

**Nota**: La escala de precios está en euros (€), y cada barra representa el precio promedio para esa categoría.

""")



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

# Personalizar el tamaño de los puntos y el formato del tooltip
fig.update_traces(
    marker=dict(size=15),
    hovertemplate=
        '<b>Potencia (cv)</b>: %{x:,}<br>' +  # Potencia con separadores de miles
        '<b>Precio contado</b>: %{y:,.2f} €<br>' +  # Precio con formato y símbolo €
        '<b>Combustible</b>: %{marker.color}<br>' +  # Tipo de combustible
        '<extra></extra>'
)

# Personalizar diseño
fig.update_layout(
    height=800,
    font=dict(size=18),
    title_font=dict(size=24),
    legend_title_font=dict(size=20),
    coloraxis_colorbar=dict(title="Tipo de Combustible")
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Relación entre precio y potencia según el combustible

Este gráfico de dispersión muestra cómo se relacionan el precio de los coches y su potencia (en caballos de fuerza, CV), categorizados según el tipo de combustible que utilizan.

#### Detalles del gráfico:
- **Eje X (Potencia)**: Representa la potencia del coche en caballos (CV). A medida que aumenta la potencia, se observan coches de mayor precio.
- **Eje Y (Precio)**: Muestra el precio de los coches en escala logarítmica, lo que permite visualizar tanto coches con precios bajos como altos en una misma escala.
- **Colores**: Cada punto está coloreado de acuerdo con el tipo de combustible del coche:
  - **Gasolina**: Naranja
  - **Diésel**: Verde
  - **Gasolina/Gas**: Azul
  - **Eléctrico**: Rosa
  - **Híbrido Enchufable**: Amarillo
  - **Gas**: Naranja

#### Observaciones clave:
1. **Tendencia general**:
   - A mayor potencia, el precio tiende a aumentar, lo que sugiere una correlación positiva entre estas variables.
   
2. **Distribución por combustible**:
   - Los coches **eléctricos** y **híbridos enchufables** suelen estar en el rango de precios más altos, incluso con potencias moderadas.
   - Los coches **de gasolina** y **diésel** abarcan un rango más amplio de precios y potencias.
   - Los coches **de gas** están principalmente en el rango de potencias y precios más bajos.

3. **Puntos notables**:
   - Existen algunos coches con alta potencia (más de 500 CV) y precios excepcionalmente altos.
   - La mayoría de los puntos están agrupados en potencias menores a 200 CV y precios menores a 100.000 €.

#### Uso del gráfico:
Este gráfico es útil para:
- Identificar tendencias en el mercado de coches según el tipo de combustible.
- Ayudar a los compradores a entender cómo varía el precio según la potencia y el combustible.
- Explorar diferencias entre tecnologías como eléctricos, híbridos y combustibles tradicionales.

**Nota**: Al pasar el cursor sobre un punto, se puede ver el precio exacto, la potencia y el tipo de combustible del coche correspondiente.            

""")


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

# Personalizar el tooltip
fig.update_traces(
    hovertemplate=
        '<b>Provincia</b>: %{location}<br>' +  # Mostrar el nombre de la provincia
        '<b>Cantidad</b>: %{customdata[0]:,}<br>' +  # Valor con separadores de miles SIN LOGARITMO
        '<extra></extra>',
    customdata=np.expand_dims(mapa_provincias['cantidad'], axis=1)  # Añadir la cantidad original al tooltip
)

# Ajustar diseño del gráfico
fig.update_layout(
    height=700,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    coloraxis_colorbar={"title": "Cantidad de coches (Log)"}
)

# Mostrar el mapa en Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Mapa Coroplético: Precio Medio de Coches por Provincia

Este mapa muestra la cantidad de coches en cada provincia de España. 

- **Color más intenso** indica **mayor cantidad de coches**.
- Las provincias con **color más claro** tienen menor cantidad de coches.
- Al pasar el cursor sobre una provincia, se puede observar la **cantidad exacta de coches**.

Apreciamos que las provincias más pobladas son las que más coches tienen. Sobresalen Madrid y Barcelona.            

""")




st.markdown("---")

#st.title("Mapa Coroplético: Precio Medio de Coches por Provincia")

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

# Personalizar el tooltip
fig.update_traces(
    hovertemplate=
        '<b>Provincia</b>: %{location}<br>' +  # Mostrar el nombre de la provincia
        '<b>Precio medio</b>: %{z:,.2f}€<br>' +  # Precio medio con separadores de miles y símbolo €
        '<extra></extra>'
)

# Ajustar diseño del gráfico
fig.update_layout(
    height=700,  # Altura del gráfico
    margin={"r": 0, "t": 50, "l": 0, "b": 0},  # Márgenes
    coloraxis_colorbar={"title": "Precio Medio (€)"}  # Título de la barra de colores
)

# Mostrar el mapa en Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Mapa Coroplético: Precio Medio de Coches por Provincia

Este mapa muestra la distribución geográfica del precio medio de coches en cada provincia de España. 

- **Color más intenso** indica un **precio medio más alto**.
- Las provincias con **color más claro** tienen un precio medio más bajo.
- Al pasar el cursor sobre una provincia, se puede observar el **precio medio exacto en euros**.

La información está basada en el precio al contado promedio calculado a partir de los datos disponibles.

Sorprende que destaque Almería como provincia con coches más caros que el resto. No se aprecia ningún patrón.            

""")