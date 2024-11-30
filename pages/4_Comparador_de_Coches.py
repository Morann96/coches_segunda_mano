import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import base64
import numpy as np
import plotly.graph_objects as go
import io
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Conexión a la base de datos
def conectar_base_datos():
    conn = st.connection('mysql', type='sql')
    return conn

# Función para cargar datos desde la base de datos
def cargar_datos():
    conn = conectar_base_datos()
    query = "SELECT * FROM vista_prestaciones_img" 
    df = conn.query(query)
    return df

# Función para convertir datos binarios a imagen
def convertir_binario_a_imagen(binario):
    if binario is not None:
        return Image.open(BytesIO(binario))
    else:
        return None
    
def imagen_to_base64(imagen):
    buffered = BytesIO()
    imagen.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def mostrar_coche(imagen):
    if imagen:
        imagen_base64 = imagen_to_base64(imagen)
        st.markdown(
            f"""
            <div style="
                display: flex; 
                justify-content: center; 
                align-items: center; 
                margin-bottom: 10px; 
                height: 350px; /* Establece la altura fija del contenedor */
            ">
                <img src="data:image/png;base64,{imagen_base64}" style="
                    max-width: 100%; 
                    max-height: 100%; 
                    object-fit: contain; /* Ajusta la imagen dentro del contenedor sin deformarla */
                ">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Mostrar un marcador de "Imagen no disponible" con la misma altura fija
        st.markdown(
            """
            <div style="
                display: flex; 
                justify-content: center; 
                align-items: center; 
                margin-bottom: 20px; 
                height: 350px; /* Misma altura fija que el contenedor de la imagen */
                background-color: #f0f0f0; 
                border: 1px solid #ccc; 
                border-radius: 5px;
            ">
                <p style="text-align: center; font-size: 16px; color: #555;">Imagen no disponible</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("""
    <style>
    /* Reducir márgenes de los selectores */
    div[data-baseweb="select"] {
        width: 135px !important; /* Mantener ancho uniforme */
        margin: 5px 10px !important; /* Ajustar márgenes generales */
    }

    /* Reducir espacio entre el título y el selector */
    p.titulo-select {
        margin-bottom: 1px !important; /* Controlar el margen inferior del título */
        text-align: center; /* Centrar texto del título */
    }
    </style>
    """, unsafe_allow_html=True)

# Cargar datos
df = cargar_datos()

# Reemplazar valores nulos solo en columnas categóricas
columnas_categoricas = ['marca', 'modelo', 'tipo_cambio', 'combustible', 'distintivo_ambiental']
df[columnas_categoricas] = df[columnas_categoricas].fillna('Desconocido')

# Asegurar que las columnas numéricas son de tipo numérico
columnas_numericas = ['precio_contado', 'kilometraje', 'potencia_cv', 'velocidad_max', 'aceleracion', 'consumo_medio', 'peso', 'capacidad_maletero']
df[columnas_numericas] = df[columnas_numericas].apply(pd.to_numeric, errors='coerce')

# Título de la página
st.markdown("<h1 style='text-align: center;'>Comparador de coches</h1>", unsafe_allow_html=True)

# Dividir en 5 columnas principales
col1, col2, col3, col4, col5 = st.columns([1, 4, 1, 4, 1])

# Columna vacía (espacio a la izquierda)
with col1:
    st.empty()

# Filtros para el Coche 1
with col2:
    st.markdown(f"<h3 style='text-align: center;'>Coche 1</h3>", unsafe_allow_html=True)

    # Primera fila de filtros
    fila1_coche1 = st.columns(4)
    with fila1_coche1[0]:
        st.markdown("<p class='titulo-select'>Marca</p>", unsafe_allow_html=True)
        marcas_disponibles = df["marca"].sort_values().unique()
        if len(marcas_disponibles) > 0:
            marca1 = st.selectbox("Marca", marcas_disponibles, key="marca1", label_visibility="collapsed")
        else:
            st.write("No hay marcas disponibles.")
            st.stop()
    with fila1_coche1[1]:
        st.markdown("<p class='titulo-select'>Modelo</p>", unsafe_allow_html=True)
        modelos_disponibles = df[df["marca"] == marca1]["modelo"].sort_values().unique()
        if len(modelos_disponibles) > 0:
            modelo1 = st.selectbox("Modelo", modelos_disponibles, key="modelo1", label_visibility="collapsed")
        else:
            st.write("No hay modelos disponibles para esta marca.")
            st.stop()
    with fila1_coche1[2]:
        st.markdown("<p class='titulo-select'>Año</p>", unsafe_allow_html=True)
        anos_disponibles = df[(df["marca"] == marca1) & (df["modelo"] == modelo1)]["ano_matriculacion"].sort_values().unique()
        if len(anos_disponibles) > 0:
            ano1 = st.selectbox("Año", anos_disponibles, key="ano1", label_visibility="collapsed")
        else:
            st.write("No hay años disponibles para este modelo.")
            st.stop()
    with fila1_coche1[3]:
        st.markdown("<p class='titulo-select'>Cambio</p>", unsafe_allow_html=True)
        cambios_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1)
        ]["tipo_cambio"].sort_values().unique()
        if len(cambios_disponibles) > 0:
            tipo_cambio1 = st.selectbox("Tipo cambio", cambios_disponibles, key="tipo_cambio1", label_visibility="collapsed")
        else:
            st.write("No hay tipos de cambio disponibles para este año.")
            st.stop()

    # Segunda fila de filtros
    fila2_coche1 = st.columns(4)
    with fila2_coche1[0]:
        st.markdown("<p class='titulo-select'>Combustible</p>", unsafe_allow_html=True)
        combustibles_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1) &
            (df["tipo_cambio"] == tipo_cambio1)
        ]["combustible"].sort_values().unique()
        if len(combustibles_disponibles) > 0:
            combustible1 = st.selectbox("Combustible", combustibles_disponibles, key="combustible1", label_visibility="collapsed")
        else:
            combustible1 = 'Desconocido'  # Asignar valor por defecto
    with fila2_coche1[1]:
        st.markdown("<p class='titulo-select'>Distintivo</p>", unsafe_allow_html=True)
        distintivos_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1) &
            (df["tipo_cambio"] == tipo_cambio1) &
            (df["combustible"] == combustible1)
        ]["distintivo_ambiental"].sort_values().unique()
        if len(distintivos_disponibles) > 0:
            distintivo1 = st.selectbox("Distintivo", distintivos_disponibles, key="distintivo1", label_visibility="collapsed")
        else:
            distintivo1 = 'Desconocido'  # Asignar valor por defecto
    with fila2_coche1[2]:
        st.markdown("<p class='titulo-select'>Potencia (CV)</p>", unsafe_allow_html=True)
        potencias_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1) &
            (df["tipo_cambio"] == tipo_cambio1) &
            (df["combustible"] == combustible1) &
            (df["distintivo_ambiental"] == distintivo1)
        ]["potencia_cv"].sort_values().unique()
        if len(potencias_disponibles) > 0:
            potencia1 = st.selectbox("Potencia", potencias_disponibles, key="potencia1", label_visibility="collapsed")
        else:
            st.write("No hay potencias disponibles para este distintivo.")
            st.stop()
    with fila2_coche1[3]:
        st.markdown("<p class='titulo-select'>Kilometraje</p>", unsafe_allow_html=True)
        kilometrajes_disponibles = df[
            (df["marca"] == marca1) &
            (df["modelo"] == modelo1) &
            (df["ano_matriculacion"] == ano1) &
            (df["tipo_cambio"] == tipo_cambio1) &
            (df["combustible"] == combustible1) &
            (df["distintivo_ambiental"] == distintivo1) &
            (df["potencia_cv"] == potencia1)
        ]["kilometraje"].sort_values().unique()
        if len(kilometrajes_disponibles) > 0:
            kilometraje1 = st.selectbox("Kilometraje", kilometrajes_disponibles, key="kilometraje1", label_visibility="collapsed")
        else:
            st.write("No hay kilometrajes disponibles para esta potencia.")
            st.stop()

