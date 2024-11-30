import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import base64
import matplotlib.pyplot as plt
import numpy as np

# Conexión a la base de datos
def conectar_base_datos():
    conn = st.connection('mysql', type='sql')  # Ajusta tu configuración aquí
    return conn

# Función para cargar datos desde la base de datos
def cargar_datos():
    conn = conectar_base_datos()
    query = "SELECT * FROM vista_prestaciones_img"  # Carga todos los datos necesarios
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
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{imagen_base64}" alt="{caption}" style="max-width: 100%; height: auto;">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.write("No hay imagen disponible.")

# Título de la aplicación
st.markdown("<h1 style='text-align: center;'>Comparador de coches</h1>", unsafe_allow_html=True)

# Cargar datos
df = cargar_datos()

# Dividir en columnas: Filtros del Coche 1, Coche 1, Coche 2, Filtros del Coche 2
filtros_coche1_col, coche1_col, coche2_col, filtros_coche2_col = st.columns([1, 4, 4, 1])

# Filtros para el margen izquierdo
with filtros_coche1_col:
    st.markdown("<h3 style='text-align: center;'>Filtros</h3>", unsafe_allow_html=True)

    # Filtro de marca
    marca_seleccionada1 = st.selectbox("Marca", df["marca"].unique(), key="marca1")

    # Filtro de modelo
    modelo_seleccionado1 = st.selectbox(
        "Modelo",
        df[df["marca"] == marca_seleccionada1]["modelo"].unique(),
        key="modelo1",
    )

    # Filtro de año de matriculación
    ano_matriculacion1 = st.selectbox(
        "Año de matriculación",
        df[(df["marca"] == marca_seleccionada1) & (df["modelo"] == modelo_seleccionado1)]["ano_matriculacion"].unique(),
        key="ano1",
    )

    # Filtro de tipo de cambio
    tipo_cambio1 = st.selectbox(
        "Tipo de cambio",
        df[
            (df["marca"] == marca_seleccionada1)
            & (df["modelo"] == modelo_seleccionado1)
            & (df["ano_matriculacion"] == ano_matriculacion1)
        ]["tipo_cambio"].unique(),
        key="tipo_cambio1",
    )

    # Filtro de combustible
    combustible1 = st.selectbox(
        "Combustible",
        df[
            (df["marca"] == marca_seleccionada1)
            & (df["modelo"] == modelo_seleccionado1)
            & (df["ano_matriculacion"] == ano_matriculacion1)
        ]["combustible"].unique(),
        key="combustible1",
    )

    # Filtro de distintivo ambiental
    distintivo_ambiental1 = st.selectbox(
        "Distintivo ambiental",
        df[
            (df["marca"] == marca_seleccionada1)
            & (df["modelo"] == modelo_seleccionado1)
            & (df["ano_matriculacion"] == ano_matriculacion1)
            & (df["combustible"] == combustible1)
        ]["distintivo_ambiental"].unique(),
        key="distintivo1",
    )

    # Filtro de potencia (CV)
    potencia_cv1 = st.selectbox(
        "Potencia (CV)",
        df[
            (df["marca"] == marca_seleccionada1)
            & (df["modelo"] == modelo_seleccionado1)
            & (df["ano_matriculacion"] == ano_matriculacion1)
            & (df["combustible"] == combustible1)
            & (df["distintivo_ambiental"] == distintivo_ambiental1)
        ]["potencia_cv"].unique(),
        key="potencia_cv1",
    )

    # Filtro de kilometraje
    kilometraje1 = st.selectbox(
        "Kilometraje (km)",
        df[
            (df["marca"] == marca_seleccionada1)
            & (df["modelo"] == modelo_seleccionado1)
            & (df["ano_matriculacion"] == ano_matriculacion1)
            & (df["combustible"] == combustible1)
            & (df["distintivo_ambiental"] == distintivo_ambiental1)
            & (df["potencia_cv"] == potencia_cv1)
        ]["kilometraje"].unique(),
        key="km1",
    )



