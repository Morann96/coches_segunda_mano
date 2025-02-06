import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import locale
from tensorflow.keras.models import load_model
import plotly.express as px
import plotly.graph_objects as go

texts = {
    "en": {
        # Títulos y encabezados
        "title_app": "Price Prediction",
        "car_features_title": "Car Features",
        
        # Filtros y entradas
        "filter_brand": "Brand:",
        "filter_model": "Model:",
        "filter_age": "Age (years):",
        "filter_environmental_distinction": "Environmental Distinction:",
        "filter_mileage": "Mileage (km):",
        "filter_power": "Power (HP):",
        "filter_fuel": "Fuel Type:",
        "filter_transmission": "Transmission Type:",
        
        # Botones
        "save_data_button": "Save Data",
        "predict_ml_button": "Prediction with Machine Learning",
        "predict_rn_button": "Prediction with Neural Network",
        
        # Mensajes de advertencia
        "save_data_warning": "Please, save the data before continuing.",
        "save_prediction_warning": "Please, save the data before making a prediction.",
        
        # Mensajes de éxito
        "prediction_ml_success": "The price predicted with ML is: ",
        "prediction_rn_success": "The price predicted with NN is: ",
        
        # Títulos de resultados y tablas
        "results_title": "Results",
        "saved_data_header": "Saved Data",
        "model_comparison_header": "Comparison between Different Models",
        "best_model_results_header": "Results of the Optimized Best Model",
        "feature_importance_header": "Feature Importance of the Best Model",
        "neural_network_comparison_header": "Neural Network Comparison",
        
        # Descripciones y explicaciones
        "neural_network_comparison_description": """
### What Do the Graphs Represent?
The graphs show the evolution of the loss function during the training of a neural network, evaluating how the model improves with each epoch. The lines indicate the following:

- **Training Loss (orange line):** Shows how well the model is fitting the training data.
- **Validation Loss (blue line):** Indicates the model's performance on unseen data (validation data).

### Differences Between MAE and MSE as Loss Functions
- **MAE (Mean Absolute Error):** Less sensitive to large errors (outliers). This makes it more robust if there are extreme data points in the training set.
- **MSE (Mean Squared Error):** Penalizes larger errors more because it squares the differences. It's ideal when you want the model to be more precise with predictions close to the actual values but can be negatively influenced by outliers.

Choosing between MAE and MSE depends on the importance of outliers in the problem you are addressing.

### How Does the Learning Rate Influence?
The learning rate is a key parameter that controls how large the steps the model takes when adjusting its weights during training. In a neural network, weights are numbers that determine the importance of each connection between neurons. During training, these weights are adjusted so that the network can learn from the data and make better predictions.

A low learning rate means the adjustment steps are small. This allows the model to find a more precise solution but can make training slow and even get stuck in local minima, preventing finding the best fit.

On the other hand, a high learning rate means the adjustment steps are large. This allows for faster training but can cause the model to overshoot the best solution and fail to converge properly. Additionally, a high learning rate can cause fluctuations in loss or even prevent it from decreasing.
""",
        
        "model_metrics_explanation": """
## Explanation of Metrics for Different ML Models

When evaluating regression models, we use various metrics to measure performance:

- **MAE (Mean Absolute Error):** Indicates, on average, how much the model's predictions deviate from the actual values.

- **MSE (Mean Squared Error):** Another way to measure error, but instead of averaging the errors directly, it squares the differences. This means larger errors have more weight. It's useful for detecting if the model frequently makes large errors but can result in a very high and hard-to-interpret number.

- **R² (Coefficient of Determination):** This number tells us how well the model understands the data. It ranges from 0 to 1, where 1 means the model is perfect. For example, if R² is 0.90, it means the model explains 90% of the variation in car prices.
""",
        
        "best_model_metrics_explanation": """
We consider the best model to be the one with the highest R². Here are its metrics:

- **Model Name:** {nombre_modelo}  
- **MAE:** {mae:.2f}
- **MSE:** {mse:.2e}
- **R²:** {r2:.2f}
""",
        
        "feature_importance_explanation": """
When we train a Machine Learning model, there are various features in the data that we use to make predictions. **Feature Importance** is a metric that tells us how important these features are to the model.
In other words, it indicates how much each feature contributes to the model's ability to make accurate predictions.

### Utility:
- **Understanding the Model:** Helps us interpret which factors influence the model's decisions the most.
- **Data Optimization:** If some features have very low importance, we can remove them to simplify the model and reduce training time.
- **Decision Making:** Allows us to identify key factors in the data and focus on them to optimize model performance.
""",
        # Feature importance
        "feature_importance_x" : 'Importance (%)',
        'feature_importance_y': 'Columns',
        
        # Gráficas entrenamiento
        "training_evolution_title": "Training Evolution of {key} with learning rate {lr}",
        "training_loss": "Training Loss",
        "validation_loss": "Validation Loss",
        "epochs_title": "Epochs",
        "loss_title": "Loss",
        "neural_network_results_header": "Results:",
    },
    "es": {
        # Títulos y encabezados
        "title_app": "Predicción de Precio",
        "car_features_title": "Características coche",
        
        # Filtros y entradas
        "filter_brand": "Marca:",
        "filter_model": "Modelo:",
        "filter_age": "Antigüedad (años):",
        "filter_environmental_distinction": "Distintivo Ambiental:",
        "filter_mileage": "Kilometraje (km):",
        "filter_power": "Potencia (CV):",
        "filter_fuel": "Combustible:",
        "filter_transmission": "Tipo de Cambio:",
        
        # Botones
        "save_data_button": "Guardar datos",
        "predict_ml_button": "Predicción con Machine Learning",
        "predict_rn_button": "Predicción con Red Neuronal",
        
        # Mensajes de advertencia
        "save_data_warning": "Por favor, guarda los datos antes de continuar.",
        "save_prediction_warning": "Por favor, guarda los datos antes de realizar una predicción.",
        
        # Mensajes de éxito
        "prediction_ml_success": "El precio predicho con ML es de: ",
        "prediction_rn_success": "El precio predicho con RN es de: ",
        
        # Títulos de resultados y tablas
        "results_title": "Resultados",
        "saved_data_header": "Datos Guardados",
        "model_comparison_header": "Comparativa entre distintos modelos",
        "best_model_results_header": "Resultados del mejor modelo optimizado",
        "feature_importance_header": "Feature importance del mejor modelo",
        "neural_network_comparison_header": "Comparativa de Redes Neuronales",
        
        # Descripciones y explicaciones
        
        
        "model_metrics_explanation": """
## Explicación de las métricas de los distintos modelos de ML

En la evaluación de modelos de regresión, utilizamos varias métricas para medir el rendimiento:

- **MAE (Error Absoluto Medio):** Nos dice, en promedio, cuánto se equivoca el modelo en sus predicciones.

- **MSE (Error Cuadrático Medio):** Es otra forma de medir el error, pero en lugar de tomar el promedio de los errores directamente, los eleva al cuadrado. Esto significa que los errores grandes tienen más peso. Es útil para detectar si el modelo comete errores grandes con frecuencia, pero puede ser un número muy alto y difícil de interpretar.

- **R² (Coeficiente de Determinación):** Este número nos dice qué tan bien el modelo entiende los datos. Va de 0 a 1, donde 1 significa que el modelo es perfecto. Por ejemplo, si el R² es 0.90, eso quiere decir que el modelo explica el 90% de la variación en los precios de los coches.
""",
        
        "best_model_metrics_explanation": """
Consideramos el mejor modelo aquél con el mayor R². Estas son sus métricas:

- **Nombre del Modelo:** {nombre_modelo} 
- **MAE:** {mae:.2f}  
- **MSE:** {mse:.2e}  
- **R²:** {r2:.2f}  
""",
        
        "feature_importance_explanation": """
Cuando entrenamos un modelo de Machine Learning, hay distintas características (o "features") en los datos que usamos para hacer predicciones. **Feature Importance** es una métrica que nos dice qué tan importantes son estas características para el modelo.
En otras palabras, indica cuánto contribuye cada característica a la capacidad del modelo para hacer predicciones precisas.

### Utilidad:
- **Entender el modelo:** Nos ayuda a interpretar qué factores influyen más en las decisiones del modelo.
- **Optimización de datos:** Si algunas características tienen muy poca importancia, podemos eliminarlas para simplificar el modelo y reducir el tiempo de entrenamiento.
- **Toma de decisiones:** Nos permite identificar los factores clave en los datos y enfocarnos en ellos para optimizar el rendimiento del modelo.
""",
"neural_network_comparison_description": """
### ¿Qué representan los gráficos?
Los gráficos muestran la evolución de la función de pérdida durante el entrenamiento de una red neuronal, evaluando cómo mejora el modelo con cada época. Las líneas indican lo siguiente:

- **Pérdida de Entrenamiento (línea naranja):** Muestra qué tan bien el modelo está ajustándose a los datos con los que se está entrenando.
- **Pérdida de Validación (línea azul):** Indica el rendimiento del modelo en datos que no ha visto antes (datos de validación).

### ¿Diferencias entre MAE y MSE como función de pérdida?
- **MAE (Error Absoluto Medio):** Es menos sensible a los errores grandes (outliers). Esto lo hace más robusto si existen datos extremos en el conjunto de entrenamiento.
- **MSE (Error Cuadrático Medio):** Penaliza más los errores grandes porque eleva al cuadrado las diferencias. Es ideal cuando quieres que el modelo sea más preciso con predicciones cercanas a los valores reales, pero puede ser influido negativamente por outliers.

Elegir entre MAE y MSE depende de la importancia de los outliers en el problema que estás resolviendo.

### ¿Cómo influye el learning rate?
El learning rate es un parámetro clave que controla qué tan grandes son los pasos que el modelo da al ajustar sus pesos durante el entrenamiento. En una red neuronal, los pesos son números que determinan la importancia de cada conexión entre las neuronas. Durante el entrenamiento, estos pesos se ajustan para que la red pueda aprender de los datos y hacer mejores predicciones.

Un learning rate bajo implica que los pasos de ajuste son pequeños. Esto permite que el modelo encuentre una solución más precisa, pero puede hacer que el entrenamiento sea lento e incluso quedar atrapado en mínimos locales, impidiendo encontrar el mejor ajuste.

Por otro lado, un learning rate alto significa que los pasos de ajuste son grandes. Esto permite entrenar más rápido, pero puede causar que el modelo se salte la mejor solución y no logre converger adecuadamente. Además, un learning rate alto puede provocar fluctuaciones en la pérdida o incluso que esta no disminuya.
""",
        # Feature importance
        "feature_importance_x" : 'Importancia (%)',
        'feature_importance_y': 'Columnas',

        # Gráficas entrenamiento
        "training_evolution_title_es": "Evolución entrenamiento de {key} con learning rate de {lr}",
        "training_evolution_title": "Training Evolution of {key} with learning rate {lr}",
        "training_loss_es": "Pérdida de Entrenamiento",
        "training_loss": "Training Loss",
        "validation_loss_es": "Pérdida de Validación",
        "validation_loss": "Validation Loss",
        "epochs_title_es": "Épocas",
        "epochs_title": "Epochs",
        "loss_title_es": "Pérdida",
        "loss_title": "Loss",
        "neural_network_results_header_es": "Resultados:",
        "neural_network_results_header": "Results:",
    }
}