# Columna vacía (espacio entre los coches)
with col3:
    st.empty()

# Filtros para el Coche 2
with col4:
    st.markdown(f"<h3 style='text-align: center;'>Coche 2</h3>", unsafe_allow_html=True)

    # Primera fila de filtros
    fila1_coche2 = st.columns(4)
    with fila1_coche2[0]:
        st.markdown("<p class='titulo-select'>Marca</p>", unsafe_allow_html=True)
        marcas_disponibles = df["marca"].sort_values().unique()
        if len(marcas_disponibles) > 0:
            marca2 = st.selectbox("Marca", marcas_disponibles, key="marca2", label_visibility="collapsed")
        else:
            st.write("No hay marcas disponibles.")
            st.stop()
    with fila1_coche2[1]:
        st.markdown("<p class='titulo-select'>Modelo</p>", unsafe_allow_html=True)
        modelos_disponibles = df[df["marca"] == marca2]["modelo"].sort_values().unique()
        if len(modelos_disponibles) > 0:
            modelo2 = st.selectbox("Modelo", modelos_disponibles, key="modelo2", label_visibility="collapsed")
        else:
            st.write("No hay modelos disponibles para esta marca.")
            st.stop()
    with fila1_coche2[2]:
        st.markdown("<p class='titulo-select'>Año</p>", unsafe_allow_html=True)
        anos_disponibles = df[(df["marca"] == marca2) & (df["modelo"] == modelo2)]["ano_matriculacion"].sort_values().unique()
        if len(anos_disponibles) > 0:
            ano2 = st.selectbox("Año", anos_disponibles, key="ano2", label_visibility="collapsed")
        else:
            st.write("No hay años disponibles para este modelo.")
            st.stop()
    with fila1_coche2[3]:
        st.markdown("<p class='titulo-select'>Cambio</p>", unsafe_allow_html=True)
        cambios_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2)
        ]["tipo_cambio"].sort_values().unique()
        if len(cambios_disponibles) > 0:
            tipo_cambio2 = st.selectbox("Tipo cambio", cambios_disponibles, key="tipo_cambio2", label_visibility="collapsed")
        else:
            st.write("No hay tipos de cambio disponibles para este año.")
            st.stop()

    # Segunda fila de filtros
    fila2_coche2 = st.columns(4)
    with fila2_coche2[0]:
        st.markdown("<p class='titulo-select'>Combustible</p>", unsafe_allow_html=True)
        combustibles_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2) &
            (df["tipo_cambio"] == tipo_cambio2)
        ]["combustible"].sort_values().unique()
        if len(combustibles_disponibles) > 0:
            combustible2 = st.selectbox("Combustible", combustibles_disponibles, key="combustible2", label_visibility="collapsed")
        else:
            combustible2 = 'Desconocido'  # Asignar valor por defecto
    with fila2_coche2[1]:
        st.markdown("<p class='titulo-select'>Distintivo</p>", unsafe_allow_html=True)
        distintivos_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2) &
            (df["tipo_cambio"] == tipo_cambio2) &
            (df["combustible"] == combustible2)
        ]["distintivo_ambiental"].sort_values().unique()
        if len(distintivos_disponibles) > 0:
            distintivo2 = st.selectbox("Distintivo", distintivos_disponibles, key="distintivo2", label_visibility="collapsed")
        else:
            distintivo2 = 'Desconocido'  # Asignar valor por defecto
    with fila2_coche2[2]:
        st.markdown("<p class='titulo-select'>Potencia (CV)</p>", unsafe_allow_html=True)
        potencias_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2) &
            (df["tipo_cambio"] == tipo_cambio2) &
            (df["combustible"] == combustible2) &
            (df["distintivo_ambiental"] == distintivo2)
        ]["potencia_cv"].sort_values().unique()
        if len(potencias_disponibles) > 0:
            potencia2 = st.selectbox("Potencia", potencias_disponibles, key="potencia2", label_visibility="collapsed")
        else:
            st.write("No hay potencias disponibles para este distintivo.")
            st.stop()
    with fila2_coche2[3]:
        st.markdown("<p class='titulo-select'>Kilometraje</p>", unsafe_allow_html=True)
        kilometrajes_disponibles = df[
            (df["marca"] == marca2) &
            (df["modelo"] == modelo2) &
            (df["ano_matriculacion"] == ano2) &
            (df["tipo_cambio"] == tipo_cambio2) &
            (df["combustible"] == combustible2) &
            (df["distintivo_ambiental"] == distintivo2) &
            (df["potencia_cv"] == potencia2)
        ]["kilometraje"].sort_values().unique()
        if len(kilometrajes_disponibles) > 0:
            kilometraje2 = st.selectbox("Kilometraje", kilometrajes_disponibles, key="kilometraje2", label_visibility="collapsed")
        else:
            st.write("No hay kilometrajes disponibles para esta potencia.")
            st.stop()

