import streamlit as st
import pandas as pd
import plotly.express as px

texts = {
    "en": {
        # Títulos y encabezados
        "title_app": "Second Hand Cars Visualization",
        "filters_header": "Filters",
        
        # Filtros y entradas
        "manual_price_range_min": "Minimum Price",
        "manual_price_range_max": "Maximum Price",
        "filter_price_range": "Price Range",
        "filter_registration_year_range": "Year of Registration Range",
        "select_brand": "Select Brand",
        "select_model": "Select Model",
        "no_models_available": "No models available for selected brands",
        "select_transmission_type": "Select Transmission Type",
        "select_provinces": "Select Provinces",
        "select_environmental_labels": "Select Environmental Labels",
        "select_number_of_doors": "Select Number of Doors",
        
        # Mensajes de datos
        "showing_results": "Showing {len} results:",
        
        # Gráficos
        "price_distribution_title": "Price Distribution",
        "price_distribution_hovertemplate": "Used Price: %{x:,.0f}€<br>Count: %{y}",
        "price_distribution_xaxis_title": "Used Price (€)",
        "price_distribution_yaxis_title": "Frequency",
        
        "price_vs_year_title": "Price vs Year of Registration",
        "price_vs_year_hovertemplate": "Year of Registration: %{x}<br>Used Price: %{y:,.0f}€",
        "price_vs_year_xaxis_title": "Year of Registration",
        "price_vs_year_yaxis_title": "Used Price (€)",
        
        "fuel_type_distribution_title": "Distribution by Fuel Type",
        "fuel_type_distribution_hovertemplate": "Fuel Type: %{x}<br>Number of Cars: %{y}",
        "fuel_type_distribution_xaxis_title": "Fuel Type",
        "fuel_type_distribution_yaxis_title": "Number of Cars",
        
        "community_distribution_title": "Distribution by Autonomous Community",
        "community_distribution_hovertemplate": "Autonomous Community: %{label}<br>Quantity: %{value}"
    },
    "es": {
        # Títulos y encabezados
        "title_app": "Visualización de Coches de Segunda Mano",
        "filters_header": "Filtros",
        
        # Filtros y entradas
        "manual_price_range_min": "Precio mínimo",
        "manual_price_range_max": "Precio máximo",
        "filter_price_range": "Rango de precio",
        "filter_registration_year_range": "Rango de año de matriculación",
        "select_brand": "Selecciona Marca",
        "select_model": "Selecciona Modelo",
        "no_models_available": "No hay modelos disponibles para las marcas seleccionadas",
        "select_transmission_type": "Selecciona Tipo de Cambio",
        "select_provinces": "Selecciona Provincias",
        "select_environmental_labels": "Selecciona Distintivos Ambientales",
        "select_number_of_doors": "Selecciona Número de Puertas",
        
        # Mensajes de datos
        "showing_results": "Mostrando {len} resultados:",
        
        # Gráficos
        "price_distribution_title": "Distribución de Precios",
        "price_distribution_hovertemplate": "Precio: %{x:,.0f}€<br>Cantidad: %{y}",
        "price_distribution_xaxis_title": "Precio (€)",
        "price_distribution_yaxis_title": "Frecuencia",
        
        "price_vs_year_title": "Relación Precio vs Año de Matriculación",
        "price_vs_year_hovertemplate": "Año de Matriculación: %{x}<br>Precio: %{y:,.0f}€",
        "price_vs_year_xaxis_title": "Año de Matriculación",
        "price_vs_year_yaxis_title": "Precio (€)",
        
        "fuel_type_distribution_title": "Distribución por Tipo de Combustible",
        "fuel_type_distribution_hovertemplate": "Tipo de Combustible: %{x}<br>Cantidad de Coches: %{y}",
        "fuel_type_distribution_xaxis_title": "Tipo de Combustible",
        "fuel_type_distribution_yaxis_title": "Cantidad de Coches",
        
        "community_distribution_title": "Distribución por Comunidad Autónoma",
        "community_distribution_hovertemplate": "Comunidad Autónoma: %{label}<br>Cantidad: %{value}"
    }
}

if 'lang' not in st.session_state:
    st.session_state.lang = "en" 

# 4. Selector de idioma
idioma = st.sidebar.radio(
    'Language',  
    ("English", "Español") 
)

st.sidebar.markdown("---")

# 5. Actualizar el estado del idioma según la selección
if idioma == "Español":
    st.session_state.lang = "es"
else:
    st.session_state.lang = "en"

lang = st.session_state.lang

# Función para conectar a la base de datos
# def conectar_base_datos():
#     conn = st.connection('mysql', type='sql')
#     return conn
  
