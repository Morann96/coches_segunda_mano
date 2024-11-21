import streamlit as st
import pandas as pd
import pickle


# Función para cargar el modelo
@st.cache_resource
def load_model():
    with open('notebooks/modelo/mejor_modelo.pkl', 'rb') as file:
        return pickle.load(file)


# Función para cargar datos preprocesados (estructura de entrada)
@st.cache_data
def load_data():
    return pd.read_csv('bin/data_preprocess.csv')


# Cargar el modelo y los datos preprocesados
model = load_model()
data = load_data()

# Interfaz de usuario
st.title("Predicción del Precio al Contado")

# Crear tres columnas para los filtros
col1, col2, col3 = st.columns(3)

# Inicializar diccionario para entrada
input_data = {}

with col1:
    # Filtros de la primera columna
    marcas = data["nombre_marca"].unique()
    input_data["nombre_marca"] = st.selectbox("Marca", options=marcas)

    modelos_disponibles = data[data["nombre_marca"] == input_data["nombre_marca"]]["nombre_modelo"].unique()
    input_data["nombre_modelo"] = st.selectbox("Modelo", options=modelos_disponibles)

with col2:
    # Filtros de la segunda columna
    distintivos = data["distintivo_ambiental"].dropna().unique()
    input_data["distintivo_ambiental"] = st.selectbox("Distintivo Ambiental", options=distintivos)

    kilometraje_unicos = sorted(data["kilometraje"].unique())
    input_data["kilometraje"] = st.selectbox("Kilometraje (Exacto)", options=kilometraje_unicos)

with col3:
    # Filtros de la tercera columna
    input_data["mes_matriculacion"] = st.selectbox("Mes de Matriculación", options=sorted(data["mes_matriculacion"].unique()))
    input_data["ano_matriculacion"] = st.selectbox("Año de Matriculación", options=sorted(data["ano_matriculacion"].unique()))

    tipo_cambio = data["tipo_cambio"].dropna().unique()
    input_data["tipo_cambio"] = st.selectbox("Tipo de Cambio", options=tipo_cambio)

    combustibles = data["combustible"].dropna().unique()
    input_data["combustible"] = st.selectbox("Combustible", options=combustibles)

# Convertir entrada en un DataFrame
input_df = pd.DataFrame([input_data])

# Botón para predecir
if st.button("Predecir"):
    try:
        # Realizar la predicción
        prediction = model.predict(input_df)[0]
        st.success(f"El precio contado predicho es: €{prediction:.2f}")
    except Exception as e:
        st.error(f"Ocurrió un error durante la predicción: {e}")










