# **Coches segunda mano**  
Aplicación web para analizar datos del mercado de coches de segunda mano, permitiendo visualizar tendencias, comparar precios y filtrar por características clave.  

https://secondhandcarstest.streamlit.app

---

## **Tabla de Contenidos**  
1. [Descripción General](#descripción-general)  
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)  
3. [Instalación y Configuración](#instalación-y-configuración)  
4. [Estructura del Proyecto](#estructura-del-proyecto)  

---

## **Descripción General**  
Esta aplicación permite a los usuarios visualizar y analizar datos del mercado de coches de segunda mano. Está diseñada tanto para aficionados como para profesionales del sector automotriz interesados en entender tendencias de precios y características de los vehículos.  

---

## **Tecnologías Utilizadas**  

- **Lenguajes de Programación**:  
  - Python 3.x  

- **Frameworks y Herramientas**:  
  - **Streamlit**: Para construir la interfaz web interactiva.  
  - **SQLite**: Base de datos ligera para almacenar datos.  

- **Librerías de Análisis de Datos**:  
  - **Pandas**: Para manipulación y análisis de datos.  
  - **NumPy**: Para operaciones matemáticas.  

- **Librerías de Visualización**:  
  - **Matplotlib**: Para gráficos básicos y personalizados.  
  - **Seaborn**: Para visualizaciones estadísticas avanzadas.  
  - **Plotly**: Para gráficos interactivos en Streamlit.  

- **Scraping y Manipulación Web**:  
  - **BeautifulSoup**: Para extracción de datos de páginas web HTML.  
  - **Requests**: Para hacer solicitudes HTTP.  
  - **Selenium**: Para scraping dinámico.  

- **Control de Versiones**:
  - **Fork**: Programa utilizado para el control de versiones (Git).
  - **Git**: Para rastrear cambios en el código y colaborar con otros desarrolladores.  
  - **GitHub**: Para alojar el código y documentar el proyecto.  

- **Gestión de Entornos y Dependencias**:  
  - **venv**: Para crear entornos virtuales.  
  - **pip**: Para la instalación de paquetes.  
  - **requirements.txt**: Archivo para gestionar las dependencias del proyecto.  

- **Otras Herramientas Útiles**:  
  - **Toml**: Para configurar credenciales sensibles con `secrets.toml`.  
  - **Jupyter Notebooks**: Para pruebas y prototipos de código.  
  - **Markdown**: Para documentar en GitHub.  
 

---

## **Instalación y Configuración**  
Sigue los pasos a continuación para configurar y ejecutar el proyecto:  

1. Clonar el repositorio:  
   ```bash
   git clone <url_del_repositorio>
   cd <nombre_del_proyecto>

2. Crear entorno virtual e instalar dependencias:  
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

3. Configurar secrets.toml con tus datos para la conexión con la base de datos:  
   ```bash
   [database]
   user = "tu_usuario"
   password = "tu_contraseña"
   host = "localhost"
   port = tu_puerto
   database = "nombre_bd"

4. Iniciar aplicacion en streamlit con Visual Studio :  
   ```bash
   streamlit run Home.py

Este proyecto se ha realizado con Jupyter Lab y Visual Studio (Streamlit).

Para visualizarlo y trabajar en el debera de tener instalado Anaconda Navigator y Visual Studio.

## **Estructura del proyecto**  
  ```bash

📦 coches-segunda-mano
 ┣ 📂 bin            # Datos usados o generados(csv e imagenes).
 ┣ 📂 lib            # (Vacio).
 ┣ 📂 notebooks      # Notebooks con todo el codigo del proyecto.
 ┣ 📂 pages          # Código de las paginas de streamlit.
 ┣ Home.py             # Pagina principal de streamlit.
 ┣ requirements.txt   # Dependencias
 ┣ README.md          # Documentación
 ┗ secrets.toml       # Archivo de configuración sensible.(Oculto)


