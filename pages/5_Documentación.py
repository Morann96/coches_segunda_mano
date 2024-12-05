# documentacion.py

import streamlit as st
from PIL import Image


# Título principal
st.title("📚 **GUÍA DEL USUARIO Y DOCUMENTACIÓN**")


# Descripción breve del proyecto
st.header("**Descripción del Proyecto**")
st.write("""
Esta aplicación web está diseñada para explorar y analizar datos del mercado de coches de segunda mano.
Con esta herramienta, puedes:
- Navegar por diferentes opciones de coches.
- Visualizar estadísticas clave.
- Filtrar información según tus intereses.
- Predecir el precio de un coche segun sus caracteristicas.

El objetivo es facilitar la comprensión del mercado de coches de segunda mano para ayudarte a tomar decisiones ¡Es fácil de usar y visualmente intuitiva!
""")

# Índice de la documentación
st.header("**Índice**")
st.markdown("""
1. Descripción del Proyecto
2. Presentación de Datos
3. Vista Detallada
4. Modelo
5. Comparador de Coches
6. Arquitectura Base de Datos
""")

# Sección: Presentación de Datos - Análisis Visual de Coches de Segunda Mano

st.header("**PRESENTACIÓN DE DATOS**")
st.write("""
En este apartado se muestran gráficos interactivos y mapas diseñados para que puedas explorar 
la información clave sobre el mercado de coches de segunda mano. 
Cada visualización incluye una breve descripción para ayudarte a entender los datos de forma sencilla.
""")

# Descripción de los gráficos
st.subheader("**1. Kilometraje vs Precio**")
st.write("""
Este gráfico te muestra cómo el precio de los coches baja a medida que aumenta el kilometraje.
Ideal para analizar tendencias generales.
""")

st.subheader("**2. Precio por Tipo Distintivo**")
st.write("""
Aquí puedes observar cómo varían los precios según los distintivos de los coches, destacando diferencias significativas entre categorías.
""")

st.subheader("**3. Distribución de Precios**")
st.write("""
Un histograma que muestra cómo se distribuyen los precios de los coches en diferentes rangos.
Te ayudará a identificar patrones en los precios del mercado.
""")

st.subheader("**4. Relación entre Potencia y Precio**")
st.write("""
Este gráfico muestra que los coches con más potencia suelen tener precios más altos.
Ideal para quienes buscan potencia en su vehículo.
""")

st.subheader("**5. Mapa de Coches disponibles por Provincia**")
st.write("""
Un mapa que visualiza cuántos coches están disponibles en cada provincia.
Puedes identificar rápidamente las regiones con más opciones.
""")

st.subheader("**6. Mapa de Precios por Provincia**")
st.write("""
Un mapa que muestra el precio medio de los coches por provincia.
Útil para comparar los precios promedio en distintas áreas geográficas.
""")

# Sección: Vista Detallada

st.header("**VISTA DETALLADA**")
st.write("""
En este apartado, puedes explorar en profundidad los datos de coches de segunda mano. 
Se incluyen múltiples filtros para personalizar la información que deseas visualizar.
""")

# Descripción de los filtros
st.subheader("**1. Filtros Disponibles**")
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
st.subheader("**2. Resultados Filtrados**")
st.write("""
La tabla muestra los coches que cumplen con los criterios seleccionados. 
Incluye información como el precio, el año de matriculación y la provincia donde está disponible.
""")

# Estadísticas básicas
st.subheader("**3. Estadísticas Básicas**")
st.write("""
Al final de la página, puedes ver estadísticas básicas que resumen los datos filtrados, 
como el precio promedio o la potencia promedio, para facilitar el análisis.
""")

# Sección: Modelo
st.header("**MODELO**")
st.write("""
En este apartado, puedes predecir el precio al contado de un coche de segunda mano 
utilizando un modelo de machine learning y redes neuronales. La herramienta permite personalizar la predicción 
según las características específicas del coche.
""")

# Descripción del formulario de entrada
st.subheader("**1. Introducción de Características**")
st.write("""
Introduce la información del coche para realizar la predicción. 
Se incluyen las siguientes características:
- Marca
- Modelo
- Antigüedad
- Kilometraje
- Potencia
- Combustible
- Tipo de Cambio
    
Cada una de estas características es clave para obtener una predicción precisa del precio del coche.
""")