# Filtros para el margen derecho
with filtros_coche2_col:
    st.markdown("<h3 style='text-align: center;'>Filtros</h3>", unsafe_allow_html=True)

    # Filtro de marca
    marca_seleccionada2 = st.selectbox("Marca", df["marca"].unique(), key="marca2")

    # Filtro de modelo
    modelo_seleccionado2 = st.selectbox(
        "Modelo",
        df[df["marca"] == marca_seleccionada2]["modelo"].unique(),
        key="modelo2",
    )

    # Filtro de año de matriculación
    ano_matriculacion2 = st.selectbox(
        "Año de matriculación",
        df[(df["marca"] == marca_seleccionada2) & (df["modelo"] == modelo_seleccionado2)]["ano_matriculacion"].unique(),
        key="ano2",
    )

    # Filtro de tipo de cambio
    tipo_cambio2 = st.selectbox(
        "Tipo de cambio",
        df[
            (df["marca"] == marca_seleccionada2)
            & (df["modelo"] == modelo_seleccionado2)
            & (df["ano_matriculacion"] == ano_matriculacion2)
        ]["tipo_cambio"].unique(),
        key="tipo_cambio2",
    )

    # Filtro de combustible
    combustible2 = st.selectbox(
        "Combustible",
        df[
            (df["marca"] == marca_seleccionada2)
            & (df["modelo"] == modelo_seleccionado2)
            & (df["ano_matriculacion"] == ano_matriculacion2)
        ]["combustible"].unique(),
        key="combustible2",
    )

    # Filtro de distintivo ambiental
    distintivo_ambiental2 = st.selectbox(
        "Distintivo ambiental",
        df[
            (df["marca"] == marca_seleccionada2)
            & (df["modelo"] == modelo_seleccionado2)
            & (df["ano_matriculacion"] == ano_matriculacion2)
            & (df["combustible"] == combustible2)
        ]["distintivo_ambiental"].unique(),
        key="distintivo2",
    )

    # Filtro de potencia (CV)
    potencia_cv2 = st.selectbox(
        "Potencia (CV)",
        df[
            (df["marca"] == marca_seleccionada2)
            & (df["modelo"] == modelo_seleccionado2)
            & (df["ano_matriculacion"] == ano_matriculacion2)
            & (df["combustible"] == combustible2)
            & (df["distintivo_ambiental"] == distintivo_ambiental2)
        ]["potencia_cv"].unique(),
        key="potencia_cv2",
    )

    # Filtro de kilometraje
    kilometraje2 = st.selectbox(
        "Kilometraje (km)",
        df[
            (df["marca"] == marca_seleccionada2)
            & (df["modelo"] == modelo_seleccionado2)
            & (df["ano_matriculacion"] == ano_matriculacion2)
            & (df["combustible"] == combustible2)
            & (df["distintivo_ambiental"] == distintivo_ambiental2)
            & (df["potencia_cv"] == potencia_cv2)
        ]["kilometraje"].unique(),
        key="km2",
    )

with coche1_col:
    st.markdown("<h3 style='text-align: center;'>Coche 1</h3>", unsafe_allow_html=True)

    # Filtrar los datos según los filtros seleccionados
    df_filtrado1 = df[
        (df["marca"] == marca_seleccionada1)
        & (df["modelo"] == modelo_seleccionado1)
        & (df["ano_matriculacion"] == ano_matriculacion1)
        & (df["tipo_cambio"] == tipo_cambio1)
        & (df["combustible"] == combustible1)
        & (df["distintivo_ambiental"] == distintivo_ambiental1)
        & (df["potencia_cv"] == potencia_cv1)
        & (df["kilometraje"] == kilometraje1)
    ]

    if not df_filtrado1.empty:
        datos_coche1 = df_filtrado1.iloc[0]
        imagen1 = convertir_binario_a_imagen(datos_coche1["foto_binaria"])

        if imagen1:
            mostrar_coche(
                imagen1,
                f'Coche 1',
            )
        else:
            st.write("No hay imagen disponible para el Coche 1.")

    else:
        st.write("No se encontraron datos para el Coche 1 con los filtros seleccionados.")


