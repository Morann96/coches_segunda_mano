import streamlit as st
import pandas as pd

# Cargar los datos
@st.cache_data
def load_data():
    data = pd.read_csv('bin/data_preprocess.csv')
    marcas_data = pd.read_csv('bin/listado_marcas.csv')
    modelos_data = pd.read_csv('bin/listado_modelos.csv')
    return data, marcas_data, modelos_data

data, marcas_data, modelos_data = load_data()

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