if 'lang' not in st.session_state:
    st.session_state.lang = "en" 

# 4. Selector de idioma
idioma = st.sidebar.radio(
    'Language',  
    ("English", "Español") 
)

# 5. Actualizar el estado del idioma según la selección
if idioma == "Español":
    st.session_state.lang = "es"
else:
    st.session_state.lang = "en"

lang = st.session_state.lang

# Función para conectar a la base de datos
# def conectar_base_datos():
#     conn = st.connection('mysql', type='sql')
#     return conn

# # Función para extraer y mostrar datos
# def mostrar_datos(tabla):
#     conn = conectar_base_datos()
#     query = f"SELECT * FROM {tabla}"
#     conn.query(query)  # Consulta SQL
#     df = conn.query(query)  # Extraer datos como DataFrame
#     return df

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
st.markdown(f'<h1 style="text-align:center; font-size: 3rem;">{texts[lang]["title_app"]}</h1>', unsafe_allow_html=True)


#tabla = "vista_prestaciones"
#data = mostrar_datos(tabla)
data =pd.read_csv("bin/datos_completos.csv")

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
    st.markdown(f'<h1 style="text-align:center; ">{texts[lang]["car_features_title"]}</h1>', unsafe_allow_html=True)
 
    # Primera fila de filtros
    filtro_col1, filtro_col2 = st.columns(2)
    with filtro_col1:
        # Filtro 1: Marca
        selected_marca = st.selectbox(
            f'{texts[lang]["filter_brand"]}',
            marcas_filtradas,
            index=marcas_filtradas.index(st.session_state.selected_marca) if st.session_state.selected_marca in marcas_filtradas else 0,
            key='selected_marca'
        )
    with filtro_col2:
        # Filtro 2: Modelo
        selected_modelo = st.selectbox(
            f'{texts[lang]["filter_model"]}',
            modelos_filtrados,
            index=modelos_filtrados.index(st.session_state.selected_modelo) if st.session_state.selected_modelo in modelos_filtrados else 0,
            key='selected_modelo'
        )

    # Segunda fila de filtros
    filtro_col3, filtro_col4 = st.columns(2)
    with filtro_col3:
        # Filtro 3: Antigüedad
        antiguedad_coche = st.number_input(f'{texts[lang]["filter_age"]}', min_value=0, step=1)
    with filtro_col4:
        # Filtro 4: Distintivo Ambiental
        distintivo_ambiental = st.selectbox(f'{texts[lang]["filter_environmental_distinction"]}', data['distintivo_ambiental'].dropna().unique())

    # Tercera fila de filtros
    filtro_col5, filtro_col6 = st.columns(2)
    with filtro_col5:
        # Filtro 5: Kilometraje
        kilometraje = st.number_input(f'{texts[lang]["filter_mileage"]}', min_value=1, step=1000)
    with filtro_col6:
        # Filtro 6: Potencia
        potencia_cv = st.number_input(f'{texts[lang]["filter_power"]}', min_value=0, step=10)

    # Cuarta fila de filtros
    filtro_col7, filtro_col8 = st.columns(2)
    with filtro_col7:
        # Filtro 7: Combustible
        combustible = st.selectbox(f'{texts[lang]["filter_fuel"]}', data['combustible'].dropna().unique())
    with filtro_col8:
        # Filtro 8: Tipo de Cambio
        tipo_cambio = st.selectbox(f'{texts[lang]["filter_transmission"]}', data['tipo_cambio'].dropna().unique())

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
    st.button(f'{texts[lang]["save_data_button"]}', on_click=guardar_datos)


