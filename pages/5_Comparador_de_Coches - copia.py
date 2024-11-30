import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import base64
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

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

# def mostrar_coche(imagen, caption, datos):
#     if imagen:
#         imagen_base64 = imagen_to_base64(imagen)
#         st.markdown(
#             f"""
#             <div style="display: flex; align-items: flex-start; margin-bottom: 20px;">
#                 <div style="flex: 1; text-align: center;">
#                     <img src="data:image/png;base64,{imagen_base64}" alt="{caption}" style="max-width: 100%; height: auto;">
#                 </div>
#                 <div style="flex: 1; padding-left: 20px;">
#                     <p style="margin: 5px 0; line-height: 1.2;"><strong>Marca:</strong> {datos["marca"]}</p>
#                     <p style="margin: 5px 0; line-height: 1.2;"><strong>Modelo:</strong> {caption}</p>
#                     <p style="margin: 5px 0; line-height: 1.2;"><strong>Precio contado:</strong> {int(datos["precio_contado"]):,} €</p>
#                     <p style="margin: 5px 0; line-height: 1.2;"><strong>Kilometraje:</strong> {int(datos["kilometraje"]):,} km</p>
#                     <p style="margin: 5px 0; line-height: 1.2;"><strong>Año de matriculación:</strong> {datos["ano_matriculacion"]}</p>
#                     <p style="margin: 5px 0; line-height: 1.2;"><strong>Tipo de cambio:</strong> {datos["tipo_cambio"]}</p>
#                     <p style="margin: 5px 0; line-height: 1.2;"><strong>Combustible:</strong> {datos["combustible"]}</p>
#                     <p style="margin: 5px 0; line-height: 1.2;"><strong>Distintivo ambiental:</strong> {datos["distintivo_ambiental"]}</p>
#                     <p style="margin: 5px 0; line-height: 1.2;"><strong>Potencia:</strong> {int(datos["potencia_cv"]):,} CV</p>
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

def mostrar_coche(imagen, caption):
    if imagen:
        imagen_base64 = imagen_to_base64(imagen)
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{imagen_base64}" alt="{caption}" style="max-width: 100%; height: auto;">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.write("No hay imagen disponible.")

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

# Título de la página
st.markdown("<h1 style='text-align: center;'>Comparador de coches</h1>", unsafe_allow_html=True)

# Dividir en 5 columnas principales
col1, col2, col3, col4, col5 = st.columns([1, 4, 1, 4, 1])

# Columna vacía (espacio a la izquierda)
with col1:
    st.empty()

