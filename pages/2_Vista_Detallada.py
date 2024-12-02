import streamlit as st
import pandas as pd
import mysql.connector as mc



# Cargar los datos
@st.cache_data
def load_data():
    data = pd.read_csv('bin/data_preprocess.csv')
    marcas_data = pd.read_csv('bin/listado_marcas.csv')
    modelos_data = pd.read_csv('bin/listado_modelos.csv')
    return data, marcas_data, modelos_data

data, marcas_data, modelos_data = load_data()

# Función para conectar a la base de datos
def conectar_base_datos():
    conn = st.connection('mysql', type='sql')
    return conn
  
# Función para extraer y mostrar datos
def obtener_datos_vista():
    conn = conectar_base_datos()
    query = "SELECT * FROM vista_prestaciones"
    df = conn.query(query)  # Ejecutar consulta y obtener datos como DataFrame
    return df

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

# Mostrar los datos filtrados
st.write(f"Mostrando {len(filtered_data)} resultados:")
st.dataframe(filtered_data)

# Estadísticas básicas
st.markdown("<h2 style='text-align: center;'>Estadísticas Básicas</h2>", unsafe_allow_html=True)
st.write(filtered_data.describe())