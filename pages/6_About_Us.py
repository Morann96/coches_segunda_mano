import streamlit as st

# Título principal
st.title("👥 **About Us**")

# Introducción general
st.write("""
¡Bienvenido a la sección **About Us**! Somos un equipo apasionado por la tecnología, la ciencia de datos y el desarrollo de herramientas prácticas que aporten valor a la sociedad. Este proyecto es el resultado de un esfuerzo colaborativo que combina experiencia en análisis de datos, machine learning y desarrollo web.
""")

# Información de los integrantes
st.header("**Nuestro Equipo**")

# Define los integrantes del equipo con sus datos
team_members = [
    {
        "name": "Miguel García",
        "role": "Dev",
        "linkedin": "https://www.linkedin.com/in/miguelgarciadelvalle-516677145",
        "github": "https://github.com/juanperez",
        "photo": "bin/imagenes/Foto_miguel.jpg"
    },
    {
        "name": "Carlos Moreno",
        "role": "Dev",
        "linkedin": "https://www.linkedin.com/in/carlos-moreno-valero-595ba013a/",
        "github": "https://github.com/cmv28061996",
        "photo": "bin/imagenes/Foto_carlos.jpeg"
    },
    {
        "name": "Jorge Morandeira",
        "role": "Dev",
        "linkedin": "https://www.linkedin.com/in/jorge-morandeira-rodr%C3%ADguez-49b0b9170/",
        "github": "https://github.com/Morann96",
        "photo": "bin/imagenes/Foto_jorge.jpg"
    }
  
]

# Mostrar la información de cada integrante
for member in team_members:
    col1, col2 = st.columns([1, 3])  # Primera columna para la foto, segunda para los detalles
    with col1:
        st.image(member["photo"], caption=member["name"], use_container_width=True)
    with col2:
        st.subheader(f"👤 {member['name']}")
        st.write(f"**Rol:** {member['role']}")
        st.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-{member['name'].replace(' ', '%20')}-blue)]({member['linkedin']})")
        st.markdown(f"[![GitHub](https://img.shields.io/badge/GitHub-{member['name'].replace(' ', '%20')}-black)]({member['github']})")
    st.markdown("---")  # Línea separadora entre miembros

