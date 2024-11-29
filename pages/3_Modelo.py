import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import mysql.connector
from datetime import datetime
import locale
import tensorflow as tf
from tensorflow.keras.models import load_model

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

# Cargar modelo
@st.cache_resource
def cargar_modelo(file_name, directory='notebooks/modelo/'):
    file_path = os.path.join(directory, file_name)
    
    if file_name.endswith('.pkl'):
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    elif file_name.endswith('.keras'):
        red_neuronal = load_model(file_path)
        return red_neuronal
    else:
        raise ValueError(f"Extensión de archivo no reconocida. Se esperaban '.pkl' o '.keras'.")

model = cargar_modelo(file_name= 'mejor_modelo.pkl')
red_neuronal = cargar_modelo(file_name='red_neuronal.keras')

# Cargar encoders

def load_pickles(directory='notebooks/encoders'):
    encoders = {}
    # Recorrer todos los archivos en el directorio
    for file_name in os.listdir(directory):
        # Filtrar solo archivos con extensión .pkl
        if file_name.endswith('.pkl'):
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'rb') as file:
                # Usar el nombre del archivo sin extensión como clave
                encoder_name = os.path.splitext(file_name)[0]
                encoders[encoder_name] = pickle.load(file)
    return encoders

encoders = load_pickles(directory='notebooks/encoders')

encoder_distintivo = encoders['distintivo_encoder']
encoder_marca = encoders['marca_encoder']
encoder_modelo = encoders['modelo_encoder']
encoder_tipo_cambio = encoders['tipo_cambio_encoder']
combustible_encoder = encoders['combustible_encoder']

escaladores = load_pickles(directory='notebooks/escaladores')
escalador_X = escaladores["x_scaler"]
escalador_y = escaladores["y_scaler"]

# Título de la aplicación
st.title("Predicción del Precio al Contado")

tabla = "vista_prestaciones"
data = mostrar_datos(tabla)

# Creamos la columna fecha_matriculacion para calcular la antigüedad del coche en años

data['fecha_matriculacion'] = (
    '01/' + data['mes_matriculacion'].astype(int).astype(str) + 
    '/' + data['ano_matriculacion'].astype(int).astype(str))

data['fecha_matriculacion'] = pd.to_datetime(data['fecha_matriculacion'], format='%d/%m/%Y')
current_date = pd.to_datetime(datetime.now())

data['antiguedad_coche'] = ((current_date - data['fecha_matriculacion']).dt.days / 365.25).round(2)

# Inicializar st.session_state
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

if 'selected_marca' not in st.session_state:
    st.session_state.selected_marca = None
if 'selected_modelo' not in st.session_state:
    st.session_state.selected_modelo = None

# Función para obtener las opciones filtradas
def get_filtered_options():
    # Obtener todas las marcas y modelos disponibles
    marcas_filtradas = data['marca'].dropna().unique().tolist()
    modelos_filtradas = data['modelo'].dropna().unique().tolist()

    if st.session_state.selected_marca:
        # Filtrar modelos basados en la marca seleccionada
        modelos_filtradas = data[data['marca'] == st.session_state.selected_marca]['modelo'].dropna().unique().tolist()
    # No filtramos las marcas para permitir cambiar la selección

    return marcas_filtradas, modelos_filtradas

marcas_filtradas, modelos_filtrados = get_filtered_options()

# Verificar si el modelo seleccionado es válido para la marca seleccionada
if st.session_state.selected_modelo and st.session_state.selected_marca:
    modelos_validos = data[data['marca'] == st.session_state.selected_marca]['modelo'].dropna().unique().tolist()
    if st.session_state.selected_modelo not in modelos_validos:
        st.session_state.selected_modelo = None

# Configurar columnas
col1, col2 = st.columns([5, 4])

