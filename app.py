import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Coches de Segunda Mano", layout="wide")

st.title("Coches de Segunda Mano")
st.write("""Filtra datos y estima el precio de mercado de tu coche.""")