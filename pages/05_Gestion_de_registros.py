import streamlit as st

import src.web_manager as wb
import src.formularios as form

st.set_page_config(page_title="Gestión de Registro - Formulário", layout="wide")

st.title("Gestión de Registros")

wb.opcion_sidebar()

# Función del Ejercicio 4.A
form.insertar_nuevo_registro()
form.modalidades_eliminacion()