import streamlit as st
import pickle
import numpy as np

# Título de la aplicación
st.title('Predicción de Precio')

# Cargar el modelo try:
try:
    modelo = pickle.load(open('modelo.pkl', 'rb'))
except FileNotFoundError:
    st.error('Error')

# Función para realizar predicciones
def predecir_precio(input_data):
    # Aquí podrías incluir cualquier preprocesamiento necesario
    prediccion = modelo.predict(input_data)
    return prediccion

# Recopilar entradas del usuario
st.header('Ingrese las características del coche')

#marca = st.selectbox('Marca', ['Ford', 'Toyota', 'BMW', 'Mercedes', 'Audi'])
#modelo_coche = st.text_input('Modelo')
#año = st.slider('Año', 1980, 2023, 2010)
#kilometraje = st.number_input('Kilometraje (km)', min_value=0, max_value=500000, value=50000)
#transmision = st.selectbox('Transmisión', ['Manual', 'Automático'])
#combustible = st.selectbox('Tipo de Combustible', ['Gasolina', 'Diesel', 'Eléctrico', 'Híbrido'])
#potencia = st.number_input('Potencia (CV)', min_value=50, max_value=500, value=100)

# Cuando el usuario hace clic en el botón 'Predecir Precio'
if st.button('Predecir Precio'):
    # Preprocesar las entradas para el modelo
    # Esto incluiría transformar variables categóricas en numéricas, escalar datos, etc.
    # Para este ejemplo, asumiremos que ya está preprocesado

    # Crear el array de características para el modelo
    input_features = np.array([[año, kilometraje, potencia]])
    
    # Realizar la predicción
    try:
        precio_predicho = predecir_precio(input_features)
        st.success(f'El precio estimado del coche es: {precio_predicho[0]:,.2f}€')
    except Exception as e:
        st.error(f'Ocurrió un error al predecir el precio: {e}')
