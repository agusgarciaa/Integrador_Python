from pathlib import Path
import os

import streamlit as st 
import src.utils as ut


st.title("")


ruta = ut.obtener_ruta_log("logs", "operations.log")

if os.path.exists(ruta):
    st.write(f"### Contenido de logs:")
    
    # Abrir y recorrer el archivo
    with open(ruta, "r", encoding="utf-8") as file:
        for linea in file:
            # Mostrar cada línea en la app
            st.text(f"{linea.strip()}")
else:
    st.error(f"El archivo {ruta} no existe.")
