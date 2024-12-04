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

texts = {
    "en": {
        "analysis_title": "Visual Analysis of Second Hand Cars",
        "separator": "---",
        "scatter_plot_title": "Relationship between Mileage and Cash Price by Year of Registration",
        "scatter_plot_labels": {
            "kilometraje": "Mileage (km)",
            "precio_contado": "Cash Price (€)",
            "ano_matriculacion": "Year of Registration"
        },
        "scatter_plot_hovertemplate": '<b>Mileage (km)</b>: %{x:,}<br>' + \
                                       '<b>Cash Price (€)</b>: %{y:,}€<br>' + \
                                       '<b>Year</b>: %{customdata[0]}<br>' + \
                                       '<extra></extra>',
        "scatter_plot_colorbar_title": "Year of Registration",
        "scatter_plot_description": """
### Relationship between Mileage and Cash Price by Year of Registration

This scatter plot represents the relationship between the mileage of cars and their cash price, categorized by the year of registration.

#### Chart Details:
- **X-Axis (Mileage)**: Represents the distance traveled by the car in kilometers (km). Higher mileage indicates more usage.
- **Y-Axis (Cash Price)**: Indicates the cash price of the car in euros (€), displayed on a logarithmic scale to show both low and high prices.
- **Colors**: Points are colored according to the year of registration:
  - **Lighter colors (yellow)**: Represent cars registered more recently (2020 or later).
  - **Darker colors (purple)**: Represent cars registered earlier (2000 or before).

#### Key Observations:
1. **General Trend**:
   - There is an inverse relationship between mileage and price: higher mileage typically results in a lower price, consistent with vehicle depreciation over usage.

2. **Year of Registration**:
   - Newer cars tend to have higher prices and lower mileage, indicating they are less used.
   - Older cars usually have higher mileage and lower prices.

3. **Outliers**:
   - Some cars have high prices despite high mileage, possibly indicating luxury brands or exclusive models.

4. **Notable Clusters**:
   - A high concentration of cars with low mileage and moderate prices, likely corresponding to nearly new or recently registered cars.

#### Chart Usage:
This chart allows you to:
- Analyze how usage (mileage) affects car prices.
- Identify price patterns based on the year of registration.
- Assist buyers in evaluating cars based on their usage and age.

**Note**: The logarithmic scale on the Y-axis facilitates the visualization of a wide range of cash prices.
""",
        "box_plot_title": "Price Distribution by Environmental Label",
        "box_plot_labels": {
            "distintivo_ambiental": "Environmental Label",
            "precio_contado": "Cash Price (€)"
        },
        "box_plot_hovertemplate": '<b>Environmental Label</b>: %{x}<br>' + \
                                    '<b>Cash Price (€)</b>: %{y:,.2f} €<br>' + \
                                    '<b>Maximum</b>: %{hoverinfo.max}<br>' + \
                                    '<b>Minimum</b>: %{hoverinfo.min}<br>' + \
                                    '<b>Median</b>: %{hoverinfo.median}<br>' + \
                                    '<extra></extra>',
        "box_plot_xaxis_title": "Environmental Label",
        "box_plot_yaxis_title": "Cash Price (€)",
        "box_plot_description": """
### Price Distribution by Environmental Label

This box plot displays the distribution of cash prices for cars based on their environmental labels.

#### Chart Details:
- **X-Axis (Environmental Label)**: Represents different categories of environmental labels assigned to cars:
  - **C**: Modern gasoline or diesel vehicles with low emissions.
  - **B**: Slightly older vehicles with higher emissions than category C.
  - **ECO**: Hybrid or low-emission vehicles.
  - **0 EMISSIONS**: Fully electric or hydrogen vehicles with zero emissions.

- **Y-Axis (Cash Price)**: Shows the cash price of cars in euros (€), displayed on a logarithmic scale to include both low and high prices proportionally.

- **Colors**: Each environmental label has a different color for easy comparison.

#### Key Observations:
1. **Cars with 0 EMISSIONS Label**:
   - Exhibit a wider price range, but their median is above other categories, reflecting that they are, on average, the most expensive.

2. **ECO Label Cars**:
   - Show intermediate prices between C and 0 EMISSIONS categories.
   - Have a wide distribution, indicating the presence of both affordable and high-end vehicles.

3. **C and B Label Cars**:
   - C label cars have higher prices than B label cars, reflecting the modernity of the vehicles.
   - B label cars are generally more affordable, with a notably lower price median.

4. **Outliers**:
   - Across all categories, especially in higher-priced segments, there are outliers (points outside the whiskers), representing cars with significantly higher prices.

#### Chart Usage:
This chart allows you to:
- Compare average and range of prices across different environmental labels.
- Identify price patterns based on emissions and associated technologies.
- Assist buyers in deciding which environmental label category fits their budget best.

**Note**: The logarithmic scale on the Y-axis facilitates the visualization of a wide range of cash prices.
""",
        "price_comparison_title": "Comparison of New Car Price vs. Second Hand Car Price by Brand",
        "price_comparison_xaxis_title": "Brand",
        "price_comparison_yaxis_title": "Average Price (€)",
        "price_comparison_hover_marca": "Brand",
        "price_comparison_hover_precio_nuevo": "New Price",
        "price_comparison_hover_precio_contado": "2nd Hand Price",
        "price_comparison_legend_new": "New Price",
        "price_comparison_legend_contado": "2nd Hand Price",
        "price_comparison_description": """
### Comparison of New Car Price vs. Second Hand Car Price by Brand

This bar chart compares the average price of new cars against the average price of second-hand cars, categorized by brand.

#### Chart Details:
- **X-Axis (Brand)**: Displays different car brands available in the market.
- **Y-Axis (Average Price)**: Represents the average price of cars in euros (€).
- **Blue Bars**: Indicate the average price of new cars for each brand.
- **Orange Bars**: Indicate the average price of second-hand cars (cash price) for each brand.

#### Key Observations:
1. **Price Differences**:
   - Luxury brands like **Aston Martin**, **Ferrari**, and **Lamborghini** show significant differences between new and second-hand car prices, with new cars being considerably more expensive.
   - More affordable brands, such as **Dacia**, **Fiat**, and **Citroën**, exhibit smaller price differences between new and second-hand cars.

2. **General Pattern**:
   - Across all brands, the average price of new cars is higher than that of second-hand cars, reflecting the usual depreciation of vehicles over time.
   - High-end brands present much higher prices compared to mainstream brands.

3. **Brand Comparisons**:
   - **Tesla** stands out with higher prices for new cars compared to mainstream brands, but with a smaller price difference between new and second-hand cars.
   - Brands like **Mercedes-Benz** and **BMW** have higher new car prices compared to their second-hand counterparts.

#### Chart Usage:
This chart is useful for:
- Analyzing how the average price of new cars compares to second-hand cars across different brands.
- Identifying brands with lower depreciation in price.
- Assisting buyers and sellers in understanding value differences between new and used cars.

**Note**: Prices are in euros (€), and each bar represents the average price for that category.
""",
        "power_price_relation_title": "Relationship between Price and Power by Fuel Type",
        "power_price_relation_labels": {
            "potencia_cv": "Power (HP)",
            "precio_contado": "Price (€)",
            "combustible": "Fuel Type"
        },
        "power_price_relation_hovertemplate": '<b>Power (HP)</b>: %{x:,}<br>' + \
                                               '<b>Price (€)</b>: %{y:,.2f} €<br>' + \
                                               '<b>Fuel Type</b>: %{customdata[0]}<br>' + \
                                               '<extra></extra>',
        "power_price_relation_description": """
### Relationship between Price and Power by Fuel Type

This scatter plot illustrates how the price of cars relates to their power (in horsepower, HP), categorized by the type of fuel they use.

#### Chart Details:
- **X-Axis (Power)**: Represents the car's power in horsepower (HP). As power increases, higher-priced cars are observed.
- **Y-Axis (Price)**: Shows the cash price of cars on a logarithmic scale, allowing visualization of both low and high prices on the same scale.
- **Colors**: Each point is colored according to the car's fuel type:
  - **Gasoline**: Orange
  - **Diesel**: Green
  - **Gasoline/Gas**: Blue
  - **Electric**: Pink
  - **Plug-in Hybrid**: Yellow
  - **Gas**: Orange

#### Key Observations:
1. **General Trend**:
   - Higher power generally correlates with higher prices, indicating a positive relationship between these variables.

2. **Distribution by Fuel Type**:
   - **Electric** and **Plug-in Hybrid** cars tend to be in the higher price range, even with moderate power.
   - **Gasoline** and **Diesel** cars cover a wider range of prices and power levels.
   - **Gas** cars are primarily in the lower power and price range.

3. **Notable Points**:
   - There are cars with high power (over 500 HP) and exceptionally high prices.
   - Most points are clustered below 200 HP and below €100,000.

#### Chart Usage:
This chart is useful for:
- Identifying trends in the market based on fuel type and power.
- Helping buyers understand how power and fuel type influence car prices.
- Exploring differences between technologies like electric, hybrid, and traditional fuels.

**Note**: Hovering over a point displays the exact price, power, and fuel type of the corresponding car.
""",
        "choropleth_map_title": "Distribution of Cars by Province",
        "choropleth_map_labels": {
            "cantidad_log": "Quantity (Log)"
        },
        "choropleth_map_hovertemplate": '<b>Province</b>: %{location}<br>' + \
                                         '<b>Quantity</b>: %{customdata[0]:,}<br>' + \
                                         '<extra></extra>',
        "choropleth_map_colorbar_title": "Quantity of Cars (Log)",
        "choropleth_map_description": """
### Choropleth Map: Distribution of Cars by Province

This map displays the number of cars in each province of Spain.

- **Darker colors** indicate a **higher number of cars**.
- **Lighter colors** represent a lower number of cars.
- Hovering over a province shows the **exact number of cars**.

It is noticeable that more populous provinces like Madrid and Barcelona have the highest number of cars.
""",
        "choropleth_map_price_title": "Average Car Price by Province",
        "choropleth_map_price_labels": {
            "precio_medio": "Average Price (€)"
        },
        "choropleth_map_price_hovertemplate": '<b>Province</b>: %{location}<br>' + \
                                               '<b>Average Price (€)</b>: %{z:,.2f}€<br>' + \
                                               '<extra></extra>',
        "choropleth_map_price_colorbar_title": "Average Price (€)",
        "choropleth_map_price_description": """
### Choropleth Map: Average Car Price by Province

This map illustrates the geographical distribution of the average car price in each province of Spain.

- **Darker colors** indicate a **higher average price**.
- **Lighter colors** represent a lower average price.
- Hovering over a province displays the **exact average price in euros**.

Interestingly, Almería stands out as the province with the most expensive cars compared to others, with no clear pattern observed.
"""
    },
    "es": {
        "analysis_title": "Análisis Visual de Coches de Segunda Mano",
        "separator": "---",
        "scatter_plot_title": "Relación entre kilometraje y precio al contado según el año de matriculación",
        "scatter_plot_labels": {
            "kilometraje": "Kilometraje (km)",
            "precio_contado": "Precio Contado (€)",
            "ano_matriculacion": "Año de Matriculación"
        },
        "scatter_plot_hovertemplate": '<b>Kilometraje</b>: %{x:,}<br>' + \
                                       '<b>Precio Contado (€)</b>: %{y:,}€<br>' + \
                                       '<b>Año</b>: %{customdata[0]}<br>' + \
                                       '<extra></extra>',
        "scatter_plot_colorbar_title": "Año de Matriculación",
        "scatter_plot_description": """
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
""",
        "box_plot_title": "Distribución del precio por distintivo ambiental",
        "box_plot_labels": {
            "distintivo_ambiental": "Distintivo Ambiental",
            "precio_contado": "Precio Contado (€)"
        },
        "box_plot_hovertemplate": '<b>Distintivo Ambiental</b>: %{x}<br>' + \
                                    '<b>Precio Contado (€)</b>: %{y:,.2f} €<br>' + \
                                    '<b>Máximo</b>: %{hoverinfo.max}<br>' + \
                                    '<b>Mínimo</b>: %{hoverinfo.min}<br>' + \
                                    '<b>Mediana</b>: %{hoverinfo.median}<br>' + \
                                    '<extra></extra>',
        "box_plot_xaxis_title": "Distintivo Ambiental",
        "box_plot_yaxis_title": "Precio Contado (€)",
        "box_plot_description": """
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
""",
        "price_comparison_title": "Precio coche nuevo vs precio coche de segunda mano por marca",
        "price_comparison_xaxis_title": "Marca",
        "price_comparison_yaxis_title": "Precio Medio (€)",
        "price_comparison_hover_marca": "Marca",
        "price_comparison_hover_precio_nuevo": "Precio Nuevo",
        "price_comparison_hover_precio_contado": "Precio 2ª Mano",
        "price_comparison_legend_new": "Precio Nuevo",
        "price_comparison_legend_contado": "Precio 2ª Mano",
        "price_comparison_description": """
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
""",
        "power_price_relation_title": "Relación entre precio y potencia según el combustible",
        "power_price_relation_labels": {
            "potencia_cv": "Potencia (cv)",
            "precio_contado": "Precio (€)",
            "combustible": "Tipo de Combustible"
        },
        "power_price_relation_hovertemplate": '<b>Potencia (cv)</b>: %{x:,}<br>' + \
                                               '<b>Precio contado</b>: %{y:,.2f} €<br>' + \
                                               '<b>Combustible</b>: %{customdata[0]}<br>' + \
                                               '<extra></extra>',
        "power_price_relation_description": """
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
""",
        "choropleth_map_title": "Distribución de coches por provincia",
        "choropleth_map_labels": {
            "cantidad_log": "Cantidad (Log)"
        },
        "choropleth_map_hovertemplate": '<b>Provincia</b>: %{location}<br>' + \
                                         '<b>Cantidad</b>: %{customdata[0]:,}<br>' + \
                                         '<extra></extra>',
        "choropleth_map_colorbar_title": "Cantidad de coches (Log)",
        "choropleth_map_description": """
### Mapa Coroplético: Distribución de Coches por Provincia

Este mapa muestra la cantidad de coches en cada provincia de España. 

- **Color más intenso** indica **mayor cantidad de coches**.
- Las provincias con **color más claro** tienen menor cantidad de coches.
- Al pasar el cursor sobre una provincia, se puede observar la **cantidad exacta de coches**.

Apreciamos que las provincias más pobladas son las que más coches tienen. Sobresalen Madrid y Barcelona.            
""",
        "choropleth_map_price_title": "Precio medio de coches por provincia",
        "choropleth_map_price_labels": {
            "precio_medio": "Precio medio (€)"
        },
        "choropleth_map_price_hovertemplate": '<b>Provincia</b>: %{location}<br>' + \
                                               '<b>Precio medio (€)</b>: %{z:,.2f}€<br>' + \
                                               '<extra></extra>',
        "choropleth_map_price_colorbar_title": "Precio Medio (€)",
        "choropleth_map_price_description": """
### Mapa Coroplético: Precio Medio de Coches por Provincia

Este mapa muestra la distribución geográfica del precio medio de coches en cada provincia de España. 

- **Color más intenso** indica un **precio medio más alto**.
- Las provincias con **color más claro** tienen un precio medio más bajo.
- Al pasar el cursor sobre una provincia, se puede observar el **precio medio exacto en euros**.

La información está basada en el precio al contado promedio calculado a partir de los datos disponibles.

Sorprende que destaque Almería como provincia con coches más caros que el resto. No se aprecia ningún patrón.            
"""
    }
}

