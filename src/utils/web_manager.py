from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st 

import src.utils.helpers as hp
import src.operaciones.lecturas as lec


#funcion 1.a sofia martins
def dataframe_dataset(nombre,separador=','):
    try:
      dataframe=pd.read_csv(nombre,sep=separador,encoding='utf-8')
      return dataframe
    except Exception as e:
        st.error(f"error al realizar del dataframe: {e}")
        return None

#Funcion 1.b y C - Fe Cordoba, Agustin Garcia
def opcion_sidebar(separador=','):
    """
    Configura la barra lateral de Streamlit para la selección del dataset.
    """
    datasets = hp.obtener_nombres_datasets()
    if not datasets:
        st.sidebar.error("No hay datasets disponibles")
        return

    if "dataset_actual" not in st.session_state:
        st.session_state.dataset_actual = None

    if "fecha_seleccion" not in st.session_state:
        st.session_state.fecha_seleccion = None

    dataset_actual = st.session_state.dataset_actual

    opciones = ["Seleccionar dataset:"] + datasets

    indice_dataset = 0  

    if dataset_actual in datasets:
        indice_dataset = datasets.index(dataset_actual) + 1  

    dataset_seleccionado = st.sidebar.selectbox(
        "Seleccione un dataset:",
        opciones,
        index=indice_dataset
    )

    if dataset_seleccionado == "Seleccionar dataset:":
        st.session_state.dataset_actual = None
        st.session_state.fecha_seleccion = None
        return

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

    nombre_dataset = st.session_state.dataset_actual.capitalize()
    cantidad_registros = lec.total_registros(archivo_dataset, separador)

    st.sidebar.success("### Dataset seleccionado")
    st.sidebar.info(f"""
                    **Nombre:** {nombre_dataset} \n
                    **Cantidad de registros:** {cantidad_registros} \n
                    **Fecha y hora de selección:**  
                    {st.session_state.fecha_seleccion.strftime('%d/%m/%Y | %H:%M:%S')} \n
                    """)


# 2.b Fe Cordoba
def aplicar_filtros(
    df,
    nombres_cientificos=None,
    observador=None,
    paises=None,
    provincias=None,
    fecha_inicio=None,
    fecha_fin=None
):
    """Filtra el DataFrame según los parámetros de búsqueda seleccionados."""
    df_filtrado = df.copy()

    if nombres_cientificos:

        df_filtrado = df_filtrado[
            df_filtrado["scientificName"].isin(nombres_cientificos)
        ]

    if observador:

        df_filtrado = df_filtrado[
            df_filtrado["recordedBy"]
            .astype(str)
            .str.contains(
                observador,
                case=False,
                na=False
            )
        ]

    nombre_dataset = st.session_state.dataset_actual
    if (nombre_dataset != 'xenocanto'):
        if paises:

          df_filtrado = df_filtrado[
             df_filtrado["countryCode"].isin(paises)
          ]
        if provincias:

         df_filtrado = df_filtrado[
             df_filtrado["stateProvince"].isin(provincias)
          ]
    else:
        if paises:
            patron_paises = "|".join(paises)
            df_filtrado = df_filtrado[df_filtrado['country'].str.contains(patron_paises, case=False, na=False)]

    if "eventDate" in df_filtrado.columns:
        df_filtrado["eventDate"] = pd.to_datetime(df_filtrado["eventDate"], errors="coerce", utc=True)

        if fecha_inicio and fecha_fin:
            df_filtrado = df_filtrado[
                (
                    df_filtrado["eventDate"]
                    >= pd.to_datetime(fecha_inicio, utc=True)
                )
                &
                (
                    df_filtrado["eventDate"]
                    <= pd.to_datetime(fecha_fin, utc=True)
                )
            ]

    return df_filtrado

#Funcion 2.D - Lucía Cipolla
def exportar_resultados (reg=None):
    """
        reg: Debe recibir lo que retorne el conjunto de todos los datos filtrados. Puede ser un tipo DataFrame o None.
    """
    if (reg.empty):
        st.warning('No se puede exportar un archivo vacío')
        return
    else:
        if (isinstance(reg,pd.DataFrame)):
            return reg.to_csv(index=False).encode('utf-8')
        else:
            st.warning('Ocurrió un problema inesperado')
