from pathlib import Path
from datetime import datetime
import csv
import statistics

import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt

import src.utils.helpers as hp
import src.operaciones.validaciones as va
import src.operaciones.lecturas as lec
import src.operaciones.actualizaciones as act
import src.utils.file_manager as fm


#funcion 1.a sofia martins
def dataframe_dataset(nombre,separador=','):
    dataframe=pd.read_csv(nombre,sep=separador,encoding='utf-8')
    return dataframe

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
        reg: Debe recibir lo que retorne mostrar_busqueda_texto_libre(). Puede ser un tipo DataFrame o None.
    """
    if (reg.empty):
        st.warning('No se puede importar un archivo vacío')
        return
    else:
        if (isinstance(reg,pd.DataFrame)):
            return reg.to_csv(index=False).encode('utf-8')
        else:
            st.warning('Ocurrió un problema inesperado')


#Función 3.E - Lucía Cipolla
def tabla_comparativa_datasets():
    """
        Si hay 2 o más datasets toma todos los datos y retorna lo necesario para armar la tabla comparativa.
        Si hay menos de 2 datasets en "processed_datasets" muestra una advertencia y retorna vacío.
        Si en el proceso de análisis no encuentra los archivos muestra una advertencia y retorna vacío.
    """
    datasets = hp.obtener_nombres_datasets()
    if len(datasets)<2:
        st.warning('Se necesitan al menos dos datasets para comparar')
        return
    
    registros_por_dataset = {}
    for nombre_dataset in datasets:
        datos = 'occurrence.txt' if (nombre_dataset=='iadiza') else 'observations.csv' if (nombre_dataset=='inaturalist') else 'Occurrence.txt'
        ruta_dat = Path("processed_datasets") / nombre_dataset / datos
        if (ruta_dat.is_file()):
            if (nombre_dataset == 'iadiza'):
                registros_por_dataset[nombre_dataset] = lec.total_registros(ruta_dat,'\t')
            else:
                registros_por_dataset[nombre_dataset] = lec.total_registros(ruta_dat)
        else:
            st.error(f'No se encontró el archivo {datos}')
            return
    
    cant_registros_coordenadas_validas = {}
    for nombre_dataset in datasets:
        datos = 'occurrence.txt' if (nombre_dataset=='iadiza') else 'observations.csv' if (nombre_dataset=='inaturalist') else 'Occurrence.txt'
        separador = '\t' if (nombre_dataset=='iadiza') else ','
        ruta = fm.obtener_raiz_proyecto() / 'processed_datasets' / nombre_dataset / datos
        if (ruta.is_file()):
            with open(ruta,encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo ,delimiter=separador)
                cant_registros_coordenadas_validas[nombre_dataset] = 0
                for fila in lector:
                    if (va.es_coordenada_valida(fila)):
                        cant_registros_coordenadas_validas[nombre_dataset] += 1
        else:
            st.error(f'No se encontró el archivo {datos}')
            return
    
    cant_registros_fecha_valida = {}
    for nombre_dataset in datasets:
        datos = 'occurrence.txt' if (nombre_dataset=='iadiza') else 'observations.csv' if (nombre_dataset=='inaturalist') else 'Occurrence.txt'
        separador = '\t' if (nombre_dataset=='iadiza') else ','
        ruta = fm.obtener_raiz_proyecto() / 'processed_datasets' / nombre_dataset / datos
        if (ruta.is_file()):
            with open(ruta,encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo ,delimiter=separador)
                if ('eventDate' not in lector.fieldnames) and ('verbatimEventDate' not in lector.fieldnames):
                    st.warning(f'No hay columnas de fecha en {nombre_dataset}')
                    continue
                
                cant_registros_fecha_valida[nombre_dataset] = 0
                for fila in lector:
                    if (va.chequear_fecha(fila.get('eventDate')) is not None) or (va.chequear_fecha(fila.get('verbatimEventDate')) is not None):
                        cant_registros_fecha_valida[nombre_dataset] += 1
        else:
            st.error(f'No se encontró el archivo {datos}')
            return
        
    cant_campos_completos_promedio = {}
    for nombre_dataset in datasets:
        datos = 'occurrence.txt' if (nombre_dataset=='iadiza') else 'observations.csv' if (nombre_dataset=='inaturalist') else 'Occurrence.txt'
        separador = '\t' if (nombre_dataset=='iadiza') else ','
        ruta = fm.obtener_raiz_proyecto() / 'processed_datasets' / nombre_dataset / datos
        if (ruta.is_file()):
            lector = pd.read_csv(ruta,delimiter=separador,encoding='utf-8')
            lector = lector.replace(r'^\s*$', None, regex=True)
            porcentaje_completadas = lector.notna().mean().mean() * 100
            
            if (porcentaje_completadas > 0):
              cant_campos_completos_promedio[nombre_dataset] = porcentaje_completadas
            else:
                cant_campos_completos_promedio[nombre_dataset] = 0
        else:
            st.error(f'No se encontró el archivo {datos}')
            return
    
    ret = {}
    for nombre in datasets:
        ret[nombre] = {'Registros Totales': registros_por_dataset.get(nombre,0),
                       'Coordenadas Validas': cant_registros_coordenadas_validas.get(nombre,0),
                       'Fechas Validas': cant_registros_fecha_valida.get(nombre,0),
                       'Registros Completos': cant_campos_completos_promedio.get(nombre,0)}
    return ret