# Columna vacía (espacio a la derecha)
with col5:
    st.empty()

# Dividir en dos columnas principales para Coche 1 y Coche 2
col1, col2, col3, col4, col5 = st.columns([1, 4, 1, 4, 1])

# Configuración para Coche 1
with col1:
    st.empty()

with col2:
    # Mostrar imagen debajo de los filtros
    df_filtrado1 = df[
        (df["marca"] == marca1)
        & (df["modelo"] == modelo1)
        & (df["ano_matriculacion"] == ano1)
        & (df["tipo_cambio"] == tipo_cambio1)
        & (df["combustible"] == combustible1)
        & (df["distintivo_ambiental"] == distintivo1)
        & (df["potencia_cv"] == potencia1)
        & (df["kilometraje"] == kilometraje1)
    ].copy()  # Crear una copia explícita

    if not df_filtrado1.empty:
        datos_coche1 = df_filtrado1.iloc[0]
        foto_binaria = datos_coche1["foto_binaria"]

        try: 
            imagen1 = convertir_binario_a_imagen(foto_binaria)
        except Exception as e:
            print(f"Error al cargar la imagen del coche 1: {e}")
            imagen1 = None

        mostrar_coche(imagen1)
        
    else:
        st.write(f"No se encontraron datos para el {marca1} {modelo1} ({ano1}) con los filtros seleccionados.")

