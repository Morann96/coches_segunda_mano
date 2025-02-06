# documentacion.py

import streamlit as st

# Verificar si existe el estado de idioma, si no, se inicializa en inglés
if 'lang' not in st.session_state:
    st.session_state.lang = "en" 

# Selector de idioma
idioma = st.sidebar.radio(
    'Language',  
    ("English", "Español") 
)

# Actualizar el idioma del estado según la selección del usuario
if idioma == "Español":
    st.session_state.lang = "es"
else:
    st.session_state.lang = "en"

lang = st.session_state.lang

# Diccionarios con las traducciones
texts = {
    "title": {
        "es": "📚 **GUÍA DEL USUARIO Y DOCUMENTACIÓN**",
        "en": "📚 **USER GUIDE AND DOCUMENTATION**"
    },
    "tech_header": {
        "es": "**TECNOLOGÍAS EMPLEADAS**",
        "en": "**TECHNOLOGIES USED**"
    },
    "tech_col1": {
        "es": """
- **Lenguaje de Programación:** Python 🐍
- **Framework de Interfaz:** [**Streamlit** 🚀](https://streamlit.io/)  
  Permite crear interfaces web interactivas de manera rápida y sencilla, sin necesidad de profundos conocimientos de frontend. Actualiza los resultados según la interacción del usuario.

- **Visualizaciones Interactivas:** [**Plotly** 📊](https://plotly.com/python/)  
  Ofrece gráficos dinámicos y mapas coropléticos. Sus componentes interactivos (zoom, hover, filtrado) facilitan un análisis detallado.

- **Tratamiento de Datos Geoespaciales:** [**GeoPandas** 🗺️](https://geopandas.org/)  
  Permite manejar datos geográficos, unir información espacial y crear mapas que muestran la distribución y precios de coches por región.
         
- **PIL (Pillow) para Imágenes** 🖼️  
  Para cargar, procesar y mostrar imágenes de los vehículos, enriqueciendo la experiencia y facilitando comparaciones visuales entre coches.

Estas tecnologías se aplican a lo largo de todo el proyecto: desde la extracción y procesamiento de datos, pasando por su análisis y visualización, hasta la predicción y comparación de precios de coches de segunda mano.
        """,
        "en": """
- **Programming Language:** Python 🐍
- **Interface Framework:** [**Streamlit** 🚀](https://streamlit.io/)  
  Allows you to quickly and easily create interactive web interfaces without extensive frontend knowledge. It updates results based on user interaction.

- **Interactive Visualizations:** [**Plotly** 📊](https://plotly.com/python/)  
  Offers dynamic graphs and choropleth maps. Its interactive components (zoom, hover, filtering) facilitate detailed analysis.

- **Geospatial Data Processing:** [**GeoPandas** 🗺️](https://geopandas.org/)  
  Enables handling of geographic data, merging spatial information, and creating maps that show the distribution and pricing of cars by region.
         
- **PIL (Pillow) for Images** 🖼️  
  Used to load, process, and display vehicle images, enhancing the user experience and enabling visual comparisons between cars.

These technologies are applied throughout the project: from data extraction and processing, through analysis and visualization, to predicting and comparing used car prices.
        """
    },
    "tech_col2": {
        "es": """
- **Extracción de Datos:** [**Selenium** 🕸️](https://www.selenium.dev/) y [**Beautiful Soup** 🍜](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
  Empleados para la automatización de tareas web y el raspado (scraping) de datos de páginas, permitiendo extraer información actualizada de forma automatizada.

- **Manipulación y Análisis de Datos:** [**Pandas** 🐼](https://pandas.pydata.org/) y [**NumPy** 🔢](https://numpy.org/)  
  Para cargar, limpiar y transformar datos. Pandas facilita la conexión a la base de datos, el filtrado por criterios y la preparación del dataset para el modelado.

- **Base de Datos:** MySQL 💿  
  Almacena la información sobre coches, precios, especificaciones técnicas y localización. Se emplean vistas y consultas SQL para extraer datos siempre actualizados.

- **Machine Learning y Deep Learning:**  
  - [**scikit-learn** 🤖](https://scikit-learn.org/): Para el modelado clásico (regresión) y la evaluación de métricas (MAE, MSE, R²).  
  - [**TensorFlow/Keras** 🧠](https://www.tensorflow.org/): Para el entrenamiento, carga e inferencia de redes neuronales que predicen el precio según las características del coche.
        """,
        "en": """
- **Data Extraction:** [**Selenium** 🕸️](https://www.selenium.dev/) and [**Beautiful Soup** 🍜](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
  Used for automating web tasks and scraping data from pages, allowing for the extraction of up-to-date information in an automated manner.

- **Data Manipulation and Analysis:** [**Pandas** 🐼](https://pandas.pydata.org/) and [**NumPy** 🔢](https://numpy.org/)  
  For loading, cleaning, and transforming data. Pandas facilitates database connections, filtering by criteria, and preparing datasets for modeling.

- **Database:** MySQL 💿  
  Stores information about cars, prices, technical specifications, and locations. Views and SQL queries are used to retrieve always up-to-date data.

- **Machine Learning and Deep Learning:**  
  - [**scikit-learn** 🤖](https://scikit-learn.org/): For classic modeling (regression) and evaluating metrics (MAE, MSE, R²).  
  - [**TensorFlow/Keras** 🧠](https://www.tensorflow.org/): For training, loading, and inference of neural networks that predict prices based on car characteristics.
        """
    },
    "db_arch_header": {
        "es": "**ARQUITECTURA BASE DE DATOS**",
        "en": "**DATABASE ARCHITECTURE**"
    },
    "db_diagram_subheader": {
        "es": "Diagrama de la Base de Datos",
        "en": "Database Diagram"
    },
    "db_tables_subheader": {
        "es": "Descripción de las Tablas y Columnas",
        "en": "Description of Tables and Columns"
    },
    "db_markdown": {
        "es": """
# Documentación de la Base de Datos

---

## **Diagrama de la Base de Datos**
El diagrama de la base de datos ilustra las relaciones entre las tablas principales que conforman el sistema. Cada tabla contiene información específica y se conecta a otras tablas mediante claves foráneas, lo que permite gestionar eficientemente la información del mercado de coches de segunda mano.

---

## **Descripción de las Tablas**

### **1. Links_coches**
Esta tabla almacena enlaces y representaciones visuales de los coches en la base de datos.
- **id_coche (PK):** Identificador único del coche.
- **link_anuncio:** URL del anuncio donde se detalla información adicional del coche.
- **foto_binaria:** Imagen del coche almacenada como un blob binario.

---

### **2. Concesionarios**
Registra la información básica sobre los concesionarios.
- **id_concesionario (PK):** Identificador único del concesionario.
- **nombre_concesionario:** Nombre del concesionario.

---

### **3. Marcas**
Contiene información sobre las diferentes marcas de coches.
- **id_marca (PK):** Identificador único de la marca.
- **nombre_marca:** Nombre de la marca (por ejemplo, Toyota, Ford).

---

### **4. Modelos**
Guarda detalles sobre los modelos específicos asociados a una marca.
- **id_modelo (PK):** Identificador único del modelo.
- **nombre_modelo:** Nombre del modelo (por ejemplo, Corolla, Fiesta).

---

### **5. Tipo_traccion**
Define los tipos de tracción disponibles en los coches.
- **id_traccion (PK):** Identificador único del tipo de tracción.
- **nombre_traccion:** Descripción del tipo de tracción (por ejemplo, tracción delantera, trasera, 4x4).

---

### **6. Prestaciones**
La tabla más importante, donde se consolida la información técnica y características específicas de cada coche.
- **id_coche (PK):** Identificador único del coche (relacionado con otras tablas).
- **id_provincia (FK):** Relación con la tabla Provincias.
- **id_concesionario (FK):** Relación con la tabla Concesionarios.
- **id_distintivo (FK):** Relación con la tabla Distintivos_ambientales.
- **id_marca (FK):** Relación con la tabla Marcas.
- **id_combustible (FK):** Relación con la tabla Combustibles.
- **id_modelo (FK):** Relación con la tabla Modelos.
- **id_tipo_cambio (FK):** Relación con la tabla Tipos_cambio.
- **id_traccion (FK):** Relación con la tabla Tipo_traccion.
- **id_sobrealimentacion (FK):** Relación con la tabla Sobrealimentaciones.
- **Mes y año de matriculación:** Registra cuándo se matriculó el coche.
- **Kilometraje:** Indica la distancia total recorrida por el coche.
- **Precio:** Contiene los precios del coche nuevo y de segunda mano.
- **Dimensiones:** Largo, ancho, alto y capacidad del maletero.
- **Especificaciones técnicas:** Número de plazas, número de puertas, tipo de combustible, potencia (en kW y CV), velocidad máxima, emisiones de CO2, etc.

---

### **7. Provincias**
Almacena información geográfica relacionada con la ubicación de los coches.
- **id_provincia (PK):** Identificador único de la provincia.
- **nombre_provincia:** Nombre de la provincia.
- **comunidad_autonoma:** Comunidad autónoma a la que pertenece la provincia.

---

### **8. Distintivos_ambientales**
Incluye los distintivos ambientales asignados a los coches.
- **id_distintivo (PK):** Identificador único del distintivo ambiental.
- **nombre_distintivo:** Descripción del distintivo (por ejemplo, ECO, Cero Emisiones).

---

### **9. Combustibles**
Define los tipos de combustible utilizados por los coches.
- **id_combustible (PK):** Identificador único del tipo de combustible.
- **nombre_combustible:** Nombre del tipo de combustible (por ejemplo, Gasolina, Diésel, Eléctrico).

---

### **10. Tipos_cambio**
Describe los tipos de cambio (transmisión) disponibles en los coches.
- **id_tipo_cambio (PK):** Identificador único del tipo de cambio.
- **nombre_tipo_cambio:** Descripción del tipo de cambio (por ejemplo, manual, automático).

---

### **11. Sobrealimentaciones**
Detalla los sistemas de sobrealimentación de los motores.
- **id_sobrealimentacion (PK):** Identificador único del tipo de sobrealimentación.
- **nombre_sobrealimentacion:** Descripción del tipo de sobrealimentación (por ejemplo, turbo, compresor).

---

## **Relaciones entre Tablas**
La tabla **Prestaciones** actúa como el núcleo de la base de datos, conectando la información de las tablas secundarias mediante claves foráneas, lo que conforma un modelo de estrella. Esto permite:
- Un acceso eficiente a los datos relacionados.
- La capacidad de realizar consultas complejas combinando varias tablas.
- La gestión centralizada de las especificaciones y características de cada coche.

---
""",
        "en": """
# Database Documentation

---

## **Database Diagram**
The database diagram illustrates the relationships between the main tables that make up the system. Each table contains specific information and is connected to other tables through foreign keys, allowing efficient management of the used car market data.

---

## **Description of the Tables**

### **1. Links_coches**
This table stores links and visual representations of the cars in the database.
- **id_coche (PK):** Unique identifier for the car.
- **link_anuncio:** URL of the ad where additional car details are provided.
- **foto_binaria:** Image of the car stored as a binary blob.

---

### **2. Concesionarios** (Dealerships)
Stores basic information about dealerships.
- **id_concesionario (PK):** Unique identifier for the dealership.
- **nombre_concesionario:** Name of the dealership.

---

### **3. Marcas** (Brands)
Contains information about different car brands.
- **id_marca (PK):** Unique identifier for the brand.
- **nombre_marca:** Name of the brand (e.g., Toyota, Ford).

---

### **4. Modelos** (Models)
Stores details about specific models associated with a brand.
- **id_modelo (PK):** Unique identifier for the model.
- **nombre_modelo:** Model name (e.g., Corolla, Fiesta).

---

### **5. Tipo_traccion** (Traction Types)
Defines the types of traction available in cars.
- **id_traccion (PK):** Unique identifier for the traction type.
- **nombre_traccion:** Description of the traction type (e.g., front-wheel drive, rear-wheel drive, 4x4).

---

### **6. Prestaciones** (Specifications)
The most important table, where technical information and specific characteristics of each car are consolidated.
- **id_coche (PK):** Unique car identifier (related to other tables).
- **id_provincia (FK):** Relationship with Provincias table.
- **id_concesionario (FK):** Relationship with Concesionarios table.
- **id_distintivo (FK):** Relationship with Distintivos_ambientales table.
- **id_marca (FK):** Relationship with Marcas table.
- **id_combustible (FK):** Relationship with Combustibles table.
- **id_modelo (FK):** Relationship with Modelos table.
- **id_tipo_cambio (FK):** Relationship with Tipos_cambio table.
- **id_traccion (FK):** Relationship with Tipo_traccion table.
- **id_sobrealimentacion (FK):** Relationship with Sobrealimentaciones table.
- **Mes y año de matriculación (Month and Year of Registration):** Records when the car was registered.
- **Kilometraje (Mileage):** Indicates the total distance traveled by the car.
- **Precio (Price):** Contains the new and used car prices.
- **Dimensiones (Dimensions):** Length, width, height, and trunk capacity.
- **Especificaciones técnicas (Technical Specifications):** Number of seats, number of doors, fuel type, power (kW and HP), top speed, CO2 emissions, etc.

---

### **7. Provincias** (Provinces)
Stores geographical information related to car locations.
- **id_provincia (PK):** Unique identifier for the province.
- **nombre_provincia:** Name of the province.
- **comunidad_autonoma:** Autonomous community to which the province belongs.

---

### **8. Distintivos_ambientales** (Environmental Badges)
Includes the environmental badges assigned to cars.
- **id_distintivo (PK):** Unique identifier for the environmental badge.
- **nombre_distintivo:** Description of the badge (e.g., ECO, Zero Emissions).

---

### **9. Combustibles** (Fuels)
Defines the types of fuel used by cars.
- **id_combustible (PK):** Unique identifier for the fuel type.
- **nombre_combustible:** Name of the fuel type (e.g., Gasoline, Diesel, Electric).

---

### **10. Tipos_cambio** (Transmission Types)
Describes the types of transmission available in cars.
- **id_tipo_cambio (PK):** Unique identifier for the transmission type.
- **nombre_tipo_cambio:** Description of the transmission (e.g., manual, automatic).

---

### **11. Sobrealimentaciones** (Forced Inductions)
Details engine forced induction systems.
- **id_sobrealimentacion (PK):** Unique identifier for the forced induction type.
- **nombre_sobrealimentacion:** Description of the forced induction (e.g., turbo, supercharger).

---

## **Relationships Between Tables**
The **Prestaciones** table acts as the core of the database, connecting information from secondary tables through foreign keys, forming a star schema. This allows:
- Efficient access to related data.
- The ability to perform complex queries combining multiple tables.
- Centralized management of each car's specifications and characteristics.

---
"""
    }
}

# Mostrar el título principal
st.title(texts["title"][lang])

# Tecnologías empleadas / Technologies used
st.header(texts["tech_header"][lang])

col1, col2 = st.columns(2)

with col1:
    st.write(texts["tech_col1"][lang])

with col2:
    st.write(texts["tech_col2"][lang])

# Arquitectura base de datos / Database architecture
st.header(texts["db_arch_header"][lang])

st.subheader(texts["db_diagram_subheader"][lang])
st.image("bin/imagenes/esquema_bbdd.png", use_container_width=True)

st.subheader(texts["db_tables_subheader"][lang])
st.markdown(texts["db_markdown"][lang])
