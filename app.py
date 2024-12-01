import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Coches de Segunda Mano",
    page_icon="🚗",
    layout="wide",
)

# Estilo CSS personalizado
st.markdown("""
    <style>
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            color: #1E88E5;
            text-align: center;
        }
        .subtitle {
            font-size: 1.5rem;
            color: #616161;
            text-align: center;
            margin-bottom: 30px;
        }
        .dev-section {
            margin-top: 30px;
        }
        .dev-names {
            font-size: 1.2rem;
            color: #424242;
            margin-left: 20px;
        }
        .image-container {
            text-align: center;
            margin: 20px 0;
        }
        hr {
            border: 1px solid #1E88E5;
        }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-title">Coches de Segunda Mano</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Filtra datos y estima el precio de mercado de tu coche.</div>', unsafe_allow_html=True)

# Imagen principal
st.markdown('<div class="image-container">', unsafe_allow_html=True)
st.image("bin/imagenes/Imagen inicial.webp", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sección de desarrolladores
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown('<div class="dev-section">', unsafe_allow_html=True)
st.subheader("Desarrollado por:")
st.markdown("""
    <ul class="dev-names">
        <li>Jorge Morandeira</li>
        <li>Carlos Moreno</li>
        <li>Miguel García</li>
    </ul>
""", unsafe_allow_html=True)

# Datos adicionales
st.subheader("Datos:")
st.markdown("Autocasión")
