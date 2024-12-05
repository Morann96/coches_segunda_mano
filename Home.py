import streamlit as st
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Página Principal",
    page_icon="🚗",
    layout="wide",
)

# Título principal (centrado y en grande)
st.markdown('<h1 style="text-align:center; font-size: 3rem; color: white;">🚗 Coches de Segunda Mano 🚗</h1>', unsafe_allow_html=True)

# Imagen centrada y ajustada
image = Image.open("bin/imagenes/Imagen inicial.webp")
st.image(image, use_container_width=True, width=500)  # La imagen ocupa el 100% del contenedor pero no más de 1200px

# Descripción del Proyecto
st.header("Descripción del Proyecto")
st.write("""
Esta aplicación web está diseñada para explorar y analizar datos del mercado de coches de segunda mano.  
Con esta herramienta, puedes:
- Navegar por diferentes opciones de coches.
- Visualizar estadísticas clave sobre el mercado.
- Filtrar información según tus intereses y necesidades.
- Predecir el precio de un coche basado en sus características.

El objetivo principal es ofrecer una experiencia fácil de usar y visualmente intuitiva para que los usuarios puedan comprender mejor el mercado de coches de segunda mano.
""")

# Introducción a las secciones de la app con iconos y estilo
st.header("Secciones de la Aplicación")

st.markdown("""
1. **📊 Presentación de Datos**  
   Explora gráficos interactivos que te ayudarán a visualizar la información clave sobre los coches de segunda mano. Desde distribuciones de precios hasta la relación entre potencia y precio.
   
2. **🔍 Vista Detallada**  
   Permite personalizar los filtros para explorar los coches en función de tu presupuesto, marca, modelo, y más. También podrás ver estadísticas detalladas sobre los resultados.
   
3. **💻 Modelo de Predicción de Precios**  
   Utiliza un modelo de Machine Learning y Redes Neuronales para predecir el precio de un coche basándote en sus características, como la marca, el kilometraje, la potencia, y más.

4. **⚖️ Comparador de Coches**  
   Compara dos coches de segunda mano en función de características clave como el precio, kilometraje, y potencia, a través de gráficos comparativos.

5. **📚 Arquitectura de la Base de Datos (Documentación)**  
   Aquí podrás entender la estructura de la base de datos que respalda toda la aplicación, con información detallada sobre las tablas y relaciones entre ellas.
""")

# Desarrolladores con iconos
st.markdown("### Desarrollado por:")
st.markdown("""
- **👨‍💻 Carlos Moreno**
- **👨‍💻 Miguel García**
- **👨‍💻 Jorge Morandeira**
""")

# Fuente de los datos
st.markdown("""
<hr style="border: 1px solid #2F4F4F;">
<p style="text-align: center; color: #2F4F4F; font-size: 14px;">
    Los datos utilizados en esta aplicación provienen de <a href="https://www.autocasion.com" target="_blank" style="color: #1E88E5; font-weight: bold;">www.autocasion.com</a>.
</p>
""", unsafe_allow_html=True)

# Pie de página con estilo
st.markdown("""
<hr style="border: 1px solid #2F4F4F;">
<p style="text-align: center; color: #2F4F4F; font-size: 14px;">
    ¡Gracias por usar nuestra aplicación!<br>
    Desarrollado con 💙 por los creadores de este proyecto.
</p>
""", unsafe_allow_html=True)