with coche2_col:
    st.markdown("<h3 style='text-align: center;'>Coche 2</h3>", unsafe_allow_html=True)

    # Filtrar los datos según los filtros seleccionados
    df_filtrado2 = df[
        (df["marca"] == marca_seleccionada2)
        & (df["modelo"] == modelo_seleccionado2)
        & (df["ano_matriculacion"] == ano_matriculacion2)
        & (df["tipo_cambio"] == tipo_cambio2)
        & (df["combustible"] == combustible2)
        & (df["distintivo_ambiental"] == distintivo_ambiental2)
        & (df["potencia_cv"] == potencia_cv2)
        & (df["kilometraje"] == kilometraje2)
    ]

    if not df_filtrado2.empty:
        datos_coche2 = df_filtrado2.iloc[0]
        imagen2 = convertir_binario_a_imagen(datos_coche2["foto_binaria"])

        if imagen2:
            mostrar_coche(
                imagen2,
                f'Coche 2',
            )
        else:
            st.write("No hay imagen disponible para el Coche 2.")

    else:
        st.write("No se encontraron datos para el Coche 2 con los filtros seleccionados.")

columnas_seleccionadas = [
    "precio_contado", "precio_nuevo", "kilometraje", "potencia_cv", 
    "velocidad_max", "aceleracion", "consumo_medio", "peso", 
    "num_plazas", "num_puertas", "capacidad_maletero", "largo", 
    "ancho", "alto"
]

if not df_filtrado1.empty and not df_filtrado2.empty:
    # Eliminar la columna 'foto_binaria' y combinar los dos DataFrames
    df_combinado = pd.concat([ df_filtrado1[columnas_seleccionadas],df_filtrado2[columnas_seleccionadas]], ignore_index=True)
    
    # Mostrar el DataFrame combinado en la interfaz
    st.markdown("<h3 style='text-align: center;'>Comparación de Coches</h3>", unsafe_allow_html=True)
    st.dataframe(df_combinado)
else:
    st.write("No se encontraron datos para ambos coches seleccionados.")




# Función para crear el gráfico de radar
# def crear_grafico_radar(coche1, coche2):
#     # Define las características a comparar
#     categorias = ["Potencia (CV)", "Kilometraje", "Año de matriculación"]
#     valores_coche1 = [
#         coche1["potencia_cv"],
#         coche1["kilometraje"],
#         coche1["ano_matriculacion"],
#     ]
#     valores_coche2 = [
#         coche2["potencia_cv"],
#         coche2["kilometraje"],
#         coche2["ano_matriculacion"],
#     ]

#     # Normalizar los valores para el gráfico de radar
#     maximos = [200, 200000, 2023]  # Ajusta los máximos según tus datos
#     valores_coche1 = [v / m for v, m in zip(valores_coche1, maximos)]
#     valores_coche2 = [v / m for v, m in zip(valores_coche2, maximos)]

#     # Añadir el primer valor al final para cerrar el gráfico
#     valores_coche1 += valores_coche1[:1]
#     valores_coche2 += valores_coche2[:1]
#     categorias += categorias[:1]

#     # Crear el gráfico
#     angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=True)
#     fig, ax = plt.subplots(figsize=(2, 2), subplot_kw={"projection": "polar"})  # Tamaño reducido

#     # Dibujar las líneas del radar para cada coche
#     ax.plot(angulos, valores_coche1, label="Coche 1", linewidth=2)
#     ax.fill(angulos, valores_coche1, alpha=0.25)

#     ax.plot(angulos, valores_coche2, label="Coche 2", linewidth=2, linestyle="dashed")
#     ax.fill(angulos, valores_coche2, alpha=0.25)

#     # Configuración de los ticks
#     ax.set_yticks([])
#     ax.set_xticks(angulos)
#     ax.set_xticklabels(categorias, fontsize=10)

#     # Leyenda y título
#     ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
#     plt.title("Comparación de Características", size=12, pad=20)

#     return fig

# # Crear el gráfico de radar y mostrarlo debajo de las imágenes solo si hay datos disponibles
# if not df_filtrado1.empty and not df_filtrado2.empty:
#     datos_coche1 = df_filtrado1.iloc[0]
#     datos_coche2 = df_filtrado2.iloc[0]
    
#     grafico_radar = crear_grafico_radar(datos_coche1, datos_coche2)
    
#     # Posicionamiento del gráfico
#     st.markdown("<h3 style='text-align: center;'>Gráfico Comparativo</h3>", unsafe_allow_html=True)
#     col1, col2, col3 = st.columns([4, 4, 4])
#     with col2:
#         st.pyplot(grafico_radar)
# else:
#     st.warning("Por favor, selecciona ambos coches para comparar.")




