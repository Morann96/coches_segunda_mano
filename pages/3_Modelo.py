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
import plotly.express as px
import plotly.graph_objects as go
from tensorflow.keras.models import load_model

st.set_page_config(layout="wide")

# Función para conectar a la base de datos
def conectar_base_datos():
    conn = st.connection('mysql', type='sql')
    return conn

# Función para extraer y mostrar datos
def mostrar_datos(tabla):
    conn = conectar_base_datos()
    query = f"SELECT * FROM {tabla}"
    conn.query(query)  # Consulta SQL
    df = conn.query(query)  # Extraer datos como DataFrame
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


model = cargar_modelo(file_name='mejor_modelo.pkl')
red_neuronal = cargar_modelo(file_name='neural_mse.keras')

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
st.markdown("<h1 style='text-align: center;'>Predicción de Precio al Contado</h1>", unsafe_allow_html=True)


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

# Inicializar estados de los botones
if 'datos_guardados' not in st.session_state:
    st.session_state.datos_guardados = False
if 'prediccion_ml' not in st.session_state:
    st.session_state.prediccion_ml = None
if 'prediccion_rn' not in st.session_state:
    st.session_state.prediccion_rn = None

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
col1, col2 = st.columns([2, 3])

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
        kilometraje = st.number_input("Kilometraje (km):", min_value=0, step=1000)
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

    # Función para guardar los datos
    def guardar_datos():
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
        st.session_state.datos_guardados = True

    # Botón para guardar los datos
    st.button("Guardar datos", on_click=guardar_datos)


with col2:
    st.header("Resultados")

    # Mostrar los datos guardados
    if st.session_state.datos_guardados:

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
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')  # En sistemas basados en Unix
    except:
        locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')  # Para Windows

    # Función para predicción con Machine Learning
    def prediccion_ml():
        try:
            # Realizar la predicción
            prediction = model.predict(x)
            prediction_unscaled = escalador_y.inverse_transform(np.array(prediction).reshape(-1, 1)).ravel()
            prediccion_valor = prediction_unscaled[0]

            # Formatear el valor con separadores de miles y decimales
            prediccion_formateada = locale.format_string("%.2f €", prediccion_valor, grouping=True)

            # Guardar el resultado en session_state
            st.session_state.prediccion_ml = prediccion_formateada
        except Exception as e:
            st.error(f"Ocurrió un error durante la predicción: {e}")

    # Función para predicción con Red Neuronal
    def prediccion_rn():
        try:
            # Realizar la predicción con 'red_neuronal'
            prediction = red_neuronal.predict(x)
            prediction_unscaled = escalador_y.inverse_transform(np.array(prediction).reshape(-1, 1)).ravel()
            prediccion_valor = prediction_unscaled[0]

            # Formatear el valor con separadores de miles y decimales
            prediccion_formateada = locale.format_string("%.2f €", prediccion_valor, grouping=True)

            # Guardar el resultado en session_state
            st.session_state.prediccion_rn = prediccion_formateada
        except Exception as e:
            st.error(f"Ocurrió un error durante la predicción: {e}")

    # Botón para predicción con Machine Learning
    if st.session_state.datos_guardados:
        st.button("Predicción con Machine Learning", on_click=prediccion_ml)

        # Mostrar resultado si existe
        if st.session_state.prediccion_ml:
            st.success(f"El precio al contado predicho con ML es de:   {st.session_state.prediccion_ml}")

        # Botón para predicción con Red Neuronal
        st.button("Predicción con Red Neuronal", on_click=prediccion_rn)

        # Mostrar resultado si existe
        if st.session_state.prediccion_rn:
            st.success(f"El precio al contado predicho con RN es de:   {st.session_state.prediccion_rn}")
    else:
        st.warning("Por favor, guarda los datos antes de realizar una predicción.")



if st.session_state.datos_guardados:
    st.markdown("---")
    st.header("Datos Guardados")
    st.dataframe(st.session_state.df)