# Proceso de guardado de datos
st.subheader("**2. Guardar Datos**")
st.write("""
Una vez rellenados los campos con las características del coche, guarda los datos para que puedan ser utilizados por el modelo.
Esto asegura que las características introducidas se procesen correctamente y estén disponibles para la predicción.
""")

# Predicción
st.subheader("**3. Realizar Predicción**")
st.write("""
Tras guardar los datos, puedes pulsar el botón de predicción para obtener el precio estimado. 
El modelo utiliza técnicas de Machine Learning y Redes Neuronales para ofrecer resultados precisos y confiables.
El sistema analizará los datos introducidos y calculará un precio aproximado basado en patrones aprendidos de coches similares en el mercado de segunda mano.
""")

# Sección de Gráficas
st.subheader("**4. Gráficas de Evaluación del Modelo**")
st.write("""
Una vez realizada la predicción, puedes visualizar algunas gráficas que ayudan a evaluar la precisión del modelo. Estas métricas son fundamentales para comprender qué tan bien se está comportando el modelo en relación con los datos reales.

- **Error Absoluto Medio (MAE)**: Representa la diferencia promedio entre los valores reales y las predicciones del modelo. Un MAE más bajo indica un mejor rendimiento del modelo. 
  
- **Error Cuadrático Medio (MSE)**: Mide el promedio de los cuadrados de los errores. A diferencia del MAE, el MSE da más peso a los errores más grandes, lo que puede ayudar a identificar problemas significativos en las predicciones. 

- **Coeficiente de Determinación (R²)**: Mide la proporción de la varianza en los datos que es explicada por el modelo. Un valor de R² cercano a 1 indica que el modelo es muy preciso, mientras que valores cercanos a 0 indican que el modelo no está explicando bien los datos. 

Estas gráficas te permiten entender cómo el modelo está haciendo las predicciones y cómo se puede mejorar su rendimiento en futuros ajustes.
""")

# Feature Importance
st.subheader("**5. Importancia de las Características (Feature Importance)**")
st.write("""
En esta sección, se muestra una tabla que resalta la importancia relativa de cada una de las características introducidas para predecir el precio del coche. 
Esta tabla te permitirá ver qué variables tienen mayor influencia en el modelo y, por lo tanto, son las más determinantes a la hora de calcular el precio.

""")

# Comparativa de Redes Neuronales
st.subheader("**6. Comparativa de Redes Neuronales**")
st.write("""
En esta sección, se presentan las gráficas que comparan el rendimiento del modelo de redes neuronales con otros enfoques utilizados. Las gráficas te ayudarán a visualizar cómo se comporta el modelo de redes neuronales en comparación con otros modelos, como la regresión lineal, en términos de precisión y rendimiento.
""")

# Notas adicionales
st.subheader("**7. Notas Importantes**")
st.write("""
- Asegúrate de que los valores introducidos son correctos y coherentes con las características reales del coche.
- En caso de que haya errores o inconsistencias, revisa las entradas y corrígelas antes de realizar la predicción.
- La calidad de la predicción depende de la precisión de los datos proporcionados. Cuanto más precisos sean los datos, más exacto será el resultado.
- Ten en cuenta que este modelo es una aproximación y los resultados pueden variar dependiendo de factores adicionales no considerados en el modelo.
""")
# Sección: Comparador de coches

st.header("**COMPARADOR DE COCHES**")

# Descripción general
st.markdown("""
En este apartado podrás seleccionar dos vehículos y compararlos en función de características clave como el precio, el kilometraje, la potencia, entre otras.
""")

# Paso 1: Selección de los coches
st.subheader("**1. Selecciona dos coches**")
st.markdown("""
Elige dos coches de la lista para compararlos. Las características que podrás comparar incluyen:
- Precio
- Kilometraje
- Potencia
- Consumo
- Número de puertas
- Año de fabricación
  
Solo tienes que seleccionar un coche para cada opción y presionar 'Comparar'.
""")

# Paso 2: Visualización de los detalles
st.subheader("**2. Visualiza los detalles**")
st.markdown("""
Verás las características principales de los coches seleccionados, como el precio, kilometraje, potencia y consumo.
""")

# Paso 3: Comparación visual
st.subheader("**3. Compara con gráficos**")
st.markdown("""
La herramienta genera un gráfico de radar para comparar visualmente los coches en base a sus características.
""")

