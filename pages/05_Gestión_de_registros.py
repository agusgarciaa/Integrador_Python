import streamlit as st
import src.webmanager as wb


wb.opcion_sidebar()

st.title("Gestión de Registros")

# Función del Ejercicio 4.A
wb.insertar_nuevo_registro()