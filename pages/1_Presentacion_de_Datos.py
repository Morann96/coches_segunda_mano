import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos
@st.cache_data
def load_data():
    data = pd.read_csv(bin/data.csv)
    return data

data = load_data()

# Título y descripción
st.title("Explorador de datos de coches de segunda mano")
st.markdown("""
Esta aplicación permite explorar y visualizar datos detallados de coches de segunda mano, con filtros interactivos y gráficos dinámicos.
""")

# Filtros en la barra lateral
st.sidebar.header("Filtros")
selected_provincia = st.sidebar.multiselect(
    "Selecciona provincia(s):", 
    options=data["provincia"].unique(), 
    default=data["provincia"].unique()
)

selected_combustible = st.sidebar.multiselect(
    "Selecciona tipo de combustible:", 
    options=data["combustible"].unique(), 
    default=data["combustible"].unique()
)

selected_carroceria = st.sidebar.multiselect(
    "Selecciona tipo de carrocería:", 
    options=data["carroceria"].dropna().unique(), 
    default=data["carroceria"].dropna().unique()
)

# Aplicar filtros
filtered_data = data[
    (data["provincia"].isin(selected_provincia)) &
    (data["combustible"].isin(selected_combustible)) &
    (data["carroceria"].isin(selected_carroceria))
]

# Mostrar datos filtrados
st.write("### Datos filtrados", filtered_data)

# Visualizaciones
st.write("## Visualizaciones")

# 1. Gráfico de barras: Distribución de coches por provincia
st.write("### Distribución de coches por provincia")
provincia_counts = filtered_data["provincia"].value_counts()
st.bar_chart(provincia_counts)

# 2. Gráfico de barras: Distribución de coches por tipo de combustible
st.write("### Distribución de coches por combustible")
combustible_counts = filtered_data["combustible"].value_counts()
st.bar_chart(combustible_counts)

# 3. Boxplot: Kilometraje por tipo de combustible
st.write("### Kilometraje por tipo de combustible")
plt.figure(figsize=(10, 5))
sns.boxplot(data=filtered_data, x="combustible", y="kilometraje")
plt.xticks(rotation=45)
plt.title("Kilometraje por combustible")
st.pyplot(plt)

# 4. Scatter plot: Relación precio vs. kilometraje
st.write("### Relación entre precio y kilometraje")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered_data, x="kilometraje", y="precio_contado", hue="combustible", ax=ax)
plt.title("Precio vs. Kilometraje")
st.pyplot(fig)

# 5. Tabla interactiva
st.write("### Vista detallada de los datos filtrados")
st.dataframe(filtered_data)