if 'lang' not in st.session_state:
    st.session_state.lang = "en" 

# 4. Selector de idioma
idioma = st.sidebar.radio(
    'Language',  
    ("English", "Español") 
)

# 5. Actualizar el estado del idioma según la selección
if idioma == "Español":
    st.session_state.lang = "es"
else:
    st.session_state.lang = "en"

lang = st.session_state.lang

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

st.markdown(f'<h1 style="text-align:center; font-size: 3rem;">{texts[lang]["analysis_title"]}</h1>', unsafe_allow_html=True)



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
    labels= texts[lang]['scatter_plot_labels'],
    title=f'{texts[lang]["scatter_plot_title"]}',
    log_y=True,
    custom_data=['ano_matriculacion']
)

# Personalizar diseño del gráfico y tooltip
fig.update_traces(
    marker=dict(size=10),
    hovertemplate= f'{texts[lang]["scatter_plot_hovertemplate"]}'
)

fig.update_layout(
    height=800,  # Altura del gráfico
    font=dict(size=18),  # Tamaño del texto general
    title_font=dict(size=24),  # Tamaño del título
    coloraxis_colorbar=dict(title = texts[lang]["scatter_plot_colorbar_title"]) 
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown(texts[lang]['scatter_plot_description'])


st.markdown("---")

#st.title("Distribución del Precio Contado por Distintivo Ambiental")

# Crear gráfico con Plotly
fig = px.box(
    df,
    x="distintivo_ambiental",
    y="precio_contado",
    color="distintivo_ambiental",
    labels= texts[lang]['box_plot_labels'],
    title= f'{texts[lang]["box_plot_title"]}',
    log_y=True,  # Escala logarítmica en el eje Y
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Personalizar diseño y formato del tooltip
fig.update_traces(
    hovertemplate= f'{texts[lang]["box_plot_hovertemplate"]}'
)

# Personalizar diseño
fig.update_layout(
    height=800,
    font=dict(size=20),
    title_font=dict(size=26),
    xaxis_title=f'{texts[lang]["box_plot_xaxis_title"]}',
    yaxis_title=f'{texts[lang]["box_plot_yaxis_title"]}',
    xaxis=dict(tickfont=dict(size=18)),
    yaxis=dict(tickfont=dict(size=18))
)

# Mostrar gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)

st.markdown(texts[lang]['box_plot_description'])



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
    name=f'{texts[lang]["price_comparison_legend_new"]}',
    marker_color="blue",  # Color de las barras
    hovertemplate= 
        f'<b>{texts[lang]["price_comparison_hover_marca"]}</b>: %{{x}}<br>' +
        f'<b>{texts[lang]["price_comparison_hover_precio_nuevo"]}</b>: %{{y:,.2f}} €<br>' +
        '<extra></extra>'
))

