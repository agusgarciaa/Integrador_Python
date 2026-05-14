from pathlib import Path
import os

import streamlit as st 
import src.utils as ut
import src.helpers as hp
import pandas as pd

#funcion 1.a sofia martins
def Dataframe_dataset(nombre,separador=','):
    dataframe=pd.read_csv(nombre,sep=separador,encoding='utf-8')
    return dataframe

#Funcion 1.b - Fe Cordoba
def opcion_sidebar():
    datasets = hp.obtener_nombres_datasets()
    if not datasets:
        st.sidebar.error("No hay datasets disponibles")
        return

    if "dataset_actual" not in st.session_state:
        st.session_state.dataset_actual = datasets[0]  # Inicializa session_state si no existe

    dataset_actual = st.session_state.dataset_actual  # Obtiene dataset guardado en sesión

    indice_dataset = 0     # Para indice del dataset guardado (por defecto 0)

    if dataset_actual in datasets:
        indice_dataset = datasets.index(dataset_actual)

    # Crea selector
    dataset_seleccionado = st.sidebar.selectbox( 
        "Seleccione un dataset",
        datasets,
        index=indice_dataset
    ) 

    st.session_state.dataset_actual = dataset_seleccionado  # Guardar selección 
    
    st.sidebar.write(f"Dataset actual: {dataset_seleccionado}") # Muestra dataset seleccionado