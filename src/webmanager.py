from pathlib import Path
from datetime import datetime

import streamlit as st 
import pandas as pd

import src.utils as ut
import src.helpers as hp
import src.validaciones as va

COUNTRY_CODES = ['AR', 'BO', 'BR', 'PY', 'UY', 'CL']


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


# Función 2.A - Ana Freitas
def mostrar_busqueda_texto_libre():
    """
    Se encarga de la interfaz de búsqueda por texto libre.
    Lee el dataset activo en la sesión y aplica el filtro case-insensitive.
    """

    # Verificamos que exista un dataset seleccionado en la sesión
    if "dataset_actual" not in st.session_state:
        st.warning("Por favor, seleccione un dataset en el menú lateral.")
        return

    nombre_dataset = st.session_state.dataset_actual
    
    # Determinamos el separador 
    separador = "\t" if  nombre_dataset == "iadiza" else ","
    
    # Buscamos el archivo físico dentro de processed_datasets
    ruta_carpeta = Path("processed_datasets") /  nombre_dataset
    archivo = None
    
    if ruta_carpeta.exists():
        for archivo in ruta_carpeta.iterdir():
            if archivo.is_file():
                archivo = archivo
                break

    if not archivo:
        st.error("No se encontró el archivo de datos para este dataset.")
        return

    # Cargamos el DataFrame completo en memoria usando la función de la Etapa 1
    df = Dataframe_dataset(archivo, separador=separador)

    st.subheader("Búsqueda por texto libre")
    
    # 1. El usuario selecciona la columna  
    columnas_disponibles = df.columns.tolist()
    columna_seleccionada = st.selectbox(
        "Seleccione la columna por la que desea buscar:",
        options=columnas_disponibles
    )
    
    # 2. El usuario ingresa el valor que pretende encontrar 
    termino_busqueda = st.text_input(f"Ingrese el valor que pretende encontrar en '{columna_seleccionada}':")
    
    # Aplicamos el filtro solo si el usuario escribió algo
    if termino_busqueda:
         # astype(str) evita errores si la columna tiene números o nulos
        mascara = df[columna_seleccionada].astype(str).str.contains(
            termino_busqueda, 
            case=False,   # case=False maneja case-insensitive
            na=False  # na=False descarta las filas vacías (NaN)
        )
        df_filtrado = df[mascara]
    else:
        df_filtrado = df.copy()

    # Retornamos el dataframe filtrado para que pueda ser usado en los siguientes ejercicios
    return df_filtrado


# para obtener valores de una columna 
def obtener_opciones(df, columna):
    valores = df[columna]

    return sorted(
        valores
        .dropna()
        .astype(str)
        .unique()
    )


# obtiene los country code del dataframe
def obtener_paises_validos(df):

    codigos = (
        df["countryCode"]
        .dropna()
        .astype(str)
        .unique()
    )

    codigos_validos = []

    for codigo in codigos:

        if not va.validar_country_code_registro(codigo, COUNTRY_CODES):
            codigos_validos.append(codigo)

    return sorted(codigos_validos)


#filtra para la busqueda 
def aplicar_filtros(
    df,
    nombres_cientificos=None,
    observador=None,
    paises=None,
    provincias=None,
    fecha_inicio=None,
    fecha_fin=None
):

    df_filtrado = df.copy()

    # Nombre científico
    if nombres_cientificos:

        df_filtrado = df_filtrado[
            df_filtrado["scientificName"].isin(nombres_cientificos)
        ]

    # Observador
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

    # Fechas
    if "eventDate" in df_filtrado.columns:

        # SOLUCIÓN DEFINITIVA: Convertimos fila por fila a UTC de forma aislada
        df_filtrado["eventDate"] = df_filtrado["eventDate"].apply(
            lambda x: pd.to_datetime(x, errors="coerce", utc=True) if pd.notna(x) else pd.NaT
        )

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