# Consejos
st.subheader("**4. Consejos**")
st.markdown("""
- Elige coches que realmente te interesen para una comparación útil.
- Usa el gráfico de radar para ver las diferencias de manera visual.
""")


# Sección: Comparador de coches

st.header("**ARQUITECTURA BASE DE DATOS**")

# Mostrar la imagen
st.subheader("Diagrama de la Base de Datos")
st.image("bin/imagenes/esquema_bbdd.png", use_container_width=True)

st.subheader("Descripción de las Tablas y Columnas")

st.markdown("""
La base de datos del proyecto está compuesta por varias tablas relacionadas, que permiten gestionar la información de concesionarios, vehículos, características técnicas, y su localización. A continuación, se describe la utilidad de cada tabla y el significado de sus columnas principales:

### 1. **Concesionarios**
- **id_concesionario (PK):** Identificador único del concesionario.
- **nombre_concesionario:** Nombre del concesionario.

### 2. **Marcas**
- **id_marca (PK):** Identificador único de la marca.
- **nombre_marca:** Nombre de la marca del vehículo (por ejemplo, Toyota, Ford).

### 3. **Modelos**
- **id_modelo (PK):** Identificador único del modelo del vehículo.
- **nombre_modelo:** Nombre del modelo (por ejemplo, Corolla, Fiesta).

### 4. **Tipo_traccion**
- **id_traccion (PK):** Identificador único del tipo de tracción.
- **nombre_traccion:** Descripción del tipo de tracción (por ejemplo, tracción delantera, trasera, 4x4).

### 5. **Links_coches**
- **id_coche (PK):** Identificador único del coche.
- **link_anuncio:** URL del anuncio donde se encuentra más información del coche.
- **foto_binaria:** Imagen del coche almacenada como un blob binario.

### 6. **Prestaciones**
Esta tabla es el núcleo de la base de datos, ya que almacena información técnica y características detalladas de cada coche:
- **id_provincia, id_concesionario, id_distintivo, etc.:** Claves foráneas que relacionan esta tabla con otras.
- **mes_matriculacion, ano_matriculacion:** Mes y año de matriculación del coche.
- **kilometraje:** Distancia recorrida por el coche (en kilómetros).
- **precio_nuevo, precio_contado:** Precios del coche (nuevo y contado).
- **largo, ancho, alto, peso:** Dimensiones y peso del vehículo.
- **capacidad_maletero:** Capacidad del maletero (en litros).
- **num_plazas, num_puertas:** Número de plazas y puertas del vehículo.
- **consumo_medio, consumo_carretera, consumo_urbano:** Valores de consumo de combustible (en litros/100 km).
- **co2:** Emisiones de dióxido de carbono (en g/km).
- **potencia_kw, potencia_cv:** Potencia del coche en kilovatios y caballos de vapor.
- **velocidad_max:** Velocidad máxima alcanzable (en km/h).
- **fecha_extraccion:** Fecha de registro de los datos.

### 7. **Provincias**
- **id_provincia (PK):** Identificador único de la provincia.
- **nombre_provincia:** Nombre de la provincia.
- **comunidad_autonoma:** Comunidad autónoma a la que pertenece la provincia.

### 8. **Distintivos_ambientales**
- **id_distintivo (PK):** Identificador único del distintivo ambiental.
- **nombre_distintivo:** Descripción del distintivo (por ejemplo, ECO, Cero Emisiones).

### 9. **Combustibles**
- **id_combustible (PK):** Identificador único del tipo de combustible.
- **nombre_combustible:** Nombre del tipo de combustible (por ejemplo, Gasolina, Diésel, Eléctrico).

### 10. **Tipos_cambio**
- **id_tipo_cambio (PK):** Identificador único del tipo de cambio.
- **nombre_tipo_cambio:** Descripción del tipo de cambio (por ejemplo, manual, automático).

### 11. **Sobrealimentaciones**
- **id_sobrealimentacion (PK):** Identificador único del tipo de sobrealimentación.
- **nombre_sobrealimentacion:** Tipo de sobrealimentación (por ejemplo, turbo, compresor).

### Relaciones entre Tablas
Las relaciones entre las tablas están establecidas mediante claves foráneas (FK) presentes en la tabla **Prestaciones**, que actúa como la tabla principal para consolidar la información de los coches.

""")