# Función para extraer y mostrar datos
# def obtener_datos_vista():
#     conn = conectar_base_datos()
#     query = "SELECT * FROM vista_prestaciones"
#     data = conn.query(query)  # Ejecutar consulta y obtener datos como DataFrame
#     return data

#data = obtener_datos_vista()

data = pd.read_csv("bin/datos_completos.csv")

# Título de la aplicación
st.markdown(f"<h1 style='text-align: center;'>{texts[lang]['title_app']}</h1>", unsafe_allow_html=True)

# Filtros
st.sidebar.header(texts[lang]['filters_header'])

# Guardar los filtros en session_state
if 'filtros' not in st.session_state:
    st.session_state.filtros = {}

# Filtrar por rango de precio

min_price = int(data['precio_contado'].min())
max_price = int(data['precio_contado'].max())

min_value = st.sidebar.number_input(texts[lang]["manual_price_range_min"], min_value=min_price, max_value=max_price, value=min_price, step=500)
max_value = st.sidebar.number_input(texts[lang]["manual_price_range_max"], min_value=min_price, max_value=max_price, value=max_price, step=500)

# min_price, max_price = st.sidebar.slider(
#     'Rango de precios',
#     min_value=min_price,
#     max_value=max_price,
#     value=(min_value, max_value)
# )
st.session_state.filtros['min_price'] = min_price
st.session_state.filtros['max_price'] = max_price

# Filtrar por año de matriculación
min_year, max_year = st.sidebar.slider(
    texts[lang]['filter_registration_year_range'],
    min_value=int(data['ano_matriculacion'].min()),
    max_value=int(data['ano_matriculacion'].max()),
    value=(int(data['ano_matriculacion'].min()), int(data['ano_matriculacion'].max()))
)
st.session_state.filtros['min_year'] = min_year
st.session_state.filtros['max_year'] = max_year

# Filtrar marcas
marcas_unicas = filtered_data = data[
    (data['precio_contado'] >= min_price) &
    (data['precio_contado'] <= max_price) &
    (data['ano_matriculacion'] >= min_year) &
    (data['ano_matriculacion'] <= max_year)
]['marca'].str.upper().dropna().unique()
marcas_unicas = [str(marca) for marca in marcas_unicas]
marcas = st.sidebar.multiselect(
    texts[lang]['select_brand'],
    options=sorted(marcas_unicas),
    default=[]
)

# Filtrar modelos dinámicamente en función de las marcas seleccionadas
if marcas:
    # Si se seleccionan marcas, mostrar los modelos que coincidan con esas marcas
    modelos_disponibles = data[
        (data['marca'].str.upper().isin(marcas)) &
        (data['precio_contado'] >= min_price) &
        (data['precio_contado'] <= max_price) &
        (data['ano_matriculacion'] >= min_year) &
        (data['ano_matriculacion'] <= max_year)
    ]['modelo'].dropna().unique()
else:
    # Si no se selecciona ninguna marca, mostrar todos los modelos disponibles
    modelos_disponibles = data[
        (data['precio_contado'] >= min_price) &
        (data['precio_contado'] <= max_price) &
        (data['ano_matriculacion'] >= min_year) &
        (data['ano_matriculacion'] <= max_year)
    ]['modelo'].dropna().unique()

# Asegúrate de que modelos_disponibles no esté vacío
if len(modelos_disponibles) > 0:
    modelos = st.sidebar.multiselect(
        texts[lang]['select_model'],
        options=sorted(modelos_disponibles),
        default=[]
    )
else:
    # Si no hay modelos disponibles, mostrar un mensaje
    st.sidebar.write(texts[lang]['no_models_available'])

# Filtrar los modelos
if modelos:
    filtered_data = data[
        (data['modelo'].isin(modelos)) &
        (data['precio_contado'] >= min_price) &
        (data['precio_contado'] <= max_price) &
        (data['ano_matriculacion'] >= min_year) &
        (data['ano_matriculacion'] <= max_year)
    ]
else:
    filtered_data = data[
        (data['precio_contado'] >= min_price) &
        (data['precio_contado'] <= max_price) &
        (data['ano_matriculacion'] >= min_year) &
        (data['ano_matriculacion'] <= max_year)
    ]

# Filtrar por tipo de cambio
tipo_cambio_unico = filtered_data['tipo_cambio'].str.upper().dropna().unique()
tipo_cambio = st.sidebar.multiselect(
    texts[lang]['select_transmission_type'],
    options=sorted(tipo_cambio_unico),
    default=[]
)

# Filtrar por provincias disponibles
provincias = st.sidebar.multiselect(
    texts[lang]['select_provinces'],
    options=filtered_data['provincia'].unique(),
    default=[]
)

