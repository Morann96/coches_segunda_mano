import streamlit as st
import pandas as pd
import pickle

# Cargar datos de entrada
@st.cache_data
def load_data():
    data = pd.read_csv('bin/data_preprocess.csv')
    return data

# Cargar modelo
@st.cache_resource
def load_model():
    with open('notebooks/mejor_modelo.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Uso
data = load_data()
model = load_model()


# Título de la aplicación
st.title("Predicción del Precio al Contado")

# Mostrar la estructura de los datos
st.header("Datos de entrenamiento")
st.write("Las columnas disponibles en el conjunto de datos son:")
st.write(data.columns.tolist())

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