with col2:
    st.markdown(f'<h1 style="text-align:center; ">{texts[lang]["results_title"]}</h1>', unsafe_allow_html=True)

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
            st.warning(f'{texts[lang]["save_data_warning"]}')

    # Configurar la localización para España
    try:
        if sys.platform.startswith('win'):
            # Para Windows
            locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
        else:
            # Para sistemas Unix (Linux, macOS, etc.)
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except locale.Error:
        # Si no se puede establecer ninguno de los locales deseados,
        # usar el locale predeterminado del sistema
        locale.setlocale(locale.LC_ALL, '')

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

        st.button(f'{texts[lang]["predict_ml_button"]}', on_click=prediccion_ml)

        # Mostrar resultado si existe
        if st.session_state.prediccion_ml:
            st.success(f'{texts[lang]["prediction_ml_success"]}    {st.session_state.prediccion_ml}')

        # Botón para predicción con Red Neuronal
        st.button(f'{texts[lang]["predict_rn_button"]}', on_click=prediccion_rn)

        # Mostrar resultado si existe
        if st.session_state.prediccion_rn:
            st.success(f'{texts[lang]["prediction_rn_success"]}   {st.session_state.prediccion_rn}')
    else:
        st.warning(f'{texts[lang]["save_prediction_warning"]}')

