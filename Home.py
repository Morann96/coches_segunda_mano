import streamlit as st
from PIL import Image

# 1. Definir los textos en diferentes idiomas
texts = {
    "en": {
        "page_title": "Second Hand Cars / Coches de Segunda Mano",
        "language_label": "Language",
        "title": "🚗 Second Hand Cars 🚗",
        "description_project": "Project Description",
        "description_content": """
        This web application is designed to explore and analyze data from the second-hand car market.
        With this tool, you can:
        - View key market statistics.
        - Filter information based on your interests and needs.
        - Predict the price of a car based on its features.
        - Compare two cars based on their characteristics.

        The main objective is to provide an easy-to-use and visually intuitive experience so users can better understand the second-hand car market.
        """,
        "sections_app": "Application Sections",
        "sections_content": """
        1. **📊 Data Presentation**  
           Explore interactive charts that help you visualize key information about second-hand cars.
           
        2. **🔍 Detailed View**  
           Customize filters to explore cars. You can also view detailed statistics about the results.
           
        3. **💻 Price Prediction Model**  
           Utilize a Machine Learning and Neural Networks model to predict the price of a car based on its features.
        
        4. **⚖️ Car Comparator**  
           Compare two second-hand cars based on key features such as price, mileage, and power through comparative charts.
        
        5. **📚 Database Architecture (Documentation)**  
           Understand the structure of the database that supports the entire application, with detailed information about tables and their relationships.
        """,
        "developers": "Developed by:",
        "developers_list": [
            "👨‍💻 Carlos Moreno",
            "👨‍💻 Miguel García",
            "👨‍💻 Jorge Morandeira"
        ],
        "data_source": """
        <hr style="border: 1px solid #2F4F4F;">
        <p style="text-align: center; color: #2F4F4F; font-size: 14px;">
            The data used in this application comes from <a href="https://www.autocasion.com" target="_blank" style="color: #1E88E5; font-weight: bold;">www.autocasion.com</a>.
        </p>
        """,
        "footer": """
        <hr style="border: 1px solid #2F4F4F;">
        <p style="text-align: center; color: #2F4F4F; font-size: 14px;">
            Thank you for using our application!<br>
            Developed with 💙 by the creators of this project.
        </p>
        """
    },
    "es": {
        "page_title": "Second Hand Cars / Coches de Segunda Mano",
        "language_label": "Idioma",
        "title": "🚗 Coches de Segunda Mano 🚗",
        "description_project": "Descripción del Proyecto",
        "description_content": """
        Esta aplicación web está diseñada para explorar y analizar datos del mercado de coches de segunda mano.
        Con esta herramienta, puedes:
        - Visualizar estadísticas clave sobre el mercado.
        - Filtrar información según tus intereses y necesidades.
        - Predecir el precio de un coche basado en sus características.
        - Comparar dos coches según sus características.

        El objetivo principal es ofrecer una experiencia fácil de usar y visualmente intuitiva para que los usuarios puedan comprender mejor el mercado de coches de segunda mano.
        """,
        "sections_app": "Secciones de la Aplicación",
        "sections_content": """
        1. **📊 Presentación de Datos**  
           Explora gráficos interactivos que te ayudarán a visualizar la información clave sobre los coches de segunda mano.
           
        2. **🔍 Vista Detallada**  
           Permite personalizar los filtros para explorar los coches. También podrás ver estadísticas detalladas sobre los resultados.
           
        3. **💻 Modelo de Predicción de Precios**  
           Utiliza un modelo de Machine Learning y Redes Neuronales para predecir el precio de un coche basándote en sus características.
        
        4. **⚖️ Comparador de Coches**  
           Compara dos coches de segunda mano en función de características clave como el precio, kilometraje y potencia, a través de gráficos comparativos.
        
        5. **📚 Arquitectura de la Base de Datos (Documentación)**  
           Aquí podrás entender la estructura de la base de datos que respalda toda la aplicación, con información detallada sobre las tablas y relaciones entre ellas.
        """,
        "developers": "Desarrollado por:",
        "developers_list": [
            "👨‍💻 Carlos Moreno",
            "👨‍💻 Miguel García",
            "👨‍💻 Jorge Morandeira"
        ],
        "data_source": """
        <hr style="border: 1px solid #2F4F4F;">
        <p style="text-align: center; color: #2F4F4F; font-size: 14px;">
            Los datos utilizados en esta aplicación provienen de <a href="https://www.autocasion.com" target="_blank" style="color: #1E88E5; font-weight: bold;">www.autocasion.com</a>.
        </p>
        """,
        "footer": """
        <hr style="border: 1px solid #2F4F4F;">
        <p style="text-align: center; color: #2F4F4F; font-size: 14px;">
            ¡Gracias por usar nuestra aplicación!<br>
            Desarrollado con 💙 por los creadores de este proyecto.
        </p>
        """
    }
}

# 2. Configuración de la página (LLAMAR SOLO UNA VEZ Y AL INICIO)
st.set_page_config(
    page_title=texts["en"]["page_title"],  # Usaremos un título bilingüe
    page_icon="🚗",
    layout="wide",
)

# 3. Inicializar el estado del idioma
if 'lang' not in st.session_state:
    st.session_state.lang = "en"  # Idioma por defecto

# 4. Selector de idioma
idioma = st.radio(
    texts["en"]["language_label"],  # Etiqueta en inglés por defecto
    ("English", "Español")
)

# 5. Actualizar el estado del idioma según la selección
if idioma == "Español":
    st.session_state.lang = "es"
else:
    st.session_state.lang = "en"

lang = st.session_state.lang

# 7. Título principal (centrado y en grande)
st.markdown(f'<h1 style="text-align:center; font-size: 3rem;">{texts[lang]["title"]}</h1>', unsafe_allow_html=True)

# 8. Imagen centrada y ajustada
image = Image.open("bin/imagenes/Imagen inicial.webp")
st.image(image, use_container_width=True, width=500)  # Ajusta el ancho según tus necesidades

# 9. Descripción del Proyecto
st.header(texts[lang]["description_project"])
st.write(texts[lang]["description_content"])

# 10. Introducción a las secciones de la app con iconos y estilo
st.header(texts[lang]["sections_app"])
st.markdown(texts[lang]["sections_content"])

# 12. Desarrolladores con iconos
st.markdown(f"### {texts[lang]['developers']}")
for developer in texts[lang]['developers_list']:
    st.markdown(f"- **{developer}**")

# 13. Fuente de los datos
st.markdown(texts[lang]["data_source"], unsafe_allow_html=True)

# 14. Pie de página con estilo
st.markdown(texts[lang]["footer"], unsafe_allow_html=True)
