# documentacion.py

import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Documentación del Proyecto",
    page_icon="🚗",
    layout="wide"
)

# Título principal
st.title("📚 Documentación del Proyecto")


# Descripción breve del proyecto
st.header("Descripción del Proyecto")
st.write("""
Esta aplicación web está diseñada para explorar y analizar datos del mercado de coches de segunda mano.
Con esta herramienta, puedes:
- Navegar por diferentes opciones de coches.
- Visualizar estadísticas clave.
- Filtrar información según tus intereses.

El objetivo es facilitar la comprensión del mercado para ayudarte a tomar decisiones informadas, incluso si no tienes conocimientos técnicos. ¡Es fácil de usar y visualmente intuitiva!
""")

# Índice de la documentación
st.header("Índice")
st.markdown("""
1. Presentación de los Datos
2. Vista Detallada
3. Modelo
4. Comparador de Coches (en desarrollo)
""")

# Sección: Presentación de Datos - Análisis Visual de Coches de Segunda Mano

st.header("PRESENTACIÓN DE DATOS")
st.write("""
En este apartado se muestran gráficos interactivos y mapas diseñados para que puedas explorar 
la información clave sobre el mercado de coches de segunda mano. 
Cada visualización incluye una breve descripción para ayudarte a entender los datos de forma sencilla.
""")

# Descripción de los gráficos
st.subheader("1. Kilometraje vs Precio")
st.write("""
Este gráfico te muestra cómo el precio de los coches baja a medida que aumenta el kilometraje.
Ideal para analizar tendencias generales.
""")

st.subheader("2. Precio por Tipo Distintivo")
st.write("""
Aquí puedes observar cómo varían los precios según los distintivos de los coches, destacando diferencias significativas entre categorías.
""")

st.subheader("3. Distribución de Precios")
st.write("""
Un histograma que muestra cómo se distribuyen los precios de los coches en diferentes rangos.
Te ayudará a identificar patrones en los precios del mercado.
""")

st.subheader("4. Relación entre Potencia y Precio")
st.write("""
Este gráfico muestra que los coches con más potencia suelen tener precios más altos.
Ideal para quienes buscan potencia en su vehículo.
""")

st.subheader("5. Mapa de Cantidades por Provincia")
st.write("""
Un mapa que visualiza cuántos coches están disponibles en cada provincia.
Puedes identificar rápidamente las regiones con más opciones.
""")

st.subheader("6. Mapa de Precios por Provincia")
st.write("""
Un mapa que muestra el precio medio de los coches por provincia.
Útil para comparar los precios promedio en distintas áreas geográficas.
""")

# Sección: Vista Detallada

st.header("VISTA DETALLADA")
st.write("""
En este apartado, puedes explorar en profundidad los datos de coches de segunda mano. 
Se incluyen múltiples filtros para personalizar la información que deseas visualizar.
""")

# Descripción de los filtros
st.subheader("1. Filtros Disponibles")
st.write("""
Utiliza los filtros en el panel lateral para ajustar los datos según tus necesidades. 
Puedes filtrar por:
- Rango de precio.
- Año de matriculación.
- Marca y modelo.
- Tipo de cambio.
- Provincia.
- Distintivo ambiental.
- Número de puertas.
""")

# Descripción de la tabla de resultados
st.subheader("2. Resultados Filtrados")
st.write("""
La tabla muestra los coches que cumplen con los criterios seleccionados. 
Incluye información como el precio, el año de matriculación y la provincia donde está disponible.
""")

# Estadísticas básicas
st.subheader("3. Estadísticas Básicas")
st.write("""
Al final de la página, puedes ver estadísticas básicas que resumen los datos filtrados, 
como el precio promedio o la potencia promedio, para facilitar el análisis.
""")

# Sección: Modelo

st.header("MODELO")
st.write("""
En este apartado, puedes predecir el precio al contado de un coche de segunda mano 
utilizando un modelo de machine learning. La herramienta permite personalizar la predicción 
según las características específicas del coche.
""")

# Descripción del formulario de entrada
st.subheader("1. Introducción de Características")
st.write("""
Introduce la información del coche para realizar la predicción. 
Se incluyen las siguientes categorías:
- **Características categóricas:** Marca, modelo, tipo de cambio, combustible, distintivo ambiental.
- **Características numéricas:** Potencia en CV, kilometraje, antigüedad del coche en años.
""")

# Proceso de guardado de datos
st.subheader("2. Guardar Datos")
st.write("""
Una vez rellenados los campos, guarda los datos para que puedan ser utilizados por el modelo.
Esto asegura que las características introducidas se procesen correctamente.
""")

# Predicción
st.subheader("3. Realizar Predicción")
st.write("""
Tras guardar los datos, pulsa el botón de predicción para obtener el precio estimado. 
El modelo utiliza técnicas avanzadas como escalado y codificación para ofrecer resultados precisos.
""")

# Notas adicionales
st.subheader("4. Notas Importantes")
st.write("""
- Asegúrate de que los valores introducidos son correctos y coherentes.
- En caso de errores, revisa las entradas proporcionadas o contacta con el soporte técnico.
- La predicción puede verse influida por la calidad de los datos de entrada.
""")

# Sección: Comparador de coches

st.header("COMPARADOR DE COCHES")