# Agregar barras para 'precio_contado'
fig.add_trace(go.Bar(
    x=precio_medio.index,  # Marcas
    y=precio_medio["precio_contado"],  # Precio contado promedio
    name=f'{texts[lang]["price_comparison_legend_contado"]}',
    marker_color="orange",  # Color de las barras
    hovertemplate=
        f'<b>{texts[lang]["price_comparison_hover_marca"]}</b>: %{{x}}<br>' +
        f'<b>{texts[lang]["price_comparison_hover_precio_contado"]}</b>: %{{y:,.2f}} €<br>' +
        '<extra></extra>'
))

# Personalizar diseño
fig.update_layout(
    title=f'{texts[lang]["price_comparison_title"]}',
    xaxis_title=f'{texts[lang]["price_comparison_xaxis_title"]}',
    yaxis_title=f'{texts[lang]["price_comparison_yaxis_title"]}',
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

st.markdown(texts[lang]['price_comparison_description'])

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
    labels=texts[lang]["power_price_relation_labels"],
    title=f'{texts[lang]["power_price_relation_title"]}',
    log_y=True,
    custom_data=['combustible']
)

# Personalizar el tamaño de los puntos y el formato del tooltip
fig.update_traces(
    marker=dict(size=15),
    hovertemplate= texts[lang]["power_price_relation_hovertemplate"]
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

st.markdown(texts[lang]['power_price_relation_description'])


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