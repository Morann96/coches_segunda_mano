import streamlit as st
import pandas as pd
import mysql.connector as mc
import plotly.express as px


# Función para conectar a la base de datos
def conectar_base_datos():
    conn = st.connection('mysql', type='sql')
    return conn
  
# Función para extraer y mostrar datos
def obtener_datos_vista():
    conn = conectar_base_datos()
    query = "SELECT * FROM vista_prestaciones"
    data = conn.query(query)  # Ejecutar consulta y obtener datos como DataFrame
    return data

data = obtener_datos_vista()

# Título de la aplicación
st.markdown("<h1 style='text-align: center;'>Visualización de Coches de Segunda Mano</h1>", unsafe_allow_html=True)

# Filtros
st.sidebar.header("Filtros")

# Guardar los filtros en session_state
if 'filtros' not in st.session_state:
    st.session_state.filtros = {}

# Filtrar por rango de precio
min_price, max_price = st.sidebar.slider(
    "Rango de precio",
    min_value=int(data['precio_contado'].min()),
    max_value=int(data['precio_contado'].max()),
    value=(int(data['precio_contado'].min()), int(data['precio_contado'].max()))
)
st.session_state.filtros['min_price'] = min_price
st.session_state.filtros['max_price'] = max_price

# Filtrar por año de matriculación
min_year, max_year = st.sidebar.slider(
    "Rango de año de matriculación",
    min_value=int(data['ano_matriculacion'].min()),
    max_value=int(data['ano_matriculacion'].max()),
    value=(int(data['ano_matriculacion'].min()), int(data['ano_matriculacion'].max()))
)
st.session_state.filtros['min_year'] = min_year
st.session_state.filtros['max_year'] = max_year

#Obtener los datos de vista_prestaciones
df_vista_prestaciones = obtener_datos_vista()

# Filtrar los datos según los filtros previos
filtered_data = df_vista_prestaciones[
    (df_vista_prestaciones['precio_contado'] >= min_price) &
    (df_vista_prestaciones['precio_contado'] <= max_price) &
    (df_vista_prestaciones['ano_matriculacion'] >= min_year) &
    (df_vista_prestaciones['ano_matriculacion'] <= max_year)
]

# Filtrar marcas
marcas_unicas = filtered_data['marca'].str.upper().dropna().unique()
marcas_unicas = [str(marca) for marca in marcas_unicas]
marcas = st.sidebar.multiselect(
    "Selecciona Marca",
    options=sorted(marcas_unicas),
    default=[]
)

# Filtrar modelos dinámicamente en función de las marcas seleccionadas
if marcas:
    # Si se seleccionan marcas, mostrar los modelos que coincidan con esas marcas
    modelos_disponibles = filtered_data[filtered_data['marca'].str.upper().isin(marcas)]['modelo'].dropna().unique()
else:
    # Si no se selecciona ninguna marca, mostrar todos los modelos disponibles
    modelos_disponibles = filtered_data['modelo'].dropna().unique()

# Asegúrate de que modelos_disponibles no esté vacío
if len(modelos_disponibles) > 0:
    modelos = st.sidebar.multiselect(
        "Selecciona Modelo",
        options=sorted(modelos_disponibles),
        default=[]
    )
else:
    # Si no hay modelos disponibles, mostrar un mensaje
    st.sidebar.write("No hay modelos disponibles para las marcas seleccionadas")

# Filtrar los modelos
if modelos:
    filtered_data = filtered_data[filtered_data['modelo'].isin(modelos)]

# Filtrar por tipo de cambio
tipo_cambio_unico = filtered_data['tipo_cambio'].str.upper().dropna().unique()
tipo_cambio = st.sidebar.multiselect(
    "Selecciona Tipo de Cambio",
    options=sorted(tipo_cambio_unico),
    default=[]
)

# Filtrar por provincias disponibles
provincias = st.sidebar.multiselect(
    "Selecciona Provincias",
    options=filtered_data['provincia'].unique(),
    default=[]
)

# Filtrar por distintivos ambientales
distintivos = st.sidebar.multiselect(
    "Selecciona Distintivos Ambientales",
    options=filtered_data['distintivo_ambiental'].unique(),
    default=filtered_data['distintivo_ambiental'].unique()
)