# Filtrar por distintivos ambientales
distintivos = st.sidebar.multiselect(
    texts[lang]['select_environmental_labels'],
    options=filtered_data['distintivo_ambiental'].unique(),
    default=filtered_data['distintivo_ambiental'].unique()
)

# Filtrar por número de puertas
puertas_unicas = filtered_data['num_puertas'].dropna().unique()
puertas = st.sidebar.multiselect(
    texts[lang]['select_number_of_doors'],
    options=sorted(puertas_unicas),
    default=[]
)

# Aplicar los filtros a los datos
filtered_data = filtered_data[
    (filtered_data['provincia'].isin(provincias) if provincias else True) &
    (filtered_data['distintivo_ambiental'].isin(distintivos) if distintivos else True) &
    (filtered_data['tipo_cambio'].str.upper().isin(tipo_cambio) if tipo_cambio else True) &
    (filtered_data['num_puertas'].isin(puertas) if puertas else True)
]

# Renombrar las columnas del DataFrame filtrado según el idioma
if lang == 'es':
    nuevos_nombres_columnas = {
        'marca': 'Marca',
        'modelo': 'Modelo',
        'mes_matriculacion': 'Mes de Matriculación',
        'ano_matriculacion': 'Año de Matriculación',
        'kilometraje': 'Kilometraje',
        'distintivo_ambiental': 'Distintivo Ambiental',
        'garantia': 'Garantía',
        'precio_nuevo': 'Precio nuevo',
        'precio_contado': 'Precio usado',
        'concesionario': 'Concesionario',
        'provincia': 'Provincia',
        'comunidad_autonoma': 'Comunidad Autónoma',
        'tipo_traccion': 'Tipo de tracción',
        'largo': 'Largo',
        'ancho': 'Ancho',
        'alto': 'Alto',
        'capacidad_maletero': 'Capacidad del maletero',
        'num_plazas': 'Número de plazas',
        'num_puertas': 'Número de Puertas',
        'batalla': 'Batalla',
        'peso': 'Peso',
        'consumo_medio': 'Consumo medio',
        'consumo_carretera': 'Consumo por carretera',
        'consumo_urbano': 'Consumo urbano',
        'co2': 'Consumo de CO²',
        'deposito': 'Capacidad depósito',
        'combustible': 'Combustible',
        'num_cilindros': 'Número de cilindros',
        'cilindrada': 'Cilindrada',
        'sobrealimentacion': 'Sobrealimentación',
        'tipo_cambio': 'Tipo de cambio',
        'num_marchas': 'Número de marchas',
        'potencia_kw': 'Potencia (kW)',
        'potencia_cv': 'Potencia (cv)',
        'par': 'Par',
        'velocidad_max': 'Velocidad Máxima',
        'aceleracion': 'Aceleración'
    }
else:
    nuevos_nombres_columnas = {
        'marca': 'Brand',
        'modelo': 'Model',
        'mes_matriculacion': 'Month of Registration',
        'ano_matriculacion': 'Year of Registration',
        'kilometraje': 'Mileage',
        'distintivo_ambiental': 'Environmental Label',
        'garantia': 'Warranty',
        'precio_nuevo': 'Original Price',
        'precio_contado': 'Used Price',
        'concesionario': 'Dealer',
        'provincia': 'Province',
        'comunidad_autonoma': 'Autonomous Community',
        'tipo_traccion': 'Drive Type',
        'largo': 'Length',
        'ancho': 'Width',
        'alto': 'Height',
        'capacidad_maletero': 'Trunk Capacity',
        'num_plazas': 'Number of Seats',
        'num_puertas': 'Number of Doors',
        'batalla': 'Wheelbase',
        'peso': 'Weight',
        'consumo_medio': 'Average Consumption',
        'consumo_carretera': 'Highway Consumption',
        'consumo_urbano': 'Urban Consumption',
        'co2': 'CO² Emission',
        'deposito': 'Tank Capacity',
        'combustible': 'Fuel Type',
        'num_cilindros': 'Number of Cylinders',
        'cilindrada': 'Engine Displacement',
        'sobrealimentacion': 'Forced Induction',
        'tipo_cambio': 'Transmission Type',
        'num_marchas': 'Number of Gears',
        'potencia_kw': 'Power (kW)',
        'potencia_cv': 'Power (hp)',
        'par': 'Torque',
        'velocidad_max': 'Top Speed',
        'aceleracion': 'Acceleration'
    }

filtered_data.rename(columns=nuevos_nombres_columnas, inplace=True)

# Mostrar los datos filtrados
st.write(texts[lang]['showing_results'].format(len=len(filtered_data)))
st.dataframe(filtered_data)

# Dividir la visualización en dos columnas
col1, col2 = st.columns(2)