with col3:
    st.empty()

# Configuración para Coche 2
with col4:
    # Mostrar imagen debajo de los filtros
    df_filtrado2 = df[
        (df["marca"] == marca2)
        & (df["modelo"] == modelo2)
        & (df["ano_matriculacion"] == ano2)
        & (df["tipo_cambio"] == tipo_cambio2)
        & (df["combustible"] == combustible2)
        & (df["distintivo_ambiental"] == distintivo2)
        & (df["potencia_cv"] == potencia2)
        & (df["kilometraje"] == kilometraje2)
    ].copy()  # Crear una copia explícita

    if not df_filtrado2.empty:
        datos_coche2 = df_filtrado2.iloc[0]
        foto_binaria = datos_coche2["foto_binaria"]

        try: 
            imagen2 = convertir_binario_a_imagen(foto_binaria)
        except Exception as e:
            print(f"Error al cargar la imagen del coche 2: {e}")
            imagen2 = None

        mostrar_coche(imagen2)
       
    else:
        st.write(f"No se encontraron datos para el {marca2} {modelo2} ({ano2}) con los filtros seleccionados.")

with col5:
    st.empty()

columnas_seleccionadas = [
    "precio_contado", "kilometraje", "potencia_cv", 
    "velocidad_max", "aceleracion", "consumo_medio", "peso", 
    "capacidad_maletero"
]