# Filtros para el Coche 1
with col2:
    marca1 = df["marca"].sort_values().unique()[0]  
    modelo1 = df[df["marca"] == marca1]["modelo"].sort_values().unique()[0]  
    ano1 = df[(df["marca"] == marca1) & (df["modelo"] == modelo1)]["ano_matriculacion"].sort_values().unique()[0]
    titulo_coche1 = f"{marca1} {modelo1} ({ano1})"
    st.markdown(f"<h3 style='text-align: center;'>{titulo_coche1}</h3>", unsafe_allow_html=True)

    # Primera fila de filtros
    fila1_coche1 = st.columns(4)
    with fila1_coche1[0]:
        st.markdown("<p class='titulo-select'>Marca</p>", unsafe_allow_html=True)
        marca1 = st.selectbox("", df["marca"].sort_values().unique(), key="marca1", label_visibility="collapsed")
    with fila1_coche1[1]:
        st.markdown("<p class='titulo-select'>Modelo</p>", unsafe_allow_html=True)
        modelo1 = st.selectbox("", df[df["marca"] == marca1]["modelo"].sort_values().unique(), key="modelo1", label_visibility="collapsed")
    with fila1_coche1[2]:
        st.markdown("<p class='titulo-select'>Año</p>", unsafe_allow_html=True)
        ano1 = st.selectbox("", df[(df["marca"] == marca1) & (df["modelo"] == modelo1)]["ano_matriculacion"].sort_values().unique(), key="ano1", label_visibility="collapsed")
    with fila1_coche1[3]:
        st.markdown("<p class='titulo-select'>Cambio</p>", unsafe_allow_html=True)
        tipo_cambio1 = st.selectbox("", df[(df["marca"] == marca1) & (df["modelo"] == modelo1) & (df["ano_matriculacion"] == ano1)]["tipo_cambio"].sort_values().unique(), key="tipo_cambio1", label_visibility="collapsed")

    # Segunda fila de filtros
    fila2_coche1 = st.columns(4)
    with fila2_coche1[0]:
        st.markdown("<p class='titulo-select'>Combustible</p>", unsafe_allow_html=True)
        combustible1 = st.selectbox(
            "",
            df[
                (df["marca"] == marca1) &
                (df["modelo"] == modelo1) &
                (df["ano_matriculacion"] == ano1) &
                (df["tipo_cambio"] == tipo_cambio1)
            ]["combustible"].sort_values().unique(),
            key="combustible1",
            label_visibility="collapsed"
        )
    with fila2_coche1[1]:
        st.markdown("<p class='titulo-select'>Distintivo</p>", unsafe_allow_html=True)
        distintivo1 = st.selectbox(
            "",
            df[
                (df["marca"] == marca1) &
                (df["modelo"] == modelo1) &
                (df["ano_matriculacion"] == ano1) &
                (df["tipo_cambio"] == tipo_cambio1) &
                (df["combustible"] == combustible1)
            ]["distintivo_ambiental"].sort_values().unique(),
            key="distintivo1",
            label_visibility="collapsed"
        )
    with fila2_coche1[2]:
        st.markdown("<p class='titulo-select'>Potencia (CV)</p>", unsafe_allow_html=True)
        potencia1 = st.selectbox(
            "",
            df[
                (df["marca"] == marca1) &
                (df["modelo"] == modelo1) &
                (df["ano_matriculacion"] == ano1) &
                (df["tipo_cambio"] == tipo_cambio1) &
                (df["combustible"] == combustible1) &
                (df["distintivo_ambiental"] == distintivo1)
            ]["potencia_cv"].sort_values().unique(),
            key="potencia1",
            label_visibility="collapsed"
        )
    with fila2_coche1[3]:
        st.markdown("<p class='titulo-select'>Kilometraje</p>", unsafe_allow_html=True)
        kilometraje1 = st.selectbox(
            "",
            df[
                (df["marca"] == marca1) &
                (df["modelo"] == modelo1) &
                (df["ano_matriculacion"] == ano1) &
                (df["tipo_cambio"] == tipo_cambio1) &
                (df["combustible"] == combustible1) &
                (df["distintivo_ambiental"] == distintivo1) &
                (df["potencia_cv"] == potencia1)
            ]["kilometraje"].sort_values().unique(),
            key="kilometraje1",
            label_visibility="collapsed"
        )

# Columna vacía (espacio entre los coches)
with col3:
    st.empty()

