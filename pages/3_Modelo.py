import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import mysql.connector
from datetime import datetime
import locale

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

# Cargar modelo
@st.cache_resource
def load_model():
    with open('notebooks/modelo/mejor_modelo.pkl', 'rb') as file:
        return pickle.load(file)

# Uso del modelo
data = mostrar_datos(tabla)
model = load_model()



# Pedir entrada de usuario para las características
st.header("Introduce las características para la predicción")



# Creamos la columna fecha_matriculacion para calcular la antigüedad del coche en años

data['fecha_matriculacion'] = (
    '01/' + data['mes_matriculacion'].astype(int).astype(str) + 
    '/' + data['ano_matriculacion'].astype(int).astype(str))

data['fecha_matriculacion'] = pd.to_datetime(data['fecha_matriculacion'], format='%d/%m/%Y')
current_date = pd.to_datetime(datetime.now())

data['antiguedad_coche'] = ((current_date - data['fecha_matriculacion']).dt.days / 365.25).round(2)



# Creamos los inputs para el usuario

categorical_features = ["marca", "modelo", "distintivo_ambiental", "tipo_cambio", "combustible", "num_puertas"]
numeric_features = ["potencia_cv", "antiguedad_coche", 'kilometraje']

columnas_modelo = ['marca', 'modelo', 'potencia_cv', 'antiguedad_coche', 'log_kilometraje', 'tipo_cambio', 'distintivo_ambiental', 'combustible']


# Encoders

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

input_data = {}


for feature in categorical_features:
    input_data[feature] = st.selectbox(f"Selecciona {feature.replace('_', ' ')}:", data[feature].unique())

for feature in numeric_features:
    input_data[feature] = st.number_input(f"Introduce {feature.replace('_', ' ')}:", min_value=0, step=1)

# Crear un DataFrame para las entradas del usuario en el estado de sesión
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()  # Inicializamos un DataFrame vacío

# Botón para guardar los datos del usuario en el DataFrame
if st.button("Guardar datos"):
    # Convertir las entradas del usuario a un DataFrame y almacenarlo
    st.session_state.df = pd.DataFrame([input_data])
    st.write("Datos guardados en el DataFrame:")
    st.dataframe(st.session_state.df)



# Operaciones adicionales con el DataFrame del usuario
if not st.session_state.df.empty:

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

    x = escalador_X.transform(df_temp)


else:
    st.warning("Por favor, guarda los datos antes de continuar.")


# Configurar la localización para España
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')  # En sistemas basados en Unix
# Para Windows, puedes intentar con 'Spanish_Spain.1252'

# Botón para predecir
if st.button("Predecir"):
    try:
        # Realizar la predicción
        prediction = model.predict(x)
        prediction_unescaled = escalador_y.inverse_transform(np.array(prediction).reshape(-1, 1)).ravel()
        prediccion_valor = prediction_unescaled[0]  # Extraer el valor escalar

        # Formatear el valor con separadores de miles y decimales
        prediccion_formateada = locale.format_string("%.2f €", prediccion_valor, grouping=True)
        
        # Mostrar el resultado
        st.success(f"El precio al contado predicho es: {prediccion_formateada}")
    except Exception as e:
        st.error(f"Ocurrió un error durante la predicción: {e}")


