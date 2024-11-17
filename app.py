import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Coches de Segunda Mano", layout="wide")

st.title("Coches de Segunda Mano")
st.write("""Filtra datos y estima el precio de mercado de tu coche.""")

st.image("bin/imagenes/Imagen inicial.webp", width=600)

st.markdown("""
---
### Desarrollado por:
- Jorge Morandeira  
- Carlos Moreno  
- Miguel García  

### Datos:
Autocasión
""")