# Filtros para el Coche 2
with col4:
    marca2 = df["marca"].sort_values().unique()[0]  
    modelo2 = df[df["marca"] == marca1]["modelo"].sort_values().unique()[0]  
    ano2 = df[(df["marca"] == marca1) & (df["modelo"] == modelo1)]["ano_matriculacion"].sort_values().unique()[0]
    titulo_coche1 = f"{marca1} {modelo1} ({ano1})"
    st.markdown(f"<h3 style='text-align: center;'>{titulo_coche1}</h3>", unsafe_allow_html=True)

    # Primera fila de filtros
    fila1_coche2 = st.columns(4)
    with fila1_coche2[0]:
        st.markdown("<p class='titulo-select'>Marca</p>", unsafe_allow_html=True)
        marca2 = st.selectbox("", df["marca"].sort_values().unique(), key="marca2", label_visibility="collapsed")
    with fila1_coche2[1]:
        st.markdown("<p class='titulo-select'>Modelo</p>", unsafe_allow_html=True)
        modelo2 = st.selectbox("", df[df["marca"] == marca2]["modelo"].sort_values().unique(), key="modelo2", label_visibility="collapsed")
    with fila1_coche2[2]:
        st.markdown("<p class='titulo-select'>Año</p>", unsafe_allow_html=True)
        ano2 = st.selectbox("", df[(df["marca"] == marca2) & (df["modelo"] == modelo2)]["ano_matriculacion"].sort_values().unique(), key="ano2", label_visibility="collapsed")
    with fila1_coche2[3]:
        st.markdown("<p class='titulo-select'>Cambio</p>", unsafe_allow_html=True)
        tipo_cambio2 = st.selectbox("", df[(df["marca"] == marca2) & (df["modelo"] == modelo2) & (df["ano_matriculacion"] == ano2)]["tipo_cambio"].sort_values().unique(), key="tipo_cambio2", label_visibility="collapsed")

    # Segunda fila de filtros
    fila2_coche2 = st.columns(4)
    with fila2_coche2[0]:
        st.markdown("<p class='titulo-select'>Combustible</p>", unsafe_allow_html=True)
        combustible2 = st.selectbox(
            "",
            df[
                (df["marca"] == marca2) &
                (df["modelo"] == modelo2) &
                (df["ano_matriculacion"] == ano2) &
                (df["tipo_cambio"] == tipo_cambio2)
            ]["combustible"].sort_values().unique(),
            key="combustible2",
            label_visibility="collapsed"
        )
    with fila2_coche2[1]:
        st.markdown("<p class='titulo-select'>Distintivo</p>", unsafe_allow_html=True)
        distintivo2 = st.selectbox(
            "",
            df[
                (df["marca"] == marca2) &
                (df["modelo"] == modelo2) &
                (df["ano_matriculacion"] == ano2) &
                (df["tipo_cambio"] == tipo_cambio2) &
                (df["combustible"] == combustible2)
            ]["distintivo_ambiental"].sort_values().unique(),
            key="distintivo2",
            label_visibility="collapsed"
        )
    with fila2_coche2[2]:
        st.markdown("<p class='titulo-select'>Potencia (CV)</p>", unsafe_allow_html=True)
        potencia2 = st.selectbox(
            "",
            df[
                (df["marca"] == marca2) &
                (df["modelo"] == modelo2) &
                (df["ano_matriculacion"] == ano2) &
                (df["tipo_cambio"] == tipo_cambio2) &
                (df["combustible"] == combustible2) &
                (df["distintivo_ambiental"] == distintivo2)
            ]["potencia_cv"].sort_values().unique(),
            key="potencia2",
            label_visibility="collapsed"
        )
    with fila2_coche2[3]:
        st.markdown("<p class='titulo-select'>Kilometraje</p>", unsafe_allow_html=True)
        kilometraje2 = st.selectbox(
            "",
            df[
                (df["marca"] == marca2) &
                (df["modelo"] == modelo2) &
                (df["ano_matriculacion"] == ano2) &
                (df["tipo_cambio"] == tipo_cambio2) &
                (df["combustible"] == combustible2) &
                (df["distintivo_ambiental"] == distintivo2) &
                (df["potencia_cv"] == potencia2)
            ]["kilometraje"].sort_values().unique(),
            key="kilometraje2",
            label_visibility="collapsed"
        )

# Columna vacía (espacio a la derecha)
with col5:
    st.empty()


# Dividir en dos columnas principales para Coche 1 y Coche 2
col1, col2, col3, col4, col5 = st.columns([1, 4, 1,4, 1])

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
    ]

    if not df_filtrado1.empty:
        datos_coche1 = df_filtrado1.iloc[0]
        imagen1 = convertir_binario_a_imagen(datos_coche1["foto_binaria"])

        if imagen1:
            mostrar_coche(imagen1, f'Coche 1')
        else:
            st.write("No hay imagen disponible para el Coche 1.")
    else:
        st.write("No se encontraron datos para el Coche 1 con los filtros seleccionados.")

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
    ]

    if not df_filtrado2.empty:
        datos_coche2 = df_filtrado2.iloc[0]
        imagen2 = convertir_binario_a_imagen(datos_coche2["foto_binaria"])

        if imagen2:
            mostrar_coche(imagen2, f'Coche 2')
        else:
            st.write("No hay imagen disponible para el Coche 2.")
    else:
        st.write("No se encontraron datos para el Coche 2 con los filtros seleccionados.")

with col5:
    st.empty()

columnas_seleccionadas = [
    "precio_contado", "kilometraje", "potencia_cv", 
    "velocidad_max", "aceleracion", "consumo_medio", "peso", 
    "capacidad_maletero"
]

if not df_filtrado1.empty and not df_filtrado2.empty:
    # Eliminar la columna 'foto_binaria' y combinar los dos DataFrames
    df_combinado = pd.concat([ df_filtrado1[columnas_seleccionadas],df_filtrado2[columnas_seleccionadas]], ignore_index=True)

    df_combinado.index = ["Coche 1", "Coche 2"]
    
    # Mostrar el DataFrame combinado en la interfaz
    st.markdown("<h3 style='text-align: center;'>Comparación de Coches</h3>", unsafe_allow_html=True)
    # Centrar el DataFrame en la interfaz
    st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
        <div style="width: 80%; text-align: center;">
    """,
    unsafe_allow_html=True
    )

    # Mostrar el DataFrame combinado
    st.dataframe(df_combinado, use_container_width=True)

    # Cerrar el contenedor HTML
    st.markdown(
        """
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.write("No se encontraron datos para ambos coches seleccionados.")

