from pathlib import Path
from datetime import datetime
import os

import streamlit as st 
import src.utils as ut
import src.helpers as hp
import pandas as pd

#funcion 1.a sofia martins
def Dataframe_dataset(nombre,separador=','):
    dataframe=pd.read_csv(nombre,sep=separador,encoding='utf-8')
    return dataframe

#Funcion 1.b y C - Fe Cordoba, Agustin Garcia
def opcion_sidebar(separador=','):
    datasets = hp.obtener_nombres_datasets()
    if not datasets:
        st.sidebar.error("No hay datasets disponibles")
        return

    if "dataset_actual" not in st.session_state:
        st.session_state.dataset_actual = datasets[0]  # Inicializa session_state si no existe
    
    if "fecha_seleccion" not in st.session_state:
        st.session_state.fecha_seleccion = datetime.now() # Inicializa con la fechaactual si no existe

    dataset_actual = st.session_state.dataset_actual  # Obtiene dataset guardado en sesión

    indice_dataset = 0     # Para indice del dataset guardado (por defecto 0)

    if dataset_actual in datasets:
        indice_dataset = datasets.index(dataset_actual)

    # Crea selector
    dataset_seleccionado = st.sidebar.selectbox( 
        "Seleccione un dataset:",
        datasets,
        index=indice_dataset
    ) 

    # Detecta cambio de dataset
    if dataset_seleccionado != st.session_state.dataset_actual:
        st.session_state.dataset_actual = dataset_seleccionado
        st.session_state.fecha_seleccion = datetime.now() 

    ruta = Path("processed_datasets") / st.session_state.dataset_actual

    if st.session_state.dataset_actual == "iadiza":
        separador = "\t"

    archivo_dataset = None

    for archivo in ruta.iterdir():

        if archivo.is_file():
            archivo_dataset = archivo

    nombre_dataset = st.session_state.dataset_actual.capitalize() # Inicia los nombres en mayúsculas
    cantidad_registros = ut.total_registros(archivo_dataset, separador)

    # Muestra en pantalla lo pedido en 1.C
    st.sidebar.success("### Dataset seleccionado")
    st.sidebar.info(f"""
                    **Nombre:** {nombre_dataset} \n
                    **Cantidad de registros:** {cantidad_registros} \n
                    **Fecha y hora de selección:**  
                    {st.session_state.fecha_seleccion.strftime('%d/%m/%Y | %H:%M:%S')} \n
                    """)
    
    