if st.session_state.datos_guardados:
    #st.markdown("---")
        st.header(f'{texts[lang]["saved_data_header"]}')
        st.dataframe(st.session_state.df)

# Mostrar métricas de todos los modelos
# Cargar el DataFrame de resultados de los modelos
@st.cache_resource
def cargar_resultados_modelos(file_name, directory='notebooks/modelo/'):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'rb') as file:
        return pickle.load(file)

resultados_modelos = cargar_resultados_modelos('resultados_modelos.pkl')
resultados_mejor_modelo = cargar_resultados_modelos('resultados_mejor_modelo.pkl')

if lang == 'es':
    nuevos_nombres_columnas = {
        'Nombre_modelo': 'Nombre Modelo',
        'MAE': 'MAE',
        'MSE': 'MSE',
        'R2_score': 'R² Score'
    }

    resultados_modelos_display = resultados_modelos.rename(columns=nuevos_nombres_columnas)
    resultados_mejor_modelo_display = resultados_mejor_modelo.rename(columns=nuevos_nombres_columnas)

else: 
    nuevos_nombres_columnas = {
        'Nombre_modelo': 'Model Name',
        'MAE': 'MAE',
        'MSE': 'MSE',
        'R2_score': 'R² Score'
    }
    resultados_modelos_display = resultados_modelos.rename(columns=nuevos_nombres_columnas)
    resultados_mejor_modelo_display = resultados_mejor_modelo.rename(columns=nuevos_nombres_columnas)