# Normalizar cada columna individualmente en todo el DataFrame
df_todos_los_coches = df[columnas_seleccionadas].copy()

columnas_log = ["precio_contado", "kilometraje", "potencia_cv"]
for col in columnas_log:
    df_todos_los_coches[col] = np.log1p(df_todos_los_coches[col])

for col in df_todos_los_coches.columns:
    df_todos_los_coches[col] = (df_todos_los_coches[col] - df_todos_los_coches[col].min()) / (df_todos_los_coches[col].max() - df_todos_los_coches[col].min())


if not df_filtrado1.empty and not df_filtrado2.empty:
    # Obtener los índices (id_coche) de los coches seleccionados
    indices_seleccionados = [df_filtrado1['id_coche'].iloc[0], df_filtrado2['id_coche'].iloc[0]]
    
    # Filtrar el DataFrame normalizado global para los coches seleccionados
    df_normalizado_seleccionados = df_todos_los_coches.loc[indices_seleccionados]

    # Filtrar columnas válidas (sin valores nulos en df_combinado)
    columnas_validas = [col for col in columnas_seleccionadas if df_combinado[col].notnull().all()]

    if columnas_validas:
        # Crear un DataFrame con solo las columnas válidas
        df_radar = df_normalizado_seleccionados[columnas_validas]

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
        df_radar.rename(columns=columnas_legibles, inplace=True)

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

        # Crear el gráfico de radar
        fig = go.Figure()

        # Añadir trazos para Coche 1
        fig.add_trace(go.Scatterpolar(
            r=valores_coche1,
            theta=categorias,
            fill='toself',
            name=nombre_coche1,  # Usar la marca y modelo como nombre
            line=dict(color='red'),  # Color rojo para el Coche 1
            fillcolor='rgba(255, 0, 0, 0.3)'  # Rojo semitransparente para el relleno
        ))

        # Añadir trazos para Coche 2
        fig.add_trace(go.Scatterpolar(
            r=valores_coche2,
            theta=categorias,
            fill='toself',
            name=nombre_coche2,  # Usar la marca y modelo como nombre
            line=dict(color='green'),  # Color verde para el Coche 2
            fillcolor='rgba(0, 255, 0, 0.3)'  # Verde semitransparente para el relleno
        ))

        config = {
            "scrollZoom": True,  # Permitir zoom con el scroll del ratón
            "displayModeBar": True,  # Mostrar barra de herramientas interactiva
            "displaylogo": False , # Ocultar el logo de Plotly
            "modeBarButtonsToAdd": ["zoomIn2d", "zoomOut2d", "resetScale2d"],  # Agregar botones de zoom
            "modeBarButtonsToRemove": []  # Opcional: eliminar pan si causa conflictos

        }

        # Configuración del diseño
        # Configurar el diseño para eventos interactivos
        fig.update_layout(
            dragmode="zoom",  # Permitir arrastrar y paneo
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickangle=45,  # Girar etiquetas de los ticks
                    tickfont=dict(size=10)  # Tamaño de fuente más pequeño
                )
            ),
            showlegend=True,
            legend=dict(
                orientation="h",  # Leyenda horizontal
                x=0.5,  # Centrar la leyenda
                xanchor="center",
                y=1.08,  # Posicionar la leyenda encima del gráfico
                yanchor='top',
                font=dict(size=12)
            ),
            title="Gráfico de Radar: Comparación de Coches",
            height=800,  # Altura personalizada
            width=800,  # Anchura personalizada
            margin=dict(l=40, r=40, t=100, b=40)  # Ajustar márgenes
        )

        # Centrar el gráfico en Streamlit
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
                <div style="width: 800px;"> <!-- Ajusta el ancho según sea necesario -->
            """,
            unsafe_allow_html=True
        )

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=False, config=config)

        # Cerrar el contenedor HTML
        st.markdown(
            """
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.write("No hay columnas válidas para crear el gráfico de radar.")
else:
    st.write("No se encontraron datos para ambos coches seleccionados.")