# Mostrar métricas de todos los modelos

# Cargar el DataFrame de resultados de los modelos
@st.cache_resource
def cargar_resultados_modelos(file_name, directory='notebooks/modelo/'):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'rb') as file:
        return pickle.load(file)

resultados_modelos = cargar_resultados_modelos('resultados_modelos.pkl')

# Mostrar el DataFrame en la aplicación
st.markdown("---")
st.markdown("<h1 style='text-align: center;'>Resultados Comparativos de Modelos</h1>", unsafe_allow_html=True)
st.dataframe(resultados_modelos)


mejor_modelo = resultados_modelos.loc[resultados_modelos['MAE'].idxmin()]

# Extraer y mostrar las métricas
nombre_modelo = mejor_modelo['Nombre_modelo']
mae = mejor_modelo['MAE']
mse = mejor_modelo['MSE']
r2 = mejor_modelo['R2_score']

# Mostrar las métricas del mejor modelo
st.markdown("### Métricas del Mejor Modelo")
st.write(f"- **Nombre del Modelo:** Random Forest")
st.write(f"- **MAE:** {mae:.2f}")
st.write(f"- **MSE:** {mse:.2e}")
st.write(f"- **R²:** {r2:.2f}")

# Explicar las métricas
st.markdown("""
## Explicación de las Métricas de los Modelos Ponderados

En la evaluación de modelos de regresión, utilizamos varias métricas para medir el rendimiento:

- **MAE (Error Absoluto Medio):** Representa el promedio de los errores absolutos entre las predicciones y los valores reales. Un valor menor indica mejores predicciones.

- **MSE (Error Cuadrático Medio):** Es el promedio de los cuadrados de los errores. Penaliza más los errores grandes debido al cuadrado.

- **R² (Coeficiente de Determinación):** Indica la proporción de la varianza de la variable dependiente que es explicada por el modelo. Un valor cercano a 1 indica un buen ajuste.

""")



#Mostrar Feature importance del modelo de ML importado

st.markdown("---")

st.markdown("<h1 style='text-align: center;'>Feature Importance Mejor Modelo</h1>", unsafe_allow_html=True)

importances = model.feature_importances_

x_columns = ["modelo", "potencia_cv", "antiguedad_coche", "log_kilometraje",
             "tipo_cambio", "marca", "distintivo_ambiental_ECO", "distintivo_ambiental_C",
             "combustible_Gasolina", "combustible_Híbrido Enchufable", "combustible_Eléctrico",
             "distintivo_ambiental_B", "combustible_Gasolina/gas", "combustible_Gas"]

# Crear un DataFrame de importancias con las columnas finales y convertir a porcentaje
df_importances = pd.DataFrame(data=zip(x_columns, importances),
                              columns=["Columnas", "Importancia"])
df_importances["Importancia"] = df_importances["Importancia"] * 100  # Convertir a porcentaje
df_importances = df_importances.sort_values("Importancia", ascending=False)

# Establecer el orden de las categorías para la gráfica
df_importances["Columnas"] = pd.Categorical(df_importances["Columnas"],
                                            categories=df_importances["Columnas"],
                                            ordered=True)

# Gráfico interactivo con Plotly en orden descendente y eje X en formato porcentaje
import plotly.express as px
fig = px.bar(df_importances, x="Importancia", y="Columnas", orientation="h",)

# Actualizar etiquetas mostradas al pasar el cursor
fig.update_traces(
    hovertemplate="<b>%{y}</b>: %{x:.2f}%"  # Mostrar dos decimales como porcentaje
)

fig.update_layout(
    height=600,
    margin=dict(l=100, r=40, t=50, b=40),
    xaxis=dict(
        tickformat=".0f",
        title="Importancia (%)",
        title_font=dict(size=18),
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        categoryorder='total ascending',
        title="Columnas",
        title_font=dict(size=18),
        tickfont=dict(size=14)
    ))