# Mostrar el DataFrame en la aplicación
st.markdown("---")
st.markdown(f'<h1 style="text-align:left; ">{texts[lang]["model_comparison_header"]}</h1>', unsafe_allow_html=True)
st.dataframe(resultados_modelos_display)


mejor_modelo = resultados_modelos.loc[resultados_modelos['R2_score'].idxmax()]

# Explicar las métricas
st.markdown(texts[lang]["model_metrics_explanation"])

# Extraer y mostrar las métricas
nombre_modelo = mejor_modelo['Nombre_modelo']
mae = mejor_modelo['MAE']
mse = mejor_modelo['MSE']
r2 = mejor_modelo['R2_score']

st.write(texts[lang]['best_model_metrics_explanation'].format (nombre_modelo = nombre_modelo, mae = mae, mse = mse, r2 = r2))


#Mostrar Feature importance del modelo de ML importado

st.markdown("---")

st.markdown(f'<h1 style="text-align:left; ">{texts[lang]["feature_importance_header"]}</h1>', unsafe_allow_html=True)

st.markdown(texts[lang]["feature_importance_explanation"])

importances = model.feature_importances_

x_columns = ['marca', 'modelo', 'potencia_cv', 'antiguedad_coche', 'log_kilometraje',
       'tipo_cambio', 'combustible_Eléctrico', 'combustible_Gas',
       'combustible_Gasolina', 'combustible_Gasolina/gas',
       'combustible_Híbrido Enchufable', 'distintivo_ambiental_B',
       'distintivo_ambiental_C', 'distintivo_ambiental_ECO']

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
        title=texts[lang]['feature_importance_x'],
        title_font=dict(size=18),
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        categoryorder='total ascending',
        title=texts[lang]['feature_importance_y'],
        title_font=dict(size=18),
        tickfont=dict(size=14)
    ))


st.plotly_chart(fig, use_container_width=True)

# Métricas mejor modelo ya entrenado

resultados_mejor_modelo = cargar_resultados_modelos('resultados_mejor_modelo.pkl')

# Mostrar el DataFrame en la aplicación

#st.markdown("<h1 style='text-align: left;'>Resultados del mejor modelo optimizado</h1>", unsafe_allow_html=True)
st.markdown(f'<h1 style="text-align:left; ">{texts[lang]["best_model_results_header"]}</h1>', unsafe_allow_html=True)
st.dataframe(resultados_mejor_modelo_display)

st.markdown("---")


# Métricas Redes Neuronales

# Directorio de los archivos
directory = "notebooks/modelo/"