# Filtrar por número de puertas
puertas_unicas = filtered_data['num_puertas'].dropna().unique()
puertas = st.sidebar.multiselect(
    "Selecciona Número de Puertas",
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

# Cambiar nombres de las columnas
nuevos_nombres_columnas = {
    'marca': 'Marca',
    'modelo': 'Modelo',
    'mes_matriculacion': 'Mes de Matriculación',
    'ano_matriculacion': 'Año de Matriculación',
    'kilometraje': 'Kilometraje',
    'distintivo_ambiental': 'Distintivo Ambiental',
    'garantia': 'Garantía',
    'precio_nuevo': 'Precio nuevo',
    'precio_contado': 'Precio Contado',
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
    'num_marchas': 'Número de machas',
    'potencia_kw': 'Potencia (kW)',
    'potencia_cv': 'Potencia (cv)',
    'par': 'Par',
    'velocidad_max': 'Velocidad Máxima',
    'aceleracion': 'Aceleración'
}

# Renombrar las columnas del DataFrame filtrado
filtered_data.rename(columns=nuevos_nombres_columnas, inplace=True)


# Mostrar los datos filtrados
st.write(f"Mostrando {len(filtered_data)} resultados:")
st.dataframe(filtered_data)

# # Estadísticas básicas
# st.markdown("<h2 style='text-align: center;'>Estadísticas Básicas</h2>", unsafe_allow_html=True)
# st.write(filtered_data.describe())

# Dividir la visualización en dos columnas
col1, col2 = st.columns(2)

# Gráfico 1: Distribución de Precios
with col1:
    st.markdown("<h2 style='text-align: center;'>Distribución de Precios</h2>", unsafe_allow_html=True)
    fig1 = px.histogram(
        filtered_data, 
        x='Precio Contado', 
        nbins=30, 
        labels={'Precio Contado': 'Precio Contado'},
        template='plotly_white'
    )
    fig1.update_traces(
        hovertemplate='Precio Contado (€): %{x:,.0f}€<br>Cantidad: %{y}'
    )
    fig1.update_layout(
        title='',
        xaxis_title='Precio Contado (€)', 
        yaxis_title='Frecuencia',
        title_x=0.5
    )
    st.plotly_chart(fig1, use_container_width=True)


# Gráfico 2: Relación Precio vs Año de Matriculación
with col2:
    st.markdown("<h2 style='text-align: center;'>Relación Precio vs Año de Matriculación</h2>", unsafe_allow_html=True)
    fig2 = px.scatter(
        filtered_data, 
        x='Año de Matriculación', 
        y='Precio Contado', 
        labels={'Año de Matriculación': 'Año de Matriculación', 'Precio Contado': 'Precio Contado (€)'},
        template='plotly_white',
        opacity=0.6
    )
    # Actualizar diseño para formatear el tooltip
    fig2.update_traces(
        hovertemplate='Año de Matriculación: %{x}<br>Precio Contado (€): %{y:,.0f}€'
    )
    fig2.update_layout(
        title='',
        xaxis_title='Año de Matriculación', 
        yaxis_title='Precio Contado (€)',
        title_x=0.5
    )
    st.plotly_chart(fig2, use_container_width=True)

# Nueva fila con dos columnas para los siguientes gráficos
col3, col4 = st.columns(2)

# Gráfico: Distribución por Tipo de Combustible
with col3:
    st.markdown("<h2 style='text-align: center;'>Distribución por Tipo de Combustible</h2>", unsafe_allow_html=True)
    combustible_count = filtered_data['Combustible'].value_counts().reset_index()
    combustible_count.columns = ['Combustible', 'Cantidad']
    fig3_alt = px.bar(
        combustible_count, 
        x='Combustible', 
        y='Cantidad', 
        labels={'Combustible': 'Tipo de Combustible', 'Cantidad': 'Cantidad de Coches'},
        template='plotly_white'
    )
    fig3_alt.update_layout(
        title='',
        xaxis_title='Tipo de Combustible', 
        yaxis_title='Cantidad de Coches',
        title_x=0.5
    )
    st.plotly_chart(fig3_alt, use_container_width=True)


# Gráfico 4: Comparación entre Comunidades Autónomas
with col4:
    st.markdown("<h2 style='text-align: center;'>Distribución por Comunidad Autónoma</h2>", unsafe_allow_html=True)
    comunidades_count = filtered_data['Comunidad Autónoma'].value_counts().reset_index()
    comunidades_count.columns = ['Comunidad Autónoma', 'Cantidad']
    fig4 = px.pie(
        comunidades_count, 
        values='Cantidad', 
        names='Comunidad Autónoma', 
        template='plotly_white'
    )
    fig4.update_layout(title_x=0.5)
    title='',
    st.plotly_chart(fig4, use_container_width=True)