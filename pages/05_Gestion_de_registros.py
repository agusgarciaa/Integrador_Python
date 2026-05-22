import streamlit as st

import src.web_manager as wb
import src.formularios as form


st.title("Gestión de Registros")

wb.opcion_sidebar()

# Función del Ejercicio 4.A
form.insertar_nuevo_registro()