# Gráfico 1: Distribución de Precios
with col1:
    st.markdown(f"<h2 style='text-align: center;'>{texts[lang]['price_distribution_title']}</h2>", unsafe_allow_html=True)
    # Definir el nombre de la columna según el idioma
    x_price_col = 'Precio usado' if lang == 'es' else 'Used Price'
    fig1 = px.histogram(
        filtered_data, 
        x=x_price_col,  # Nombre renombrado
        nbins=30, 
        labels={x_price_col: texts[lang]['price_distribution_xaxis_title']},
        template='plotly_white'
    )
    fig1.update_traces(
        hovertemplate=texts[lang]['price_distribution_hovertemplate']
    )
    fig1.update_layout(
        title='',
        xaxis_title=texts[lang]['price_distribution_xaxis_title'], 
        yaxis_title=texts[lang]['price_distribution_yaxis_title'],
        title_x=0.5,
        font=dict(size=14),
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12))
    )
    st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Relación Precio vs Año de Matriculación
with col2:
    st.markdown(f"<h2 style='text-align: center;'>{texts[lang]['price_vs_year_title']}</h2>", unsafe_allow_html=True)
    x_year_col = 'Año de Matriculación' if lang == 'es' else 'Year of Registration'
    y_price_col = 'Precio usado' if lang == 'es' else 'Used Price'
    fig2 = px.scatter(
        filtered_data, 
        x=x_year_col,  # Nombre renombrado
        y=y_price_col, 
        labels={
            x_year_col: texts[lang]['price_vs_year_xaxis_title'],
            y_price_col: texts[lang]['price_vs_year_yaxis_title']
        },
        template='plotly_white',
        opacity=0.6
    )
    # Actualizar diseño para formatear el tooltip
    fig2.update_traces(
        hovertemplate=texts[lang]['price_vs_year_hovertemplate']
    )
    fig2.update_layout(
        title='',
        xaxis_title=texts[lang]['price_vs_year_xaxis_title'], 
        yaxis_title=texts[lang]['price_vs_year_yaxis_title'],
        title_x=0.5,
        font=dict(size=14),
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12))
    )
    st.plotly_chart(fig2, use_container_width=True)

# Nueva fila con dos columnas para los siguientes gráficos
col3, col4 = st.columns(2)

# Gráfico: Distribución por Tipo de Combustible
with col3:
    st.markdown(f"<h2 style='text-align: center;'>{texts[lang]['fuel_type_distribution_title']}</h2>", unsafe_allow_html=True)
    combustible_col = 'Combustible' if lang == 'es' else 'Fuel Type'
    cantidad_col = 'Cantidad' if lang == 'es' else 'Number of Cars'
    combustible_count = filtered_data[combustible_col].value_counts().reset_index()
    combustible_count.columns = [combustible_col, cantidad_col]
    fig3_alt = px.bar(
        combustible_count, 
        x=combustible_col, 
        y=cantidad_col, 
        labels={
            combustible_col: texts[lang]['fuel_type_distribution_xaxis_title'],
            cantidad_col: texts[lang]['fuel_type_distribution_yaxis_title']
        },
        template='plotly_white'
    )
    fig3_alt.update_traces(
        hovertemplate=texts[lang]['fuel_type_distribution_hovertemplate']
    )
    fig3_alt.update_layout(
        title='',
        xaxis_title=texts[lang]['fuel_type_distribution_xaxis_title'], 
        yaxis_title=texts[lang]['fuel_type_distribution_yaxis_title'],
        title_x=0.5,
        font=dict(size=14),
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12))
    )
    st.plotly_chart(fig3_alt, use_container_width=True)

# Gráfico 4: Comparación entre Comunidades Autónomas
with col4:
    st.markdown(f"<h2 style='text-align: center;'>{texts[lang]['community_distribution_title']}</h2>", unsafe_allow_html=True)
    comunidad_col = 'Comunidad Autónoma' if lang == 'es' else 'Autonomous Community'
    cantidad_col = 'Cantidad' if lang == 'es' else 'Quantity'
    comunidades_count = filtered_data[comunidad_col].value_counts().reset_index()
    comunidades_count.columns = [comunidad_col, cantidad_col]
    fig4 = px.pie(
        comunidades_count, 
        values=cantidad_col, 
        names=comunidad_col, 
        labels={comunidad_col: texts[lang]['community_distribution_title']},
        template='plotly_white'
    )
    fig4.update_traces(
        hovertemplate=texts[lang]['community_distribution_hovertemplate']
    )
    fig4.update_layout(
        title='',
        title_x=0.5,
        font=dict(size=14)
    )
    st.plotly_chart(fig4, use_container_width=True)
