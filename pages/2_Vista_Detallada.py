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

# Función para conectar a la base de datos y comprobar la conexión con streamlit
def comprobar_conexion():
    try:
        conn = conectar_base_datos()
        conn.connect
        return True
    except mc.Error as err:
        return False

# Interfaz de Streamlit
st.title("Conexión a la Base de Datos")

def click_button():
     if comprobar_conexion():
         st.success("Conexión exitosa a la base de datos.")
     else:
         st.error("Error al conectar a la base de datos.")

# Botón para comprobar la conexión
st.button("Comprobar conexión a la BBDD", on_click=click_button)
   


        

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

# Filtrar por rango de precio
min_price, max_price = st.sidebar.slider(
    "Rango de precio",
    min_value=int(data['precio_contado'].min()),
    max_value=int(data['precio_contado'].max()),
    value=(int(data['precio_contado'].min()), int(data['precio_contado'].max()))
)

# Filtrar por año de matriculación
min_year, max_year = st.sidebar.slider(
    "Rango de año de matriculación",
    min_value=int(data['ano_matriculacion'].min()),
    max_value=int(data['ano_matriculacion'].max()),
    value=(int(data['ano_matriculacion'].min()), int(data['ano_matriculacion'].max()))
)

# Extraer marcas únicas directamente desde el DataFrame principal
marcas_unicas = data['id_marca'].str.upper().dropna().unique()  # Convertir a mayúsculas y eliminar NaN
marcas_unicas = [str(marca) for marca in marcas_unicas]  # Asegurar que todo sea string

# Filtrar por marca
marcas = st.sidebar.multiselect(
    "Selecciona Marca",
    options=sorted(marcas_unicas),  # Ordenar alfabéticamente
    default=[]
)

# Filtrar por tipo de cambio
cambio_unico = data['tipo_cambio'].str.upper().dropna().unique()
tipo_cambio = st.sidebar.multiselect(
    "Selecciona Tipo de Cambio",
    options=sorted(cambio_unico),
    default=[]
)

# Filtrar por provincia
provincias = st.sidebar.multiselect(
    "Selecciona Provincias",
    options=data['id_provincia'].unique(),
    default=[]
)

# Filtrar por distintivo ambiental
distintivos = st.sidebar.multiselect(
    "Selecciona Distintivos Ambientales",
    options=data['id_distintivo_ambiental'].unique(),
    default=data['id_distintivo_ambiental'].unique()
)

# Filtrar por número de puertas
puertas_unicas = data['num_puertas'].dropna().unique()
puertas = st.sidebar.multiselect(
    "Selecciona Número de Puertas",
    options=sorted(puertas_unicas),
    default=[]
)

# Aplicar filtros
filtered_data = data[
    (data['id_provincia'].isin(provincias) if provincias else True) &
    (data['id_distintivo_ambiental'].isin(distintivos) if distintivos else True) &
    (data['precio_contado'] >= min_price) &
    (data['precio_contado'] <= max_price) &
    (data['id_marca'].str.upper().isin(marcas) if marcas else True) &  # Usar directamente el filtro de marcas
    (data['ano_matriculacion'] >= min_year) &
    (data['num_puertas'].isin(puertas) if puertas else True) &
    (data['tipo_cambio'].str.upper().isin(tipo_cambio) if tipo_cambio else True) &
    (data['ano_matriculacion'] <= max_year)
]

# Mostrar datos filtrados
st.write(f"Mostrando {len(filtered_data)} resultados:")
st.dataframe(filtered_data)

# Estadísticas básicas
st.header("Estadísticas Básicas")
st.write(filtered_data.describe())




