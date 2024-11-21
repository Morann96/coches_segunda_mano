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
def mostrar_datos(tabla):
    conn = conectar_base_datos()
    query = f"SELECT * FROM {tabla}"
    conn.query(query)  # Consulta SQL
    df = conn.query(query) # Extraer datos como DataFrame
    st.dataframe(df)  # Mostrar los datos en Streamlit

# Streamlit App
st.title("Explorar Tabla")

# Input para el nombre de la tabla
tabla = st.text_input("Nombre de la tabla:")

if st.button("Mostrar datos"):
    if tabla:
        mostrar_datos(tabla)
    else:
        st.warning("Por favor, introduce un nombre de tabla.")



# Título de la aplicación
st.title("Visualización de Coches de Segunda Mano")

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

# Filtrar los datos según los filtros previos
filtered_data = data[
    (data['precio_contado'] >= min_price) &
    (data['precio_contado'] <= max_price) &
    (data['ano_matriculacion'] >= min_year) &
    (data['ano_matriculacion'] <= max_year)
]

# Filtrar marcas
marcas_unicas = filtered_data['id_marca'].str.upper().dropna().unique()
marcas_unicas = [str(marca) for marca in marcas_unicas]
marcas = st.sidebar.multiselect(
    "Selecciona Marca",
    options=sorted(marcas_unicas),
    default=[]
)

# Filtrar por tipo de cambio según la marca seleccionada
if marcas:
    filtered_data = filtered_data[filtered_data['id_marca'].str.upper().isin(marcas)]

tipo_cambio_unico = filtered_data['tipo_cambio'].str.upper().dropna().unique()
tipo_cambio = st.sidebar.multiselect(
    "Selecciona Tipo de Cambio",
    options=sorted(tipo_cambio_unico),
    default=[]
)

# Filtrar por provincias disponibles
provincias = st.sidebar.multiselect(
    "Selecciona Provincias",
    options=filtered_data['id_provincia'].unique(),
    default=[]
)

# Filtrar por distintivos ambientales
distintivos = st.sidebar.multiselect(
    "Selecciona Distintivos Ambientales",
    options=filtered_data['id_distintivo_ambiental'].unique(),
    default=filtered_data['id_distintivo_ambiental'].unique()
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
    (filtered_data['id_provincia'].isin(provincias) if provincias else True) &
    (filtered_data['id_distintivo_ambiental'].isin(distintivos) if distintivos else True) &
    (filtered_data['tipo_cambio'].str.upper().isin(tipo_cambio) if tipo_cambio else True) &
    (filtered_data['num_puertas'].isin(puertas) if puertas else True)
]

# Mostrar los datos filtrados
st.write(f"Mostrando {len(filtered_data)} resultados:")
st.dataframe(filtered_data)

# Estadísticas básicas
st.header("Estadísticas Básicas")
st.write(filtered_data.describe())