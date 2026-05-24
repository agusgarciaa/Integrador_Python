import streamlit as st
import src.rutas as rut
import src.web_manager as wb
import src.formularios as form

st.set_page_config(page_title="Gestión de Registro - Formulário", layout="wide")

st.title("Gestión de Registros")

wb.opcion_sidebar()

# Función del Ejercicio 4.A
form.insertar_nuevo_registro()
if st.session_state.get('dataset_actual')is not None:
    dataset=st.session_state.get('dataset_actual')
    delimiter='\t' if dataset=="iadiza" else ','
    if dataset=="iadiza":
        archivo="occurrence.txt"
    elif dataset=="inaturalist":
        archivo="observations.csv"
    elif dataset=="xenocanto":
        archivo="Occurrence.txt"
    if archivo:
      ruta_raw = rut.obtener_ruta_de_datos("raw_datasets", dataset, archivo)
      ruta_processed = rut.obtener_ruta_de_datos("processed_datasets", dataset, archivo)
      ruta_log = rut.obtener_ruta_log("logs", "operations.log")
      if "df_actual" not in st.session_state or st.sidebar.button("Recargar Datos"):
        st.session_state.df_actual = wb.dataframe_dataset(ruta_processed, delimiter)
      form.modalidades_eliminacion(ruta_raw, ruta_processed, ruta_log, delimiter, wb.dataframe_dataset(ruta_processed, delimiter))