with col1:
    st.header("Características coche")

    # Primera fila de filtros
    filtro_col1, filtro_col2 = st.columns(2)
    with filtro_col1:
        # Filtro 1: Marca
        selected_marca = st.selectbox(
            "Marca:",
            marcas_filtradas,
            index=marcas_filtradas.index(st.session_state.selected_marca) if st.session_state.selected_marca in marcas_filtradas else 0,
            key='selected_marca'
        )
    with filtro_col2:
        # Filtro 2: Modelo
        selected_modelo = st.selectbox(
            "Modelo:",
            modelos_filtrados,
            index=modelos_filtrados.index(st.session_state.selected_modelo) if st.session_state.selected_modelo in modelos_filtrados else 0,
            key='selected_modelo'
        )

    # No necesitamos modificar st.session_state después de los widgets

    # Segunda fila de filtros
    filtro_col3, filtro_col4 = st.columns(2)
    with filtro_col3:
        # Filtro 3: Antigüedad
        antiguedad_coche = st.number_input("Antigüedad (años):", min_value=0, step=1)
    with filtro_col4:
        # Filtro 4: Distintivo Ambiental
        distintivo_ambiental = st.selectbox("Distintivo Ambiental:", data['distintivo_ambiental'].dropna().unique())

    # Tercera fila de filtros
    filtro_col5, filtro_col6 = st.columns(2)
    with filtro_col5:
        # Filtro 5: Kilometraje
        kilometraje = st.number_input("Kilometraje:", min_value=0, step=1000)
    with filtro_col6:
        # Filtro 6: Potencia
        potencia_cv = st.number_input("Potencia (CV):", min_value=0, step=10)

    # Cuarta fila de filtros
    filtro_col7, filtro_col8 = st.columns(2)
    with filtro_col7:
        # Filtro 7: Combustible
        combustible = st.selectbox("Combustible:", data['combustible'].dropna().unique())
    with filtro_col8:
        # Filtro 8: Tipo de Cambio
        tipo_cambio = st.selectbox("Tipo de Cambio:", data['tipo_cambio'].dropna().unique())

    # Botón para guardar los datos
    if st.button("Guardar datos"):
        input_data = {
            'marca': st.session_state.selected_marca,
            'modelo': st.session_state.selected_modelo,
            'antiguedad_coche': antiguedad_coche,
            'distintivo_ambiental': distintivo_ambiental,
            'kilometraje': kilometraje,
            'potencia_cv': potencia_cv,
            'combustible': combustible,
            'tipo_cambio': tipo_cambio,
        }

        # Guardar los datos en el estado de sesión
        st.session_state.df = pd.DataFrame([input_data])
        st.write("Datos guardados:")
        st.dataframe(st.session_state.df)

with col2:
    st.header("Resultados")

    # Operaciones adicionales con el DataFrame del usuario
    if not st.session_state.df.empty:

        columnas_modelo = ['marca', 'modelo', 'potencia_cv', 'antiguedad_coche', 'log_kilometraje', 'tipo_cambio', 'distintivo_ambiental', 'combustible']

        df_temp = st.session_state.df.copy()
        df_temp['kilometraje'] = df_temp['kilometraje'].astype(int)

        # Calcular logaritmo del kilometraje en el DataFrame del usuario
        df_temp['log_kilometraje'] = np.log(df_temp['kilometraje'])
        df_temp.drop(columns=['kilometraje'], inplace=True)
        df_temp = df_temp[columnas_modelo]
        
        # Aplicar target encoder
        df_temp['marca'] = encoder_marca.transform(df_temp['marca'])
        df_temp['modelo'] = encoder_modelo.transform(df_temp['modelo'])

        # Aplicar label encoder
        df_temp['tipo_cambio'] = encoder_tipo_cambio.transform(df_temp['tipo_cambio'])

        # Aplicar el OneHotEncoder
        encoded_cols = combustible_encoder.transform(df_temp[['combustible']])

        encoded_cols = pd.DataFrame(encoded_cols, columns=combustible_encoder.get_feature_names_out(['combustible']), index=df_temp.index)
        df_temp = pd.concat([df_temp, encoded_cols], axis=1)
        df_temp.drop(columns=['combustible'], inplace=True)

        encoded_cols = encoder_distintivo.transform(df_temp[['distintivo_ambiental']])
        
        encoded_cols = pd.DataFrame(encoded_cols, columns=encoder_distintivo.get_feature_names_out(['distintivo_ambiental']), index=df_temp.index)
        df_temp = pd.concat([df_temp, encoded_cols], axis=1)
        df_temp.drop(columns=['distintivo_ambiental'], inplace=True)

        # Escalar los datos
        x = escalador_X.transform(df_temp)


    else:
        st.warning("Por favor, guarda los datos antes de continuar.")

    # Configurar la localización para España
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')  # En sistemas basados en Unix
    # Para Windows, puedes intentar con 'Spanish_Spain.1252'

    # Botón para predecir
    if st.button("Predicción con Machine Learning"):
        try:
            # Realizar la predicción
            prediction = model.predict(x)
            prediction_unescaled = escalador_y.inverse_transform(np.array(prediction).reshape(-1, 1)).ravel()
            prediccion_valor = prediction_unescaled[0] 

            # Formatear el valor con separadores de miles y decimales
            prediccion_formateada = locale.format_string("%.2f €", prediccion_valor, grouping=True)
            
            # Mostrar el resultado
            st.success(f"El precio al contado predicho es: {prediccion_formateada}")
        except Exception as e:
            st.error(f"Ocurrió un error durante la predicción: {e}")


    if st.button("Predicción con Red Neuronal"):
        try:
            # Realizar la predicción con 'red_neuronal'
            prediction = red_neuronal.predict(x)
            prediction_unescaled = escalador_y.inverse_transform(np.array(prediction).reshape(-1, 1)).ravel()
            prediccion_valor = prediction_unescaled[0]  

            # Formatear el valor con separadores de miles y decimales
            prediccion_formateada = locale.format_string("%.2f €", prediccion_valor, grouping=True)
            
            # Mostrar el resultado
            st.success(f"El precio al contado predicho es: {prediccion_formateada}")
        except Exception as e:
            st.error(f"Ocurrió un error durante la predicción: {e}")