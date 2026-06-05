import streamlit as st

import src.utils.rutas as rut
import src.utils.web_manager as wb
import src.visuals.formularios as form

st.title("Gestión de Registros")
wb.opcion_sidebar()

dataset = st.session_state.get('dataset_actual')
if not dataset:
    st.warning("Por favor seleccioná un dataset desde el menú lateral antes de continuar.")
    st.stop()

delimiter = '\t' if dataset == "iadiza" else ','

if dataset == "iadiza":
    archivo = "occurrence.txt"
elif dataset == "inaturalist":
    archivo = "observations.csv"
elif dataset == "xenocanto":
    archivo = "Occurrence.txt"
else:
    archivo = None

if archivo:
    ruta_raw = rut.obtener_ruta_de_datos("raw_datasets", dataset, archivo)
    ruta_processed = rut.obtener_ruta_de_datos("processed_datasets", dataset, archivo)
    ruta_log = rut.obtener_ruta_log("logs", "operations.log")

    df_actual = wb.dataframe_dataset(ruta_processed, delimiter)

    if st.session_state.get("_dataset_cargado") != dataset:
        st.session_state._dataset_cargado = dataset
        st.session_state.pop('registro_encontrado', None)
        st.cache_data.clear()
        st.rerun()


tab_insertar, tab_modificar, tab_eliminar = st.tabs([
    "Insertar Registro", 
    "Buscar y Editar Registro", 
    "Modalidades de Eliminación"
])

with tab_insertar:
    st.header("Ingresar los datos de un nuevo registro")
    st.info("💡 Complete los campos requeridos. Los datos serán validados bajo las reglas del estándar Darwin Core.")
    # Función del Ejercicio 4.A - Ana Freitas
    form.insertar_nuevo_registro(
    df=df_actual,
    archivo_target=ruta_processed,
    separador=delimiter
)


with tab_modificar:
    st.header("Modificación y actualización de datos")
    st.write("Primero localice el registro mediante su identificador para habilitar el formulario de edición.")
    # Función 4.B - Agustin Gracia
    form.buscar_registro(df_actual, dataset)
    
    # Función  4.C - Lucia Cipolla
    if 'registro_encontrado' in st.session_state:
        st.markdown("---")
        st.subheader("Campos editables del registro encontrado")
        form.editar_registro()


with tab_eliminar:
    st.header("Sección de bajas y remoción de registros")
    st.warning("⚠️ Atención! Estas acciones modifican permanentemente el dataset procesado.")
    # Ejercicio 4.D - Sofia Martins
    form.modalidades_eliminacion(ruta_raw, ruta_processed, ruta_log, delimiter, df_actual)