if not df_filtrado1.empty and not df_filtrado2.empty:

    # Crear copia del DataFrame con las columnas seleccionadas
    df_todos_los_coches = df[columnas_seleccionadas].copy()

    # Asegurar que las columnas numéricas son de tipo numérico
    df_todos_los_coches = df_todos_los_coches.apply(pd.to_numeric, errors='coerce')

    columnas_log = ["precio_contado", "kilometraje", "potencia_cv"]
    for col in columnas_log:
        # Reemplazar valores nulos o negativos antes de aplicar log
        df_todos_los_coches[col] = df_todos_los_coches[col].fillna(0)
        df_todos_los_coches[col] = df_todos_los_coches[col].apply(lambda x: np.log1p(x) if x >= 0 else 0)

    # Normalizar las columnas numéricas
    min_vals = {}
    max_vals = {}

    for col in df_todos_los_coches.columns:
        min_vals[col] = df_todos_los_coches[col].min()
        max_vals[col] = df_todos_los_coches[col].max()


    # Función para normalizar un DataFrame utilizando min y max
    def normalize_df(df_to_normalize, min_vals, max_vals, columnas_log):
        df_normalized = df_to_normalize.copy()
        for col in columnas_log:
            df_normalized[col] = df_normalized[col].fillna(0)
            df_normalized[col] = df_normalized[col].apply(lambda x: np.log1p(x) if x >= 0 else 0)
        for col in df_normalized.columns:
            min_val = min_vals[col]
            max_val = max_vals[col]
            if max_val - min_val != 0:
                if col != 'aceleracion':
                    df_normalized[col] = (df_normalized[col] - min_val) / (max_val - min_val)
                else:
                    df_normalized[col] = (max_val - df_normalized[col]) / (max_val - min_val)
            else:
                df_normalized[col] = 0.0
        return df_normalized
    
    # Normalizar los DataFrames filtrados
    df_filtrado1_normalized = normalize_df(df_filtrado1[columnas_seleccionadas].copy(), min_vals, max_vals, columnas_log)
    df_filtrado2_normalized = normalize_df(df_filtrado2[columnas_seleccionadas].copy(), min_vals, max_vals, columnas_log)

    # Combinar los DataFrames normalizados
    df_normalizado_seleccionados = pd.concat([df_filtrado1_normalized, df_filtrado2_normalized], ignore_index=True)

    # Combinar los DataFrames originales (no normalizados) para verificar columnas válidas
    df_combinado = pd.concat([df_filtrado1[columnas_seleccionadas], df_filtrado2[columnas_seleccionadas]], ignore_index=True).copy()

    columnas_validas = [col for col in columnas_seleccionadas if df_combinado[col].notnull().all()]

    if columnas_validas:
        # Crear un DataFrame con solo las columnas válidas y hacer una copia
        df_radar = df_normalizado_seleccionados[columnas_validas].copy()

        columnas_legibles = {
            "precio_contado": "Precio",
            "kilometraje": "Kilometraje",
            "potencia_cv": "Potencia (CV)",
            "velocidad_max": "Velocidad Máxima",
            "aceleracion": "Aceleración",
            "consumo_medio": "Consumo Medio",
            "peso": "Peso",
            "capacidad_maletero": "Capacidad del Maletero"
        }

        # Renombrar las columnas para que sean más legibles
        df_radar = df_radar.rename(columns=columnas_legibles)

        # Preparar los datos para el gráfico
        categorias = df_radar.columns.tolist()
        valores_coche1 = df_radar.iloc[0].tolist()  # Valores del coche 1
        valores_coche2 = df_radar.iloc[1].tolist()  # Valores del coche 2

        # Agregar el primer y último valor para cerrar el radar
        valores_coche1.append(valores_coche1[0])
        valores_coche2.append(valores_coche2[0])
        categorias.append(categorias[0])

        # Obtener los nombres personalizados para la leyenda
        nombre_coche1 = f"{df_filtrado1['marca'].iloc[0]} {df_filtrado1['modelo'].iloc[0]}"
        nombre_coche2 = f"{df_filtrado2['marca'].iloc[0]} {df_filtrado2['modelo'].iloc[0]}"

        # Crear cinco columnas de igual ancho
        col1, col2, col3, col4, col5 = st.columns([1, 7, 1, 7, 1])

        with col4:
            inner_col1, inner_col2, inner_col3 = st.columns([1, 5, 1])

            with inner_col1:
                st.empty()

            with inner_col2:

                # Combinar los datos de los coches seleccionados y crear una copia explícita
                df_combinado = pd.concat([df_filtrado1[columnas_seleccionadas], df_filtrado2[columnas_seleccionadas]], ignore_index=True).copy()

                # Obtener los nombres personalizados para las columnas (marca y modelo de los coches)
                if (df_filtrado1['marca'].iloc[0] == df_filtrado2['marca'].iloc[0]) and (df_filtrado1['modelo'].iloc[0] == df_filtrado2['modelo'].iloc[0]):
                    # Si la marca y el modelo son iguales, añadir '1' y '2'
                    nombre_coche1 = f"{df_filtrado1['marca'].iloc[0]} {df_filtrado1['modelo'].iloc[0]} 1"
                    nombre_coche2 = f"{df_filtrado2['marca'].iloc[0]} {df_filtrado2['modelo'].iloc[0]} 2"
                else:
                    # Si son diferentes, usar los nombres sin '1' y '2'
                    nombre_coche1 = f"{df_filtrado1['marca'].iloc[0]} {df_filtrado1['modelo'].iloc[0]}"
                    nombre_coche2 = f"{df_filtrado2['marca'].iloc[0]} {df_filtrado2['modelo'].iloc[0]}"

                # Transponer el dataframe y asignar los nombres de las columnas
                df_combinado_transpuesto = df_combinado.T.copy()  # Crear una copia explícita
                df_combinado_transpuesto.columns = [nombre_coche1, nombre_coche2]

                # Renombrar las filas (índice) del dataframe transpuesto sin inplace=True
                df_combinado_transpuesto = df_combinado_transpuesto.rename(index=columnas_legibles)

                # Añadir espacio vertical antes del DataFrame
                st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

                st.dataframe(df_combinado_transpuesto)

            with inner_col3: 
                st.empty()


        # Colocar el gráfico en la segunda columna
        with col2:
            # Crear un marcador de posición para el gráfico
            graph_placeholder = st.empty()

            slider_col1, slider_col2, slider_col3 = st.columns([1, 2, 1]) 

            with slider_col1:
                st.empty()  # Espacio vacío a la izquierda

            with slider_col2:
                # Añadir espacio superior para mover el slider hacia abajo
                st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Ajusta la altura según necesidad

                # Colocar el slider dentro de la columna central
                radial_min, radial_max = st.slider(
                    'Rango del eje radial', 
                    0.0, 
                    1.0, 
                    (0.0, 1.0), 
                    0.01, 
                    key='radial_slider'
                )

                # Opcional: Añadir espacio inferior para mover el slider hacia arriba
                st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Ajusta la altura según necesidad

            with slider_col3:
                st.empty()  # Espacio vacío a la derecha

            # Crear y configurar el gráfico de radar
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=valores_coche1,
                theta=categorias,
                fill='toself',
                name=nombre_coche1,
                line=dict(color='red'),
                fillcolor='rgba(255, 0, 0, 0.3)'
            ))

            fig.add_trace(go.Scatterpolar(
                r=valores_coche2,
                theta=categorias,
                fill='toself',
                name=nombre_coche2,
                line=dict(color='green'),
                fillcolor='rgba(0, 255, 0, 0.3)'
            ))

            # Configuración del gráfico
            config = {
                "displayModeBar": False
            }

            fig.update_layout(
                dragmode=False,
                uirevision='constant',
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[radial_min, radial_max],
                        tickangle=45,
                        tickfont=dict(size=10)
                    )
                ),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    x=0.5,
                    xanchor="center",
                    y=1.12,
                    yanchor='top',
                    font=dict(size=12)
                ),
                height=600,
                width=600,
                margin=dict(l=40, r=40, t=100, b=40)
            )

            # Mostrar el gráfico en el marcador de posición
            graph_placeholder.plotly_chart(fig, use_container_width=True, config=config)

    else:
        st.write("No hay columnas válidas para crear el gráfico de radar.")
else:
    st.write("No se encontraron datos para ambos coches seleccionados.")