st.plotly_chart(fig, use_container_width=True)




# Métricas mejor modelo ya entrenado

resultados_mejor_modelo = cargar_resultados_modelos('resultados_mejor_modelo.pkl')

# Mostrar el DataFrame en la aplicación

st.markdown("<h1 style='text-align: center;'>Resultados del mejor modelo entrenado de nuevo</h1>", unsafe_allow_html=True)
st.dataframe(resultados_mejor_modelo)

st.markdown("---")


# Métricas Redes Neuronales

# Directorio de los archivos
directory = "notebooks/modelo/"


# Diccionario con la información de las redes neuronales
redes_neuronales = {
    "MAE 1": {
        "historial": "historial_neural_mae_1.pkl",
        "resultados": "resultados_neural_mae_1.pkl",
        "modelo": "neural_mae_1.keras"
    },
    "MAE 2": {
        "historial": "historial_neural_mae_2.pkl",
        "resultados": "resultados_neural_mae_2.pkl",
        "modelo": "neural_mae_2.keras"
    },
    "MAE 3": {
        "historial": "historial_neural_mae_3.pkl",
        "resultados": "resultados_neural_mae_3.pkl",
        "modelo": "neural_mae_3.keras"
    },
    "MSE 1": {
        "historial": "historial_neural_mse.pkl",
        "resultados": "resultados_neural_mse.pkl",
        "modelo": "neural_mse.keras"
    },
    "MSE 2": {
        "historial": "historial_neural_mse_2.pkl",
        "resultados": "resultados_neural_mse_2.pkl",
        "modelo": "neural_mse_2.keras"
    },
    "MSE 3": {
        "historial": "historial_neural_mse_3.pkl",
        "resultados": "resultados_neural_mse_3.pkl",
        "modelo": "neural_mse_3.keras"
    }
}

# Funciones para cargar archivos
@st.cache_resource
def cargar_archivo_pkl(file_name):
    with open(os.path.join(directory, file_name), 'rb') as file:
        return pickle.load(file)

@st.cache_resource
def cargar_modelo_keras(file_name):
    return load_model(os.path.join(directory, file_name))

# Visualización en Streamlit
st.title("Comparativa de Redes Neuronales")
st.markdown("""
Este dashboard compara la evolución de la pérdida y los resultados de predicción de seis redes neuronales. 
\nLa escogida fue la llamada MSE 1, que tiene menos pérdida que el resto de alternativas.
""")

col1, col2 = st.columns(2)

# Contadores para alternar entre las columnas
for i, (key, value) in enumerate(redes_neuronales.items()):
    # Alternar entre las columnas
    current_col = col1 if i % 2 == 0 else col2
    
    with current_col:
        # Mostrar el historial de pérdida
        st.markdown(f"### Historial y Resultados de {key}")
        historial = cargar_archivo_pkl(value["historial"])
        loss = historial["loss"]
        val_loss = historial.get("val_loss", None)
        epochs = range(1, len(loss) + 1)

        # Gráfica de la pérdida
        fig_loss = go.Figure()
        fig_loss.add_trace(go.Scatter(x=list(epochs), y=loss, mode='lines', name='Pérdida de Entrenamiento'))
        if val_loss:
            fig_loss.add_trace(go.Scatter(x=list(epochs), y=val_loss, mode='lines', name='Pérdida de Validación'))

        fig_loss.update_layout(
            title=f"Evolución de la Pérdida - {key}",
            xaxis_title='Épocas',
            yaxis_title='Pérdida',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50),
            xaxis=dict(tickmode='linear', tick0=1, dtick=1),
            legend=dict(font=dict(size=10))
        )
        st.plotly_chart(fig_loss, use_container_width=True)

        # Mostrar los resultados de predicción debajo de la gráfica
        st.markdown("#### Resultados:")
        resultados = cargar_archivo_pkl(value["resultados"])
        st.dataframe(resultados)

        # Separador visual entre secciones
        st.markdown("---")