# Diccionario con la información de las redes neuronales
redes_neuronales = {
    "MAE 1": {
        "historial": "historial_neural_mae_1.pkl",
        "resultados": "resultados_neural_mae_1.pkl",
        "modelo": "neural_mae_1.keras",
        'learning_rate' : '0.50%'
    },
    "MAE 2": {
        "historial": "historial_neural_mae_2.pkl",
        "resultados": "resultados_neural_mae_2.pkl",
        "modelo": "neural_mae_2.keras",
        'learning_rate' : '0.30%'
    },
    "MAE 3": {
        "historial": "historial_neural_mae_3.pkl",
        "resultados": "resultados_neural_mae_3.pkl",
        "modelo": "neural_mae_3.keras",
        'learning_rate' : '0.35%'
    },
    "MSE 1": {
        "historial": "historial_neural_mse.pkl",
        "resultados": "resultados_neural_mse.pkl",
        "modelo": "neural_mse.keras",
        'learning_rate' : '0.50%'
    },
    "MSE 2": {
        "historial": "historial_neural_mse_2.pkl",
        "resultados": "resultados_neural_mse_2.pkl",
        "modelo": "neural_mse_2.keras",
        'learning_rate' : '0.30%'
    },
    "MSE 3": {
        "historial": "historial_neural_mse_3.pkl",
        "resultados": "resultados_neural_mse_3.pkl",
        "modelo": "neural_mse_3.keras",
        'learning_rate' : '0.35%'
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
st.title(f'{texts[lang]["neural_network_comparison_header"]}')

st.markdown(texts[lang]["neural_network_comparison_description"])

col1, col2 = st.columns(2)

# Contadores para alternar entre las columnas
for i, (key, value) in enumerate(redes_neuronales.items()):
    # Alternar entre las columnas
    current_col = col1 if i % 2 == 0 else col2
    lr = value['learning_rate']
    
    with current_col:
        # Formatear el título dinámico según el idioma
        if lang == "en":
            title = texts[lang]["training_evolution_title"].format(key=key, lr=lr)
        else:
            title = texts[lang]["training_evolution_title_es"].format(key=key, lr=lr)
        
        # Mostrar el título
        st.markdown(f"### {title}")
        
        historial = cargar_archivo_pkl(value["historial"])
        loss = historial["loss"]
        val_loss = historial.get("val_loss", None)
        epochs = range(1, len(loss) + 1)

        # Gráfica de la pérdida
        fig_loss = go.Figure()
        if lang == "en":
            fig_loss.add_trace(go.Scatter(
                x=list(epochs), y=loss,
                mode='lines', name=texts[lang]["training_loss"],
                line=dict(color='orange')
            ))
            if val_loss:
                fig_loss.add_trace(go.Scatter(
                    x=list(epochs), y=val_loss, 
                    mode='lines', name=texts[lang]["validation_loss"]
                ))
            fig_loss.update_layout(
                title=f"Loss Evolution - {key}",
                xaxis_title=texts[lang]["epochs_title"],
                yaxis_title=texts[lang]["loss_title"],
                height=400,
                margin=dict(l=50, r=50, t=50, b=50),
                xaxis=dict(tickmode='linear', tick0=1, dtick=1),
                legend=dict(font=dict(size=10))
            )
        else:
            fig_loss.add_trace(go.Scatter(
                x=list(epochs), y=loss,
                mode='lines', name=texts[lang]["training_loss_es"],
                line=dict(color='orange')
            ))
            if val_loss:
                fig_loss.add_trace(go.Scatter(
                    x=list(epochs), y=val_loss, 
                    mode='lines', name=texts[lang]["validation_loss_es"]
                ))
            fig_loss.update_layout(
                title=f"Evolución de la Pérdida - {key}",
                xaxis_title=texts[lang]["epochs_title_es"],
                yaxis_title=texts[lang]["loss_title_es"],
                height=400,
                margin=dict(l=50, r=50, t=50, b=50),
                xaxis=dict(tickmode='linear', tick0=1, dtick=1),
                legend=dict(font=dict(size=10))
            )
        
        st.plotly_chart(fig_loss, use_container_width=True)

        # Mostrar los resultados de predicción debajo de la gráfica
        if lang == "en":
            results_header = texts[lang]["neural_network_results_header"]
        else:
            results_header = texts[lang]["neural_network_results_header_es"]
        
        st.markdown(f"#### {results_header}")
        resultados = cargar_archivo_pkl(value["resultados"])

        if lang == 'en':
            nuevos_nombres_columnas = {
                'Número de épocas': 'Epochs Number',
                'MSE final': 'Final MSE',
                'MAE final': 'Final MAE'
            }

            resultados_nn_display = resultados.rename(columns=nuevos_nombres_columnas)

        else: 
            resultados_nn_display = resultados

        st.dataframe(resultados_nn_display)

        # Separador visual entre secciones
        st.markdown("---")






