import streamlit as st
import pandas as pd
import pickle
import mysql.connector

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

    return df

# Título de la aplicación
st.title("Predicción del Precio al Contado")

tabla = "vista_prestaciones"

st.dataframe(mostrar_datos(tabla))


# MODELO




# Cargar datos de entrada
@st.cache_data
def load_data():
    return pd.read_csv('bin/data_preprocess.csv')

# Cargar modelo
@st.cache_resource
def load_model():
    with open('notebooks/modelo/mejor_modelo.pkl', 'rb') as file:
        return pickle.load(file)

# Uso del modelo
data = load_data()
model = load_model()



# Pedir entrada de usuario para las características
st.header("Introduce las características para la predicción")

# Obtener las columnas excepto la columna objetivo
features = [col for col in data.columns if col != "precio_contado"]
input_data = {}

for feature in features:
    input_data[feature] = st.number_input(f"{feature}", value=0.0)

# Convertir los datos ingresados en un DataFrame
input_df = pd.DataFrame([input_data])

# Botón para predecir
if st.button("Predecir"):
    try:
        # Realizar la predicción
        prediction = model.predict(input_df)[0]
        st.success(f"El precio contado predicho es: €{prediction:.2f}")
    except Exception as e:
        st.error(f"Ocurrió un error durante la predicción: {e}")


